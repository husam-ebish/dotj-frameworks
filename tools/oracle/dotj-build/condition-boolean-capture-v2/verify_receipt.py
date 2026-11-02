"""Read-only recovery receipt verification. No execution selectors."""
import importlib.util
from pathlib import Path
s = importlib.util.spec_from_file_location('recovery_protocol', Path(__file__).with_name('protocol.py'))
p = importlib.util.module_from_spec(s)
s.loader.exec_module(p)
def main():
    a = p.verify_parser().parse_args()
    _, value = p.receipt(a.receipt, a.receipt_sha256, a.original_lock_sha256, a.execution_lock_sha256)
    print('VERIFIED_RECOVERY_RECEIPT rows=' + str(len(value['rows'])))
if __name__ == '__main__':
    main()
