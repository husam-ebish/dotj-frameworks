"""Run pinned TimeSpan total-duration and signed component boundary vectors."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--properties')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
