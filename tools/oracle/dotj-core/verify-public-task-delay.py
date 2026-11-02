"""Read-only verification of the selected five-member delay candidate."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
if (ROOT/'planning/stage-2/repos/dotj-core/evidence/public-task-wait-async-v1.json').is_file():
    sys.path.insert(0,str(Path(__file__).resolve().parent/'public-task-wait-async-v1'))
    from verify_candidate import main
elif (ROOT/'planning/stage-2/repos/dotj-core/evidence/public-task-run-token-v1.json').is_file():
    sys.path.insert(0,str(Path(__file__).resolve().parent/'public-task-run-token-v1'))
    from verify_candidate import main
else:
    sys.path.insert(0,str(Path(__file__).resolve().parent/'public-task-delay-product-v1'))
    from verify_product import main
if __name__=='__main__':main()
