import os
import re
import html
import sys
import webbrowser
from dataclasses import dataclass, field

# =========================================================
# STFL Compiler v1.3
# AI-Friendly HTML DSL
# =========================================================

INPUT_FILE = "examples/index.stfl"
OUTPUT_FILE = "output/index.html"

# =========================================================
# CSS SHORTCUTS
# =========================================================

CSS_MAP = {
    "bg": "background",
    "text": "color",
    "color": "color",
    "size": "font-size",
    "radius": "border-radius",
    "padding": "padding",
    "margin": "margin",
    "gap": "gap",
    "align": "text-align",
    "width": "width",
    "height": "height",
    "shadow": "box-shadow",
    "border": "border",
    "opacity": "opacity",
    "font": "font-family",
    "weight": "font-weight",
}

UNITLESS = {
    "opacity",
    "font-weight",
    "z-index",
    "line-height",
    "flex-grow",
    "flex-shrink",
    "order",
}

# =========================================================
# ELEMENT MAP
# =========================================================

ELEMENT_MAP = {
    "title": "h1",
    "subtitle": "h2",
    "text": "p",
    "button": "button",
    "item": "li",
}

CONTAINERS = {
    "box": "div",
    "section": "section",
    "header": "header",
    "footer": "footer",
    "main": "main",
    "nav": "nav",
    "article": "article",
    "aside": "aside",
}

SELF_CLOSING = {
    "img",
    "input",
    "divider",
    "meta",
}

SAFE_PROTOCOLS = (
    "http://",
    "https://",
    "mailto:",
    "/",
    "#",
)

# =========================================================
# REGEX
# =========================================================

STRING_RE = re.compile(
    r'"((?:\\.|[^"])*)"|\'((?:\\.|[^\'])*)\''
)

# =========================================================
# AST NODE
# =========================================================

@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    text: str = ""
    children: list = field(default_factory=list)

# =========================================================
# UTILITIES
# =========================================================

def escape(value):
    return html.escape(str(value), quote=True)


def smart_split(text, delimiter=","):

    result = []
    current = ""
    depth = 0
    quote = None

    for ch in text:

        if ch in "\"'":

            if quote is None:
                quote = ch
            elif quote == ch:
                quote = None

        elif quote is None:

            if ch in "([{":
                depth += 1

            elif ch in ")]}":
                depth -= 1

        if ch == delimiter and depth == 0 and quote is None:

            result.append(current.strip())
            current = ""

        else:

            current += ch

    if current.strip():
        result.append(current.strip())

    return result


def extract_text(line):

    match = STRING_RE.search(line)

    if not match:
        return ""

    value = match.group(1) or match.group(2) or ""

    return value.replace('\\"', '"').replace("\\'", "'")


def try_add_px(value, prop=""):

    if prop in UNITLESS:
        return value

    parts = value.split()

    final = []

    for p in parts:

        if re.match(r"^-?\d+(\.\d+)?$", p):
            final.append(p + "px")
        else:
            final.append(p)

    return " ".join(final)


def sanitize_url(url):

    url = url.strip()

    lower = url.lower()

    dangerous = (
        "javascript:",
        "data:",
        "vbscript:",
    )

    for d in dangerous:
        if lower.startswith(d):
            return "#"

    return escape(url)

# =========================================================
# ATTRIBUTE PARSER
# =========================================================

def extract_bracket_content(line):

    start = line.find("[")

    if start == -1:
        return None

    depth = 0

    for i in range(start, len(line)):

        ch = line[i]

        if ch == "[":
            depth += 1

        elif ch == "]":
            depth -= 1

            if depth == 0:
                return line[start + 1:i]

    return None


def remove_brackets(line):

    start = line.find("[")

    if start == -1:
        return line

    depth = 0

    end = start

    for i in range(start, len(line)):

        ch = line[i]

        if ch == "[":
            depth += 1

        elif ch == "]":
            depth -= 1

            if depth == 0:
                end = i
                break

    return (line[:start] + line[end + 1:]).strip()


