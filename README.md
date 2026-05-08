
# STFL

Simple Text Format Language

STFL is an AI-friendly web language designed to be simpler than HTML, editable in TXT editors, and easy for AI systems to generate.

---

# Features

- Simple syntax
- TXT editable
- AI friendly
- HTML compiler
- No closing tags
- Indentation-based layout
- Lightweight
- Easy to learn

---

# Example

## STFL

```stfl
page "My Website"

title "Welcome"

text "Hello STFL"

button "Start"

link "GitHub" -> https://github.com
Output HTML
HTML

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>My Website</title>
</head>
<body>

<h1>Welcome</h1>

<p>Hello STFL</p>

<button>Start</button>

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
STFL Syntax
page
Defines webpage title.

stfl

page "My Site"
Compiles to:

HTML

<title>My Site</title>
title
Creates heading.

stfl

title "Hello"
Output:

HTML

<h1>Hello</h1>
text
Creates paragraph.

stfl

text "Hello World"
Output:

HTML

<p>Hello World</p>
button
Creates button.

stfl

button "Click"
Output:

HTML

<button>Click</button>
img
Creates image.

stfl

img "logo.png"
Output:

HTML

<img src="logo.png">
link
Creates hyperlink.

stfl

link "OpenAI" -> https://openai.com
Output:

HTML

<a href="https://openai.com">OpenAI</a>
Layout Components
section
Creates section block.

stfl

section:
  title "News"
Output:

HTML

<section>
  <h1>News</h1>
</section>
card
Creates card container.

stfl

card:
  text "Card Content"
Output:

HTML

<div class="card">
  <p>Card Content</p>
</div>
Attributes
class
stfl

title "Hello" [class=main]
Output:

HTML

<h1 class="main">Hello</h1>
id
stfl

button "Start" [id=begin]
Output:

HTML

<button id="begin">Start</button>
Escaping Quotes
Use backslash:

stfl

text "He said \"Hello\""
Output:

HTML

<p>He said "Hello"</p>
Full Example
stfl

page "STFL Demo"

section:

  title "Welcome" [class=hero]

  text "STFL is AI friendly"

  button "Start"

  card:
    title "Fast"

    text "Simple syntax"

link "GitHub" -> https://github.com
Project Structure
text

stfl/
├── compiler/
│   └── stfl.py
├── examples/
│   └── index.stfl
├── output/
│   └── index.html
├── spec/
│   └── stfl-spec.md
├── docs/
│   └── ai-guide.md
├── README.md
└── LICENSE
AI Usage
STFL is designed for AI generation.

Prompt example:

text

Generate a STFL landing page.

Rules:
- Only output STFL
- No HTML
- Use title/text/button/section/card
Future Features
AST parser
CSS system
Components
Variables
Loops
Conditions
React compiler
Live preview
VSCode extension
License
MIT License

text


━━━━━━━━━━━━━━━━━━━

# spec/stfl-spec.md

```md
# STFL Specification v0.2

---

# Syntax Rules

- UTF-8 encoding
- Indentation-based
- No closing tags
- Double quotes for text
- Optional attributes

---

# Components

## page

```stfl
page "Site"
title
stfl

title "Hello"
text
stfl

text "Hello"
button
stfl

button "Click"
img
stfl

img "image.png"
link
stfl

link "GitHub" -> https://github.com
Containers
section
stfl

section:
card
stfl

card:
Attributes
stfl

title "Hello" [class=hero,id=main]
Escaping
stfl

text "He said \"Hello\""
Comments
stfl

# this is comment
text


━━━━━━━━━━━━━━━━━━━

# docs/ai-guide.md

```md
# STFL AI Guide

STFL is optimized for AI generation.

---

# Rules

- Only output STFL
- Never output HTML
- Use indentation
- Use semantic blocks

---

# Recommended Components

- page
- section
- card
- hero
- title
- text
- button

---

# Example Prompt

```text
Generate a modern STFL website.

Requirements:
- dark theme
- hero section
- pricing cards
- footer
Example Output
stfl

page "AI Site"

hero:
  title "Future"

  text "AI Native Web"

  button "Start"
text


━━━━━━━━━━━━━━━━━━━

# examples/landing.stfl

```stfl
page "Landing"

section:

  title "STFL"

  text "AI Native Web Language"

  button "Get Started"

card:
  title "Fast"

  text "Simple syntax"

card:
  title "AI Friendly"

  text "Perfect for LLMs"

link "GitHub" -> https://github.com