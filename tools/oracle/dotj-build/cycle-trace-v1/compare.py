"""Independent frozen-native projection and authored trace expectations."""
import argparse
import json
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from corpus import read_contract,descriptor
from native_lock import normalize

def native_projection(row):
    diagnostics=[]
    for d in row['diagnostics']:
        quotes=re.findall(r'"([^"]*)"',d['message']);target=quotes[0]
        code=d['code'];context={'MSB4210':'ROOT','MSB4011':'PREVIOUS','MSB4019':'MISSING','MSB4020':'INVALID',None:'CIRCULAR'}[code]
        previous=None
        if context=='PREVIOUS':
            m=re.fullmatch(r'(.*) \((\d+),(\d+)\)',quotes[1]);assert m
            previous=dict(owner=m[1],line=int(m[2]),column=int(m[3]))
        diagnostics.append(dict(referenceCode=code,owner=d['file'],importedProject=target,
            current={k:d[k] for k in ('line','column','endLine','endColumn')},previous=previous,
            rootContext=target if context=='ROOT' else None,kind=d['kind'].upper(),contextKind=context))
    e=row['evaluation']
    def edges(values):
        return None if values is None else [dict(owner=v['owner'],target=v['project'],line=v['line'],column=v['column']) for v in values]
    if e['success']:
        assert (e['duplicateImports'] is None)==(e['duplicateGetterFailure'] is not None)
        evaluation=dict(success=True,properties=e['properties'],imports=edges(e['imports']),duplicateImports=edges(e['duplicateImports']))
    else:
        evaluation=dict(success=False,reason='MISSING_IMPORT' if e['code']=='MSB4019' else 'CIRCULAR_IMPORT',code=e['code'],
            file=e['file'],target=diagnostics[-1]['importedProject'],current={k:e[k] for k in ('line','column','endLine','endColumn')})
    return dict(evaluation=evaluation,diagnostics=diagnostics)

def compare(raw_path,fixture_root,platform,contract_path,native_path):
    raw=json.loads(Path(raw_path).read_text());contract=read_contract(contract_path)
    native=json.loads(Path(native_path).read_text());assert native['status']=='PASS_NATIVE_FULL_COORDINATE_TWO_PASS'
    expected_rows={(r['id'],r['profile']):r for r in native['rows'] if r['platform']==platform}
    actual=normalize(raw['rows'],str(fixture_root));assert len(actual)==57 and len({(r['id'],r['profile']) for r in actual})==57
    checks=[]
    for row in actual:
        key=row['id'],row['profile'];expected=native_projection(expected_rows[key]['observation']);observed=row['observation']
        assert {k:v for k,v in observed.items() if k!='traces'}==expected, (key,'native projection',observed,expected)
        case=next(c for c in contract['cases'] if c['id']==row['id']);sep='\\' if platform=='windows' else '/'
        prefix='<fixtures>'+sep+row['id']+sep
        def path(p):return prefix+p.replace('/',sep)
        traces=[]
        for trace in case['traces'][row['profile']]:
            traces.append(dict(nodes=[path(n) for n in trace['nodes']],
                edges=[dict(owner=path(e['owner']),target=path(e['target']),line=e['line'],column=e['column']) for e in trace['edges']],
                cycleStartIndex=trace['cycleStartIndex'],profile=row['profile'],diagnosticIndices=trace['diagnosticIndices']))
        assert observed['traces']==traces,(key,'trace',observed['traces'],traces)
        checks.append(dict(id=row['id'],profile=row['profile'],passed=True,traceCount=len(traces)))
    return dict(status='PASS',platform=platform,rows=checks,raw=descriptor(raw_path),contract=descriptor(contract_path),native=descriptor(native_path),fixtureRoot=str(fixture_root))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--raw',type=Path,required=True);p.add_argument('--fixture-root',required=True)
    p.add_argument('--platform',choices=['windows','linux'],required=True);p.add_argument('--contract',type=Path,required=True)
    p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    value=compare(a.raw,a.fixture_root,a.platform,a.contract,a.native);assert not a.output.exists()
    a.output.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(status='PASS',rows=57,**descriptor(a.output))))
