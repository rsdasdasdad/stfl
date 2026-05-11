
# STFL AI Specification

Version: v1.3

STFL (Simple Text Format Language) is an AI-native web language designed for simple webpage generation using plain text and indentation-based structure. It compiles to standard HTML via `compiler/beta_stfl.py`.

This document defines the official AI generation rules for STFL v1.3.

---

# Core Principles

STFL is designed to:

- Be easier than HTML
- Be AI-friendly
- Avoid closing tags
- Reduce syntax noise
- Use semantic structure
- Support fast UI generation

---

# Compiler

```bash
# Default: examples/index.stfl → output/index.html
python compiler/beta_stfl.py

# Custom paths
python compiler/beta_stfl.py input.stfl output.html

# Drag & Drop (Windows): drop .stfl files on beta_stfl.py
```

---

# AI Output Rules

When generating STFL:

- Only output valid STFL
- Never output HTML
- Never output Markdown
- Use indentation for structure (2 spaces per level)
- Prefer semantic containers
- Use double quotes for text values
- Avoid unnecessary symbols

---

# File Extension

```text
.stfl
```

---

# Basic Elements

---

## Page

Defines webpage title. Should be first line.

```stfl
page "My Website"
```

---

## Title

Creates `<h1>`.

```stfl
title "Hello World"
```

---

## Subtitle

Creates `<h2>`.

```stfl
subtitle "Welcome"
```

---

## Text

Creates `<p>`.

```stfl
text "Hello World"
```

---

## Button

Creates `<button>`. Add `onclick` for interactivity.

```stfl
button "Start"
button "Click" [onclick=alert("hi")]
```

---

## Image

Creates `<img>`.

```stfl
img "logo.png"
```

---

## Input

Creates `<input type="text">`.

```stfl
input "Enter your name"
```

---

## Divider

Creates `<hr>`.

```stfl
divider
```

---

## Item

Creates `<li>` (list item). Use inside containers.

```stfl
item "Feature one"
item "Feature two"
```

---

## Link

Creates `<a>` hyperlink. URLs are auto-sanitized (javascript:/data: protocols are blocked).

```stfl
link "GitHub" -> https://github.com
```

---

## Icon

