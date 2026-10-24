"""Verify TimeSpan public field types, values, modifiers and zero construction."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--constants')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
