"""Run pinned TimeSpan multiplication, division and interval-ratio vectors."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--arithmetic')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
