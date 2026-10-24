"""Verify selected checked DateTime tick, interval and Gregorian calendar arithmetic."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--checked-arithmetic')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-comparison.py')),run_name='__main__')
