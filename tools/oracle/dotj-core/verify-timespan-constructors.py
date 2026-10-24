"""Run the shared differential harness for TimeSpan component constructors."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--constructors')
runpy.run_path(str(Path(__file__).with_name('verify-timespan-intervals.py')), run_name='__main__')
