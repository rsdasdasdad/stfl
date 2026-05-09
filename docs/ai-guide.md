
# STFL AI Specification

Version: v0.6

STFL (Simple Text Format Language) is an AI-native web language designed for simple webpage generation using plain text and indentation-based structure.

This document defines the official AI generation rules for STFL.

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

# AI Output Rules

When generating STFL:

- Only output valid STFL
- Never output HTML
- Never output Markdown
- Use indentation for structure
- Prefer semantic containers
- Use double quotes
- Avoid unnecessary symbols

---

# File Extension

```text
.stfl
```

---

# Basic Syntax

---

## Page

Defines webpage title.

```stfl
page "My Website"
```

---

## Title

Creates main heading.

```stfl
title "Hello"
```

---

## Subtitle

Creates secondary heading.

```stfl
subtitle "Welcome"
```

---

## Text

Creates paragraph.

```stfl
text "Hello World"
```

---

## Button

Creates button.

```stfl
button "Start"
```

---

## Image

Creates image.

```stfl
img "logo.png"
```

---

## Input

Creates text input.

```stfl
input "Enter your name"
```

---

## Divider

Creates horizontal line.

```stfl
divider
```

---

## Link

Creates hyperlink.

```stfl
link "GitHub" -> https://github.com
```

---

# Layout System

STFL uses semantic layout containers.

AI should prefer semantic containers over generic HTML structures.

---

## box

Generic layout container.

```stfl
box:
  title "Hello"
```

---

## Recommended Semantic Containers

Use these whenever possible:

```stfl
hero:
section:
card:
navbar:
footer:
sidebar:
container:
grid:
```

Example:

```stfl
hero:
  title "Welcome"
```

---

# Attributes

Attributes are written using square brackets.

---

## Class

```stfl
title "Hello" [class=hero]
```

---

## ID

```stfl
button "Start" [id=main]
```

---

## Multiple Attributes

```stfl
text "Hello" [class=main,id=hero]
```

---

# CSS System

STFL includes built-in CSS shorthand syntax.

---

# Inline Styles

Styles are written below components using indentation.

Example:

```stfl
title "Hello":
  color = red
  size = 32
  align = center
```

---

# Supported Style Properties

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
| line-height | line-height |
| max-width | max-width |

---

# Global Styles

Reusable styles.

Syntax:

```stfl
style ".hero" -> bg:black, text:white
```

Usage:

```stfl
title "Hello" [class=hero]
```

---

# Font System

---

## Import Font

```stfl
font_import "Inter"
```

---

## Use Font

```stfl
title "Hello":
  font = Inter
```

---

## Chinese Fonts

```stfl
text "你好":
  font = "Microsoft YaHei"
```

---

# SVG System

STFL supports raw SVG.

---

## Native SVG

```stfl
svg "<svg viewBox='0 0 24 24'><circle cx='12' cy='12' r='10'/></svg>"
```

---

# Icon System

STFL supports Iconify icons.

---

## Icon Syntax

```stfl
icon "mdi:github"
```

---

## Logo Icons

```stfl
icon "logos:python"
```

---

## Phosphor Icons

```stfl
icon "ph:rocket-launch-duotone"
```

---

# Icon Styling

```stfl
icon "mdi:github":
  size = 64
  color = white
```

---

# Comments

```stfl
# this is comment
```

---

# Escaping Quotes

Use backslash.

```stfl
text "He said \"Hello\""
```

---

# AI Best Practices

AI should:

- Prefer semantic containers
- Use clean indentation
- Avoid deeply nested structures
- Use reusable styles
- Use modern UI structure
- Prefer minimal syntax
- Use icons for visual UI
- Use responsive layout concepts

---

# Recommended Structure

Recommended webpage structure:

```stfl
page "Website"

navbar:

hero:

section:

footer:
```

---

# Example Landing Page

```stfl
page "STFL"

font_import "Inter"

style ".hero" -> bg:black, text:white, padding:80px

box [class=hero]:

  title "STFL"

  text "AI Native Web Language"

  button "Get Started"

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

- AST parser
- Components
- Variables
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
```