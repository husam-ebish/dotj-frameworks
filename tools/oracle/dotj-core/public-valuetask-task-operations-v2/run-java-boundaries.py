"""Current fixed-mode operational entrypoint; see SUPERSESSION.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import operations
if __name__ == "__main__":
    operations.main_boundaries()
