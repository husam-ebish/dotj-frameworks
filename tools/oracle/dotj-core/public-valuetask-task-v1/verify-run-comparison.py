"""Verify-only retained receipt consumer; never captures or launches children."""
import importlib.util,sys
from pathlib import Path
FIXED=Path('D:/AI/Implementation/dotj Frameworks/worktrees/dotj-core-valuetask-task-v1/tools/oracle/dotj-core/public-valuetask-task-v1')
if Path(__file__).resolve().parent!=FIXED.resolve():raise ValueError('entrypoint path changed')
sys.path.insert(0,str(FIXED))
spec=importlib.util.spec_from_file_location('batch2515_verify',FIXED/'run-comparison.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if __name__=='__main__':
    if '--mode' in sys.argv:raise ValueError('mode fixed to verify-only')
    sys.argv[1:1]=['--mode','verify'];m.main()
