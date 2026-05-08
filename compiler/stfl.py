import re
import os

INPUT_FILE = "examples/index.stfl"
OUTPUT_FILE = "output/index.html"

html = []

def extract_text(line):
    match = re.findall(r'"(.*?)"', line)
    return match[0] if match else ""

def compile_line(line):
    line = line.strip()

    if not line:
        return ""

    # PAGE
    if line.startswith("page"):
        title = extract_text(line)

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
</head>
<body>
"""

    # TITLE
    if line.startswith("title"):
        text = extract_text(line)
        return f"<h1>{text}</h1>"

    # TEXT
    if line.startswith("text"):
        text = extract_text(line)
        return f"<p>{text}</p>"

    # BUTTON
    if line.startswith("button"):
        text = extract_text(line)
        return f"<button>{text}</button>"

    # IMAGE
    if line.startswith("img"):
        src = extract_text(line)
        return f'<img src="{src}">'

    # LINK
    if line.startswith("link"):
        text = extract_text(line)

        url_match = re.search(r'->\s*(.+)', line)
        url = url_match.group(1) if url_match else "#"

        return f'<a href="{url}">{text}</a>'

    return ""

# Read STFL
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Compile
for line in lines:
    compiled = compile_line(line)

    if compiled:
        html.append(compiled)

# Close HTML
html.append("</body>")
html.append("</html>")

# Create output folder
os.makedirs("output", exist_ok=True)

# Write output
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write("\n".join(html))

print("STFL compiled successfully.")
print(f"Output: {OUTPUT_FILE}")