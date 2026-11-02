"""Verify-only fixed entrypoint. No execution flags, selectors, or child launch."""
import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('boolean_v1_protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def main():
    a=p.verify_parser().parse_args();r,v=p.receipt(a.receipt,a.receipt_sha256,a.lock_sha256)
    print('VERIFIED_NATIVE_BOOLEAN_RECEIPT rows='+str(len(v['rows'])))
if __name__=='__main__':main()
