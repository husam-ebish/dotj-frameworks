"""Explicit entrypoint for the eight separate Java-only controls."""
import importlib.util,sys
from pathlib import Path
FIXED=Path('D:/AI/Implementation/dotj Frameworks/worktrees/dotj-core-valuetask-task-v1/tools/oracle/dotj-core/public-valuetask-task-v1')
if Path(__file__).resolve().parent!=FIXED.resolve():raise ValueError('entrypoint path changed')
sys.path.insert(0,str(FIXED))
spec=importlib.util.spec_from_file_location('batch2515_comparison',FIXED/'run-comparison.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if __name__=='__main__':
    if '--mode' in sys.argv:raise ValueError('mode fixed to Java boundaries')
    sys.argv[1:1]=['--mode','boundaries'];m.main()
