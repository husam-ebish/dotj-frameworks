"""Verify selected DateTime binary carriers and native local overlap reconstruction."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--binary')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-dst.py')),run_name='__main__')
