"""Check custom exact TimeSpan parsing against pinned None-style span reference results."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--custom-timespan')
runpy.run_path(str(Path(__file__).with_name('verify-temporal-span-exact-parsing.py')),run_name='__main__')
