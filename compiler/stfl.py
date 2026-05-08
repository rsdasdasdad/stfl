import os
import re

INPUT_FILE = "examples/index.stfl"
OUTPUT_FILE = "output/index.html"

CSS_MAP = {
    "bg": "background", "text": "color", "size": "font-size",
    "radius": "border-radius", "spacing": "padding", 
    "font": "font-family", "bold": "font-weight",
    "flex": "display", "dir": "flex-direction", "gap": "gap"
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
    return "".join([f' {k}="{v}"' for k, v in attrs.items()])

def compile_stfl():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    html_body = []
    css_rules = []
    font_imports = []
    page_title = "STFL Page"
    use_icon_engine = False
    
    # 新增：缩进层级栈，用于自动生成 </div>
    stack = [] 

    for line in lines:
        if not line.strip() or line.strip().startswith("#"): continue
        
        # 计算当前行的缩进空格数
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        # 如果当前缩进小于等于栈顶的缩进，说明容器结束了，自动闭合 </div>
        while stack and stack[-1][0] >= indent:
            _, closing_tag = stack.pop()
            html_body.append(closing_tag)

        attrs = parse_attributes(stripped)
        html_attrs = attrs_to_html(attrs)
        line_no_attrs = re.sub(r'\[.*?\]', '', stripped).strip()

        # 1. 页面头部配置
        if stripped.startswith("page "):
            page_title = extract_text(line_no_attrs)
            continue
        if stripped.startswith("font_import "):
            font_url = extract_text(line_no_attrs).replace(" ", "+")
            font_imports.append(f'<link href="https://fonts.googleapis.com/css2?family={font_url}:wght@400;700&display=swap" rel="stylesheet">')
            continue

        # 2. CSS 引擎
        if stripped.startswith("style "):
            selector = extract_text(line_no_attrs)
            if "->" in stripped:
                rules_str = stripped.split("->")[1].strip()
                rules = [r.strip() for r in rules_str.split(",")]
                compiled_rules = []
                for r in rules:
                    if ":" in r:
                        k, v = r.split(":", 1)
                        real_k = CSS_MAP.get(k.strip(), k.strip())
                        compiled_rules.append(f"{real_k}: {v.strip()};")
                css_rules.append(f"{selector} {{ {' '.join(compiled_rules)} }}")
            continue

        # 3. 新增：Box 容器引擎 (完美替代 div)
        if stripped.startswith("box:") or (stripped.startswith("box ") and stripped.endswith(":")):
            html_body.append(f"<div{html_attrs}>")
            # 把当前缩进级别压入栈中，等待后续闭合
            stack.append((indent, "</div>"))
            continue

        # 4. 图标与组件
        if stripped.startswith("svg "): html_body.append(f"<span{html_attrs} class='stfl-svg'>{extract_text(line_no_attrs)}</span>")
        elif stripped.startswith("icon "):
            html_body.append(f'<iconify-icon icon="{extract_text(line_no_attrs)}"{html_attrs}></iconify-icon>')
            use_icon_engine = True
        elif stripped.startswith("title "): html_body.append(f"<h1{html_attrs}>{extract_text(line_no_attrs)}</h1>")
        elif stripped.startswith("subtitle "): html_body.append(f"<h2{html_attrs}>{extract_text(line_no_attrs)}</h2>")
        elif stripped.startswith("text "): html_body.append(f"<p{html_attrs}>{extract_text(line_no_attrs)}</p>")
        elif stripped.startswith("button "): html_body.append(f"<button{html_attrs}>{extract_text(line_no_attrs)}</button>")
        elif stripped.startswith("img "): html_body.append(f'<img src="{extract_text(line_no_attrs)}"{html_attrs}>')
        elif stripped.startswith("input "): html_body.append(f'<input type="text" placeholder="{extract_text(line_no_attrs)}"{html_attrs}>')
        elif stripped.startswith("item "): html_body.append(f"<li{html_attrs}>{extract_text(line_no_attrs)}</li>")
        elif stripped == "divider": html_body.append(f"<hr{html_attrs}>")
        elif stripped.startswith("link "):
            url_part = stripped.split("->")
            url = re.sub(r'\[.*?\]', '', url_part[1]).strip() if len(url_part) > 1 else "#"
            html_body.append(f'<a href="{url}"{html_attrs}>{extract_text(line_no_attrs)}</a>')

    # 文件结束时，闭合所有未闭合的容器
    while stack:
        html_body.append(stack.pop()[1])

    icon_script = '<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>' if use_icon_engine else ""
    css_string = "\n  ".join(css_rules)
    font_string = "\n".join(font_imports)
    
    default_css = """
  body { font-family: system-ui, -apple-system, sans-serif; padding: 20px; line-height: 1.5; color: #333; }
  img { max-width: 100%; }
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
  {css_string}
</style>
</head>
<body>
\n""" + "\n".join(html_body) + "\n\n</body>\n</html>"

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✅ STFL v0.6 编译成功！（已支持 Box 容器与自动缩进引擎）")

if __name__ == "__main__":
    compile_stfl()