def parse_attributes(line):

    attrs = {}

    raw = extract_bracket_content(line)

    if not raw:
        return attrs

    parts = smart_split(raw)

    for part in parts:

        if "=" not in part:
            continue

        key, value = part.split("=", 1)

        key = key.strip()
        value = value.strip().strip("\"'")

        if not re.match(r"^[a-zA-Z_:][-a-zA-Z0-9_:.]*$", key):
            continue

        attrs[key] = escape(value)

    return attrs


def attrs_to_html(attrs):

    return "".join(
        f' {k}="{v}"'
        for k, v in attrs.items()
    )

# =========================================================
# CLASS SHORTHAND
# =========================================================

def parse_class_shorthand(name):

    parts = name.split(".")

    base = parts[0]

    classes = parts[1:]

    return base, classes

# =========================================================
# STYLE COLLECTION
# =========================================================

def collect_styles(lines, start, parent_indent):

    styles = {}
    attrs = {}

    i = start

    while i < len(lines):

        raw = lines[i]

        if not raw.strip():
            i += 1
            continue

        indent = len(raw) - len(raw.lstrip())

        if indent <= parent_indent:
            break

        line = raw.strip()

        if "=" not in line:
            i += 1
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip().strip("\"'")

        if key in ("class", "id"):

            attrs[key] = value

        else:

            real = CSS_MAP.get(key, key)

            styles[real] = try_add_px(value, real)

        i += 1

    return styles, attrs, i

# =========================================================
# RENDERER
# =========================================================

def render_node(node):

    attrs = attrs_to_html(node.attrs)

    # RAW HTML
    if node.tag == "raw":
        return node.text

    # SVG SAFE
    if node.tag == "svg":
        return f'<span class="stfl-svg"{attrs}>{node.text}</span>'

    # IMG
    if node.tag == "img":
        return f'<img src="{escape(node.text)}"{attrs}>'

    # INPUT
    if node.tag == "input":
        return f'<input type="text" placeholder="{escape(node.text)}"{attrs}>'

    # VIDEO
    if node.tag == "video":
        return f'<video controls src="{escape(node.text)}"{attrs}></video>'

    # AUDIO
    if node.tag == "audio":
        return f'<audio controls src="{escape(node.text)}"{attrs}></audio>'

    # LINK
    if node.tag == "a":
        return f'<a{attrs}>{escape(node.text)}</a>'

    # ICON
    if node.tag == "icon":
        return f'<iconify-icon icon="{escape(node.text)}"{attrs}></iconify-icon>'

    # HR
    if node.tag == "divider":
        return f"<hr{attrs}>"

    # META
    if node.tag == "meta":
        return f"<meta{attrs}>"

    children = "".join(
        render_node(c)
        for c in node.children
    )

    return f"<{node.tag}{attrs}>{escape(node.text)}{children}</{node.tag}>"

# =========================================================
# PARSER
# =========================================================

