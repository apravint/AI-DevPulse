# ⚡ AI-DevPulse 🛡️🤖
### Autonomous AI Code Reviewer, Security Vulnerability Scanner & Refactoring Agent CLI

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20Inference-black.svg)](https://ollama.com)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-brightgreen.svg)](.github/workflows/devpulse.yml)

**AI-DevPulse** is an open-source autonomous CLI tool and GitHub Action designed to audit codebase quality, detect security vulnerabilities (hardcoded secrets, OWASP flaws, unsanitized commands), and auto-apply clean refactoring fixes across your entire repository.

---

## ✨ Features

- 🔍 **Automated Codebase Audit**: Recursively scans `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.go`, `.rs`, `.sh` files for logic flaws, security vulnerabilities, and code smells.
- ⚡ **Multi-Provider Support**:
  - **Local Ollama** (`qwen2.5:7b`, `deepseek-r1:8b`, `qwen2.5:1.5b`) for 100% offline & free analysis.
  - **Google Gemini API** (`gemini-2.5-flash`).
  - **Heuristic Static Scanner** (zero-dependency default mode).
- 🛠️ **Auto-Fix & Refactoring Engine (`--fix`)**: Automatically rewrites code with safety backups (`.bak`).
- 📊 **Rich Terminal Summary & Markdown Reports**: Renders clean colored terminal tables and exports `DEVPULSE_REPORT.md` for PR integration.
- 🤖 **CI/CD Integration**: Pre-configured GitHub Actions workflow (`.github/workflows/devpulse.yml`).

---

## ⚡ Quickstart & Installation

### 1. Install via Pip
```bash
git clone https://github.com/apravint/AI-DevPulse.git
cd AI-DevPulse
pip install -e .
```

### 2. Run a Local Code Audit
```bash
# Run heuristic scan on current directory
devpulse --path .

# Run Ollama local AI model audit
devpulse --path . --provider ollama --model qwen2.5:1.5b

# Run with auto-fix enabled
devpulse --path . --provider ollama --fix
```

---

## ⚙️ CLI Flag Reference

| Flag | Short | Default | Description |
| :--- | :--- | :--- | :--- |
| `--path` | `-p` | `.` | Target repository or folder to audit |
| `--provider` | | `heuristic` | LLM provider (`heuristic`, `ollama`, `gemini`) |
| `--model` | | `qwen2.5:1.5b` | Target LLM model name |
| `--api-key` | | `""` | API Key for cloud providers |
| `--fix` | | `False` | Apply AI-suggested refactored code fixes directly |
| `--report` | | `DEVPULSE_REPORT.md` | Output path for Markdown report |

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
