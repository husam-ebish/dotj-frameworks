"""Dedicated root-owned source-compile launcher; actual launch requires reviewed approval."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import root_phase
if __name__ == "__main__":
    root_phase.run("source-compile")
