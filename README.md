Markdown

# STFL

Simple Text Format Language

STFL is an AI-friendly web language designed to be simpler than HTML, editable in TXT editors, and easy for AI systems to generate.

---

# Features

- Simple syntax
- TXT editable
- AI friendly
- HTML compiler
- Built-in CSS system
- No closing tags
- Lightweight
- Easy to learn

---

# Example

## STFL

```stfl
page "My Website"

title "Welcome":
  color = white
  bg = blue
  size = 40
  padding = 20

text "Hello STFL":
  color = gray
  size = 18

button "Start":
  bg = black
  color = white
  padding = 12
  radius = 8

link "GitHub" -> https://github.com
HTML Output
HTML

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>My Website</title>
</head>
<body>

<h1 style="color:white;background:blue;font-size:40px;padding:20px;">
Welcome
</h1>

<p style="color:gray;font-size:18px;">
Hello STFL
</p>

<button style="background:black;color:white;padding:12px;border-radius:8px;">
Start
</button>

<a href="https://github.com">GitHub</a>

</body>
</html>
Installation
Clone repository:

Bash

git clone https://github.com/rsdasdasdad/stfl.git
Enter folder:

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
Syntax
page
Defines webpage title.

stfl

page "My Site"
title
Creates heading.

stfl

title "Hello"
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
link
Creates hyperlink.

stfl

link "OpenAI" -> https://openai.com
Containers
section
Creates section block.

stfl

section:
  title "News"
card
Creates card container.

stfl

card:
  text "Card Content"
Attributes
class
stfl

title "Hello" [class=hero]
id
stfl

button "Start" [id=begin]
CSS System
STFL includes a built-in CSS styling system.

Style blocks are written below components using indentation.

Example
stfl

title "Hello":
  color = red
  size = 32
  align = center
Output:

HTML

<h1 style="color:red;font-size:32px;text-align:center;">
Hello
</h1>
Supported CSS Properties
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
Example UI
stfl

page "Landing"

title "STFL":
  color = white
  bg = black
  size = 48
  padding = 24
  align = center

text "AI Native Web Language":
  color = gray
  size = 20
  align = center

button "Get Started":
  bg = blue
  color = white
  padding = 14
  radius = 10
Escaping Quotes
Use backslash:

stfl

text "He said \"Hello\""
Output:

HTML

<p>He said "Hello"</p>
AI Usage
STFL is designed for AI generation.

Prompt example:

text

Generate a STFL landing page.

Rules:
- Only output STFL
- No HTML
- Use title/text/button/section/card
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
Future Features
AST parser
Component system
Variables
Loops
Conditions
External CSS
React compiler
VSCode extension
Live preview
