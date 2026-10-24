"""Verify exact TimeSpan Int32/Int64 single-unit factory overloads."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--integer-factories')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
