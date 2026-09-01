"""Browser automation helpers for HF token retrieval."""
from __future__ import annotations

import os
import socket
import subprocess
import shutil
import time
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    Console = None

try:
    from nlp2cmd.browser_token import HFTokenRetriever, TokenConfig
    _BROWSER_TOKEN_AVAILABLE = True
except ImportError:
    _BROWSER_TOKEN_AVAILABLE = False

try:
    from nlp2cmd.browser_manager import ExistingBrowserManager, BrowserConfig
    _BROWSER_MANAGER_AVAILABLE = True
except ImportError:
    _BROWSER_MANAGER_AVAILABLE = False


def get_hf_token_via_browser(console: Optional[Console] = None) -> Optional[str]:
    """Open browser to help user get HF_TOKEN from Hugging Face.
    
    Browser priority:
    1. Connect to existing browser (Firefox/Chrome via CDP)
    2. Open new system browser (firefox/chrome commands)
    3. Use Playwright (requires manual login)
    
    Returns the token if successfully retrieved.
    """
    if console:
        console.print("[cyan]🌐 Opening Hugging Face in browser...[/cyan]")
    else:
        print("🌐 Opening Hugging Face in browser...")
    
    # Try priority 1: Connect to existing browser
    token = _try_existing_browser(console)
    if token:
        return token
    
    # Try priority 2: Open new system browser
    token = _try_system_browser(console)
    if token:
        return token
    
    # Try priority 3: Use Playwright
    token = _try_playwright_browser(console)
    if token:
        return token
    
    return None


def _try_existing_browser(console: Optional[Console] = None) -> Optional[str]:
    """Try to connect to existing browser via CDP with detailed logging."""
    import socket
    
    if console:
        console.print("[dim]   [Stage 1/3] Checking for existing browser...[/dim]")
    
    # Check common CDP ports
    cdp_ports = [9222, 9223, 9224, 9333]
    found_port = None
    
    for port in cdp_ports:
        if console:
            console.print(f"[dim]     Checking port {port}...[/dim]")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", port))
            sock.close()
            
            if result == 0:
                found_port = port
                if console:
                    console.print(f"[green]     ✓ Found browser on port {port}[/green]")
                break
            else:
                if console:
                    console.print(f"[dim]     Port {port}: not available[/dim]")
        except Exception as e:
            if console:
                console.print(f"[dim]     Port {port}: error - {e}[/dim]")
    
    if not found_port:
        if console:
            console.print("[dim]     ℹ No existing browser with CDP found[/dim]")
            console.print("[dim]       Tip: Run 'firefox --remote-debugging-port=9222' first[/dim]")
        return None
    
    # Try to connect via Playwright CDP
    if console:
        console.print(f"[cyan]     → Connecting via Playwright to port {found_port}...[/cyan]")
    
    connection_success = False
    browser = None
    browser_type = None
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # Try Chrome/Chromium first
            try:
                browser = p.chromium.connect_over_cdp(f"http://localhost:{found_port}")
                browser_type = "Chrome/Chromium"
                connection_success = True
                if console:
                    console.print(f"[green]     ✓ Connected to {browser_type} via CDP[/green]")
            except Exception as chrome_err:
                if console:
                    console.print(f"[dim]     Chromium CDP failed: {str(chrome_err)[:50]}...[/dim]")
                
                # Try Firefox
                try:
                    browser = p.firefox.connect_over_cdp(f"http://localhost:{found_port}")
                    browser_type = "Firefox"
                    connection_success = True
                    if console:
                        console.print(f"[green]     ✓ Connected to Firefox via CDP[/green]")
                except Exception as firefox_err:
                    if console:
                        console.print(f"[red]     ✗ CDP connection failed for both browsers[/red]")
                        console.print(f"[dim]       Chrome error: {str(chrome_err)[:30]}...[/dim]")
                        console.print(f"[dim]       Firefox error: {str(firefox_err)[:30]}...[/dim]")
                    return None
            
            if not connection_success or not browser:
                if console:
                    console.print(f"[red]     ✗ Browser connection established but browser object is None[/red]")
                return None
            
            # Create new context and page
            if console:
                console.print(f"[dim]     Creating browser context...[/dim]")
            
            try:
                context = browser.new_context()
                page = context.new_page()
                if console:
                    console.print(f"[green]     ✓ Browser context created[/green]")
            except Exception as ctx_err:
                if console:
                    console.print(f"[red]     ✗ Failed to create browser context: {ctx_err}[/red]")
                return None
            
            # Navigate
            if console:
                console.print(f"[cyan]     → Navigating to huggingface.co...[/cyan]")
            
            nav_success = False
            expected_url_pattern = "huggingface.co/settings/tokens"
            actual_url = None
            
            try:
                page.goto("https://huggingface.co/settings/tokens", timeout=30000)
                actual_url = page.url
                
                # Verify we reached the expected page (or at least HF domain)
                if expected_url_pattern in actual_url:
                    nav_success = True
                    if console:
                        console.print(f"[green]     ✓ Page loaded at correct URL[/green]")
                elif "huggingface.co/login" in actual_url:
                    # This is expected if not logged in, but we should warn
                    nav_success = True  # Page loaded, just needs login
                    if console:
                        console.print(f"[yellow]     ⚠ Page loaded but requires login first[/yellow]")
                        console.print(f"[dim]       URL: {actual_url}[/dim]")
                elif "huggingface.co" in actual_url:
                    nav_success = True
                    if console:
                        console.print(f"[yellow]     ⚠ Page loaded on HF domain but different path[/yellow]")
                        console.print(f"[dim]       URL: {actual_url}[/dim]")
                else:
                    if console:
                        console.print(f"[red]     ✗ Page loaded but unexpected URL[/red]")
                        console.print(f"[dim]       Expected: {expected_url_pattern}[/dim]")
                        console.print(f"[dim]       Actual: {actual_url}[/dim]")
                        
            except Exception as e:
                if console:
                    console.print(f"[red]     ✗ Navigation failed: {e}[/red]")
                    if actual_url:
                        console.print(f"[dim]       Last URL: {actual_url}[/dim]")
                    nav_success = False
            
    except ImportError:
        if console:
            console.print(f"[red]     ✗ Playwright not installed[/red]")
        return None
    except Exception as e:
        if console:
            console.print(f"[red]     ✗ CDP connection error: {e}[/red]")
        return None


