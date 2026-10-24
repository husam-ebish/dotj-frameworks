"""Verify DateTime tick constructors, zero initialization and canonical readonly values."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--tick-domain')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-comparison.py')),run_name='__main__')
