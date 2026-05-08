import os
import re

INPUT_FILE = "examples/index.stfl"
OUTPUT_FILE = "output/index.html"

html = []
font_links = []

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
    "gap": "gap",
    "font": "font-family"
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

            # font with spaces
            if key == "font" and " " in value:
                value = f'"{value}"'

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

    j = i + 1

    while j < len(lines):

        next_line = lines[j]

        # style block
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

    # =========================
    # FONT IMPORT
    # =========================

    if stripped.startswith("font_import"):

        font_name = extract_text(stripped)

        google_font = font_name.replace(" ", "+")

        link = f'<link href="https://fonts.googleapis.com/css2?family={google_font}&display=swap" rel="stylesheet">'

        font_links.append(link)

        return "", j - 1

    # =========================
    # PAGE
    # =========================

    if stripped.startswith("page"):

        title = extract_text(stripped)

        font_html = "\n".join(font_links)

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>

{font_html}

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 40px;
}}

.card {{
    border: 1px solid #ddd;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}}

button {{
    border: none;
    cursor: pointer;
}}

</style>

</head>
<body>
""", j - 1

    # =========================
    # TITLE
    # =========================

    if stripped.startswith("title"):

        text = extract_text(stripped)

        return f"<h1{html_attrs}{style_attr}>{text}</h1>", j - 1

    # =========================
    # TEXT
    # =========================

    if stripped.startswith("text"):

        text = extract_text(stripped)

        return f"<p{html_attrs}{style_attr}>{text}</p>", j - 1

    # =========================
    # BUTTON
    # =========================

    if stripped.startswith("button"):

        text = extract_text(stripped)

        return f"<button{html_attrs}{style_attr}>{text}</button>", j - 1

    # =========================
    # IMAGE
    # =========================

    if stripped.startswith("img"):

        src = extract_text(stripped)

        return f'<img src="{src}"{html_attrs}{style_attr}>', j - 1

    # =========================
    # LINK
    # =========================

    if stripped.startswith("link"):

        text = extract_text(stripped)

        url_match = re.search(r'->\s*(.+)', stripped)
        url = url_match.group(1) if url_match else "#"

        return f'<a href="{url}"{html_attrs}{style_attr}>{text}</a>', j - 1

    # =========================
    # SECTION
    # =========================

    if stripped.startswith("section:"):

        return f"<section{html_attrs}{style_attr}>", j - 1

    # =========================
    # CARD
    # =========================

    if stripped.startswith("card:"):

        return f'<div class="card"{style_attr}>', j - 1

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

# auto close tags
html.append("</body>")
html.append("</html>")

# create output folder
os.makedirs("output", exist_ok=True)

# write html
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write("\n".join(html))

print("STFL compiled successfully.")
print(f"Output: {OUTPUT_FILE}")
