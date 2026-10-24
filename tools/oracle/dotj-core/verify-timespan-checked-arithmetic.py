"""Verify TimeSpan checked addition, subtraction, duration and negation."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--checked-arithmetic')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
