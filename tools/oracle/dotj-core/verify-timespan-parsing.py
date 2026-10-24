"""Verify selected invariant TimeSpan Parse and TryParse results, errors and out reset."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--parsing')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
