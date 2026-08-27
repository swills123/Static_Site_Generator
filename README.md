# Static Site Generator

A static site generator built from scratch in Python. It converts a directory of Markdown files into a fully linked static website, using a simple HTML template and CSS stylesheet.

Live demo: https://swills123.github.io/Static_Site_Generator/

## Features

- Full Markdown-to-HTML pipeline, built without external Markdown libraries:
  - Inline parsing: **bold**, _italic_, `code`, links, and images
  - Block parsing: paragraphs, headings (`#` through `######`), quotes, ordered and unordered lists, and code blocks
- Recursively converts an entire `content/` directory tree into a matching HTML site
- Copies static assets (images, CSS) from `static/` into the output directory
- Supports a configurable base path, so the same codebase can run locally (`/`) or be deployed to a subdirectory (e.g. GitHub Pages)
- Extracts page titles automatically from each Markdown file's `h1` heading

## Project Structure

```
├── content/           # Markdown source files (site pages, in nested folders)
├── static/            # Static assets: images, CSS
├── src/                # Python source code
│   ├── main.py                # Entry point; orchestrates the build
│   ├── textnode.py            # TextNode/TextType + conversion to HTMLNode
│   ├── htmlnode.py             # HTMLNode, LeafNode, ParentNode
│   ├── inline_markdown.py      # Inline markdown parsing (bold, italic, links, images)
│   ├── markdown_blocks.py      # Block-level parsing and HTML generation
│   └── tests/                  # Unit tests
├── template.html       # HTML template with {{ Title }} and {{ Content }} placeholders
├── main.sh             # Builds the site locally and serves it at localhost:8888
├── build.sh            # Builds the site for production (GitHub Pages base path)
├── test.sh             # Runs the unit test suite
└── docs/               # Generated site output (served by GitHub Pages)
```

## Usage

### Run locally

```sh
./main.sh
```

This generates the site into `docs/` using `/` as the base path, then starts a local server at `http://localhost:8888`.

### Build for production

```sh
./build.sh
```

This generates the site into `docs/` using `/Static_Site_Generator/` as the base path, matching the GitHub Pages deployment URL.

### Run tests

```sh
./test.sh
```

## How It Works

1. **Copy static assets** — everything in `static/` is recursively copied into the output directory.
2. **Walk the content tree** — every Markdown file under `content/` is found recursively.
3. **Parse Markdown** — each file is split into blocks (paragraphs, headings, lists, quotes, code), and each block's inline text is parsed for bold, italic, code, links, and images.
4. **Render to HTML** — the parsed blocks are converted into a tree of HTML nodes and rendered to an HTML string.
5. **Apply the template** — the generated content and extracted title are injected into `template.html`, and any root-relative links are rewritten with the configured base path.
6. **Write the output** — the final HTML file is written to the output directory, mirroring the structure of `content/`.

## Adding a New Page

1. Create a new folder under `content/` (or add a file directly in `content/`) containing an `index.md` file.
2. Start the file with a single `#` heading — this becomes the page's `<title>`.
3. Rebuild the site with `./main.sh` or `./build.sh`.

## Tech Stack

- Python (standard library only — no external Markdown or templating dependencies)
- `unittest` for testing
- Deployed via GitHub Pages

## Credits

Built as part of the [Static Site Generator course on Boot.dev](https://www.boot.dev/courses/build-static-site-generator-python).