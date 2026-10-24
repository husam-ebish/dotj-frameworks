"""Verify the three selected DateTime exact formats, year range and failure reset."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--exact-parsing')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-comparison.py')),run_name='__main__')
