"""
Main Command-Line Interface for AI-DevPulse
"""

import sys
import argparse
from rich.console import Console
from devpulse.llm_client import DevPulseLLMClient
from devpulse.auditor import run_codebase_audit
from devpulse.reporter import print_audit_summary, generate_markdown_report
from devpulse.refactor import apply_refactored_fixes

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="⚡ AI-DevPulse: Autonomous AI Code Reviewer, Security Scanner & Refactoring Agent CLI"
    )
    parser.add_argument("--path", "-p", default=".", help="Path to repository or code directory (default: current dir)")
    parser.add_argument("--provider", choices=["ollama", "gemini", "heuristic"], default="heuristic", help="LLM Provider (default: heuristic / static)")
    parser.add_argument("--model", default="qwen2.5:1.5b", help="Model name for Ollama/Gemini (default: qwen2.5:1.5b)")
    parser.add_argument("--api-key", default="", help="API Key for cloud providers")
    parser.add_argument("--fix", action="store_true", help="Automatically apply AI-suggested code fixes with .bak backups")
    parser.add_argument("--report", default="DEVPULSE_REPORT.md", help="Output Markdown report path")

    args = parser.parse_args()

    console.print(f"[bold cyan]⚡ Launching AI-DevPulse Audit on:[/bold cyan] [yellow]{args.path}[/yellow]")
    console.print(f"[dim]Provider: {args.provider} | Model: {args.model}[/dim]\n")

    # Initialize Client
    llm_client = DevPulseLLMClient(
        provider=args.provider,
        api_key=args.api_key,
        model=args.model
    )

    # Run Codebase Audit
    results = run_codebase_audit(args.path, llm_client)

    if not results:
        console.print("[bold yellow]No supported source code files found to audit.[/bold yellow]")
        sys.exit(0)

    # Output Terminal Summary
    print_audit_summary(results)

    # Export Markdown Report
    if args.report:
        generate_markdown_report(results, args.report)

    # Apply fixes if requested
    if args.fix:
        console.print("\n[bold yellow]🛠️ Applying AI Code Fixes...[/bold yellow]")
        fixes_applied = apply_refactored_fixes(results, args.path)
        console.print(f"[bold green]✓ Total files auto-fixed: {fixes_applied}[/bold green]")

if __name__ == "__main__":
    main()
