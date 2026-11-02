"""Typed exact placeholder rendering. Never launches or rewrites proposals."""
import argparse, importlib.util, json
from pathlib import Path
s=importlib.util.spec_from_file_location('v3protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def render(value,bindings):
    if type(value) is list:return [render(x,bindings) for x in value]
    if type(value) is dict:return {k:render(v,bindings) for k,v in value.items()}
    if type(value) is str:
        for k,v in bindings.items():value=value.replace('{'+k+'}',p.digest(v))
    return value
def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--execution-lock-sha256',required=True);parser.add_argument('--review-sha256',required=True)
    parser.add_argument('--compiled-lock-sha256');a=parser.parse_args();p.verify_execution(a.execution_lock_sha256)
    bindings={'executionLockSha256':a.execution_lock_sha256,'reviewSha256':a.review_sha256}
    if a.compiled_lock_sha256 is not None:bindings['compiledLockSha256']=a.compiled_lock_sha256
    print(json.dumps(render(p.read(p.HERE/'native-proposal.json'),bindings),indent=2))
if __name__=='__main__':main()
