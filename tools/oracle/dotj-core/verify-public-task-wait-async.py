"""Pure selected nongeneric default-clock WaitAsync candidate verification."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'public-task-wait-async-v1'))
from verify_candidate import main
if __name__=='__main__':main()
