"""Verify selected modern local file-time export, import and overlap state."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--filetime')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-dst.py')),run_name='__main__')
