"""Root-only postcompile binding. No launch and no pre-created artifact hashes."""
import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('v3protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def main():
    a=p.parser('compile').parse_args();p.verify_execution(a.execution_lock_sha256);p.review(a.review_sha256,a.execution_lock_sha256)
    p.require(not p.BINDING.exists(),'artifact lock immutable once written')
    value=p.binding_value(a.execution_lock_sha256,a.review_sha256)
    # Exclusive creation; failed/absent/forged proof cannot produce a lock.
    import json
    with p.BINDING.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(value,indent=2)+'\n')
    print(p.sha(p.BINDING))
if __name__=='__main__':main()
