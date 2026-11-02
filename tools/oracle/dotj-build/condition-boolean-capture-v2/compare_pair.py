"""Read-only comparison of precisely the two designated recovery outputs."""
import importlib.util
from pathlib import Path
s = importlib.util.spec_from_file_location('recovery_protocol', Path(__file__).with_name('protocol.py'))
p = importlib.util.module_from_spec(s)
s.loader.exec_module(p)
def main():
    a = p.verify_parser(pair=True).parse_args()
    p.require(a.first.resolve() == p.A2 / 'native-pass1/receipt.json'
              and a.second.resolve() == p.A2 / 'native-pass2/receipt.json', 'ordered designated pair')
    r1, v1 = p.receipt(a.first, a.first_sha256, a.original_lock_sha256, a.execution_lock_sha256)
    r2, v2 = p.receipt(a.second, a.second_sha256, a.original_lock_sha256, a.execution_lock_sha256)
    p.compare_values(r1, v1, r2, v2)
    print('VERIFIED_RECOVERY_PAIR rows=' + str(len(v1['rows'])) + ' newNativeExecutions=2 lifetimeNativeAttempts=3')
if __name__ == '__main__':
    main()
