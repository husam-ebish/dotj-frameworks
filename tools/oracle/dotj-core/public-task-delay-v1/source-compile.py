"""Dedicated source-compile.py entrypoint. No alternate mode selector."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase_tools
if __name__ == "__main__":
    phase_tools.execute('source-compile')
