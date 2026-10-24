"""Check invariant g/G exact TimeSpan parsing against the pinned reference."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--general-timespan')
runpy.run_path(str(Path(__file__).with_name('verify-temporal-span-exact-parsing.py')),run_name='__main__')
