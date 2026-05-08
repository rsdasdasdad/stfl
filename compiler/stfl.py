import os
import re

INPUT_FILE = "examples/index.stfl"
OUTPUT_FILE = "output/index.html"

# STFL CSS 简写引擎
CSS_MAP = {
    "bg": "background",
    "text": "color",
    "size": "font-size",
    "radius": "border-radius",
    "spacing": "padding",
    "font": "font-family",
    "bold": "font-weight"
}

def extract_text(line):
    start = line.find('"')
    end = line.rfind('"')
    if start != -1 and end != -1 and start != end:
        return line[start+1:end].replace('\\"', '"')
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
    res = ""
    for k, v in attrs.items():
        res += f' {k}="{v}"'
    return res

def compile_stfl():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    html_body = []
    css_rules = []
    font_imports = []
    page_title = "STFL Page"
    use_icon_engine = False # 是否启用了内置 SVG 图标引擎

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"): continue

        attrs = parse_attributes(line)
        html_attrs = attrs_to_html(attrs)
        line_no_attrs = re.sub(r'\[.*?\]', '', line).strip()

        # 1. 页面设置
        if line.startswith("page "):
            page_title = extract_text(line_no_attrs)
            continue
        if line.startswith("font_import "):
            font_url = extract_text(line_no_attrs).replace(" ", "+")
            font_imports.append(f'<link href="https://fonts.googleapis.com/css2?family={font_url}:wght@400;700&display=swap" rel="stylesheet">')
            continue

        # 2. CSS 引擎
        if line.startswith("style "):
            selector = extract_text(line_no_attrs)
            if "->" in line:
                rules_str = line.split("->")[1].strip()
                rules = [r.strip() for r in rules_str.split(",")]
                compiled_rules = []
                for r in rules:
                    if ":" in r:
                        k, v = r.split(":", 1)
                        real_k = CSS_MAP.get(k.strip(), k.strip())
                        compiled_rules.append(f"{real_k}: {v.strip()};")
                css_rules.append(f"{selector} {{ {' '.join(compiled_rules)} }}")
            continue

        # 3. 新增：原生 SVG 与内置 Icon 引擎
        if line.startswith("svg "):
            svg_code = extract_text(line_no_attrs)
            # 用 span 包裹以支持类名和样式，并确保 SVG 颜色继承
            html_body.append(f"<span{html_attrs} class='stfl-svg'>{svg_code}</span>")
            continue
            
        if line.startswith("icon "):
            icon_name = extract_text(line_no_attrs)
            html_body.append(f'<iconify-icon icon="{icon_name}"{html_attrs}></iconify-icon>')
            use_icon_engine = True
            continue

        # 4. 基础 HTML 组件
        if line.startswith("title "): html_body.append(f"<h1{html_attrs}>{extract_text(line_no_attrs)}</h1>")
        elif line.startswith("subtitle "): html_body.append(f"<h2{html_attrs}>{extract_text(line_no_attrs)}</h2>")
        elif line.startswith("text "): html_body.append(f"<p{html_attrs}>{extract_text(line_no_attrs)}</p>")
        elif line.startswith("button "): html_body.append(f"<button{html_attrs}>{extract_text(line_no_attrs)}</button>")
        elif line.startswith("img "): html_body.append(f'<img src="{extract_text(line_no_attrs)}"{html_attrs}>')
        elif line.startswith("input "): html_body.append(f'<input type="text" placeholder="{extract_text(line_no_attrs)}"{html_attrs}>')
        elif line.startswith("item "): html_body.append(f"<li{html_attrs}>{extract_text(line_no_attrs)}</li>")
        elif line == "divider": html_body.append(f"<hr{html_attrs}>")
        elif line.startswith("link "):
            url_part = line.split("->")
            url = re.sub(r'\[.*?\]', '', url_part[1]).strip() if len(url_part) > 1 else "#"
            html_body.append(f'<a href="{url}"{html_attrs}>{extract_text(line_no_attrs)}</a>')

    # 动态引入外部脚本
    icon_script = '<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>' if use_icon_engine else ""
    css_string = "\n  ".join(css_rules)
    font_string = "\n".join(font_imports)
    
    default_css = """
  body { font-family: system-ui, -apple-system, sans-serif; padding: 20px; line-height: 1.5; color: #333; }
  img { max-width: 100%; }
  /* SVG 默认样式：继承文字颜色并垂直居中 */
  .stfl-svg svg { width: 1em; height: 1em; vertical-align: -0.125em; fill: currentColor; }
  iconify-icon { display: inline-flex; vertical-align: -0.125em; }
    """

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
  /* STFL Generated CSS */
  {css_string}
</style>
</head>
<body>
\n""" + "\n".join(html_body) + "\n\n</body>\n</html>"

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✅ STFL v0.5 编译成功！（已支持 原生 SVG 与 Iconify 引擎）")

if __name__ == "__main__":
    compile_stfl()
