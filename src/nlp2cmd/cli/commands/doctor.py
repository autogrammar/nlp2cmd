"""
NLP2CMD Doctor - System diagnostic and repair tool.

Checks and fixes common issues before running nlp2cmd:
- Ollama availability and required models
- HuggingFace token configuration
- Python dependencies
- Playwright/browser setup
- Environment variables
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    Console = None

from nlp2cmd.cli.commands.doctor_browser import get_hf_token_via_browser
from nlp2cmd.cli.commands.doctor_types import CheckResult, Status

__all__ = [
    "CheckResult",
    "NP2CMDDoctor",
    "Status",
    "doctor_command",
    "get_hf_token_via_browser",
    "run_doctor",
]


class NP2CMDDoctor:
    """System diagnostic and auto-repair for nlp2cmd."""

    def __init__(self, console: Optional[Console] = None, auto_fix: bool = False):
        self.console = console
        self.auto_fix = auto_fix
        self.results: list[CheckResult] = []
        self.ollama_host = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.required_models = ["qwen2.5:3b", "llama3.2", "mistral"]

    def _print(self, message: str, style: str = ""):
        """Print with or without rich."""
        if self.console and HAS_RICH:
            self.console.print(message, style=style)
        else:
            print(message)

    def _check_port(self, host: str, port: int, timeout: float = 2.0) -> bool:
        """Check if a port is open."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host.replace("http://", "").replace("https://", ""), port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def check_ollama_server(self) -> CheckResult:
        """Check if Ollama server is running."""
        host = self.ollama_host.replace("http://", "").replace("https://", "").split(":")[0]
        port = 11434

        if not self._check_port(host, port):
            # Try to auto-start Ollama
            if self.auto_fix:
                try:
                    # Check if ollama binary exists
                    result = subprocess.run(
                        ["which", "ollama"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        self._print("   Starting Ollama server...", "yellow")
                        # Start ollama in background
                        subprocess.Popen(
                            ["ollama", "serve"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            start_new_session=True
                        )
                        time.sleep(3)  # Wait for startup

                        # Check again
                        if self._check_port(host, port):
                            return CheckResult(
                                name="Ollama Server",
                                status=Status.FIXED,
                                message="Ollama server was not running - started automatically",
                                fix_applied=True
                            )
                except Exception as e:
                    pass

            return CheckResult(
                name="Ollama Server",
                status=Status.ERROR,
                message=f"Ollama server not running on {self.ollama_host}",
                details={"host": host, "port": port},
                fix_command="ollama serve"
            )

        return CheckResult(
            name="Ollama Server",
            status=Status.OK,
            message=f"Ollama server running on {self.ollama_host}"
        )

    def check_ollama_models(self) -> CheckResult:
        """Check if required Ollama models are available."""
        if not HAS_REQUESTS:
            return CheckResult(
                name="Ollama Models",
                status=Status.WARNING,
                message="Cannot check models - requests library not available"
            )

        try:
            resp = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            if resp.status_code != 200:
                return CheckResult(
                    name="Ollama Models",
                    status=Status.ERROR,
                    message=f"Cannot list models: HTTP {resp.status_code}"
                )

            data = resp.json()
            available_models = [m.get("name", "") for m in data.get("models", [])]

            # Check for configured model first
            configured_model = os.getenv("NLP2CMD_PLANNER_MODEL", "qwen2.5:3b")

            if configured_model in available_models:
                return CheckResult(
                    name="Ollama Models",
                    status=Status.OK,
                    message=f"Required model '{configured_model}' is available",
                    details={"available": available_models, "required": configured_model}
                )

            # Check for any fallback model
            for model in self.required_models:
                if model in available_models:
                    return CheckResult(
                        name="Ollama Models",
                        status=Status.WARNING,
                        message=f"Preferred model '{configured_model}' not found, but '{model}' is available",
                        details={"available": available_models, "preferred": configured_model, "using": model}
                    )

            # No suitable model found - try to pull
            if self.auto_fix:
                model_to_pull = configured_model if ":" in configured_model else "qwen2.5:3b"
                self._print(f"   Pulling model {model_to_pull}...", "yellow")
                try:
                    result = subprocess.run(
                        ["ollama", "pull", model_to_pull],
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    if result.returncode == 0:
                        return CheckResult(
                            name="Ollama Models",
                            status=Status.FIXED,
                            message=f"Model '{model_to_pull}' pulled successfully",
                            fix_applied=True
                        )
                except Exception as e:
                    pass

            return CheckResult(
                name="Ollama Models",
                status=Status.ERROR,
                message=f"No suitable model found. Required: {configured_model}",
                details={"available": available_models, "required": configured_model},
                fix_command=f"ollama pull {configured_model}"
            )

        except requests.exceptions.ConnectionError:
            return CheckResult(
                name="Ollama Models",
                status=Status.ERROR,
                message="Cannot connect to Ollama server"
            )
        except Exception as e:
            return CheckResult(
                name="Ollama Models",
                status=Status.ERROR,
                message=f"Error checking models: {e}"
            )

    def check_hf_token(self) -> CheckResult:
        """Check HuggingFace token configuration."""
        token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")

        if token:
            # Mask token for display
            masked = token[:4] + "..." + token[-4:] if len(token) > 8 else "***"
            return CheckResult(
                name="HF Token",
                status=Status.OK,
                message=f"HF_TOKEN configured ({masked})",
                details={"token_length": len(token)}
            )

        # Check if huggingface-cli is configured
        hf_home = Path.home() / ".huggingface"
        token_file = hf_home / "token"

        if token_file.exists():
            return CheckResult(
                name="HF Token",
                status=Status.WARNING,
                message="Token found in ~/.huggingface/token but HF_TOKEN not set",
                details={"token_file": str(token_file)},
                fix_command="export HF_TOKEN=$(cat ~/.huggingface/token)"
            )

        return CheckResult(
            name="HF Token",
            status=Status.WARNING,
            message="HF_TOKEN not set - unauthenticated requests may be rate limited",
            details={"hint": "Get token from https://huggingface.co/settings/tokens"},
            fix_command="export HF_TOKEN=your_token_here"
        )

    def check_playwright(self) -> CheckResult:
        """Check Playwright browser installation."""
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browsers = []
                for browser_type in [p.chromium, p.firefox, p.webkit]:
                    try:
                        browser_type.executable_path
                        browsers.append(browser_type.name)
                    except Exception:
                        pass

                if browsers:
                    return CheckResult(
                        name="Playwright",
                        status=Status.OK,
                        message=f"Playwright ready with {', '.join(browsers)}",
                        details={"browsers": browsers}
                    )
                else:
                    return CheckResult(
                        name="Playwright",
                        status=Status.ERROR,
                        message="No browsers installed",
                        fix_command="playwright install chromium"
                    )
        except ImportError:
            return CheckResult(
                name="Playwright",
                status=Status.WARNING,
                message="Playwright not installed - web automation will use fallback",
                fix_command="pip install playwright && playwright install chromium"
            )
        except Exception as e:
            if "sync api inside the asyncio loop" in str(e).lower():
                return CheckResult(
                    name="Playwright",
                    status=Status.WARNING,
                    message="Playwright check skipped in active asyncio loop (runtime may still be OK)",
                    details={"error": str(e)},
                    fix_command="Run `nlp2cmd doctor` from a regular shell (outside async loop) for full check",
                )
            return CheckResult(
                name="Playwright",
                status=Status.ERROR,
                message=f"Playwright error: {e}",
                fix_command="playwright install"
            )

    def check_visual_stream_tools(self) -> CheckResult:
        """Check prerequisites for visual stream recording (vnc/novnc/xvfb)."""
        vnc_server = shutil.which("vncserver")
        novnc_proxy = shutil.which("novnc_proxy")
        xvfb_run = shutil.which("xvfb-run")

        details = {
            "vncserver": bool(vnc_server),
            "novnc_proxy": bool(novnc_proxy),
            "xvfb_run": bool(xvfb_run),
        }

        if vnc_server and novnc_proxy:
            return CheckResult(
                name="Visual Streams",
                status=Status.OK,
                message="VNC/noVNC tooling detected",
                details=details,
            )

        if xvfb_run:
            return CheckResult(
                name="Visual Streams",
                status=Status.WARNING,
                message="VNC/noVNC not fully configured (xvfb-run available as fallback)",
                details=details,
                fix_command="Install VNC + noVNC for --source vnc/novnc video recording",
            )

        return CheckResult(
            name="Visual Streams",
            status=Status.WARNING,
            message="No visual stream backend detected (vnc/novnc/xvfb)",
            details=details,
            fix_command="Install at least one backend (recommended: VNC + noVNC, or xvfb-run)",
        )

    def check_environment(self) -> CheckResult:
        """Check environment configuration."""
        issues = []
        details = {}

        # Check Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        details["python_version"] = python_version

        if sys.version_info < (3, 9):
            issues.append(f"Python {python_version} is old (recommend 3.9+)")

        # Check .env file
        env_file = Path(".env")
        if env_file.exists():
            details["env_file"] = str(env_file)
        else:
            details["env_file"] = None

        # Check for common env vars
        env_vars = {
            "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "default: http://localhost:11434"),
            "NLP2CMD_PLANNER_MODEL": os.getenv("NLP2CMD_PLANNER_MODEL", "default: qwen2.5:3b"),
            "CANVAS_LLM_TIMEOUT": os.getenv("CANVAS_LLM_TIMEOUT", "default: 60"),
        }
        details["env_vars"] = env_vars

        if issues:
            return CheckResult(
                name="Environment",
                status=Status.WARNING,
                message="; ".join(issues),
                details=details
            )

        return CheckResult(
            name="Environment",
            status=Status.OK,
            message=f"Python {python_version}, configuration OK",
            details=details
        )

    def check_dependencies(self) -> CheckResult:
        """Check critical Python dependencies."""
        critical_deps = [
            "requests",
            "transformers",
            "torch",
            "sentence_transformers",
            "click",
            "rich",
        ]

        missing = []
        installed = []

        for dep in critical_deps:
            try:
                __import__(dep)
                installed.append(dep)
            except ImportError:
                missing.append(dep)

        if missing:
            return CheckResult(
                name="Dependencies",
                status=Status.ERROR,
                message=f"Missing: {', '.join(missing)}",
                details={"installed": installed, "missing": missing},
                fix_command=f"pip install {' '.join(missing)}"
            )

        return CheckResult(
            name="Dependencies",
            status=Status.OK,
            message=f"All critical dependencies installed ({len(installed)} packages)"
        )

    def run_all_checks(self) -> list[CheckResult]:
        """Run all diagnostic checks."""
        checks = [
            self.check_ollama_server,
            self.check_ollama_models,
            self.check_hf_token,
            self.check_playwright,
            self.check_visual_stream_tools,
            self.check_environment,
            self.check_dependencies,
        ]

        self._print("\n[bold cyan]🔍 NLP2CMD System Doctor[/bold cyan]\n" if HAS_RICH else "\n🔍 NLP2CMD System Doctor\n")

        for check_func in checks:
            result = check_func()
            self.results.append(result)
            self._display_result(result)

        return self.results

    def _display_result(self, result: CheckResult):
        """Display a check result."""
        if HAS_RICH and self.console:
            icons = {
                Status.OK: "[green]✓[/green]",
                Status.WARNING: "[yellow]⚠[/yellow]",
                Status.ERROR: "[red]✗[/red]",
                Status.INFO: "[blue]ℹ[/blue]",
                Status.FIXED: "[green]🔧[/green]",
            }
            icon = icons.get(result.status, "?")
            self.console.print(f"{icon} [bold]{result.name}:[/bold] {result.message}")

            if result.fix_command and not result.fix_applied:
                self.console.print(f"   [dim]Fix: {result.fix_command}[/dim]")
        else:
            icons = {
                Status.OK: "✓",
                Status.WARNING: "⚠",
                Status.ERROR: "✗",
                Status.INFO: "ℹ",
                Status.FIXED: "🔧",
            }
            icon = icons.get(result.status, "?")
            print(f"{icon} {result.name}: {result.message}")
            if result.fix_command and not result.fix_applied:
                print(f"   Fix: {result.fix_command}")

    def print_summary(self):
        """Print summary of all checks."""
        ok = sum(1 for r in self.results if r.status == Status.OK)
        fixed = sum(1 for r in self.results if r.status == Status.FIXED)
        warnings = sum(1 for r in self.results if r.status == Status.WARNING)
        errors = sum(1 for r in self.results if r.status == Status.ERROR)

        if HAS_RICH and self.console:
            table = Table(title="Summary")
            table.add_column("Status", justify="center")
            table.add_column("Count", justify="right")
            table.add_row("[green]OK[/green]", str(ok))
            if fixed:
                table.add_row("[green]Fixed[/green]", str(fixed))
            if warnings:
                table.add_row("[yellow]Warnings[/yellow]", str(warnings))
            if errors:
                table.add_row("[red]Errors[/red]", str(errors))

            self.console.print("\n")
            self.console.print(table)

            if errors > 0:
                self.console.print("\n[red bold]❌ System has errors - fix before running nlp2cmd[/red bold]")
            elif warnings > 0:
                self.console.print("\n[yellow bold]⚠ System has warnings - nlp2cmd may work with limitations[/yellow bold]")
            else:
                self.console.print("\n[green bold]✅ System is ready![/green bold]")
        else:
            print(f"\n--- Summary ---")
            print(f"OK: {ok}")
            if fixed:
                print(f"Fixed: {fixed}")
            if warnings:
                print(f"Warnings: {warnings}")
            if errors:
                print(f"Errors: {errors}")

            if errors > 0:
                print("\n❌ System has errors - fix before running nlp2cmd")
            elif warnings > 0:
                print("\n⚠ System has warnings - nlp2cmd may work with limitations")
            else:
                print("\n✅ System is ready!")

    def generate_fix_script(self) -> str:
        """Generate a shell script with all fixes."""
        commands = []
        for result in self.results:
            if result.fix_command and not result.fix_applied:
                commands.append(f"# {result.name}: {result.message}")
                commands.append(result.fix_command)
                commands.append("")

        if not commands:
            return "# No fixes needed - system is ready!"

        return "#!/bin/bash\n# NLP2CMD Doctor Fix Script\n\n" + "\n".join(commands)


def run_doctor(auto_fix: bool = False, output_json: bool = False, fix_script: Optional[str] = None):
    """Run the doctor diagnostic."""
    console = Console() if HAS_RICH else None

    doctor = NP2CMDDoctor(console=console, auto_fix=auto_fix)
    results = doctor.run_all_checks()
    doctor.print_summary()

    if output_json:
        # JSON output for programmatic use
        output = {
            "results": [
                {
                    "name": r.name,
                    "status": r.status.value,
                    "message": r.message,
                    "details": r.details,
                    "fix_applied": r.fix_applied,
                    "fix_command": r.fix_command,
                }
                for r in results
            ],
            "summary": {
                "ok": sum(1 for r in results if r.status == Status.OK),
                "fixed": sum(1 for r in results if r.status == Status.FIXED),
                "warnings": sum(1 for r in results if r.status == Status.WARNING),
                "errors": sum(1 for r in results if r.status == Status.ERROR),
                "ready": not any(r.status == Status.ERROR for r in results),
            }
        }
        print(json.dumps(output, indent=2))
        return output["summary"]["ready"]

    if fix_script:
        script = doctor.generate_fix_script()
        Path(fix_script).write_text(script)
        print(f"\nFix script written to: {fix_script}")
        print("Run with: bash " + fix_script)

    # Return exit code based on errors
    has_errors = any(r.status == Status.ERROR for r in results)
    return not has_errors


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NLP2CMD System Doctor")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues where possible")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of formatted text")
    parser.add_argument("--fix-script", type=str, help="Generate fix script to file")
    parser.add_argument("--get-token", action="store_true", help="Open browser to get HF_TOKEN")
    args = parser.parse_args()

    if args.get_token:
        console = Console() if HAS_RICH else None
        token = get_hf_token_via_browser(console)
        if token:
            # Save token
            env_file = Path(".env")
            if env_file.exists():
                content = env_file.read_text()
                if "HF_TOKEN=" in content:
                    lines = content.split("\n")
                    new_lines = [f"HF_TOKEN={token}" if l.startswith("HF_TOKEN=") else l for l in lines]
                    content = "\n".join(new_lines)
                else:
                    content += f"\nHF_TOKEN={token}\n"
                env_file.write_text(content)
            else:
                env_file.write_text(f"HF_TOKEN={token}\n")
            
            os.environ["HF_TOKEN"] = token
            if console:
                console.print(f"[green]✓ HF_TOKEN saved to {env_file}[/green]")
            else:
                print(f"✓ HF_TOKEN saved to {env_file}")
            sys.exit(0)
        else:
            print("✗ Failed to get token")
            sys.exit(1)

    success = run_doctor(auto_fix=args.fix, output_json=args.json, fix_script=args.fix_script)
    sys.exit(0 if success else 1)


# Click CLI integration
try:
    import click

    @click.command(name="doctor")
    @click.option("--fix", is_flag=True, help="Auto-fix issues where possible")
    @click.option("--json", "output_json", is_flag=True, help="Output JSON instead of formatted text")
    @click.option("--fix-script", type=click.Path(), help="Generate fix script to file")
    @click.option("--set-token", help="Set HF_TOKEN to .env file")
    @click.option("--get-token", is_flag=True, help="Open browser to get HF_TOKEN from Hugging Face")
    @click.pass_context
    def doctor_command(ctx, fix: bool, output_json: bool, fix_script: Optional[str], set_token: Optional[str], get_token: bool):
        """Diagnose and fix nlp2cmd system issues."""
        console = Console() if HAS_RICH else None
        
        if get_token:
            token = get_hf_token_via_browser(console)
            if token:
                # Save token
                env_file = Path(".env")
                if env_file.exists():
                    content = env_file.read_text()
                    if "HF_TOKEN=" in content:
                        lines = content.split("\n")
                        new_lines = [f"HF_TOKEN={token}" if l.startswith("HF_TOKEN=") else l for l in lines]
                        content = "\n".join(new_lines)
                    else:
                        content += f"\nHF_TOKEN={token}\n"
                    env_file.write_text(content)
                else:
                    env_file.write_text(f"HF_TOKEN={token}\n")
                
                os.environ["HF_TOKEN"] = token
                if console:
                    console.print(f"[green]✓ HF_TOKEN saved to {env_file}[/green]")
                else:
                    print(f"✓ HF_TOKEN saved to {env_file}")
                ctx.exit(0)
            else:
                print("✗ Failed to get token")
                ctx.exit(1)
        
        if set_token:
            # Write token to .env file
            env_file = Path(".env")
            token_line = f"HF_TOKEN={set_token}\n"
            
            if env_file.exists():
                content = env_file.read_text()
                # Replace existing HF_TOKEN or append
                if "HF_TOKEN=" in content:
                    lines = content.split("\n")
                    new_lines = []
                    for line in lines:
                        if line.startswith("HF_TOKEN="):
                            new_lines.append(f"HF_TOKEN={set_token}")
                        else:
                            new_lines.append(line)
                    content = "\n".join(new_lines)
                else:
                    content += f"\n{token_line}"
                env_file.write_text(content)
            else:
                env_file.write_text(token_line)
            
            # Also set for current session
            os.environ["HF_TOKEN"] = set_token
            
            if console:
                console.print(f"[green]✓ HF_TOKEN saved to {env_file} and set for current session[/green]")
            else:
                print(f"✓ HF_TOKEN saved to {env_file}")
            ctx.exit(0)
        
        success = run_doctor(auto_fix=fix, output_json=output_json, fix_script=fix_script)
        ctx.exit(0 if success else 1)

except ImportError:
    # Click not available - define stub
    def doctor_command(*args, **kwargs):
        pass
