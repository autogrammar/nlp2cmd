"""
Command Line Interface for NLP2CMD.

Provides interactive REPL mode, file operations, and environment analysis.

This module is the slim entry point. Heavy implementations are in:
- cli/commands/run.py       — --run mode with error recovery
- cli/commands/generate.py  — single-query generation (fast path)
- cli/commands/interactive.py — InteractiveSession REPL
- cli/commands/tools.py     — repair, validate, analyze_env subcommands
- cli/helpers.py            — shared utilities, adapter factory, browser fallbacks
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Optional

# Import click with fallback stubs (service mode must not crash if click missing)
try:
    import click as _click_mod
    click = _click_mod
except Exception:  # pragma: no cover
    click = None  # type: ignore


def _ensure_click_stub() -> None:
    """Minimal click API so decorators work when click is unavailable."""
    global click
    if click is not None and hasattr(click, "group"):
        return

    class _ClickStub:
        @staticmethod
        def group(*_args, **_kwargs):
            def decorator(func):
                return func
            return decorator

        @staticmethod
        def command(*_args, **_kwargs):
            def decorator(func):
                return func
            return decorator

        @staticmethod
        def option(*_args, **_kwargs):
            def decorator(func):
                return func
            return decorator

        class Choice:
            def __init__(self, _choices, **_kwargs):
                pass

        class Path:
            def __init__(self, *_args, **_kwargs):
                pass

    click = _ClickStub()  # type: ignore[assignment]


_ensure_click_stub()

# Import rich console
try:
    from rich.console import Console
    console = Console()
except ImportError:  # pragma: no cover
    console = None  # type: ignore

# Import environment loading
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

# Import auto-repair system
try:
    from nlp2cmd.cli.auto_repair import execute_with_auto_recovery, with_auto_repair
    HAS_AUTO_REPAIR = True
except ImportError:
    HAS_AUTO_REPAIR = False

# ---------------------------------------------------------------------------
# Backward-compatible re-exports (tests & external code import from here)
# ---------------------------------------------------------------------------
# Re-export InteractiveSession from its new location
from nlp2cmd.cli.commands.interactive import InteractiveSession  # noqa: F401

# Re-export handle_run_mode and keep _handle_run_query monkeypatch-compatible.
from nlp2cmd.cli.commands import run as _run_commands
from nlp2cmd.cli.helpers import ExecutionRunner  # noqa: F401


def _handle_run_query(*args, **kwargs):
    _run_commands.ExecutionRunner = ExecutionRunner
    return _run_commands._handle_run_query(*args, **kwargs)

# Re-export helpers used by the main() dispatcher


# ---------------------------------------------------------------------------
# Lazy subcommand registration
# ---------------------------------------------------------------------------
def _register_subcommands_for_args(argv: list[str]) -> None:
    """Register Click subcommands lazily based on argv.

    This avoids importing heavy optional subsystems (e.g. service/FastAPI) for
    the common case of single-query command generation.
    """
    if not hasattr(click, "Group"):
        return

    # If user asks for help, register everything so commands show up.
    wants_help = any(a in {"--help", "-h"} for a in argv)

    # Find first non-flag token (potential subcommand)
    subcmd = None
    for a in argv:
        if a.startswith("-"):
            continue
        subcmd = a
        break

    try:
        if wants_help or subcmd in {"web-schema"}:
            from nlp2cmd.cli.web_schema import web_schema_group
            main.add_command(web_schema_group)
    except Exception:
        pass

    try:
        if wants_help or subcmd in {"doctor"}:
            from nlp2cmd.cli.commands.doctor import doctor_command
            main.add_command(doctor_command)
    except Exception:
        pass

    try:
        if wants_help or subcmd in {"examples"}:
            from nlp2cmd.cli.commands.examples import examples_group
            main.add_command(examples_group)
    except Exception:
        pass

    try:
        if wants_help or subcmd in {"history"}:
            from nlp2cmd.cli.history import history_group
            main.add_command(history_group)
    except Exception:
        pass

    try:
        if wants_help or subcmd in {"cache"}:
            from nlp2cmd.cli.cache import cache_group
            main.add_command(cache_group)
    except Exception:
        pass

    # Service commands are the heaviest (can pull FastAPI/uvicorn). Register only on demand.
    try:
        if wants_help or subcmd in {"service", "config-service"}:
            from nlp2cmd.service.cli import add_service_command
            add_service_command(main)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Click group — main entry point
# ---------------------------------------------------------------------------

# Stub commands for when click is not available
def repair(*args, **kwargs):
    pass

def validate(*args, **kwargs):
    pass

def analyze_env(*args, **kwargs):
    pass

def version(*args, **kwargs):
    pass


def _run_preflight_checks(console, verbose: bool = False, auto_fix: bool = False, execute_web: bool = False) -> bool:
    """Run quick pre-flight checks before executing commands.
    
    Warns about common issues that will cause problems later.
    Outputs actionable tasks in nlp2cmd format.
    
    Args:
        console: Rich console for output
        verbose: Show verbose output
        auto_fix: Automatically fix issues without prompting
        execute_web: Whether --execute-web is enabled (can use browser)
    
    Returns:
        True if checks passed or issues were fixed, False if user aborted
    """
    warnings = []
    actionable_tasks = []
    needs_token = False
    needs_ollama = False
    
    # Check HF_TOKEN
    hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        needs_token = True
        warnings.append(
            "[yellow]⚠ HF_TOKEN not set - HF Hub requests will be unauthenticated (rate limits)[/yellow]"
        )
        if execute_web:
            actionable_tasks.append(
                "[cyan]📋 Auto-fix available:[/cyan] I can open browser to get HF_TOKEN for you"
            )
    
    # Check Ollama for canvas/web commands (only if we might need it)
    ollama_host = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        host = ollama_host.replace("http://", "").replace("https://", "").split(":")[0]
        result = sock.connect_ex((host, 11434))
        sock.close()
        if result != 0:
            needs_ollama = True
            warnings.append(
                "[yellow]⚠ Ollama not running on port 11434 - canvas drawing commands will use fallback[/yellow]"
            )
            actionable_tasks.append(
                "[cyan]📋 Task: Start Ollama Server[/cyan]\n"
                "   Auto-fix: nlp2cmd doctor --fix\n"
                "   Manual: ollama serve"
            )
    except Exception:
        pass
    
    if warnings and console:
        if verbose:
            console.print("\n[dim]--- Pre-flight checks ---[/dim]")
        for warning in warnings:
            console.print(warning)
        # Print actionable tasks
        for task in actionable_tasks:
            console.print(task)
        if verbose:
            console.print("[dim]-------------------------[/dim]\n")
        
        # Interactive auto-fix for HF_TOKEN if execute_web is enabled
        if needs_token and execute_web:
            if auto_fix:
                should_fix = True
            else:
                console.print("\n[cyan]💡 I can automatically open browser to get HF_TOKEN from Hugging Face.[/cyan]")
                try:
                    response = input("   Do you want me to do this now? [Y/n]: ").strip().lower()
                    should_fix = response in ('', 'y', 'yes')
                except (EOFError, KeyboardInterrupt):
                    should_fix = False
            
            if should_fix:
                console.print("[cyan]🌐 Opening browser to get HF_TOKEN...[/cyan]")
                try:
                    from nlp2cmd.cli.commands.doctor import get_hf_token_via_browser
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
                        console.print(f"[green]✓ HF_TOKEN saved! Continuing with your task...[/green]\n")
                        return True
                    else:
                        console.print("[yellow]⚠ Could not get HF_TOKEN. Continuing without it (may hit rate limits)...[/yellow]\n")
                        return True  # Continue anyway
                except Exception as e:
                    console.print(f"[red]✗ Error getting HF_TOKEN: {e}[/red]")
                    console.print("[yellow]   Continuing anyway...[/yellow]\n")
                    return True
            else:
                console.print("[dim]   Skipping auto-fix. You can run 'nlp2cmd doctor --get-token' later.[/dim]\n")
    
    return True  # Continue with task


@click.group(invoke_without_command=True)
@click.option("-i", "--interactive", is_flag=True, help="Start interactive mode")
@click.option(
    "-d", "--dsl",
    type=click.Choice(["auto", "sql", "shell", "docker", "kubernetes", "dql", "appspec", "browser"]),
    default="auto",
    help="DSL type"
)
@click.option(
    "--appspec",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to an app2schema.appspec JSON file (required for --dsl appspec)",
)
@click.option("-q", "--query", help="Single query to process")
@click.option(
    "--stdin",
    "stdin_mode",
    is_flag=True,
    help="Read query text from stdin (usually automatic when piped; e.g. echo 'list files' | nlp2cmd)",
)
@click.option(
    "--stdout",
    "stdout_only",
    is_flag=True,
    help="Print only the generated command to stdout (no extra formatting)",
)
@click.option(
    "-oo",
    "--only-output",
    "only_output",
    is_flag=True,
    help="In --run mode, print only the executed command output (suppress generation/execution UI)",
)
@click.option("-r", "--run", is_flag=True, help="Execute query immediately with interactive error recovery")
@click.option("--auto-repair", is_flag=True, help="Auto-apply repairs")
@click.option("--explain", is_flag=True, help="Explain how the result was produced")
@click.option("--execute-web", is_flag=True, help="Execute dom_dql.v1 actions via Playwright (requires playwright)")
@click.option("-ac", "--auto-confirm", is_flag=True, help="Skip confirmation prompts when using --run")
@click.option("--no-submit", is_flag=True, help="In --run mode, do not submit forms (skip submit/Enter actions)")
@click.option(
    "--auto-install/--no-auto-install",
    default=True,
    help="Auto-install missing Python deps/tools when using --run (e.g. playwright)",
)
@click.option(
    "--source",
    "source_uri",
    default=None,
    help="Stream source URI (e.g. ssh://user@host, rtsp://cam/stream, libvirt:///system, vnc://host:5901)",
)
@click.option(
    "--log-dir",
    "log_dir",
    default=None,
    type=click.Path(),
    help="Directory for session logs (used with --source)",
)
@click.option("--screenshot", "do_screenshot", is_flag=True, help="Save screenshot after --source action (PNG to --log-dir)")
@click.option("--video", "video_fmt", default=None, type=click.Choice(["mp4", "webm"]), help="Record short video of --source action")
@click.option("--duration", "video_duration", default=3, type=int, help="Video duration in seconds (default: 3)")
@click.option("--md", "do_md", is_flag=True, help="Generate Markdown log with inline thumbnails for --source action")
@click.option("-v", "--version", is_flag=True, help="Show version information")
@click.option("--verbose", is_flag=True, help="Enable verbose debug output")
@click.option(
    "--show-schema",
    "show_schema",
    is_flag=True,
    help="Show available schemas (intents, entities, templates) and exit",
)
@click.option(
    "--show-decision-tree",
    "show_decision_tree",
    is_flag=True,
    help="Show decision tree for a query (what intents detected, entities extracted, etc.)",
)
@click.option(
    "--debug-log-md",
    "debug_log_md",
    type=click.Path(),
    default=None,
    help="Generate debug log in markdown format to file",
)
@click.option(
    "--record-session",
    "record_session",
    type=click.Path(),
    default=None,
    help="Record CLI session to webm video file",
)
@click.pass_context
def main(
    ctx,
    interactive: bool,
    dsl: str,
    appspec: Optional[Path],
    query: Optional[str],
    stdin_mode: bool,
    stdout_only: bool,
    only_output: bool,
    run: bool,
    auto_repair: bool,
    explain: bool,
    execute_web: bool,
    auto_confirm: bool,
    no_submit: bool,
    auto_install: bool,
    source_uri: Optional[str],
    log_dir: Optional[str],
    do_screenshot: bool,
    video_fmt: Optional[str],
    video_duration: int,
    do_md: bool,
    version: bool,
    verbose: bool,
    show_schema: bool,
    show_decision_tree: bool,
    debug_log_md: Optional[str],
    record_session: Optional[str],
):
    """NLP2CMD - Natural Language to Domain-Specific Commands."""
    # Start timing from the very beginning
    script_start_time = time.time()
    
    if load_dotenv is not None:
        try:
            load_dotenv()
        except Exception:
            pass
    
    # Pre-flight health check for critical issues
    if not show_schema and not show_decision_tree and not version:
        checks_passed = _run_preflight_checks(console, verbose, auto_fix=auto_confirm, execute_web=execute_web)
        if not checks_passed:
            return  # User aborted
    
    ctx.ensure_object(dict)
    ctx.obj["dsl"] = dsl
    ctx.obj["auto_repair"] = auto_repair
    ctx.obj["log_dir"] = log_dir
    ctx.obj["script_start_time"] = script_start_time
    ctx.obj["verbose"] = verbose

    # Handle --show-schema flag
    if show_schema:
        from nlp2cmd.cli.debug_info import show_schema_info
        show_schema_info(console)
        return

    # Handle --show-decision-tree flag (requires --query)
    if show_decision_tree:
        if not query:
            console.print("[red]Error: --show-decision-tree requires --query <text>[/red]")
            console.print("Example: nlp2cmd --show-decision-tree --query 'otwórz firefox'")
            return
        from nlp2cmd.cli.debug_info import show_decision_tree_info
        show_decision_tree_info(query, console)
        return

    if ctx.invoked_subcommand is None:
        auto_stdin = (not stdin_mode) and (not query) and (not sys.stdin.isatty())
        if (stdin_mode or auto_stdin) and not query:
            try:
                stdin_text = sys.stdin.read()
            except Exception:
                stdin_text = ""
            stdin_text = (stdin_text or "").strip()
            if stdin_text:
                query = stdin_text

    if stdout_only:
        run = False
        explain = False
        interactive = False
        execute_web = False

    if ctx.invoked_subcommand is None:
        if version:
            from nlp2cmd import __version__
            console.print(f"nlp2cmd version {__version__}")
            return
        # --source stream mode: dispatch to StreamRouter
        if source_uri and query:
            from nlp2cmd.streams import StreamRouter
            router = StreamRouter()

            # Determine output directory
            _out = Path(log_dir) if log_dir else Path(".")
            _out.mkdir(parents=True, exist_ok=True)

            # Session logging with screenshots (--md or --log-dir)
            logger = None
            if do_md or log_dir:
                from nlp2cmd.cli.session_logger import SessionLogger
                logger = SessionLogger("session", output_dir=_out, thumbnail_width=256)
                logger.start(f"nlp2cmd --source {source_uri}", description=query)

            if run:
                result = router.execute(source_uri, query)
            else:
                result = router.query(source_uri, query)

            # Automatic fallback path: when stream execution fails, run Doctor and retry once.
            # This is especially useful for VNC/noVNC mismatch errors.
            if run and result.error:
                retry_source = None
                err_lower = str(result.error).lower()
                if source_uri.startswith("vnc://") and (
                    "not connected via novnc" in err_lower or "use novnc:// scheme" in err_lower
                ):
                    retry_source = "novnc://" + source_uri[len("vnc://"):]
                    console.print(f"[yellow]↻ Stream retry with corrected scheme: {retry_source}[/yellow]")
                    result = router.execute(retry_source, query)
                    source_uri = retry_source

                if result.error:
                    try:
                        from nlp2cmd.cli.commands.doctor import run_doctor
                        console.print("[yellow]🔧 Uruchamiam fallback: nlp2cmd doctor --fix[/yellow]")
                        run_doctor(auto_fix=True, output_json=False)
                        console.print("[yellow]↻ Ponawiam zadanie po Doctor...[/yellow]")
                        result = router.execute(source_uri, query)
                    except Exception as doc_err:
                        console.print(f"[yellow]Doctor fallback failed: {doc_err}[/yellow]")

            if result.output:
                console.print(result.output)
            if result.error:
                console.print(f"[red]{result.error}[/red]")
            if result.data and not stdout_only:
                from nlp2cmd.cli.helpers import print_yaml_block
                print_yaml_block(result.data, console=console)

            # --screenshot: save PNG
            if do_screenshot and result.screenshot:
                png_path = _out / "screenshot.png"
                png_path.write_bytes(result.screenshot)
                console.print(f"Screenshot: {png_path}")
            elif do_screenshot and not result.screenshot:
                # Try to get screenshot from adapter
                try:
                    adapter = router.get_adapter(source_uri)
                    shot = adapter.screenshot()
                    if shot:
                        png_path = _out / "screenshot.png"
                        png_path.write_bytes(shot)
                        console.print(f"Screenshot: {png_path}")
                        result.screenshot = shot
                except Exception:
                    pass

            # --video: record short video via adapter (visual streams)
            if video_fmt:
                try:
                    adapter = router.get_adapter(source_uri)
                    if hasattr(adapter, '_page') and adapter._page:
                        vid_path = _out / f"recording.{video_fmt}"
                        page = adapter._page
                        import time as _t
                        frames = []
                        end_t = _t.time() + video_duration
                        while _t.time() < end_t:
                            frames.append(page.screenshot())
                            page.wait_for_timeout(200)
                        # Save as animated sequence (simple approach: save frames + convert)
                        for i, f in enumerate(frames):
                            (_out / f"frame_{i:04d}.png").write_bytes(f)
                        console.print(f"Captured {len(frames)} frames ({video_duration}s) → {_out}/frame_*.png")
                        # Try ffmpeg conversion
                        import subprocess as _sp
                        try:
                            _sp.run([
                                "ffmpeg", "-y", "-framerate", "5",
                                "-i", str(_out / "frame_%04d.png"),
                                "-c:v", "libx264" if video_fmt == "mp4" else "libvpx",
                                "-pix_fmt", "yuv420p",
                                str(vid_path),
                            ], capture_output=True, timeout=30)
                            # Cleanup frames
                            for fp in _out.glob("frame_*.png"):
                                fp.unlink()
                            console.print(f"Video: {vid_path}")
                        except Exception:
                            console.print(f"Frames saved (install ffmpeg for {video_fmt} conversion)")
                    else:
                        console.print(f"[yellow]--video requires a visual stream (vnc/novnc/spice/rdp)[/yellow]")
                except Exception as e:
                    console.print(f"[yellow]Video capture failed: {e}[/yellow]")

            # --md: generate markdown log
            if logger:
                logger.step(
                    query,
                    screenshot_bytes=result.screenshot,
                    extra={"source": source_uri, "success": result.success,
                           **(result.data or {})},
                )
                if result.output:
                    logger.info(result.output[:500])
                if result.error:
                    logger.warning(result.error)
                md_path = logger.end(summary={"source": source_uri, "query": query})
                console.print(f"Session log: {md_path}")

            router.close_all()
            return
        if run and query:
            # Wrap with auto-repair for automatic error recovery
            def _execute_run():
                _handle_run_query(
                    query,
                    dsl=dsl,
                    appspec=appspec,
                    auto_confirm=auto_confirm,
                    no_submit=no_submit,
                    execute_web=execute_web,
                    auto_install=auto_install,
                    auto_repair=auto_repair,
                    only_output=only_output,
                    verbose=verbose,
                    video_fmt=video_fmt,
                    video_duration=video_duration,
                )
            
            if HAS_AUTO_REPAIR and auto_repair:
                execute_with_auto_recovery(
                    _execute_run,
                    auto_confirm=auto_confirm,
                    console=console,
                    execute_web=execute_web,
                )
            else:
                _execute_run()
        elif query:
            if dsl == "appspec":
                from nlp2cmd.cli.commands.generate import handle_appspec_query
                
                # Wrap with auto-repair for automatic error recovery
                def _execute_appspec():
                    handle_appspec_query(
                        query,
                        dsl=dsl,
                        appspec=appspec,
                        auto_repair=auto_repair,
                        explain=explain,
                        execute_web=execute_web,
                        verbose=verbose,
                    )
                
                if HAS_AUTO_REPAIR and auto_repair:
                    execute_with_auto_recovery(
                        _execute_appspec,
                        auto_confirm=auto_confirm,
                        console=console,
                        execute_web=execute_web,
                    )
                else:
                    _execute_appspec()
            elif dsl == "auto":
                from nlp2cmd.cli.commands.generate import handle_generate_query
                
                # Wrap with auto-repair for automatic error recovery
                def _execute_generate():
                    return handle_generate_query(
                        query,
                        dsl=dsl,
                        appspec=appspec,
                        explain=explain,
                        execute_web=execute_web,
                        stdout_only=stdout_only,
                        script_start_time=ctx.obj.get("script_start_time", time.time()),
                        verbose=verbose,
                        debug_log_md=debug_log_md,
                        record_video=record_session,
                    )
                
                if HAS_AUTO_REPAIR and auto_repair:
                    result = execute_with_auto_recovery(
                        _execute_generate,
                        auto_confirm=auto_confirm,
                        console=console,
                        execute_web=execute_web,
                    )
                else:
                    _execute_generate()
        elif interactive:
            session = InteractiveSession(
                dsl=dsl,
                auto_repair=auto_repair,
                appspec=str(appspec) if appspec else None,
            )
            session.run()
        else:
            console.print(ctx.get_help())

# Apply command method stub after main function definition
if not hasattr(click, 'Group'):
    def _stub_command(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    main.command = _stub_command
    main.add_command = lambda cmd: None

# Stub command decorators for when click is not available
_command_decorator = main.command if hasattr(main, 'command') else lambda *args, **kwargs: lambda func: func


@_command_decorator
@click.argument("query")
@click.option("--json", "as_json", is_flag=True, help="Output full payload as JSON")
@click.option("--execute", is_flag=True, help="Execute plan via Propact CLI")
@click.option("--dry-run", is_flag=True, help="With --execute: validate routes only, do not run")
@click.option("--explain", is_flag=True, help="Show IntentIR, execution routes, contract/post-check hints")
@click.option("--verbose", is_flag=True, help="Verbose query-input analysis (implies --explain)")
@click.pass_context
def plan(
    ctx,
    query: str,
    as_json: bool,
    execute: bool,
    dry_run: bool,
    explain: bool,
    verbose: bool,
):
    """Plan NL query → Propact markdown (requires nlp2cmd[integration])."""
    from nlp2cmd.cli.commands.plan import cmd_plan

    raise SystemExit(
        cmd_plan(
            query,
            as_json=as_json,
            execute=execute,
            dry_run=dry_run,
            explain=explain or verbose,
            verbose=verbose,
        )
    )


@_command_decorator
@click.argument("file", type=click.Path(exists=True))
@click.option("--backup", is_flag=True, help="Create backup before repair")
@click.pass_context
def repair(ctx, file: str, backup: bool):
    """Repair a configuration file."""
    from nlp2cmd.cli.commands.tools import cmd_repair
    cmd_repair(file, backup)


@_command_decorator
@click.argument("file", type=click.Path(exists=True))
@click.pass_context
def validate(ctx, file: str):
    """Validate a configuration file."""
    from nlp2cmd.cli.commands.tools import cmd_validate
    cmd_validate(file)


@_command_decorator
@click.option("-o", "--output", type=click.Path(), help="Output file (JSON)")
@click.pass_context
def analyze_env(ctx, output: Optional[str]):
    """Analyze system environment."""
    from nlp2cmd.cli.commands.tools import cmd_analyze_env
    cmd_analyze_env(output)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def cli_entry_point():
    """Entry point that handles natural language queries before Click."""
    try:
        from nlp2cmd.autoupdate import check_for_updates
        check_for_updates("nlp2cmd")
    except Exception:
        pass

    import sys
    
    # Get command line arguments
    args = sys.argv[1:]  # Skip the script name
    
    # Lazily register subcommands depending on argv
    _register_subcommands_for_args(args)
    
    # Check if this looks like a natural language query
    # Look for text that contains spaces after flags
    has_text_with_spaces = any(' ' in arg and not arg.startswith('-') for arg in args)
    
    # Also check if we have exactly one argument that contains spaces (single query)
    is_single_query = len(args) == 1 and ' ' in args[0] and not args[0].startswith('-')
    
    # Check if --query flag is already present
    has_query_flag = '--query' in args or '-q' in args
    
    # Skip rewriting when first arg is a known subcommand — subcommands handle
    # their own positional arguments (e.g. "examples autonomous 'draw a star'")
    _KNOWN_SUBCOMMANDS = {
        "examples", "doctor", "web-schema", "history", "cache", "service",
        "plan", "repair", "validate", "analyze_env",
    }
    is_subcommand = args and args[0] in _KNOWN_SUBCOMMANDS
    
    if (not is_subcommand and
        ((len(args) >= 2 and has_text_with_spaces and
        not any(arg.startswith('-') and '=' in arg for arg in args) and  # Avoid flags with values
        not has_query_flag) or  # Don't process if --query is already there
        is_single_query)):
        
        # Parse and rewrite args
        text_parts = []
        option_parts = []
        
        for i, a in enumerate(args):
            if a.startswith("-"):
                option_parts.append(a)
            elif ' ' in a:
                # This looks like natural language text
                text_parts.append(a)
            else:
                # Single word, could be option value or text
                # If we don't have any text parts yet and this isn't a known option, treat it as text
                if not text_parts and i == len(args) - 1:
                    text_parts.append(a)
                else:
                    option_parts.append(a)
        
        query_text = " ".join(text_parts).strip()
        
        # Build new args
        new_args = option_parts.copy()
        
        # If we have a query, add --query
        if query_text:
            new_args.extend(["--query", query_text])
        
        # Replace sys.argv
        sys.argv[1:] = new_args
    
    # Call the main Click function
    main()


if __name__ == "__main__":
    cli_entry_point()
