# FP Template

Template repo for **Cem & Javi** — LaTeX, Python scripting, and AI chat (DeepSeek or ChatGPT via OpenAI SDK).

---

## TLDR — Quick Start

1. Install **uv** and run `uv sync`.
2. Copy `.env.example` → `.env`.
3. Fill **either** DeepSeek **or** OpenAI keys.
4. Activate venv.
5. Test:

   ```bash
   deepseek-chat "Sanity check: 1-2 lines."
   ```

---

## Install Guide

### Linux / macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

### Windows PowerShell

```powershell
irm https://astral.sh/uv/install.ps1 | iex
uv sync
```

---

## Configure your AI

Create `.env` with **either** DeepSeek **or** OpenAI keys.

### Option A — DeepSeek

```
DEEPSEEK_API_KEY=...
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

### Option B — OpenAI (ChatGPT)

```
OPENAI_API_KEY=...
# Optional if using the public API:
# OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

> The CLI uses whichever provider you’ve configured in `.env`.

---

## Installing LaTeX

We use `latexmk` (as configured in VS Code). LaTeX is a **system install**, not a Python package.

## Linux (Debian/Ubuntu)

```sh
sudo apt-get update
sudo apt-get install -y texlive-latex-extra latexmk biber
# Optional: everything (large download)
# sudo apt-get install texlive-full
```

## macOS

**Option A (full):** Install MacTeX (GUI) from tug.org.
**Option B (minimal via Homebrew):**

```sh
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install latexmk biber
```

---

## Windows — Fast MiKTeX Setup

### 1 Download & Install

1. Visit [miktex.org/download](https://miktex.org/download).
2. Download **`basic-miktex-x64.exe`**.
3. Run the installer with these settings:

   * **Install for:** *Only for me* (faster, no admin rights needed)
   * **Preferred paper size:** *A4* (or *Letter*)
   * **Install missing packages on-the-fly:** ✅ *Yes*
   * **Update MiKTeX automatically:** optional, leave enabled if you want

### Minimal Setup Tips

**Do not install** the following extras — they slow down installation and aren’t needed for VS Code builds:

| ❌ Skip                                              |
| --------------------------------------------------- |
| **Complete / Full installation**                    |
| **MiKTeX Console (Admin)**                          |
| **Ghostscript, Perl, GSView, SumatraPDF, Texworks** |
| **Extra fonts / documentation packages**            |
| **Non-Latin language collections**                  |

### Verify Installation

After installation, open **PowerShell** and check:

```powershell
latexmk -v
pdflatex --version
```

If either command isn’t found, restart your terminal or VS Code and ensure MiKTeX’s `bin` directory is in your system **PATH**.

---

## Structure

```
src/
 ├─ ai/                  # API clients
 └─ scripts/deepseek_chat.py  # CLI entrypoint
tex/
 └─ main.tex
.vscode/
Makefile
pyproject.toml
```

---

## Usage

Activate the virtual environment, then run the chat CLI.

### Linux / macOS

```bash
source .venv/bin/activate
deepseek-chat "Hello from the lab"
```

### Windows PowerShell

```powershell
. .\.venv\Scripts\Activate.ps1
deepseek-chat "Hello from the lab"
```

**Model override (optional):**

```bash
MODEL=gpt-4o-mini deepseek-chat "Summarize today's experiment."
# or (PowerShell)
$env:MODEL="gpt-4o-mini"; deepseek-chat "Summarize today's experiment."
```

---

## Common Commands

| Purpose       | Linux / macOS               | Windows PowerShell           |
| ------------- | --------------------------- | ---------------------------- |
| Activate venv | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| Run chat CLI  | `deepseek-chat "msg"`       | `deepseek-chat "msg"`        |
| Format code   | `make fmt`                  | `make fmt`                   |
| Lint code     | `make lint`                 | `make lint`                  |
| Type check    | `make type`                 | `make type`                  |
| Build PDF     | `make pdf`                  | `make pdf`                   |
| Watch LaTeX   | `make watch`                | `make watch`                 |
| Clean build   | `make clean`                | `make clean`                 |
