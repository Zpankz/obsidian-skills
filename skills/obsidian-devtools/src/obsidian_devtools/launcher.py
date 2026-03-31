"""
Obsidian Process Launcher and Management
"""
import subprocess
import time
import logging
import psutil
from typing import Optional, List

# Standard path on macOS
OBSIDIAN_PATH = "/Applications/Obsidian.app/Contents/MacOS/Obsidian"

logger = logging.getLogger(__name__)

class ObsidianLauncher:
    def __init__(self, port: int = 9222):
        self.port = port
        self.debug_flag = f"--remote-debugging-port={port}"
        # Bind strictly to localhost for security
        self.address_flag = "--remote-debugging-address=127.0.0.1"

    def is_running(self) -> bool:
        """Check if any Obsidian process is running."""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == 'Obsidian':
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def get_debug_process(self) -> Optional[psutil.Process]:
        """Return the psutil.Process if Obsidian is running with the debug flag."""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'Obsidian':
                    cmdline = proc.info.get('cmdline', [])
                    # Check for the specific port flag
                    if any(f"--remote-debugging-port={self.port}" in arg for arg in cmdline):
                        return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def launch(self, restart: bool = False) -> str:
        """
        Ensures Obsidian is running with the debug flag.

        Args:
            restart: If True, kill existing non-debug instances and start fresh.

        Returns:
            Status message string.

        Raises:
            RuntimeError: If Obsidian is running without debug and restart=False.
        """
        debug_proc = self.get_debug_process()
        if debug_proc:
            return f"Obsidian is already running in debug mode (PID: {debug_proc.pid})"

        # Check for non-debug instances
        running = self.is_running()
        if running:
            if not restart:
                raise RuntimeError(
                    "Obsidian is running but NOT in debug mode. "
                    "Please close Obsidian manually or call with restart=True."
                )

            logger.info("Killing existing Obsidian instances...")
            self._kill_all()
            time.sleep(2) # Wait for cleanup

        logger.info(f"Launching Obsidian with {self.debug_flag}...")

        # Launch detached process
        subprocess.Popen(
            [OBSIDIAN_PATH, self.debug_flag, self.address_flag],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        # Wait for it to potentially appear
        for _ in range(10):
            time.sleep(1)
            if self.get_debug_process():
                return "Obsidian launched in debug mode."

        return "Obsidian launched, but debug port not yet confirmed."

    def _kill_all(self):
        """Terminates all Obsidian processes."""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == 'Obsidian':
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

ensure_debug_mode = ObsidianLauncher().launch
