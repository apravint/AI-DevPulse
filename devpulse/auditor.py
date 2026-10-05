"""
Codebase Directory Scanner & Security Auditor for AI-DevPulse
"""

import os
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".go", ".rs", ".sh"
}

IGNORE_DIRS = {
    ".git", ".github", "__pycache__", "node_modules", "venv", ".venv", "dist", "build", "target", ".idea", ".vscode"
}

def scan_repository(repo_path="."):
    """Recursively scans repository directory for source code files."""
    repo_path = Path(repo_path).resolve()
    code_files = []

    for root, dirs, files in os.walk(repo_path):
        # Filter out ignored directories in place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(repo_path)
                code_files.append((str(rel_path), full_path))

    return code_files

def run_codebase_audit(repo_path=".", llm_client=None):
    """Audits entire repository codebase and produces structured report data."""
    code_files = scan_repository(repo_path)
    audit_results = []

    for rel_path, full_path in code_files:
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if not content.strip() or len(content) > 100000:
                continue

            result = llm_client.analyze_code(rel_path, content) if llm_client else {}
            result["file"] = rel_path
            result["path"] = str(full_path)
            audit_results.append(result)
        except Exception as e:
            audit_results.append({
                "file": rel_path,
                "score": 0.0,
                "issues": [f"File read error: {str(e)}"],
                "refactored_code": None
            })

    return audit_results
