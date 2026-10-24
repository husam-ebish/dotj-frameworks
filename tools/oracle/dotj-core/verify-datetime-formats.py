"""Verify selected invariant DateTime formatting overloads, dispatch and sortable text."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--formats')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-comparison.py')),run_name='__main__')
