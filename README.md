# STFL — Simple Text Format Language

**STFL** is an AI-friendly web language designed to be simpler than HTML. No closing tags, minimal syntax noise, easy for AI to generate, editable with any text editor, and compilable via drag-and-drop.

## Features

- **No closing tags** — indentation-based structure auto-closes containers
- **TXT editable** — edit with Notepad, VS Code, vim, or any text editor
- **AI friendly** — optimized for LLM generation (fewer tokens, less syntax)
- **Inline CSS system** — attach styles directly to elements
- **Box containers** — auto-indent layout engine (`box:` → `<div>`)
- **Global style rules** — reusable CSS via `style ".class" -> key:val`
- **Google Fonts** — import web fonts with `font_import "Font Name"`
- **100,000+ icons** — Iconify integration (`icon "mdi:github"`)
- **SVG support** — embed SVG directly
- **Drag & Drop compile** — drop `.stfl` files onto `stfl.py` to compile instantly
- **Lightweight** — single Python script compiles to standard HTML

## Quick Start

### Prerequisites

- Python 3.8+

### Installation

```bash
git clone https://github.com/rsdasdasdad/stfl.git
cd stfl
```

### Compile

```bash
python compiler/stfl.py
```

Or specify a custom input/output:

```bash
python compiler/stfl.py examples/landing.stfl output/landing.html
```

### Drag & Drop Compile (v0.8)

On Windows, drag any `.stfl` file and drop it onto `compiler/stfl.py`:

```
stfl.py  ←  drop file here
  ↓
compiles to same directory as .html
  ↓
opens in browser automatically
```

The console window shows compilation results — press Enter to open in browser, then Enter again to exit.

Output: `output/index.html`

## Syntax Reference

### Basic Elements

| STFL | HTML Output | Description |
|------|-------------|-------------|
| `page "Title"` | `<title>Title</title>` | Page title |
| `title "Heading"` | `<h1>Heading</h1>` | Heading |
| `subtitle "Text"` | `<h2>Text</h2>` | Subheading |
| `text "Content"` | `<p>Content</p>` | Paragraph |
| `button "Click"` | `<button>Click</button>` | Button |
| `img "file.png"` | `<img src="file.png">` | Image |
| `input "Name"` | `<input placeholder="Name">` | Input field |
| `item "Item"` | `<li>Item</li>` | List item |
| `link "Label" -> url` | `<a href="url">Label</a>` | Hyperlink |
| `divider` | `<hr>` | Horizontal rule |
| `svg "<svg>..."` | `<span class="stfl-svg">...</span>` | SVG embed |
| `icon "mdi:home"` | `<iconify-icon icon="mdi:home">` | Icon (Iconify) |

### Attributes

Place attributes inside square brackets:

```stfl
title "Hello" [class=hero]
button "Start" [id=start]
text "Content" [class=main,id=hero]
```

### Inline CSS (v0.7)

Attach styles directly to elements using indentation:

```stfl
title "Welcome":
  color = white
  size = 48
  font = Inter
  align = center
  padding = 20
  radius = 12
```

#### Style Properties

| STFL | CSS |
|------|-----|
| `bg` | `background` |
| `color` / `text` | `color` |
| `size` | `font-size` |
| `weight` / `bold` | `font-weight` |
| `align` | `text-align` |
| `radius` | `border-radius` |
| `spacing` / `padding` | `padding` |
| `margin` | `margin` |
| `width` | `width` |
| `height` | `height` |
| `border` | `border` |
| `font` | `font-family` |
| `flex` | `display` |
| `dir` | `flex-direction` |
| `gap` | `gap` |
| `display` | `display` |
| `opacity` | `opacity` |
| `shadow` | `box-shadow` |

### Box Containers

Create `<div>` elements that auto-close based on indentation:

```stfl
box [class=card]:
  title "Card Title"
  text "Card content"

box [id=main]:
  title "Main Section"
  box [class=nested]:
    text "Nested container"
```

Output:

```html
<div class="card">
  <h1>Card Title</h1>
  <p>Card content</p>
</div>
<div id="main">
  <h1>Main Section</h1>
  <div class="nested">
    <p>Nested container</p>
  </div>
</div>
```

### Global CSS Rules

Define reusable styles:

```stfl
style ".hero" -> bg:black, text:white, size:48px
style ".card" -> bg:white, padding:20px, radius:12, shadow:0 2px 8px rgba(0,0,0,0.1)
```

Usage:

```stfl
title "Welcome" [class=hero]
```

### Google Fonts

```stfl
font_import "Inter"
font_import "Noto Sans SC"

title "Hello":
  font = Inter
```

### Comments

```stfl
# this is a comment
# comments are ignored during compilation
```

### Escaping Quotes

```stfl
text "He said \"Hello\""
```

## Full Example

```stfl
page "STFL Demo"

font_import "Inter"

style ".hero" -> bg:linear-gradient(135deg, #667eea 0%, #764ba2 100%), text:white, padding:60px, radius:16

box [class=hero]:
  title "STFL":
    size = 48
    color = white
    font = Inter
    align = center

  text "Simple Text Format Language":
    size = 20
    color = white
    align = center

  button "Get Started":
    bg = #667eea
    color = white
    padding = 14
    radius = 10

divider

text "Built with STFL":
  color = gray
  size = 14
  align = center
```

## Project Structure

```
stfl/
├── compiler/
│   └── stfl.py          # STFL compiler (Python)
├── examples/
│   ├── index.stfl        # Main example
│   └── landing.stfl      # Landing page example
├── output/               # Compiled HTML output
├── docs/
│   └── ai-guide.md       # Guide for AI generation
├── spec/
│   └── stfl-spec.md      # Language specification
└── README.md
```

## Why STFL?

- **Less verbose** — no closing tags means less typing and fewer errors
- **Easier for AI** — fewer tokens, simpler grammar, cleaner output
- **TXT-native** — works with any text editor, no IDE required
- **Semantic** — cleaner structure than raw HTML
- **Fast prototyping** — go from idea to rendered page in seconds

## License

MIT
