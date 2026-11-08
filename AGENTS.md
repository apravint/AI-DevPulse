# AGENTS.md - Developer & AI Agent Guide for AI-DevPulse 🤖

## 🎯 Repository Overview
**AI-DevPulse**: AI-DevPulse is an open-source autonomous CLI tool and GitHub Action designed to audit codebase quality, detect security vulnerabilities (hardcoded secrets, OWASP flaws, unsanitized commands), and auto-apply clean refactoring fixes across your entire repository. - 🔍 Automated Codebase Audit: Recursively scans .py, .js, .ts, .java, .cpp, .go, .rs, .sh files for logic flaws, security vulnerabilities, and code smells.

---

## 🏗️ Repository Architecture
Key directories and entrypoints: `.github/, DEVPULSE_REPORT.md, LICENSE, README.md, devpulse/, requirements.txt, setup.py`.

### Tech Stack & Runtime
- **Language:** Python 3.10+ (Type-annotated, modern packaging)
- **Packaging & Tooling:** `pyproject.toml` / `setup.py` / `pip install -e .`

## ⚙️ Executable Verification Commands

Before declaring any coding or refactoring task complete, run verification:

### 1. Fast Syntax & Bytecode Compilation
```bash
python3 -m py_compile $(find . -maxdepth 3 -name '*.py' -not -path '*/.*' -not -path '*/venv/*')
```

### 2. Static Analysis & Linting
```bash
ruff check . || flake8 . || python3 -m py_compile **/*.py
```

### 3. Test Suite Execution
```bash
python3 -m unittest discover -s tests
```

---

## 🛡️ Coding & Safety Guidelines for Autonomous Agents

1. **Documentation Integrity:** Preserve all existing docstrings, header comments, and licensing banners. Never delete context unless specifically instructed.
2. **Zero Hardcoded Secrets:** Never embed API keys, OAuth tokens, personal access tokens, or sensitive credentials in committed files. Read credentials exclusively from environment variables or secure credential paths.
3. **Git Hygiene:**
   - Do not force-push (`git push --force`) or execute destructive resets.
   - Never modify root git configurations or harness infrastructure outside task scope.
   - Keep git diffs atomic, focused, and verified before committing.
4. **Agent Workflow Protocol:**
   - **Plan:** Inspect codebase architecture and dependencies before editing.
   - **Act:** Make minimal, clean, high-precision changes.
   - **Verify:** Run the appropriate verification commands listed above.
   - **Reflect:** Confirm zero regressions and review `git diff`.

---
*Maintained by Ayyappa Pravin • Built for Antigravity, Claude, Cursor & Autonomous AI Agents.*
