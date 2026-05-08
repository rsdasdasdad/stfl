import os
import re

INPUT_FILE = "examples/index.stfl"
OUTPUT_FILE = "output/index.html"

html = []

# =========================
# TOOLS
# =========================

def extract_text(line):
    start = line.find('"')
    end = line.rfind('"')

    if start == -1 or end == -1 or start == end:
        return ""

    text = line[start + 1:end]
    text = text.replace('\\"', '"')

    return text

def parse_attributes(line):
    attrs = {}

    if "[" in line and "]" in line:
        attr_text = line[line.find("[")+1:line.find("]")]
        parts = attr_text.split(",")

        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                attrs[key.strip()] = value.strip()

    return attrs

def attrs_to_html(attrs):
    result = ""

    if "class" in attrs:
        result += f' class="{attrs["class"]}"'

    if "id" in attrs:
        result += f' id="{attrs["id"]}"'

    return result

# =========================
# STYLE SYSTEM
# =========================

STYLE_MAP = {
    "color": "color",
    "bg": "background",
    "size": "font-size",
    "width": "width",
    "height": "height",
    "padding": "padding",
    "margin": "margin",
    "radius": "border-radius",
    "align": "text-align",
    "weight": "font-weight",
    "border": "border",
    "display": "display",
    "flex": "display:flex",
    "gap": "gap"
}

def compile_style(style_lines):
    css = []

    for line in style_lines:
        line = line.strip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip()

        if key in STYLE_MAP:

            css_key = STYLE_MAP[key]

            if key == "flex":
                css.append("display:flex;")
                continue

            # auto px
            if value.isdigit() and key in [
                "size",
                "width",
                "height",
                "padding",
                "margin",
                "radius",
                "gap"
            ]:
                value += "px"

            css.append(f"{css_key}:{value};")

    return " ".join(css)

# =========================
# PARSER
# =========================

def compile_block(lines, i):

    line = lines[i].rstrip()
    stripped = line.strip()

    if not stripped:
        return "", i

    if stripped.startswith("#"):
        return "", i

    attrs = parse_attributes(stripped)
    html_attrs = attrs_to_html(attrs)

    styles = []

    # detect style block
    j = i + 1

    while j < len(lines):

        next_line = lines[j]

        if next_line.startswith("  "):
            styles.append(next_line)
            j += 1
        else:
            break

    style_attr = ""

    if styles:
        css = compile_style(styles)

        if css:
            style_attr = f' style="{css}"'

    # PAGE
    if stripped.startswith("page"):
        title = extract_text(stripped)

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
</head>
<body>
"""

        return html, j - 1

    # TITLE
    if stripped.startswith("title"):
        text = extract_text(stripped)
        return f"<h1{html_attrs}{style_attr}>{text}</h1>", j - 1

    # TEXT
    if stripped.startswith("text"):
        text = extract_text(stripped)
        return f"<p{html_attrs}{style_attr}>{text}</p>", j - 1

    # BUTTON
    if stripped.startswith("button"):
        text = extract_text(stripped)
        return f"<button{html_attrs}{style_attr}>{text}</button>", j - 1

    # IMAGE
    if stripped.startswith("img"):
        src = extract_text(stripped)
        return f'<img src="{src}"{html_attrs}{style_attr}>', j - 1

    # LINK
    if stripped.startswith("link"):

        text = extract_text(stripped)

        url_match = re.search(r'->\s*(.+)', stripped)
        url = url_match.group(1) if url_match else "#"

        return f'<a href="{url}"{html_attrs}{style_attr}>{text}</a>', j - 1

    return "", j - 1

# =========================
# MAIN
# =========================

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()

i = 0

while i < len(lines):

    compiled, new_i = compile_block(lines, i)

    if compiled:
        html.append(compiled)

    i = new_i + 1

html.append("</body>")
html.append("</html>")

os.makedirs("output", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write("\n".join(html))

print("STFL compiled successfully.")
print(f"Output: {OUTPUT_FILE}")
