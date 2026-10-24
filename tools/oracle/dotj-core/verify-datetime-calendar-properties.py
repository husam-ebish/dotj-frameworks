"""Verify selected DateTime calendar properties and weekday/Kind enum projection."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--calendar-properties')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-comparison.py')),run_name='__main__')
