"""Read-only verification of the selected five-member delay candidate."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'public-task-delay-product-v1'))
from verify_product import main
if __name__=='__main__':main()
