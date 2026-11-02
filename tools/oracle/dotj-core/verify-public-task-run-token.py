"""Read-only final Run(Action,token) candidate verification."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'public-task-run-token-v1'))
from verify_candidate import main
if __name__=='__main__':main()
