# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Quarto-based personal blog and technical website for Chuck Pepe-Ranney, featuring blog posts, TIL (Today I Learned) entries, and educational content. The site is built with Quarto and includes both Jupyter notebooks (.ipynb) and Quarto markdown (.qmd) files.

## Git Worktree Structure

This repository uses a bare git repository (`.bare/`) with multiple worktrees, all living as sibling directories under the same parent:

```
chuckpr.github.io-worktree/
├── .bare/    # Bare git repository (shared by all worktrees)
├── src/      # Main blog content (this directory)
├── about/    # About page content
└── cv/       # CV content
```

### Creating a new worktree

From inside any existing worktree (e.g. `src/`), create a new worktree alongside it:

```bash
git worktree add ../<branch-name>
```

This creates a new directory at the parent level tracking the named branch.

### Removing a worktree

```bash
git worktree remove ../<branch-name>
```

### Development workflow

All new work — TIL posts, blog posts, and site features — should be developed on a dedicated branch in its own worktree rather than directly on `src`:

1. Create a worktree: `git worktree add ../<branch-name>`
2. Develop in that worktree
3. Merge into `src` when complete
4. Clean up: `git worktree remove ../<branch-name>` and `git branch -d <branch-name>`

## Build and Development Commands

### Preview the site
```bash
quarto preview
```
Starts a local development server with live reload at http://localhost:4200

### Build the site
```bash
quarto render
```
Generates the static site in `_site/` directory

### Pre-commit hooks
```bash
pre-commit run --all-files
```
Runs ruff format and isort on Jupyter notebooks via nbQA

## Content Structure

### TIL (Today I Learned) Posts
- Located in `til/*/index.ipynb` or `til/*/index.qmd`
- Each TIL entry is in its own directory with isolated dependencies
- Many TILs use **pixi** for per-project Python environment management
- Each pixi-enabled TIL has its own `pixi.toml` and `pixi.lock` files

To create a new TIL:
1. Use the cookiecutter template in `til-template/`
2. Run: `cookiecutter til-template/` and provide a title
3. This creates a new directory with `index.ipynb`, `pixi.toml`, `.gitignore`, and `.gitattributes`

### Blog Posts
- Located in `posts/*/index.qmd`
- Traditional longer-form blog content
- Metadata defined in YAML frontmatter

### Metadata and Listing System

The site uses a pre-render script to automatically generate metadata:
- `pre-render/make-metadata-listing.py` scans all `.ipynb` and `.qmd` files
- Extracts YAML frontmatter from first cell (notebooks) or file header (qmd)
- Generates `listing.yaml` which drives the site listings
- This script runs automatically before each Quarto render (configured in `_quarto.yml`)

**Important**: The `listing.yaml` file is auto-generated. Do not edit it directly - modify source file frontmatter instead.

## Environment Setup

### Conda Environment
The project uses a conda environment defined in `environment.yaml`:
```bash
conda env create -f environment.yaml
conda activate blog
```

Core dependencies:
- R packages: rmarkdown, knitr, tidyverse, gt, reticulate
- Python packages: polars, great_tables

### Direnv Integration
The `.envrc` file automatically activates the conda environment when entering the directory (requires direnv).

## Styling and Theming

The site supports light/dark mode themes:
- `custom.scss` - Light theme customizations (cosmo base)
- `custom-dark.scss` - Dark theme customizations (solar base)
- `_theme-shared.scss` - Shared theme variables and styles
- `_theme-light-vars.scss` - Light mode CSS variables
- `_theme-dark-vars.scss` - Dark mode CSS variables

Theme configuration is in `_quarto.yml` under `format.html.theme`.

## Content Execution

### Freeze System
Quarto freeze mode is enabled (`freeze: auto` in `_quarto.yml`) to cache computational outputs:
- Cached outputs stored in `_freeze/` directory
- Only re-executes when source files change
- Delete relevant `_freeze/` subdirectory to force re-execution

### Jupyter Notebook Rendering
- Some notebooks have `execute: enabled: true` in frontmatter to ensure execution during render
- Notebooks can include dynamic markdown using `IPython.display.Markdown` or Quarto inline code syntax
- Use `#| echo: false` for hidden code cells

## DNA Helix Animation

The homepage features an animated Braille-art DNA double helix (`dna-helix.js`), embedded in `index.qmd`.

- **Rendering**: Two sine-wave strands offset by pi, connected by rungs, encoded into Unicode Braille characters (U+2800-U+28FF). Each Braille glyph represents a 2x4 pixel block.
- **Coloring**: Per-character `<span>` elements with CSS classes: `.s1` (blue-green strand), `.s2` (orange strand), `.rg` (gray rungs). Uses `innerHTML` not `textContent`.
- **Glow**: Layered `text-shadow` in `_theme-shared.scss`, intensified in dark mode via `body.quarto-dark` selectors.
- **Handedness**: Right-handed helix (negative `PHASE_SPEED`).
- **Accessibility**: Respects `prefers-reduced-motion` (renders one static frame). Container has `aria-hidden="true"`.
- **Responsiveness**: Re-measures character width on resize. Hidden below 400px viewport width.

## Key Files

- `_quarto.yml` - Main Quarto configuration
- `listing.yaml` - Auto-generated metadata for all content (do not edit directly)
- `dna-helix.js` - Animated Braille DNA helix (homepage decoration)
- `gallery.ejs` - Custom listing template for posts display
- `fish.xml` - Syntax highlighting definition for Fish shell
- `.pre-commit-config.yaml` - Defines pre-commit hooks for notebook formatting

## Working with Pixi Projects

Many TIL entries use pixi for dependency management:
```bash
cd til/some-til-entry/
pixi install          # Install dependencies
pixi shell            # Enter pixi environment
jupyter lab           # Run Jupyter in pixi environment
```

## Site Deployment

The site is deployed to GitHub Pages at https://chuckpr.github.io. The rendered `_site/` directory contents are pushed to the deployment branch.
