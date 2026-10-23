"""Screenshot and video recording utilities for browser automation."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4


def get_timestamp() -> str:
    """Generate timestamp string for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists, create if not."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def ask_for_screenshot(console: Any, default_path: str) -> tuple[bool, str]:
    """
    Ask user if they want to take a screenshot.
    
    Returns:
        Tuple of (should_take_screenshot, final_path)
    """
    try:
        response = console.input(
            f"[yellow]Zrobić zrzut ekranu? [T/n]: [/yellow]"
        ).strip().lower()
        
        if response in ("", "y", "yes", "t", "tak"):
            custom_path = console.input(
                f"[cyan]Ścieżka zapisu [{default_path}]: [/cyan]"
            ).strip()
            
            if custom_path:
                return True, custom_path
            return True, default_path
        
        return False, ""
    except Exception:
        return False, ""


def take_screenshot(page: Any, path: str, console: Optional[Any] = None) -> Optional[str]:
    """
    Take a screenshot of current page state.
    
    Args:
        page: Playwright page object
        path: Path to save screenshot
        console: Optional console for output
        
    Returns:
        Path to saved screenshot or None if failed
    """
    try:
        # Ensure directory exists
        filepath = Path(path)
        ensure_dir(filepath.parent)
        
        # Take screenshot
        page.screenshot(path=str(filepath), full_page=True)
        
        if console:
            console.print(f"[green]📸 Zrzut ekranu zapisany: {filepath.resolve()}[/green]")
        
        return str(filepath)
    except Exception as e:
        if console:
            console.print(f"[red]❌ Błąd zrzutu ekranu: {e}[/red]")
        return None


class VideoRecorder:
    """Video recording manager for Playwright browser automation."""
    
    def __init__(self, output_dir: str = "./recordings"):
        """
        Initialize video recorder.
        
        Args:
            output_dir: Directory to save recordings
        """
        self.output_dir = Path(output_dir)
        self.video_path: Optional[str] = None
        self.is_recording = False
        
    def start_recording(self, name_prefix: str = "automation") -> Optional[str]:
        """
        Start video recording.
        
        Args:
            name_prefix: Prefix for video filename
            
        Returns:
            Expected path to video file or None
        """
        try:
            timestamp = get_timestamp()
            self.video_path = str(self.output_dir / f"{name_prefix}_{timestamp}_{uuid4().hex}.webm")
            self.is_recording = True
            
            # Ensure directory exists
            ensure_dir(self.output_dir)
            
            return self.video_path
        except Exception:
            self.is_recording = False
            return None
    
    def stop_recording(self, console: Optional[Any] = None, saved_path: Optional[str] = None) -> Optional[str]:
        """
        Finalize recording and return only a nonempty saved video file.
        
        Args:
            console: Optional console for output
            saved_path: Actual path returned by Playwright save (if known)
            
        Returns:
            Path to saved video or None
        """
        if not self.is_recording:
            return None
            
        try:
            if saved_path:
                self.video_path = str(saved_path)
            output = Path(self.video_path) if self.video_path else None
            if output is None or not output.is_file() or output.stat().st_size == 0:
                if console:
                    console.print(f"[red]❌ Brak niepustego pliku nagrania: {self.video_path}[/red]")
                return None
            if console and self.video_path:
                console.print(f"[green]🎥 Nagranie zapisane: {self.video_path}[/green]")
            return self.video_path
        except Exception as e:
            if console:
                console.print(f"[red]❌ Błąd zapisu nagrania: {e}[/red]")
            return None
        finally:
            self.is_recording = False


def ask_for_video_recording(console: Any) -> tuple[bool, str]:
    """
    Ask user if they want to record video.
    
    Returns:
        Tuple of (should_record, output_dir)
    """
    try:
        response = console.input(
            f"[yellow]Nagrać wideo z procesu? [T/n]: [/yellow]"
        ).strip().lower()
        
        if response in ("", "y", "yes", "t", "tak"):
            custom_dir = console.input(
                f"[cyan]Folder zapisu [./recordings]: [/cyan]"
            ).strip()
            
            if custom_dir:
                return True, custom_dir
            return True, "./recordings"
        
        return False, ""
    except Exception:
        return False, ""
