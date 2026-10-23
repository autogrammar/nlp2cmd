#!/usr/bin/env python3
"""
NLP2CMD Desktop GUI Automation Demo via noVNC.

Demonstrates controlling a Linux desktop environment through natural language:
- Opens applications (calculator, terminal, file manager, text editor)
- Types text, clicks buttons, fills forms in desktop apps
- Records the noVNC browser viewport as a unique WebM file in docker/novnc/recordings

Prerequisites:
    docker compose -f docker/novnc/docker-compose.yml up -d
    # Wait ~10s for desktop to start
    # Open http://localhost:6080/vnc.html to watch live

Usage:
    python3 docker/novnc/demos/demo_desktop_gui.py
    python3 docker/novnc/demos/demo_desktop_gui.py --record
    python3 docker/novnc/demos/demo_desktop_gui.py --headless
"""

from __future__ import annotations

import argparse
from contextlib import ExitStack, contextmanager
from datetime import date
import subprocess
import sys
import time
from pathlib import Path


def ensure_playwright():
    """Ensure playwright is available."""
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        print("Installing playwright...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        return True


def _connect_novnc(page, novnc_url: str, logger) -> bool:
    """Connect to noVNC with retry logic. Returns True if connected."""
    vnc_page = f"{novnc_url.rstrip('/')}/vnc.html?autoconnect=true"
    for attempt in range(1, 11):
        try:
            page.goto(vnc_page, wait_until="load", timeout=8000)
            page.wait_for_function(
                "document.documentElement.classList.contains('noVNC_connected')",
                timeout=15000,
            )
            return True
        except Exception as e:
            err = str(e)
            if "ERR_CONNECTION_REFUSED" in err or "net::" in err:
                msg = f"Retry {attempt}/10..." if attempt > 1 else "Container not ready, retrying..."
                print(f"  {msg}")
                logger.info(msg)
                time.sleep(3)
            else:
                logger.warning(f"Connection error: {e}")
                return False
    return False


def _launch_desktop_application(page, command, *, startup_ms=2000):
    """Allow XFCE's asynchronous command lookup to enable the launch action."""
    page.keyboard.press("Alt+F2")
    page.wait_for_timeout(1000)
    page.keyboard.press("Control+a")
    page.keyboard.type(command, delay=50)
    # Enter sent immediately after typing can be ignored by Application Finder.
    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")
    page.wait_for_timeout(startup_ms)


def _run_desktop_steps(page, logger):
    """Perform the demonstration independently of resource management."""
    # --- Step 2: Terminal ---
    print("\n[2/6] Opening terminal...")
    page.keyboard.press("Control+Alt+t")
    page.wait_for_timeout(2000)
    logger.step("Opened terminal (Ctrl+Alt+T)", page=page)

    cmd = "echo 'Hello from NLP2CMD! Autonomous desktop control.'"
    print(f"  Typing: {cmd}")
    page.keyboard.type(cmd, delay=30)
    page.wait_for_timeout(300)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    logger.step("Executed shell command", page=page)
    logger.code(cmd)

    # --- Step 3: Calculator ---
    print("\n[3/6] Opening calculator...")
    page.keyboard.type("galculator &", delay=30)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)
    logger.step("Opened galculator", page=page)

    calc_expr = "42*137"
    print(f"  Calculating: {calc_expr}")
    page.keyboard.type(calc_expr, delay=100)
    page.wait_for_timeout(300)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    logger.step(f"Entered calculation {calc_expr}; expected result 5754", page=page, extra={
        "expression": calc_expr,
        "expected_result": 5754,
    })

    # --- Step 4: Text editor ---
    print("\n[4/6] Opening text editor...")
    _launch_desktop_application(page, "mousepad")
    logger.step("Opened Mousepad text editor (Alt+F2)", page=page)

    doc_text = (
        "NLP2CMD Desktop Automation Report\n"
        "==================================\n\n"
        f"Date: {date.today().isoformat()}\n"
        "System: Linux (XFCE via noVNC)\n\n"
        "This document was created autonomously by NLP2CMD.\n"
    )
    print("  Typing document...")
    page.keyboard.type(doc_text, delay=8)
    page.wait_for_timeout(500)
    logger.step("Typed document content", page=page)
    logger.code(doc_text, language="text")

    print("  Saving (Ctrl+S)...")
    page.keyboard.press("Control+s")
    page.wait_for_timeout(1500)
    page.keyboard.press("Control+a")
    page.keyboard.type("/home/nlp2cmd/nlp2cmd_report.txt", delay=30)
    # GTK resolves the filename asynchronously before enabling Save.
    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    logger.step("Saved document via Ctrl+S", page=page, extra={
        "filename": "/home/nlp2cmd/nlp2cmd_report.txt",
    })

    # --- Step 5: File manager ---
    print("\n[5/6] Opening file manager...")
    _launch_desktop_application(page, "thunar /home/nlp2cmd")
    logger.step("Opened Thunar file manager", page=page, extra={
        "path": "/home/nlp2cmd",
    })

    # --- Step 6: Firefox ---
    print("\n[6/6] Opening Firefox...")
    # Show the result of this session without depending on an external website.
    url = "file:///home/nlp2cmd/nlp2cmd_report.txt"
    _launch_desktop_application(page, f"firefox {url}", startup_ms=5000)
    logger.step("Opened Firefox browser", page=page, extra={"url": url})

    # --- Final ---
    page.wait_for_timeout(2000)
    logger.step("Final desktop state", page=page)



