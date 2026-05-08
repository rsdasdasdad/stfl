Markdown

# STFL

Simple Text Format Language

STFL is an AI-friendly web language designed to be simpler than HTML, editable with TXT editors, and easy for AI systems to generate.

---

# Features

- Simple syntax
- TXT editable
- AI friendly
- HTML compiler
- Built-in CSS system
- SVG support
- Global icon system
- Google Fonts support
- No closing tags
- Lightweight
- Easy to learn

---

# Installation

Clone repository:

```bash
git clone https://github.com/rsdasdasdad/stfl.git
Enter project:

Bash

cd stfl
Requirements
Python 3.8+
Check Python:

Bash

python --version
Compile STFL
Run compiler:

Bash

python compiler/stfl.py
Generated file:

text

output/index.html
Basic Syntax
page
Defines webpage title.

stfl

page "My Website"
title
Creates heading.

stfl

title "Hello"
Output:

HTML

<h1>Hello</h1>
subtitle
Creates subtitle.

stfl

subtitle "Welcome"
text
Creates paragraph.

stfl

text "Hello World"
button
Creates button.

stfl

button "Click"
img
Creates image.

stfl

img "logo.png"
input
Creates input field.

stfl

input "Enter your name"
divider
Creates horizontal divider.

stfl

divider
item
Creates list item.

stfl

item "Feature One"
link
Creates hyperlink.

stfl

link "GitHub" -> https://github.com
Attributes
Attributes are written inside brackets.

class
stfl

title "Hello" [class=hero]
id
stfl

button "Start" [id=start]
Multiple Attributes
stfl

text "Hello" [class=main,id=hero]
CSS System
STFL includes built-in CSS styling.

Inline Style Block
stfl

title "Hello":
  color = red
  size = 32
  align = center
Supported Style Properties
STFL	CSS
color	color
bg	background
size	font-size
width	width
height	height
padding	padding
margin	margin
radius	border-radius
align	text-align
weight	font-weight
border	border
display	display
gap	gap
font	font-family
Example
stfl

button "Start":
  bg = blue
  color = white
  padding = 12
  radius = 8
Global CSS Rules
Define reusable styles.

Syntax
stfl

style ".hero" -> bg:black, text:white, size:48px
Usage
stfl

title "Welcome" [class=hero]
Font System
STFL supports custom fonts and Google Fonts.

Import Font
stfl

font_import "Inter"
Use Font
stfl

title "Hello":
  font = Inter
Chinese Fonts
stfl

text "你好":
  font = "Microsoft YaHei"
SVG System
STFL includes built-in SVG support.

Native SVG
stfl

svg "<svg viewBox='0 0 24 24'><circle cx='12' cy='12' r='10'/></svg>"
Icon System
STFL supports global icons using Iconify.

More than 100,000 icons available.

Basic Icon
stfl

icon "mdi:github"
Logo Icon
stfl

icon "logos:python"
Phosphor Icon
stfl

icon "ph:rocket-launch-duotone"
Styling Icons
stfl

icon "mdi:github":
  size = 64
  color = black
Icon Search
Search icons here:

https://icones.js.org/

Escaping Quotes
Use backslash:

stfl

text "He said \"Hello\""
Comments
stfl

# this is comment
Full Example
stfl

page "STFL Demo"

font_import "Inter"

style ".hero" -> bg:black, text:white, padding:40px

title "STFL" [class=hero]:
  font = Inter
  size = 48

subtitle "AI Native Web Language"

text "Build websites with plain text."

divider

button "Get Started":
  bg = blue
  color = white
  padding = 14
  radius = 10

icon "mdi:github":
  size = 48

link "GitHub" -> https://github.com

svg "<svg viewBox='0 0 24 24'><circle cx='12' cy='12' r='10' fill='red'/></svg>"
Example Output
HTML

<h1 class="hero" style="font-family:Inter;font-size:48px;">
STFL
</h1>
Project Structure
text

stfl/
├── compiler/
│   └── stfl.py
├── docs/
├── examples/
├── output/
├── spec/
├── README.md
└── LICENSE
AI Usage
STFL is optimized for AI generation.

Example Prompt
text

Generate a modern STFL landing page.

Rules:
- Only output STFL
- No HTML
- Use icons
- Use CSS system
Why STFL?
STFL is designed for:

Humans
AI systems
Fast prototyping
Modern UI generation
Unlike HTML:

No closing tags
Less syntax noise
Easier for AI
More semantic
Future Features
AST parser
Components
Variables
Loops
Conditions
Theme system
React compiler
Vue compiler
VSCode extension
Live preview
