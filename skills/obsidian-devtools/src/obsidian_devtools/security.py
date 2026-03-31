"""
Security Guard for Obsidian DevTools
Enforces Safe Mode and sanitizes input.
"""
import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class SecurityGuard:
    def __init__(self, safe_mode: bool = True):
        self.safe_mode = safe_mode

        # Dangerous patterns to block in Safe Mode
        # We block file system writes, process creation, and vault modifications
        self.blocked_patterns = [
            r"fs\.write", r"fs\.append", r"fs\.unlink", r"fs\.rm", r"fs\.mkdir",
            r"child_process", r"exec\(", r"spawn\(",
            r"app\.vault\.modify", r"app\.vault\.create", r"app\.vault\.delete",
            r"app\.vault\.trash", r"app\.vault\.rename",
            r"electron\.remote", r"process\.exit",
            r"innerHTML\s*=", # Prevention of basic DOM XSS if we were rendering it
        ]

        # Whitelist of explicitly allowed safe operations (conceptually, not used for regex blocking)
        # We assume read operations are safe.

    def validate_eval(self, expression: str) -> Tuple[bool, str]:
        """
        Validates a JavaScript expression against security policies.

        Returns:
            (is_valid, error_message)
        """
        if not self.safe_mode:
            return True, ""

        # Check for blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, expression):
                return False, f"Operation blocked in Safe Mode: matches pattern '{pattern}'"

        return True, ""

    def sanitize_context(self) -> str:
        """
        Returns a JS snippet to prepend to eval requests.
        This snippet masks dangerous globals in the execution scope.
        """
        if not self.safe_mode:
            return ""

        # We shadow dangerous globals with undefined
        return """
        (function() {
            const process = undefined;
            const require = undefined;
            const module = undefined;
            const global = undefined;
            // Execute user code below
        """

    def wrap_expression(self, expression: str) -> str:
        """
        Wraps the user expression in an IIFE with shadowed globals.
        """
        if not self.safe_mode:
            return expression

        return f"""
        (function() {{
            const process = undefined;
            const require = undefined;
            const module = undefined;

            return (function() {{
                {expression}
            }})();
        }})()
        """
