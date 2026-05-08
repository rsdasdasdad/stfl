import os
import re
import sys

INPUT_FILE = "examples/index.stfl"
OUTPUT_FILE = "output/index.html"

CSS_MAP = {
    "bg": "background", "color": "color", "text": "color",
    "size": "font-size", "radius": "border-radius",
    "spacing": "padding", "padding": "padding", "margin": "margin",
    "font": "font-family", "bold": "font-weight",
    "flex": "display", "dir": "flex-direction", "gap": "gap",
    "align": "text-align", "width": "width", "height": "height",
    "border": "border", "display": "display", "weight": "font-weight",
    "opacity": "opacity", "shadow": "box-shadow",
}


def extract_text(line):
    start = line.find('"')
    end = line.rfind('"')
    if start != -1 and end != -1 and start != end:
        return line[start + 1:end].replace('\\"', '"')
    return ""


def parse_attributes(line):
    match = re.search(r'\[(.*?)\]', line)
    attrs = {}
    if match:
        parts = match.group(1).split(",")
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                attrs[k.strip()] = v.strip()
    return attrs


def attrs_to_html(attrs):
    return "".join(f' {k}="{v}"' for k, v in attrs.items())


def make_element(tag, content, attrs, self_closing=False):
    """Generate an HTML element string."""
    html_attrs = attrs_to_html(attrs)
    if self_closing:
        return f"<{tag}{html_attrs}>"
    return f"<{tag}{html_attrs}>{content}</{tag}>"


def try_add_px(val):
    """Add px suffix if value is a plain number."""
    try:
        int(val)
        return val + "px"
    except ValueError:
        return val


