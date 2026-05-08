import os
import re

INPUT_FILE = "examples/index.stfl"
OUTPUT_FILE = "output/index.html"

html = []
stack = []

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

def compile_line(line):
    stripped = line.strip()

    if not stripped:
        return ""

    if stripped.startswith("#"):
        return ""

    attrs = parse_attributes(stripped)
    html_attrs = attrs_to_html(attrs)

    if stripped.startswith("page"):
        title = extract_text(stripped)

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
"""

    if stripped.startswith("title"):
        text = extract_text(stripped)
        return f"<h1{html_attrs}>{text}</h1>"

    if stripped.startswith("text"):
        text = extract_text(stripped)
        return f"<p{html_attrs}>{text}</p>"

    if stripped.startswith("button"):
        text = extract_text(stripped)
        return f"<button{html_attrs}>{text}</button>"

    if stripped.startswith("img"):
        src = extract_text(stripped)
        return f'<img src="{src}"{html_attrs}>'

    if stripped.startswith("link"):
        text = extract_text(stripped)

        url_match = re.search(r'->\s*(.+)', stripped)
        url = url_match.group(1) if url_match else "#"

        return f'<a href="{url}"{html_attrs}>{text}</a>'

    if stripped.startswith("section:"):
        stack.append("</section>")
        return f"<section{html_attrs}>"

    if stripped.startswith("card:"):
        stack.append("</div>")
        return '<div class="card">'

    return ""

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    compiled = compile_line(line)

    if compiled:
        html.append(compiled)

while stack:
    html.append(stack.pop())

html.append("</body>")
html.append("</html>")

os.makedirs("output", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write("\n".join(html))

print("STFL compiled successfully.")
print(f"Output: {OUTPUT_FILE}")
