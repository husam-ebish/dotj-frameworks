"""Verify invariant TimeSpan general formats through String and buffer carriers."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--general-timespan')
runpy.run_path(str(Path(__file__).with_name('verify-temporal-span-formatting.py')),run_name='__main__')