Creates `<iconify-icon>` with 100,000+ icons from Iconify (https://icones.js.org).

```stfl
icon "mdi:github"
icon "logos:python"
icon "ph:rocket-launch-duotone"
```

---

## SVG

Embeds raw SVG without HTML escaping.

```stfl
svg "<svg viewBox='0 0 24 24'><circle cx='12' cy='12' r='10'/></svg>"
```

---

## Video (v1.3)

Creates `<video controls>`.

```stfl
video "https://example.com/clip.mp4"
```

---

## Audio (v1.3)

Creates `<audio controls>`.

```stfl
audio "https://example.com/sound.mp3"
```

---

## Raw HTML (v1.3)

Outputs raw HTML without escaping. Use for custom embeds, inline scripts, or third-party widgets.

```stfl
raw "<div style='background:yellow;padding:16px'>Custom HTML</div>"
raw "<script>alert('hello')</script>"
```

---

# Directives

---

## CSS Variables (v1.3)

Define CSS custom properties that generate `:root { --key: value; }`.

```stfl
var primary=#6366f1
var secondary=#ec4899
var radius=12
```

Reference in styles:

```stfl
button "Click":
  bg = var(--primary)
  radius = var(--radius)
```

---

## Meta Tags (v1.3)

Add `<meta>` tags to `<head>`. Use commas between attributes.

```stfl
meta [name=description, content="STFL demo"]
meta [name=theme-color, content="#6366f1"]
```

---

## External CSS (v1.3)

Link external stylesheets.

```stfl
css "https://cdn.example.com/style.css"
```

---

## External JS (v1.3)

Link external JavaScript (loaded at end of `<body>`).

```stfl
js "https://cdn.example.com/app.js"
```

---

## Font Import

Import Google Fonts. Auto-adds `<link rel="preconnect">` for performance.

```stfl
font_import "Inter"
font_import "Noto Sans SC"
```

---

# Layout System

STFL uses indentation-based containers that auto-close. No closing tags needed.

Available containers:

| STFL | HTML | Use Case |
|------|------|----------|
| `box:` | `<div>` | Generic container |
| `section:` | `<section>` | Thematic section |
| `header:` | `<header>` | Page/component header |
| `footer:` | `<footer>` | Page/component footer |
| `main:` | `<main>` | Primary content |
| `nav:` | `<nav>` | Navigation block |
| `article:` | `<article>` | Self-contained content |
| `aside:` | `<aside>` | Sidebar or complement |

Containers close when the next line has equal or lesser indentation.

```stfl
box [class=card]:
  title "Hello"
  text "World"

section:
  box [class=nested]:
    text "Nested works via deeper indent"
```

---

# Attributes

Attributes use square brackets. Commas between multiple attributes.

```stfl
title "Hello" [class=hero]
button "Start" [id=main]
text "Hello" [class=main, id=hero]
```

Attribute values are HTML-escaped automatically.

---

# Class Shorthand (v1.3)

Use dot syntax to add CSS classes. Works on all elements and containers.

| Shorthand | Equivalent |
|-----------|------------|
| `title.large` | `title [class=large]` |
| `button.primary.large` | `button [class="primary large"]` |
| `box.card.bordered` | `box [class="card bordered"]` |

```stfl
title.large "Hello" [id=main]:
  color = blue

button.primary "Click":
  bg = var(--primary)
```

---

# CSS System

## Inline Styles

Styles are written below elements using a colon suffix and indented properties.

```stfl
title "Hello":
  color = red
  size = 32
  align = center
```

Numeric values automatically get `px` suffix. Unitless CSS properties never get `px`.

### Supported Style Properties

| STFL | CSS |
|------|------|
| color | color |
| bg | background |
| size | font-size |
| width | width |
| height | height |
| padding | padding |
| margin | margin |
| radius | border-radius |
| align | text-align |
| weight | font-weight |
| border | border |
| display | display |
| gap | gap |
| font | font-family |
| opacity | opacity |
| shadow | box-shadow |
| line-height | line-height |
| max-width | max-width |
| class | (attribute) |
| id | (attribute) |

### Unitless Properties

These properties never get `px` auto-appended:

- opacity
- font-weight
- z-index
- line-height
- flex-grow
- flex-shrink
- order

### Multi-Value Properties

Space-separated values each get `px` independently:

```stfl
button "Start":
  padding = 14 28    # → padding: 14px 28px
  margin = 0 auto   # → margin: 0px auto
```

---

## Global Styles

Define reusable CSS rules. Two formats:

One-liner with `->`:

```stfl
style ".hero" -> bg:black, text:white, padding:40px
```

Multi-line with indented properties:

```stfl
style ".card":
  bg = white
  padding = 24
  radius = 12
  shadow = 0 2px 8px rgba(0,0,0,0.1)
```

Usage:

```stfl
title "Welcome" [class=hero]
```

---

# Comments

```stfl
# this is a comment
```

---

# Escaping Quotes

Use backslash inside quoted strings.

```stfl
text "He said \"Hello\""
```

Both single and double quotes are supported by the compiler.

---

# AI Best Practices

When generating STFL v1.3:

- Use semantic containers (section, nav, article) over generic `box:`
- Use class shorthand (`title.large`) for cleaner code
- Use `var` for theme colors and spacing
- Add `meta` for SEO/description
- Use `onclick` for interactive buttons
- Follow the pattern: directives first, then content
- Use icons (`icon "mdi:name"`) for visual elements
- Use `raw` only when HTML passthrough is needed (embeds, scripts)
- Keep indentation consistent (2 spaces per level)

---

# Recommended Structure

```
page "Website Title"
var primary=#6366f1
font_import "Inter"
meta [name=description, content="..."]

style ".header" -> bg:var(--primary), text:white

section.header:

nav:

main:

footer:
```

---

# Security Notes (v1.3)

- URLs in `link` elements are sanitized: `javascript:` and `data:` protocols are blocked
- All attribute values are HTML-escaped
- Attribute keys are validated against pattern injection
- Raw SVG content is not escaped, use with trusted content only

---

# Example Landing Page

```stfl
page "STFL Landing"

var primary=#6366f1
var radius=12

font_import "Inter"

meta [name=description, content="STFL demo"]

style ".hero" -> bg:var(--primary), text:white, padding:80px
style ".card" -> bg:white, padding:24, radius:var(--radius), shadow:0 2px 8px rgba(0,0,0,0.1)

section.hero [style=text-align:center]:
  title "STFL v1.3"
  text "AI Native Web Language"

box [class=card]:
  title "Features"
  item "No closing tags"
  item "AI friendly"

icon "mdi:github"

link "GitHub" -> https://github.com
```

---

# AI Generation Constraints

AI should NOT:

- Output HTML tags
- Use closing tags
- Generate invalid indentation
- Mix Markdown with STFL
- Use unsupported syntax
- Generate random symbols
- Use `javascript:` protocol in links

---

# Purpose

STFL is designed for:

- AI webpage generation
- Rapid prototyping
- Lightweight websites
- Landing pages
- Dashboards
- Documentation sites
- AI-native interfaces

---

# Future Features

Planned:

- Components
- Loops
- Conditions
- React compiler
- Vue compiler
- Live preview
- VSCode extension

---

# Official Positioning

STFL is:

```text
AI Native Web Language
```

Designed for both:

- Humans
- AI systems
