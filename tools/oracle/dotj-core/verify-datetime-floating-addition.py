"""Verify selected DateTime floating-unit precision, truncation, range and Kind contracts."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--floating-addition')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-comparison.py')),run_name='__main__')
