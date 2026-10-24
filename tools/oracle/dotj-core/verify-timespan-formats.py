"""Verify selected c/t/T formats, format errors and IFormattable dispatch."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--formats')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
