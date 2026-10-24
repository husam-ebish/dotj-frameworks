"""Verify selected null-provider TimeSpan custom format syntax against pinned CLR results."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--custom-formats')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
