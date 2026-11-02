"""Read-only; cannot launch."""
import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('v3protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def main():
    a=p.parser('verify').parse_args();p.receipt(a.receipt,a.receipt_sha256,a.execution_lock_sha256,a.compiled_lock_sha256,a.review_sha256);print('VERIFIED_COMPLETE_V3_CAPTURE_PENDING_ROOT_CONTRACT')
if __name__=='__main__':main()
