"""Read-only comparison; no outcome category/value filtering."""
import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('v3protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def compare(r1,v1,r2,v2):
    p.require(r1['fixtureRoot']!=r2['fixtureRoot'] and r1['process']['processId']!=r2['process']['processId'],'distinct independent new processes')
    p.require(p.normalized(v1,r1['fixtureRoot'])==p.normalized(v2,r2['fixtureRoot']),'native pair differs; retain raw, no retry')
def main():
    a=p.parser('pair').parse_args()
    r1,v1=p.receipt(a.first,a.first_sha256,a.execution_lock_sha256,a.compiled_lock_sha256,a.review_sha256)
    r2,v2=p.receipt(a.second,a.second_sha256,a.execution_lock_sha256,a.compiled_lock_sha256,a.review_sha256)
    compare(r1,v1,r2,v2);print('VERIFIED_V3_PAIR_297_ROWS_NATIVE_SEMANTICS_PENDING_ROOT_CONTRACT')
if __name__=='__main__':main()
