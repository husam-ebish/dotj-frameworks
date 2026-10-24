"""Verify selected invariant ISO DateTime parsing, fractional rounding and output reset."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--parsing')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-comparison.py')),run_name='__main__')
