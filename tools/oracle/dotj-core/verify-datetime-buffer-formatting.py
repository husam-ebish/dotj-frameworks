"""Verify selected DateTime character and UTF-8 buffers against direct CLR span delegates."""
import runpy
import sys
from pathlib import Path

sys.argv.append('--buffer-formatting')
runpy.run_path(str(Path(__file__).with_name('verify-datetime-comparison.py')),run_name='__main__')