def parse_stfl(lines):

    root = Node("root")

    stack = [(-1, root)]

    css_rules = []

    fonts = []

    metas = []

    external_css = []

    external_js = []

    variables = {}

    page_title = "STFL Page"

    use_icons = False

    i = 0

    while i < len(lines):

        raw = lines[i]

        if not raw.strip() or raw.strip().startswith("#"):
            i += 1
            continue

        indent = len(raw) - len(raw.lstrip())

        line = raw.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()

        attrs = parse_attributes(line)

        clean = remove_brackets(line)

        # PAGE
        if clean.startswith("page "):

            page_title = extract_text(clean)

            i += 1
            continue

        # VARIABLES
        if clean.startswith("var "):

            expr = clean[4:]

            if "=" in expr:

                k, v = expr.split("=", 1)

                variables[k.strip()] = v.strip()

            i += 1
            continue

        # META
        if clean.startswith("meta"):

            metas.append(Node("meta", attrs=attrs))

            i += 1
            continue

        # EXTERNAL CSS
        if clean.startswith("css "):

            external_css.append(extract_text(clean))

            i += 1
            continue

        # EXTERNAL JS
        if clean.startswith("js "):

            external_js.append(extract_text(clean))

            i += 1
            continue

        # FONT
        if clean.startswith("font_import "):

            fonts.append(
                extract_text(clean).replace(" ", "+")
            )

            i += 1
            continue

        # STYLE
        if clean.startswith("style "):

            if "->" in clean:

                left, right = clean.split("->", 1)

                selector = extract_text(left)

                rules = smart_split(right)

                compiled = []

                for rule in rules:

                    if ":" not in rule:
                        continue

                    k, v = rule.split(":", 1)

                    k = k.strip()
                    v = v.strip()

                    real = CSS_MAP.get(k, k)

                    compiled.append(
                        f"{real}: {try_add_px(v, real)};"
                    )

                css_rules.append(
                    f"{selector} {{ {' '.join(compiled)} }}"
                )

                i += 1
                continue

            selector = extract_text(clean)

            styles, _, new_i = collect_styles(
                lines,
                i + 1,
                indent
            )

            css = "; ".join(
                f"{k}: {v}"
                for k, v in styles.items()
            )

            css_rules.append(
                f"{selector} {{ {css}; }}"
            )

            i = new_i
            continue

        # INLINE STYLE ELEMENT
        if clean.endswith(":"):

            temp = clean[:-1].strip()

            first = temp.split()[0]

            base, classes = parse_class_shorthand(first)

            has_text = '"' in temp or "'" in temp

            if (
                base in ELEMENT_MAP
                or base in (
                    "link",
                    "icon",
                    "svg",
                    "img",
                    "input",
                    "video",
                    "audio",
                    "raw",
                )
            ) and has_text:

                text = extract_text(temp)

                styles, style_attrs, new_i = collect_styles(
                    lines,
                    i + 1,
                    indent
                )

                attrs.update(style_attrs)

                if classes:

                    attrs["class"] = (
                        attrs.get("class", "") +
                        " " +
                        " ".join(classes)
                    ).strip()

                if styles:

                    attrs["style"] = "; ".join(
                        f"{k}: {v}"
                        for k, v in styles.items()
                    )

                if base in ELEMENT_MAP:

                    tag = ELEMENT_MAP[base]

                elif base == "link":

                    tag = "a"

                    if "->" in temp:

                        href = temp.split("->", 1)[1].strip()

                        attrs["href"] = sanitize_url(href)

                elif base == "icon":

                    tag = "icon"

                    use_icons = True

                else:

                    tag = base

                node = Node(
                    tag=tag,
                    attrs=attrs,
                    text=text
                )

                stack[-1][1].children.append(node)

                i = new_i

                continue

        # CONTAINER
        if clean.endswith(":"):

            name = clean[:-1].strip()

            base, classes = parse_class_shorthand(name)

            tag = CONTAINERS.get(base, "div")

            if classes:

                attrs["class"] = (
                    attrs.get("class", "") +
                    " " +
                    " ".join(classes)
                ).strip()

            node = Node(
                tag=tag,
                attrs=attrs
            )

            stack[-1][1].children.append(node)

            stack.append((indent, node))

            i += 1

            continue

        # NORMAL ELEMENT

        name = clean.split()[0]

        base, classes = parse_class_shorthand(name)

        text = extract_text(clean)

        styles, style_attrs, new_i = collect_styles(
            lines,
            i + 1,
            indent
        )

        attrs.update(style_attrs)

        if classes:

            attrs["class"] = (
                attrs.get("class", "") +
                " " +
                " ".join(classes)
            ).strip()

        if styles:

            attrs["style"] = "; ".join(
                f"{k}: {v}"
                for k, v in styles.items()
            )

        if base in ELEMENT_MAP:

            tag = ELEMENT_MAP[base]

        elif base == "link":

            tag = "a"

            if "->" in clean:

                href = clean.split("->", 1)[1].strip()

                attrs["href"] = sanitize_url(href)

        elif base == "icon":

            tag = "icon"

            use_icons = True

        elif base in (
            "svg",
            "video",
            "audio",
            "raw",
        ):

            tag = base

        elif base in SELF_CLOSING:

            tag = base

        else:

            tag = "div"

        node = Node(
            tag=tag,
            attrs=attrs,
            text=text
        )

        stack[-1][1].children.append(node)

        i = new_i

    return (
        root,
        css_rules,
        fonts,
        metas,
        external_css,
        external_js,
        variables,
        page_title,
        use_icons,
    )

