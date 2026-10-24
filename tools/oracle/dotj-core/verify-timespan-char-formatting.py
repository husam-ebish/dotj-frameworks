"""Verify TimeSpan character buffers, output counts and interface dispatch against pinned CLR."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--char-formatting')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