def _try_system_browser(console: Optional[Console] = None) -> Optional[str]:
    """Try to open new system browser with detailed stage logging."""
    import subprocess
    import time
    import socket
    
    if console:
        console.print("[dim]   [Stage 2/3] Opening system browser...[/dim]")
    
    # Try to open Firefox or Chrome/Chromium
    browsers_to_try = [
        ("firefox", ["firefox", "--new-window", "--remote-debugging-port=9222"]),
        ("google-chrome", ["google-chrome", "--new-window", "--remote-debugging-port=9222"]),
        ("chromium", ["chromium", "--new-window", "--remote-debugging-port=9222"]),
        ("chromium-browser", ["chromium-browser", "--new-window", "--remote-debugging-port=9222"]),
    ]
    
    for browser_name, cmd in browsers_to_try:
        try:
            # Stage 2.1: Check if browser binary exists
            if console:
                console.print(f"[dim]     Checking {browser_name}...[/dim]")
            
            result = subprocess.run(["which", browser_name], capture_output=True, timeout=5)
            if result.returncode != 0:
                if console:
                    console.print(f"[dim]     ✗ {browser_name} not found[/dim]")
                continue
            
            if console:
                console.print(f"[cyan]     → Launching {browser_name}...[/cyan]")
            
            # Stage 2.2: Launch browser with CDP enabled
            try:
                process = subprocess.Popen(
                    cmd + ["about:blank"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                if console:
                    console.print(f"[dim]     PID: {process.pid}[/dim]")
            except Exception as e:
                if console:
                    console.print(f"[red]     ✗ Failed to launch: {e}[/red]")
                continue
            
            # Stage 2.3: Wait for browser to initialize
            if console:
                console.print("[dim]     Waiting for browser to start (3s)...[/dim]")
            time.sleep(3)
            
            # Stage 2.4: Try to connect via CDP (with actual protocol verification)
            if console:
                console.print("[dim]     Checking CDP port 9222 (with protocol verification)...[/dim]")
            
            cdp_available = False
            for attempt in range(5):
                try:
                    # First: basic TCP check
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex(("localhost", 9222))
                    sock.close()
                    
                    if result == 0:
                        # Second: verify it's actually a CDP endpoint by making HTTP request
                        import urllib.request
                        try:
                            response = urllib.request.urlopen(
                                "http://localhost:9222/json/version", 
                                timeout=3
                            )
                            cdp_info = response.read().decode('utf-8')
                            if 'Browser' in cdp_info or 'Protocol-Version' in cdp_info:
                                cdp_available = True
                                if console:
                                    console.print(f"[green]     ✓ CDP port 9222 ready (verified protocol)[/green]")
                                break
                            else:
                                if console:
                                    console.print(f"[dim]     Attempt {attempt+1}/5: port open but not CDP protocol[/dim]")
                        except Exception as http_err:
                            if console:
                                console.print(f"[dim]     Attempt {attempt+1}/5: port open but CDP check failed: {str(http_err)[:40]}[/dim]")
                    else:
                        if console:
                            console.print(f"[dim]     Attempt {attempt+1}/5: port not ready (code: {result})[/dim]")
                except Exception as e:
                    if console:
                        console.print(f"[dim]     Attempt {attempt+1}/5: {str(e)[:40]}[/dim]")
                time.sleep(1)
            
            if not cdp_available:
                if console:
                    console.print(f"[yellow]     ✗ CDP not available after 5 attempts[/yellow]")
                    console.print(f"[dim]       Browser launched but CDP protocol not responding[/dim]")
                continue
            
            # Stage 2.5: Connect with Playwright
            if console:
                console.print(f"[cyan]     → Connecting via Playwright CDP...[/cyan]")
            
            connection_success = False
            browser = None
            
            try:
                from playwright.sync_api import sync_playwright
                
                with sync_playwright() as p:
                    try:
                        browser = p.chromium.connect_over_cdp("http://localhost:9222")
                        connection_success = True
                        if console:
                            console.print(f"[green]     ✓ Connected to {browser_name} via CDP[/green]")
                    except Exception as e:
                        if console:
                            console.print(f"[yellow]     ⚠ CDP connect failed: {str(e)[:50]}...[/yellow]")
                            console.print(f"[dim]     Falling back to manual mode...[/dim]")
                        return _manual_browser_instructions(console, browser_name)
                    
                    if not connection_success or not browser:
                        if console:
                            console.print(f"[red]     ✗ Connection reported success but browser is None[/red]")
                        return _manual_browser_instructions(console, browser_name)
                    
                    try:
                        context = browser.new_context()
                        page = context.new_page()
                        if console:
                            console.print(f"[green]     ✓ Browser context created[/green]")
                    except Exception as ctx_err:
                        if console:
                            console.print(f"[red]     ✗ Failed to create context: {ctx_err}[/red]")
                        return _manual_browser_instructions(console, browser_name)
                    
                    # Stage 2.6: Navigate to HF
                    if console:
                        console.print(f"[cyan]     → Navigating to huggingface.co...[/cyan]")
                    
                    nav_success = False
                    expected_url_pattern = "huggingface.co/settings/tokens"
                    actual_url = None
                    
                    try:
                        page.goto("https://huggingface.co/settings/tokens", timeout=30000)
                        actual_url = page.url
                        
                        # Verify we reached the expected page (or at least HF domain)
                        if expected_url_pattern in actual_url:
                            nav_success = True
                            if console:
                                console.print(f"[green]     ✓ Page loaded at correct URL[/green]")
                        elif "huggingface.co/login" in actual_url:
                            nav_success = True  # Page loaded, just needs login
                            if console:
                                console.print(f"[yellow]     ⚠ Page loaded but requires login first[/yellow]")
                                console.print(f"[dim]       URL: {actual_url}[/dim]")
                        elif "huggingface.co" in actual_url:
                            nav_success = True
                            if console:
                                console.print(f"[yellow]     ⚠ Page loaded on HF domain but different path[/yellow]")
                                console.print(f"[dim]       URL: {actual_url}[/dim]")
                        else:
                            if console:
                                console.print(f"[red]     ✗ Page loaded but unexpected URL[/red]")
                                console.print(f"[dim]       Expected: {expected_url_pattern}[/dim]")
                                console.print(f"[dim]       Actual: {actual_url}[/dim]")
                                
                    except Exception as e:
                        if console:
                            console.print(f"[red]     ✗ Navigation failed: {e}[/red]")
                            if actual_url:
                                console.print(f"[dim]       Last URL: {actual_url}[/dim]")
                        nav_success = False
                    
                    # Stage 2.7: Get token from user (even if nav had issues, let user try)
                    if nav_success or actual_url:  # Only proceed if we at least loaded something
                        return _navigate_and_get_token(page, console, browser_name)
                    else:
                        if console:
                            console.print(f"[red]     ✗ Cannot proceed - page did not load[/red]")
                        return None
                    
            except ImportError:
                if console:
                    console.print(f"[red]     ✗ Playwright not installed[/red]")
                return _manual_browser_instructions(console, browser_name)
            except Exception as e:
                if console:
                    console.print(f"[red]     ✗ Playwright error: {e}[/red]")
                return _manual_browser_instructions(console, browser_name)
                        
        except Exception as e:
            if console:
                console.print(f"[red]   ✗ Error with {browser_name}: {e}[/red]")
            continue
    
    if console:
        console.print("[red]   ✗ No system browser could be opened[/red]")
    return None


def _try_playwright_browser(console: Optional[Console] = None) -> Optional[str]:
    """Last resort: Use Playwright to launch browser with detailed logging."""
    try:
        from playwright.sync_api import sync_playwright
        
        if console:
            console.print("[dim]   [Stage 3/3] Using Playwright (last resort)...[/dim]")
            console.print("[yellow]     ⚠ Note: You'll need to login manually[/yellow]")
        else:
            print("   [Stage 3/3] Using Playwright (you may need to login manually)...")
        
        with sync_playwright() as p:
            # Try Firefox first (better privacy)
            browser_type = "firefox"
            try:
                if console:
                    console.print("[dim]     Launching Firefox...[/dim]")
                browser = p.firefox.launch(headless=False)
                if console:
                    console.print("[green]     ✓ Firefox launched[/green]")
            except Exception as firefox_err:
                if console:
                    console.print(f"[dim]     Firefox failed: {firefox_err}[/dim]")
                    console.print("[dim]     Trying Chromium...[/dim]")
                
                try:
                    browser = p.chromium.launch(headless=False)
                    browser_type = "chromium"
                    if console:
                        console.print("[green]     ✓ Chromium launched[/green]")
                except Exception as chromium_err:
                    if console:
                        console.print(f"[red]     ✗ Both browsers failed[/red]")
                    return None
            
            # Create context and page
            if console:
                console.print("[dim]     Creating browser context...[/dim]")
            
            context = browser.new_context()
            page = context.new_page()
            
            # Navigate
            if console:
                console.print(f"[cyan]     → Navigating to huggingface.co...[/cyan]")
            
            nav_success = False
            expected_url_pattern = "huggingface.co/settings/tokens"
            actual_url = None
            
            try:
                page.goto("https://huggingface.co/settings/tokens", timeout=30000)
                actual_url = page.url
                
                # Verify we reached the expected page (or at least HF domain)
                if expected_url_pattern in actual_url:
                    nav_success = True
                    if console:
                        console.print(f"[green]     ✓ Page loaded at correct URL[/green]")
                elif "huggingface.co/login" in actual_url:
                    nav_success = True
                    if console:
                        console.print(f"[yellow]     ⚠ Page loaded but requires login first[/yellow]")
                        console.print(f"[dim]       URL: {actual_url}[/dim]")
                elif "huggingface.co" in actual_url:
                    nav_success = True
                    if console:
                        console.print(f"[yellow]     ⚠ Page loaded on HF domain but different path[/yellow]")
                        console.print(f"[dim]       URL: {actual_url}[/dim]")
                else:
                    if console:
                        console.print(f"[red]     ✗ Page loaded but unexpected URL[/red]")
                        console.print(f"[dim]       Expected: {expected_url_pattern}[/dim]")
                        console.print(f"[dim]       Actual: {actual_url}[/dim]")
                        
            except Exception as e:
                if console:
                    console.print(f"[red]     ✗ Navigation failed: {e}[/red]")
                    if actual_url:
                        console.print(f"[dim]       Last URL: {actual_url}[/dim]")
                nav_success = False
            
            # Only proceed if page loaded
            if nav_success or actual_url:
                return _navigate_and_get_token(page, console, browser_type)
            else:
                if console:
                    console.print(f"[red]     ✗ Cannot proceed - page did not load[/red]")
                return None
            
    except ImportError:
        if console:
            console.print("[red]     ✗ Playwright not installed[/red]")
        else:
            print("     ✗ Playwright not installed")
        return None
    except Exception as e:
        if console:
            console.print(f"[red]     ✗ Playwright error: {e}[/red]")
        else:
            print(f"     ✗ Playwright error: {e}")
        return None


def _navigate_and_get_token(page, console: Optional[Console], browser_type: str) -> Optional[str]:
    """Navigate to HuggingFace and get token from user."""
    
    if console:
        console.print(f"[dim]       [Token Step 1/4] Already navigated to HF tokens page[/dim]")
    
    # Verify page loaded by checking URL
    try:
        current_url = page.url
        if console:
            console.print(f"[dim]       Current URL: {current_url}[/dim]")
    except Exception as e:
        if console:
            console.print(f"[yellow]       ⚠ Could not get URL: {e}[/yellow]")
    
    # Show instructions
    if console:
        console.print(f"[cyan]       [Token Step 2/4] Showing instructions:[/cyan]")
        console.print("         1. Login to Hugging Face if needed")
        console.print("         2. Click 'New token' button")
        console.print("         3. Set name: 'nlp2cmd'")
        console.print("         4. Select 'Read' role")
        console.print("         5. Click 'Generate token'")
        console.print("         6. Copy the token and paste it here")
    else:
        print("\n📋 Instructions:")
        print("   1. Login to Hugging Face if needed")
        print("   2. Click 'New token' button")
        print("   3. Set name: 'nlp2cmd'")
        print("   4. Select 'Read' role")
        print("   5. Click 'Generate token'")
        print("   6. Copy the token and paste it here")
    
    # Interactive prompt for token
    if console:
        console.print(f"[cyan]       [Token Step 3/4] Waiting for user input...[/cyan]")
        console.print(f"[bold yellow]       ⚠️  CHECK YOUR TERMINAL - waiting for token input![/bold yellow]")
        console.print(f"[bold]       The browser should be open.[/bold]")
        console.print(f"[bold]       After you create the token in the browser, come back here and paste it below.[/bold]")
    
    try:
        # Print visible separator to catch attention
        print("\n" + "="*60)
        print("🔐 ENTER YOUR HF_TOKEN BELOW 🔐")
        print("="*60)
        
        token = input("🔑 Paste HF_TOKEN here: ").strip()
        
        print("="*60)
        
        if console:
            console.print(f"[dim]       Input received: {'Yes' if token else 'No'}[/dim]")
        
        if token:
            if console:
                console.print(f"[cyan]       [Token Step 4/4] Closing browser page...[/cyan]")
            
            try:
                page.close()
                if console:
                    console.print(f"[green]       ✓ Page closed[/green]")
            except Exception as e:
                if console:
                    console.print(f"[dim]       Note: Could not close page: {e}[/dim]")
            
            return token
        else:
            if console:
                console.print(f"[yellow]       ⚠ No token entered[/yellow]")
    except EOFError:
        if console:
            console.print(f"[red]       ✗ EOFError (no input available)[/red]")
    except KeyboardInterrupt:
        if console:
            console.print(f"[yellow]       ⚠ User cancelled (KeyboardInterrupt)[/yellow]")
    except Exception as e:
        if console:
            console.print(f"[red]       ✗ Error getting input: {e}[/red]")
    
    # Cleanup on failure
    if console:
        console.print(f"[dim]       Cleaning up...[/dim]")
    
    try:
        page.close()
    except Exception:
        pass
    
    return None


def _try_existing_browser_dispatch(console: Optional[Console] = None) -> Optional[str]:
    """New existing browser token retrieval using modular ExistingBrowserManager.
    
    This is the refactored version that uses the browser_manager package.
    Falls back to legacy _try_existing_browser if modular version unavailable.
    """
    if not _BROWSER_MANAGER_AVAILABLE:
        return _try_existing_browser(console)
    
    try:
        if console:
            console.print("[dim]   [Stage 1/3] Using modular browser manager...[/dim]")
        
        manager = ExistingBrowserManager()
        result = manager.connect_and_navigate(verbose=True, console=console)
        
        if not result.success:
            if console and result.error:
                console.print(f"[dim]     Modular manager failed: {result.error}[/dim]")
            return _try_existing_browser(console)
        
        if result.page:
            token = manager.get_token_interactive(result, verbose=True, console=console)
            return token
        
        return None
        
    except Exception as e:
        # Fall back to legacy implementation
        if console:
            console.print(f"[dim]     Modular manager failed: {e}[/dim]")
            console.print("[dim]     Falling back to legacy implementation...[/dim]")
        return _try_existing_browser(console)


def _try_playwright_browser_dispatch(console: Optional[Console] = None) -> Optional[str]:
    """New browser token retrieval using modular HFTokenRetriever.
    
    This is the refactored version that uses the browser_token package.
    Falls back to legacy _try_playwright_browser if modular version unavailable.
    """
    if not _BROWSER_TOKEN_AVAILABLE:
        return _try_playwright_browser(console)
    
    try:
        if console:
            console.print("[dim]   [Stage 3/3] Using modular browser token retriever...[/dim]")
            console.print("[yellow]     ⚠ Note: You'll need to login manually[/yellow]")
        
        retriever = HFTokenRetriever()
        result = retriever.retrieve()
        
        if result.success:
            if console:
                console.print(f"[green]     ✓ Token retrieved via {result.browser_type}[/green]")
            return result.token
        else:
            if console:
                if result.error:
                    console.print(f"[red]     ✗ {result.error}[/red]")
                else:
                    console.print(f"[yellow]     ⚠ {result.message}[/yellow]")
            return None
            
    except Exception as e:
        # Fall back to legacy implementation
        if console:
            console.print(f"[dim]     Modular retriever failed: {e}[/dim]")
            console.print("[dim]     Falling back to legacy implementation...[/dim]")
        return _try_playwright_browser(console)


def _manual_browser_instructions(console: Optional[Console], browser_name: str) -> Optional[str]:
    """Show manual instructions when browser automation fails."""
    if console:
        console.print(f"\n[cyan]📋 {browser_name} opened. Please:[/cyan]")
        console.print("   1. Go to: https://huggingface.co/settings/tokens")
        console.print("   2. Login if not logged in")
        console.print("   3. Create new token (name: nlp2cmd, role: read)")
        console.print("   4. Copy the token")
    else:
        print(f"\n📋 {browser_name} opened. Please:")
        print("   1. Go to: https://huggingface.co/settings/tokens")
        print("   2. Login if not logged in")
        print("   3. Create new token (name: nlp2cmd, role: read)")
        print("   4. Copy the token")
    
    try:
        token = input("\n🔑 Paste HF_TOKEN here: ").strip()
        if token:
            return token
    except (EOFError, KeyboardInterrupt):
        pass
    
    return None

