"""Verify TimeSpan UTF-8 buffers and pinned literal encoding boundaries."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--utf8-formatting')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
