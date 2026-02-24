"""
Shared logger — use across app for consistent logging.
Week 1–2: Configure level, format, and optional file handler.
"""

import logging

# TODO (Week 1): Configure logging (level=INFO, format with timestamp).
# Example: logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def get_logger(name: str) -> logging.Logger:
    """Return a logger for the given module name."""
    return logging.getLogger(name)
