"""Verify composite TimeSpan integer factories and trailing-zero adapters."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--composite-factories')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
