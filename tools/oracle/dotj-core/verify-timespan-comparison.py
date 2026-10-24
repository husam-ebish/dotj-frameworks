"""Verify selected TimeSpan ordering, equality, hashing and boxed-object errors."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--comparison')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
