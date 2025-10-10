# FP Template

Template for **Cem & Javi**: LaTeX docs and Python tooling for academic papers.

---

## Create and Activate a Virtual Environment

You must work inside a local virtual environment (`.venv`). Do **not** use system Python.

### Fedora / Linux

```bash
# Create venv in project root
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Verify you're inside the venv
which python
# → .../yourproject/.venv/bin/python
```

### Windows Setup Guide

**Choose your terminal** (pick ONE of these options):

#### Option A: PowerShell (Recommended)

1. **Open PowerShell as Administrator** (Right-click → "Run as administrator")
2. **Enable script execution** (run once):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. **Close admin PowerShell, open regular PowerShell in project folder**
4. **Create and activate virtual environment**:
   ```powershell
   # Create venv
   python -m venv .venv
   
   # Activate it
   .\.venv\Scripts\Activate.ps1
   
   # Verify (should show (.venv) in prompt)
   python --version
   ```

#### Option B: Command Prompt (cmd) - If PowerShell fails

```cmd
REM Create venv
python -m venv .venv

REM Activate it
.venv\Scripts\activate.bat

REM Verify (should show (.venv) in prompt)
python --version
```

#### Option C: Git Bash - If you have Git for Windows

```bash
# Create venv
python -m venv .venv

# Activate it
source .venv/Scripts/activate

# Verify
which python
```

**Troubleshooting Windows Issues:**
- ❌ **"python not found"**: Install Python from [python.org](https://python.org), check "Add to PATH"
- ❌ **"Execution policy error"**: Use Option A step 2, or try Option B (cmd) instead
- ❌ **Still having issues**: Use Option C (Git Bash) which works like Linux

> After activation the prompt starts with `(.venv)`. Run `deactivate` to exit.

---

## TL;DR

### Linux / macOS

```bash
# 1) Install uv + deps and create venv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# 2) Install LaTeX dependencies (Fedora example)
sudo dnf install -y texlive-scheme-medium latexmk biber texlive-cleveref

# 3) Activate environment
source .venv/bin/activate

# 4) Ready to work!
# Add your Python scripts to src/scripts/
# Edit LaTeX content in tex/sections/
```

### Windows (Quick Start)

**Prerequisites**: Install Python from [python.org](https://python.org) (check "Add to PATH")

#### Method 1: Using uv (Fast - PowerShell)
```powershell
# 1) Install uv package manager
irm https://astral.sh/uv/install.ps1 | iex

# 2) Create environment and install dependencies
uv sync

# 3) Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

#### Method 2: Traditional Python (If uv fails - any terminal)
```bash
# Works in PowerShell, cmd, or Git Bash
python -m venv .venv

# Activate (choose your terminal):
.\.venv\Scripts\Activate.ps1    # PowerShell
# .venv\Scripts\activate.bat     # Command Prompt
# source .venv/Scripts/activate  # Git Bash

# Install dependencies
python -m pip install -e .
```

#### LaTeX Setup for Windows
1. **Download MiKTeX**: [https://miktex.org/download](https://miktex.org/download)
2. **Install with default settings**
3. **✅ Enable**: "Install missing packages on-the-fly"
4. **Test installation**:
   ```
   latexmk -v
   pdflatex --version
   ```

---

## Build the PDF

1. Open `tex/main.tex` in VS Code.
2. Press **Ctrl + Alt + B** (or **Cmd + Alt + B** on macOS) to build the project.
3. The compiled PDF will appear in `build/main.pdf`.

---

## LaTeX Installation

* **Fedora Linux:**

  ```bash
  sudo dnf install -y texlive-scheme-medium latexmk biber
  ```
* **macOS:**

  ```bash
  brew install --cask basictex
  sudo tlmgr update --self
  sudo tlmgr install latexmk biber
  ```
* **Windows:**

  1. Install from [https://miktex.org/download](https://miktex.org/download)
  2. Enable “install missing packages on-the-fly”.
  3. Verify:

     ```powershell
     latexmk -v
     pdflatex --version
     ```


---

## Common Development Commands

| Task          | Linux / macOS               | Windows                          |
| ------------- | --------------------------- | -------------------------------- |
| Activate venv | `source .venv/bin/activate` | `. .\.venv\Scripts\Activate.ps1` |
| Format Python | `python -m black src/`      | `python -m black src/`           |
| Lint Python   | `python -m ruff check src/` | `python -m ruff check src/`      |
| Type check    | `python -m mypy src/`       | `python -m mypy src/`            |
| Build PDF     | `Ctrl+Alt+B` (VS Code)      | `Ctrl+Alt+B` (VS Code)           |
| Manual PDF    | `latexmk -pdf tex/main.tex` | `latexmk -pdf tex/main.tex`      |
| Clean builds  | `latexmk -c`                | `latexmk -c`                     |

---

## Repository Structure

```
src/
  scripts/                  # Your Python data analysis scripts
tex/
  sections/                 # LaTeX document sections (00-07)
  main.tex                  # Main LaTeX document
  references.bib            # Bibliography database
build/                      # Generated PDFs (git ignored)
.vscode/                    # VS Code configuration
.venv/                      # Python virtual environment
pyproject.toml              # Python project configuration
README.md
WARP.md                     # AI assistant guidance
```

---
