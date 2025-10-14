# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a template repository for "Cem & Javi" combining LaTeX document generation and Python tooling for academic/scientific papers. The template is structured for German academic documents with modular sections.

## Essential Commands

### Environment Setup
```bash
# Install uv package manager and sync dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Activate virtual environment
source .venv/bin/activate

# Alternative: traditional venv setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### LaTeX Development
```bash
# Build PDF (primary method - VS Code LaTeX Workshop)
# Open tex/main.tex in VS Code and press Ctrl+Alt+B

# Manual build using latexmk
latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory=build tex/main.tex

# Watch for changes and auto-rebuild
latexmk -pdf -pvc -interaction=nonstopmode -output-directory=build tex/main.tex

# Clean build artifacts
latexmk -c -output-directory=build tex/main.tex
```

### Python Development
```bash
# Format code
uv run black src/
# OR: python -m black src/

# Lint with ruff
uv run ruff check src/
# OR: python -m ruff check src/

# Type checking with mypy
uv run mypy src/
# OR: python -m mypy src/
```

### Package Installation
```bash
# LaTeX dependencies (Fedora/RHEL)
sudo dnf install -y texlive-scheme-medium latexmk biber texlive-cleveref

# LaTeX dependencies (macOS)
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install latexmk biber

# LaTeX dependencies (Windows)
# Download and install MiKTeX from https://miktex.org/download
# Enable "install missing packages on-the-fly"
```

## Architecture

### LaTeX Structure
- **tex/main.tex**: Master document with German localization and academic formatting
  - Uses `babel` with `ngerman` for German language support
  - Configured with `biblatex` and `biber` for bibliography management
  - Includes mathematical typesetting with `amsmath`, `siunitx` for units
  - `cleveref` for intelligent cross-referencing
- **tex/sections/**: Modular document sections following German academic structure:
  - `00_zusammenfassung.tex` - Abstract/Summary
  - `01_einführung.tex` - Introduction
  - `02_theorie.tex` - Theory
  - `03_durchführung.tex` - Methodology/Procedure
  - `04_ergebnisse.tex` - Results
  - `05_diskussion.tex` - Discussion
  - `06_schlussfolgerung.tex` - Conclusion
  - `07_anhang.tex` - Appendix
- **tex/references.bib**: Bibliography database
- **build/**: Generated PDF output directory (excluded from git)

### Python Structure
- **src/scripts/**: Directory for utility scripts and tools
  - Currently empty but configured for future Python tooling
- **pyproject.toml**: Modern Python project configuration using hatchling build system
  - Pre-configured with Black (code formatting), Ruff (linting), MyPy (type checking)
  - Target Python 3.10+

### Configuration Files
- **.vscode/settings.json**: VS Code workspace configuration
  - LaTeX Workshop integration with automatic build on save
  - Python development setup with strict type checking
  - File exclusions for build artifacts
- **.env.example**: Template for environment variables (currently empty, ready for project-specific config)

## Development Workflow

### LaTeX Document Development
1. Edit content in `tex/sections/*.tex` files
2. Use VS Code with LaTeX Workshop extension for live preview
3. Build generates PDF in `build/main.pdf`
4. Bibliography managed through `tex/references.bib` using biblatex/biber

### Python Script Development
1. Add new scripts to `src/scripts/`
2. Use strict type hints (MyPy configured for strict mode)
3. Format with Black (88 character line length)
4. Lint with Ruff (E, F, I rules enabled)
5. Entry points can be defined in `pyproject.toml` [project.scripts] section

## Key Features

- **Academic Paper Template**: German-language academic document structure
- **Modern Python Tooling**: uv package manager, hatchling build system
- **VS Code Integration**: Configured for both LaTeX and Python development
- **Modular Design**: Separate sections for easy document organization
- **Quality Tools**: Pre-configured linting, formatting, and type checking