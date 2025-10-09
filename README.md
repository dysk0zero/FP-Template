# FP Template

Template for **Cem & Javi**: LaTeX docs, Python tooling, and an AI chat CLI (DeepSeek or ChatGPT via OpenAI).

---

## TL;DR

### Linux / macOS

```bash
# 1) Install uv + deps and create venv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# 2) Install LaTeX dependencies (Fedora example)
sudo dnf install -y texlive-scheme-medium latexmk biber texlive-cleveref

# 3) Configure secrets
cp .env.example .env   # fill with either DeepSeek or OpenAI keys

# 4) Activate & test CLI
source .venv/bin/activate
deepseek-chat "Sanity check"
```

### Windows

```powershell
# 1) Install uv + deps and create venv
irm https://astral.sh/uv/install.ps1 | iex
uv sync

# 2) Install LaTeX dependencies (MiKTeX recommended)
# Download from https://miktex.org/download and allow it to install missing packages automatically.

# 3) Configure secrets
Copy-Item .env.example .env   # fill with either DeepSeek or OpenAI keys

# 4) Activate & test CLI
. .\.venv\Scripts\Activate.ps1
deepseek-chat "Sanity check"
```

---

## Build the PDF

### Option A — VS Code
1. Open `tex/main.tex` in VS Code.  
2. Press **Ctrl + Alt + B** (or **Cmd + Alt + B** on macOS) to build the project.  
3. The compiled PDF will appear in `build/main.pdf`.

### Option B — Terminal
You can also use the provided Makefile:

**Linux / macOS**
```bash
make pdf      # build once
make watch    # auto-rebuild on save
make clean    # remove build artifacts
```

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

## Configure AI API

Create `.env` with **either** DeepSeek **or** OpenAI settings.

**DeepSeek**

```
DEEPSEEK_API_KEY=...
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

**OpenAI (ChatGPT)**

```
OPENAI_API_KEY=...
# Optional override:
# OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

> The CLI uses whichever provider is configured in `.env`.
> Temporary override:
> Linux/macOS: `MODEL=gpt-4o-mini deepseek-chat "…”`
> Windows: `$env:MODEL="gpt-4o-mini"; deepseek-chat "…"`

---

## Common Commands

| Task          | Linux / macOS               | Windows PowerShell               |
| ------------- | --------------------------- | -------------------------------- |
| Activate venv | `source .venv/bin/activate` | `. .\.venv\Scripts\Activate.ps1` |
| Chat CLI      | `deepseek-chat "message"`   | `deepseek-chat "message"`        |
| Format        | `make fmt`                  | `make fmt`                       |
| Lint          | `make lint`                 | `make lint`                      |
| Type check    | `make type`                 | `make type`                      |
| Build PDF     | `make pdf`                  | `make pdf`                       |
| Watch LaTeX   | `make watch`                | `make watch`                     |
| Clean         | `make clean`                | `make clean`                     |

> `make` must be available on Windows (e.g., Git for Windows, MSYS2). Otherwise use the direct `latexmk`/tooling commands above.

---

## Repo Structure

```
data/
src/
  ai/                       # Provider clients
  scripts/                  # Your python scripts
  scripts/deepseek_chat.py  # CLI entrypoint
tex/
  sections/                 
  main.tex
  references.bib
.vscode/
Makefile
pyproject.toml
README.md
```

---