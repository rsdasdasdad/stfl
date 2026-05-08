# Layout System

STFL includes a lightweight layout system for building modern UI structures.

Unlike HTML, STFL layouts are indentation-based and AI friendly.

---

# div

Creates a generic container.

## STFL

```stfl
div:
  title "Hello"

  text "World"
HTML Output
HTML

<div>
  <h1>Hello</h1>
  <p>World</p>
</div>
div with class
STFL
stfl

div [class=hero]:
  title "STFL"
Output
HTML

<div class="hero">
  <h1>STFL</h1>
</div>
div with id
STFL
stfl

div [id=main]:
div with styles
STFL
stfl

div [class=card]:
  bg = white
  padding = 20
  radius = 12
Output
HTML

<div class="card"
style="
background:white;
padding:20px;
border-radius:12px;
">
</div>
Semantic Containers
STFL also supports semantic layout blocks.

These are recommended for AI generation.

section
stfl

section:
  title "News"
card
stfl

card:
  text "Content"
hero
stfl

hero:
  title "Welcome"
navbar
stfl

navbar:
  link "Home" -> /
footer
stfl

footer:
  text "2026 STFL"
Why Layout Blocks?
STFL layout system is designed for:

AI generation
Clean structure
Readability
Less syntax noise
Faster prototyping
Example UI
stfl

page "Landing"

hero [class=main-hero]:

  title "STFL":
    size = 48

  text "AI Native Web Language"

  button "Get Started":
    bg = blue
    color = white

section:

  card:
    title "Simple"

    text "TXT editable"

  card:
    title "AI Friendly"

    text "Optimized for LLMs"

footer:
  text "Powered by STFL"
Future Layout Features
Planned features:

grid
flex
stack
sidebar
container
columns
responsive layout
component nesting