# =========================================================
# HTML GENERATOR
# =========================================================

DEFAULT_CSS = """
body {
    font-family: system-ui, -apple-system, sans-serif;
    padding: 20px;
    line-height: 1.5;
    color: #333;
}

img,
video {
    max-width: 100%;
}

.stfl-svg svg {
    width: 1em;
    height: 1em;
    fill: currentColor;
}

iconify-icon {
    display: inline-flex;
    vertical-align: -0.125em;
}
"""

def generate_html(
    ast,
    css_rules,
    fonts,
    metas,
    external_css,
    external_js,
    variables,
    title,
    use_icons
):

    body = "".join(
        render_node(child)
        for child in ast.children
    )

    css = "\n".join(css_rules)

    variable_css = ""

    if variables:

        variable_css = ":root {\n"

        for k, v in variables.items():
            variable_css += f"  --{k}: {v};\n"

        variable_css += "}"

    preconnect = ""
    font_links = ""

    if fonts:

        preconnect = (
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        )

        font_links = "\n".join(
            f'<link href="https://fonts.googleapis.com/css2?family={f}:wght@400;700&display=swap" rel="stylesheet">'
            for f in fonts
        )

    meta_html = "".join(
        render_node(m)
        for m in metas
    )

    css_links = "\n".join(
        f'<link rel="stylesheet" href="{escape(x)}">'
        for x in external_css
    )

    js_links = "\n".join(
        f'<script src="{escape(x)}"></script>'
        for x in external_js
    )

    icon_script = ""

    if use_icons:

        icon_script = (
            '<script src="https://code.iconify.design/'
            'iconify-icon/1.0.7/iconify-icon.min.js"></script>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{escape(title)}</title>

{meta_html}

{preconnect}

{font_links}

{css_links}

{icon_script}

<style>

{DEFAULT_CSS}

{variable_css}

{css}

</style>

</head>

<body>

{body}

{js_links}

</body>

</html>
"""

# =========================================================
# COMPILER
# =========================================================

def derive_output_path(input_path):

    base, ext = os.path.splitext(input_path)

    if ext.lower() in (".stfl", ".txt"):
        return base + ".html"

    return input_path + ".html"


def compile_stfl(input_path, output_path=None):

    if output_path is None:
        output_path = derive_output_path(input_path)

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    (
        ast,
        css_rules,
        fonts,
        metas,
        external_css,
        external_js,
        variables,
        title,
        use_icons,
    ) = parse_stfl(lines)

    final_html = generate_html(
        ast,
        css_rules,
        fonts,
        metas,
        external_css,
        external_js,
        variables,
        title,
        use_icons,
    )

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print("=" * 48)
    print(" STFL Compiler v1.3")
    print("=" * 48)
    print(f" Input : {input_path}")
    print(f" Output: {output_path}")
    print(" Compile Success.")
    print("=" * 48)

    return output_path

# =========================================================
# BROWSER
# =========================================================

def open_in_browser(output_path):

    webbrowser.open(
        "file://" + os.path.abspath(output_path)
    )

# =========================================================
# MAIN
# =========================================================

def main():

    drag = len(sys.argv) > 1

    inp = (
        sys.argv[1]
        if drag
        else INPUT_FILE
    )

    out = (
        sys.argv[2]
        if len(sys.argv) > 2
        else (
            OUTPUT_FILE
            if not drag
            else None
        )
    )

    result = compile_stfl(inp, out)

    if drag:

        print()

        try:
            input("Press Enter to open in browser...")
        except UnicodeEncodeError:
            input()

        open_in_browser(result)

# =========================================================

if __name__ == "__main__":
    main()