def _finalize_context(context, capture, logger):
    """Closing the context flushes Playwright's WebM before reading its path."""
    context.close()
    video = capture.get("video")
    if video is not None:
        path = Path(video.path())
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError("Playwright did not produce a nonempty recording")
        capture["path"] = path
        logger.info(f"Video saved (WebM): {path}")


@contextmanager
def _browser_session(playwright, *, headless, record, output_dir, logger):
    """Own only this browser session; never control container-wide processes."""
    capture = {}
    with ExitStack() as resources:
        browser = playwright.chromium.launch(headless=headless)
        resources.callback(browser.close)
        options = {"viewport": {"width": 1280, "height": 800}}
        if record:
            options.update(
                record_video_dir=str(output_dir),
                record_video_size={"width": 1280, "height": 800},
            )
        context = browser.new_context(**options)
        resources.callback(_finalize_context, context, capture, logger)
        page = context.new_page()
        if record:
            capture["video"] = page.video
            if page.video is None:
                raise RuntimeError("Playwright video recording is unavailable")
        yield page, capture


def run_demo(*, record=False, headless=False, novnc_url="http://localhost:6080", output_dir=None):
    """Record the supplied noVNC page as WebM; finalize partial runs on failure.

    Playwright records the browser viewport, including the noVNC desktop canvas.
    Unique Playwright filenames keep previous sessions intact. Docker-side MP4
    recording is no longer needed, so --url works with a remote noVNC instance.
    """
    from playwright.sync_api import sync_playwright

    src_path = str(Path(__file__).resolve().parents[3] / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from nlp2cmd.cli.session_logger import SessionLogger

    output_dir = Path(output_dir) if output_dir is not None else Path(__file__).resolve().parents[1] / "recordings"
    output_dir.mkdir(parents=True, exist_ok=True)
    logger = SessionLogger("desktop_gui_demo", output_dir=output_dir, thumbnail_width=256)
    logger.start("NLP2CMD Desktop GUI Automation Demo", description="XFCE via noVNC + Playwright")
    completed = False
    capture = {}
    try:
        with sync_playwright() as playwright:
            with _browser_session(playwright, headless=headless, record=record,
                                  output_dir=output_dir, logger=logger) as (page, capture):
                if not _connect_novnc(page, novnc_url, logger):
                    raise RuntimeError(f"Could not connect to noVNC at {novnc_url}")
                page.wait_for_selector("canvas", state="visible", timeout=15000)
                page.locator("canvas").focus()
                logger.step("Connected to desktop via noVNC", page=page, extra={"url": novnc_url})
                _run_desktop_steps(page, logger)
        completed = True
    except Exception as error:
        logger.warning(f"Demo failed: {error}")
        raise
    finally:
        report = logger.end(summary={"Status": "completed" if completed else "failed",
                                     "Protocol": "Playwright → noVNC → VNC → desktop"})
        print(f"Markdown report: {report}")
        if capture.get("path"):
            print(f"Video (WebM): {capture['path']}")
    return capture.get("path")


def main():
    parser = argparse.ArgumentParser(description="NLP2CMD Desktop GUI Automation Demo")
    parser.add_argument("--record", action="store_true", help="Record video of the demo session")
    parser.add_argument("--headless", action="store_true", help="Run Playwright in headless mode")
    parser.add_argument("--url", default="http://localhost:6080", help="noVNC URL (default: http://localhost:6080)")
    args = parser.parse_args()

    try:
        ensure_playwright()
        run_demo(record=args.record, headless=args.headless, novnc_url=args.url)
    except Exception as error:
        print(f"Demo failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
