"""
Auto-Fix & Code Refactoring Engine for AI-DevPulse
"""

import os
from rich.console import Console

console = Console()

def apply_refactored_fixes(audit_results, repo_path="."):
    """Applies LLM-suggested code fixes to files if available."""
    fixed_count = 0

    for res in audit_results:
        refactored = res.get("refactored_code")
        file_path = res.get("path")

        if refactored and file_path and os.path.exists(file_path):
            try:
                # Backup original file
                backup_path = f"{file_path}.bak"
                with open(file_path, "r", encoding="utf-8", errors="ignore") as orig:
                    orig_content = orig.read()
                with open(backup_path, "w", encoding="utf-8") as bak:
                    bak.write(orig_content)

                # Write refactored content
                with open(file_path, "w", encoding="utf-8") as out:
                    out.write(refactored)

                fixed_count += 1
                console.print(f"[bold green]✓ Refactored & fixed:[/bold green] {res.get('file')} (Backup: {backup_path})")
            except Exception as e:
                console.print(f"[bold red]❌ Failed to apply fix for {res.get('file')}: {e}[/bold red]")

    return fixed_count
