# FP Template

Template for **Cem & Javi**: LaTeX docs and Python tooling for academic papers in German academic contexts.

---

## Table of Contents

- [FP Template](#fp-template)
  - [Table of Contents](#table-of-contents)
  - [Quick Start](#quick-start)
    - [Initial Setup](#initial-setup)
    - [Daily Workflow](#daily-workflow)
    - [For New Users](#for-new-users)
  - [Project Overview](#project-overview)
  - [Installation --- Setup Instructions](#installation-----setup-instructions)
    - [Prerequisites](#prerequisites)
    - [Environment Setup](#environment-setup)
      - [Option 1: Using uv (Recommended - Fastest)](#option-1-using-uv-recommended---fastest)
      - [Option 2: Traditional Python venv](#option-2-traditional-python-venv)
    - [LaTeX Installation](#latex-installation)
      - [Fedora Linux](#fedora-linux)
      - [macOS](#macos)
      - [Windows](#windows)
  - [Workflows](#workflows)
    - [LaTeX Document Development](#latex-document-development)
      - [Building PDF Documents](#building-pdf-documents)
      - [Document Structure](#document-structure)
    - [Python Data Analysis](#python-data-analysis)
      - [Using the CLI (Recommended)](#using-the-cli-recommended)
      - [Available Analysis Tools](#available-analysis-tools)
  - [Repository Structure](#repository-structure)
  - [Common Commands Reference](#common-commands-reference)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
      - [Python Environment](#python-environment)
      - [LaTeX Build](#latex-build)
      - [Windows Specific](#windows-specific)
    - [Getting Help](#getting-help)
  - [For New Team Members](#for-new-team-members)

---

## Quick Start

### Initial Setup

**Installation Checklist:**
- [ ] Install uv package manager
- [ ] Run `uv sync` to create virtual environment
- [ ] Install LaTeX distribution for your OS
- [ ] Verify Python setup: `academic-analysis --help`
- [ ] Test LaTeX build: `latexmk -pdf tex/main.tex`

### Daily Workflow

**Every time you work on the project:**

```bash
# Activate environment
source .venv/bin/activate  # Linux/macOS
# OR: .\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Work with LaTeX (VS Code recommended)
# Open tex/main.tex → Ctrl+Alt+B to build PDF

# Use Python tools
academic-analysis demo-workflow  # Run example analysis
academic-analysis --help         # See all commands

# Verify everything works
academic-analysis --help && latexmk -pdf tex/main.tex

# Deactivate when done
deactivate
```

### For New Users
Start with the [Setup Instructions](#setup-instructions) below for detailed, step-by-step guidance.

---

## Project Overview

This template combines **LaTeX document generation** with **Python data analysis tools** specifically designed for German academic papers. It provides:

- **Structured LaTeX documents** following German academic conventions
- **Python CLI tools** for statistical analysis and visualization
- **Modern development workflow** with uv package management
- **VS Code integration** for both LaTeX and Python development

---

## Installation --- Setup Instructions

### Prerequisites

- **Python 3.10+** ([python.org](https://python.org))
- **Git** for version control
- **VS Code** with LaTeX Workshop extension (recommended)

### Environment Setup

#### Option 1: Using uv (Recommended - Fastest)

**Linux/macOS:**
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create environment and install dependencies
uv sync

# Activate environment
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
# Install uv
irm https://astral.sh/uv/install.ps1 | iex

# Create environment
uv sync

# Activate
.\.venv\Scripts\Activate.ps1
```

#### Option 2: Traditional Python venv

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Windows:**
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
# OR: .venv\Scripts\activate.bat  # Command Prompt
# OR: source .venv/Scripts/activate  # Git Bash
pip install -e .
```

### LaTeX Installation

#### Fedora Linux
```bash
sudo dnf install -y texlive-scheme-medium latexmk biber texlive-cleveref
```

#### macOS
```bash
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install latexmk biber
```

#### Windows
1. Download and install **MiKTeX** from [miktex.org/download](https://miktex.org/download)
2. Enable "Install missing packages on-the-fly" during installation
3. Verify installation:
   ```powershell
   latexmk -v
   pdflatex --version
   ```

---

## Workflows

### LaTeX Document Development

#### Building PDF Documents

**Primary Method (VS Code):**
1. Open [`tex/main.tex`](tex/main.tex:1) in VS Code
2. Press **Ctrl + Alt + B** (or **Cmd + Alt + B** on macOS)
3. Generated PDF appears in `build/main.pdf`

**Manual Build:**
```bash
latexmk -pdf tex/main.tex
```

#### Document Structure
- **Main Document**: [`tex/main.tex`](tex/main.tex:1)
- **Sections**: `tex/sections/00-07_*.tex` (German academic structure)
- **Bibliography**: [`tex/references.bib`](tex/references.bib:1)

### Python Data Analysis

#### Using the CLI (Recommended)

The [`academic-analysis`](src/scripts/main.py:23) CLI provides comprehensive data analysis workflows:

```bash
# Show available commands
academic-analysis --help

# Run complete demonstration
academic-analysis demo-workflow

# Generate and analyze sample data
academic-analysis generate-sample-data --size 100
academic-analysis analyze-column sample_data.csv --column measurement_1

# Create publication-quality plots
academic-analysis create-plot data.csv --x-col group --y-col measurement_1 --plot-type box
```

#### Available Analysis Tools

- **Data Loading**: [`data_loader.py`](src/scripts/data_loader.py:1) - CSV, Excel, JSON support
- **Statistical Analysis**: [`statistical_analysis.py`](src/scripts/statistical_analysis.py:1) - t-tests, ANOVA, correlations
- **Plot Generation**: [`plot_generator.py`](src/scripts/plot_generator.py:1) - Publication-quality visualizations

---

## Repository Structure

```
├── src/scripts/              # Python data analysis tools
│   ├── main.py               # CLI interface (academic-analysis)
│   ├── data_loader.py        # Data loading and validation
│   ├── statistical_analysis.py # Statistical tests
│   └── plot_generator.py     # Plot generation
├── tex/                      # LaTeX document structure
│   ├── main.tex              # Main document (German academic format)
│   ├── references.bib        # Bibliography database
│   └── sections/             # Modular document sections
│       ├── 00_zusammenfassung.tex    # Abstract/Summary
│       ├── 01_einführung.tex         # Introduction
│       ├── 02_theorie.tex            # Theory
│       ├── 03_durchführung.tex       # Methodology
│       ├── 04_ergebnisse.tex         # Results
│       ├── 05_diskussion.tex         # Discussion
│       ├── 06_schlussfolgerung.tex   # Conclusion
│       └── 07_anhang.tex             # Appendix
├── build/                    # Generated PDFs (git ignored)
├── .vscode/                  # VS Code configuration
├── pyproject.toml            # Python project configuration
└── README.md
```

---

## Common Commands Reference

| Task | Command |
|------|---------|
| **Environment** | |
| Activate venv (Linux/macOS) | `source .venv/bin/activate` |
| Activate venv (Windows) | `.\.venv\Scripts\Activate.ps1` |
| Sync dependencies (uv) | `uv sync` |
| **Python Development** | |
| Format code | `python -m black src/` |
| Lint code | `python -m ruff check src/` |
| Type checking | `python -m mypy src/` |
| **LaTeX Development** | |
| Build PDF (VS Code) | `Ctrl+Alt+B` |
| Manual build | `latexmk -pdf tex/main.tex` |
| Clean builds | `latexmk -c` |
| **Data Analysis** | |
| Show CLI help | `academic-analysis --help` |
| Demo workflow | `academic-analysis demo-workflow` |
| Generate sample data | `academic-analysis generate-sample-data --size 100` |

---

## Troubleshooting

### Common Issues

#### Python Environment
- **"Command not found"**: Ensure virtual environment is activated (prompt shows `(.venv)`)
- **"uv not found"**: Install uv using the instructions in [Environment Setup](#environment-setup)
- **Import errors**: Run `uv sync` or `pip install -e .` to install dependencies

#### LaTeX Build
- **"latexmk not found"**: Install LaTeX using [LaTeX Installation](#latex-installation) instructions
- **Missing packages**: MiKTeX should install missing packages automatically on Windows
- **Build failures**: Check `build/main.log` for detailed error messages

#### Windows Specific
- **PowerShell execution policy**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Python not in PATH**: Reinstall Python and check "Add to PATH" option
- **LaTeX issues**: Try Git Bash terminal if PowerShell/Command Prompt fail

### Getting Help

1. Check the build log: `build/main.log`
2. Verify environment activation: `which python` (Linux/macOS) or `Get-Command python` (Windows)
3. Ensure all prerequisites are installed
4. Consult the [WARP.md](WARP.md:1) file for additional guidance

---

## For New Team Members

If you're the third student joining this project:

1. **Start with Setup Instructions**: Follow the [Setup Instructions](#setup-instructions) step by step
2. **Verify Installation**: Run `academic-analysis --help` to confirm Python setup
3. **Test LaTeX**: Build the PDF using VS Code (Ctrl+Alt+B)
4. **Explore Examples**: Use `academic-analysis demo-workflow` to see the tools in action
5. **Ask Questions**: Don't hesitate to ask Cem or Javi for help with the workflow

The project is designed to be collaborative - all tools and document structure are standardized for easy team integration.
