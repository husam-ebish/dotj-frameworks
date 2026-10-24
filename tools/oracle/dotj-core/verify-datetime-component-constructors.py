"""Verify Gregorian DateTime components, Kind, microseconds and exception validation order."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--component-constructors')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-comparison.py')),run_name='__main__')
