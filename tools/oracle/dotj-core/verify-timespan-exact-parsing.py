"""Verify selected TimeSpan constant exact formats and direct CLR output reset."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--exact-parsing')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')),run_name='__main__')
