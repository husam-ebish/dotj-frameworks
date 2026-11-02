"""Verify-only pair comparison. Preserves raw captures; normalizes fixture roots only."""
import argparse, copy, importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('boolean_v1_protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def normalized(value,root):
    value=copy.deepcopy(value)
    def replace(text):return text.replace(root,'<fixture-root>') if type(text) is str else text
    for row in value['rows']:
        ev=row['evaluation']
        if ev['success']:
            for edge in ev['imports']+(ev['duplicateImports'] or []):
                for k in ['owner','project']:edge[k]=replace(edge[k])
            if ev['duplicateGetterFailure'] is not None:ev['duplicateGetterFailure']['message']=replace(ev['duplicateGetterFailure']['message'])
        else:
            for k in ['file','message']:ev[k]=replace(ev[k])
        for event in row['diagnostics']:
            for k in ['file','message']:event[k]=replace(event[k])
    return value
def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    for name in ['first','second']:parser.add_argument('--'+name,type=Path,required=True);parser.add_argument('--'+name+'-sha256',required=True)
    parser.add_argument('--lock-sha256',required=True);a=parser.parse_args()
    r1,v1=p.receipt(a.first,a.first_sha256,a.lock_sha256);r2,v2=p.receipt(a.second,a.second_sha256,a.lock_sha256)
    p.require(a.first.resolve()!=a.second.resolve() and r1['process']['processId']!=r2['process']['processId'],'two distinct retained native runs')
    p.require(normalized(v1,r1['fixtureRoot'])==normalized(v2,r2['fixtureRoot']),'native outcomes differ; preserve failure, no retry')
    # Host trace contains different owned output/temp/home paths and OS metadata. It is
    # retained and hash-bound independently, NOT normalized into semantic observations.
    print('VERIFIED_NATIVE_BOOLEAN_PAIR rows='+str(len(v1['rows']))+' nativeExecutions=2')
if __name__=='__main__':main()
