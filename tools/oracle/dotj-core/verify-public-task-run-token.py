"""Read-only final Run(Action,token) candidate verification."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
profile='public-task-wait-async-v1' if (ROOT/'planning/stage-2/repos/dotj-core/evidence/public-task-wait-async-v1.json').is_file() else 'public-task-run-token-v1'
sys.path.insert(0,str(Path(__file__).resolve().parent/profile))
from verify_candidate import main
if __name__=='__main__':main()
