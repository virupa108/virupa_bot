import logging
import colorama
from colorama import Fore, Back, Style
import os

# Force colors even in Docker
os.environ['FORCE_COLOR'] = '1'
os.environ['TERM'] = 'xterm-256color'
colorama.init(strip=False)  # Simplified init

class ColoredFormatter(logging.Formatter):
    """Custom formatter with forced colors for docker compose"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force ANSI colors with different shades
        self.COLORS = {
            'DEBUG': {
                'level': '\033[94m',     # Light Blue
                'filename': '\033[96;1m', # Cyan Bold
                'lineno': '\033[36m',     # Dark Cyan
                'msg': '\033[94m'         # Light Blue
            },
            'INFO': {
                'level': '\033[95m',      # Light Purple
                'filename': '\033[95;1m',  # Purple Bold
                'lineno': '\033[35m',      # Dark Purple
                'msg': '\033[95m'         # Purple
            },
            'WARNING': {
                'level': '\033[93m',      # Light Yellow
                'filename': '\033[33;1m',  # Yellow Bold
                'lineno': '\033[33m',      # Yellow
                'msg': '\033[33m'         # Yellow
            },
            'ERROR': {
                'level': '\033[91m',      # Light Red
                'filename': '\033[31;1m',  # Red Bold
                'lineno': '\033[31m',      # Red
                'msg': '\033[31m'         # Red
            },
            'CRITICAL': {
                'level': '\033[97;41m',   # White on Red
                'filename': '\033[31;1m',  # Bright Red Bold
                'lineno': '\033[31m',      # Red
                'msg': '\033[31;1m'       # Bright Red
            }
        }
        self.RESET = '\033[0m'

    def format(self, record):
        # Get color scheme for this level
        colors = self.COLORS.get(record.levelname, self.COLORS['INFO'])

        # Apply colors to each component with adjusted padding
        record.levelname = f"{colors['level']}{record.levelname:8}{self.RESET}"
        record.filename = f"{colors['filename']}{record.filename:8}{self.RESET}"
        record.lineno = f"{colors['lineno']}{record.lineno:3d}{self.RESET}"

        # Color the message
        record.msg = f"{colors['msg']}{record.msg}{self.RESET}"

        return super().format(record)

def setup_logger():
    """Set up and return a logger with forced colors"""
    # Remove any existing handlers
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    # Create console handler with colored formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter(
        fmt='%(levelname)s %(filename)s:%(lineno)s - %(message)s'
    ))

    # Set up root logger
    root.addHandler(console_handler)
    root.setLevel(logging.INFO)

    return logging.getLogger(__name__)