def compile_stfl(input_path=INPUT_FILE, output_path=OUTPUT_FILE):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    html_body = []
    css_rules = []
    font_imports = []
    page_title = "STFL Page"
    use_icon_engine = False
    stack = []  # (indent, closing_tag)
    i = 0

    ELEMENT_MAP = {
        "title": ("h1", False),
        "subtitle": ("h2", False),
        "text": ("p", False),
        "button": ("button", False),
        "item": ("li", False),
        "divider": ("hr", True),
    }

    while i < len(lines):
        line = lines[i]

        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue

        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        # Close containers whose indent >= current indent
        while stack and stack[-1][0] >= indent:
            _, closing_tag = stack.pop()
            html_body.append(closing_tag)

        attrs = parse_attributes(stripped)
        line_no_attrs = re.sub(r'\[.*?\]', "", stripped).strip()
        is_box = line_no_attrs.startswith("box")
        has_colon = line_no_attrs.endswith(":")

        # --- Element with inline CSS (e.g., title "Hello": / text "World":) ---
        if has_colon and not is_box:
            element_line = line_no_attrs.rstrip(":").strip()

            inline_styles = {}
            j = i + 1
            while j < len(lines):
                if not lines[j].strip() or lines[j].strip().startswith("#"):
                    j += 1
                    continue
                child_indent = len(lines[j]) - len(lines[j].lstrip())
                if child_indent <= indent:
                    break
                css_line = lines[j].strip()
                if "=" in css_line:
                    prop, val = css_line.split("=", 1)
                    pname = prop.strip()
                    if pname in ("class", "id"):
                        attrs[pname] = val.strip()
                    else:
                        real_prop = CSS_MAP.get(pname, pname)
                        inline_styles[real_prop] = try_add_px(val.strip())
                j += 1
            i = j

            if inline_styles:
                style_str = "; ".join(f"{k}: {v}" for k, v in inline_styles.items())
                attrs["style"] = style_str

            content = extract_text(element_line)
            tag_name = element_line.split()[0] if element_line.split() else ""

            if tag_name in ELEMENT_MAP:
                tag, self_closing = ELEMENT_MAP[tag_name]
                if self_closing:
                    html_body.append(f"<{tag}{attrs_to_html(attrs)}>")
                else:
                    html_body.append(f"<{tag}{attrs_to_html(attrs)}>{content}</{tag}>")
            elif tag_name == "link":
                url_parts = element_line.split("->")
                url = url_parts[1].strip() if len(url_parts) > 1 else "#"
                html_body.append(f'<a href="{url}"{attrs_to_html(attrs)}>{content}</a>')
            elif tag_name == "img":
                html_body.append(f'<img src="{content}"{attrs_to_html(attrs)}>')
            elif tag_name == "input":
                html_body.append(f'<input type="text" placeholder="{content}"{attrs_to_html(attrs)}>')
            elif tag_name == "icon":
                html_body.append(f'<iconify-icon icon="{content}"{attrs_to_html(attrs)}></iconify-icon>')
                use_icon_engine = True
            elif tag_name == "svg":
                html_body.append(f'<span{attrs_to_html(attrs)} class="stfl-svg">{content}</span>')
            else:
                html_body.append(f"<div{attrs_to_html(attrs)}>{content}</div>")
            continue

        # --- Box container ---
        if is_box and has_colon:
            html_body.append(f"<div{attrs_to_html(attrs)}>")
            stack.append((indent, "</div>"))
            i += 1
            continue

        # --- Regular elements (no inline CSS) ---
        html_attrs = attrs_to_html(attrs)
        content = extract_text(line_no_attrs)

        if stripped.startswith("page "):
            page_title = content
        elif stripped.startswith("font_import "):
            font_url = content.replace(" ", "+")
            font_imports.append(
                f'<link href="https://fonts.googleapis.com/css2?family={font_url}:wght@400;700&display=swap" rel="stylesheet">'
            )
        elif stripped.startswith("style "):
            selector = content
            if "->" in stripped:
                rules_str = stripped.split("->")[1].strip()
                # Split on commas, but not inside parentheses
                rules = []
                depth = 0
                current = ""
                for ch in rules_str:
                    if ch == "(":
                        depth += 1
                        current += ch
                    elif ch == ")":
                        depth -= 1
                        current += ch
                    elif ch == "," and depth == 0:
                        rules.append(current.strip())
                        current = ""
                    else:
                        current += ch
                if current.strip():
                    rules.append(current.strip())
                compiled_rules = []
                for r in rules:
                    if ":" in r:
                        k, v = r.split(":", 1)
                        real_k = CSS_MAP.get(k.strip(), k.strip())
                        compiled_rules.append(f"{real_k}: {v.strip()};")
                css_rules.append(f"{selector} {{ {' '.join(compiled_rules)} }}")
        elif stripped.startswith("title "):
            html_body.append(f"<h1{html_attrs}>{content}</h1>")
        elif stripped.startswith("subtitle "):
            html_body.append(f"<h2{html_attrs}>{content}</h2>")
        elif stripped.startswith("text "):
            html_body.append(f"<p{html_attrs}>{content}</p>")
        elif stripped.startswith("button "):
            html_body.append(f"<button{html_attrs}>{content}</button>")
        elif stripped.startswith("img "):
            html_body.append(f'<img src="{content}"{html_attrs}>')
        elif stripped.startswith("input "):
            html_body.append(f'<input type="text" placeholder="{content}"{html_attrs}>')
        elif stripped.startswith("item "):
            html_body.append(f"<li{html_attrs}>{content}</li>")
        elif stripped == "divider":
            html_body.append(f"<hr{html_attrs}>")
        elif stripped.startswith("link "):
            url_parts = stripped.split("->")
            url = re.sub(r'\[.*?\]', "", url_parts[1]).strip() if len(url_parts) > 1 else "#"
            html_body.append(f'<a href="{url}"{html_attrs}>{content}</a>')
        elif stripped.startswith("icon "):
            html_body.append(f'<iconify-icon icon="{content}"{html_attrs}></iconify-icon>')
            use_icon_engine = True
        elif stripped.startswith("svg "):
            html_body.append(f'<span{html_attrs} class="stfl-svg">{content}</span>')
        elif stripped.startswith("box:"):
            html_body.append(f"<div{html_attrs}>")
            stack.append((indent, "</div>"))

        i += 1

    # Close remaining containers
    while stack:
        html_body.append(stack.pop()[1])

    # Assemble final HTML
    icon_script = '<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>' if use_icon_engine else ""
    css_string = "\n  ".join(css_rules)
    font_string = "\n".join(font_imports)

    default_css = """  body { font-family: system-ui, -apple-system, sans-serif; padding: 20px; line-height: 1.5; color: #333; }
  img { max-width: 100%; }
  .stfl-svg svg { width: 1em; height: 1em; vertical-align: -0.125em; fill: currentColor; }
  iconify-icon { display: inline-flex; vertical-align: -0.125em; }"""

    final_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{font_string}
{icon_script}
<style>
{default_css}
  {css_string}
</style>
</head>
<body>

{"\n".join(html_body)}

</body>
</html>"""

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"STFL Compiler v0.7")
    print(f"  Input : {input_path}")
    print(f"  Output: {output_path}")
    print("Compile Success.")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE
    out = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_FILE
    compile_stfl(inp, out)
