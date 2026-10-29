"""Compare retained native runs without discarding ordered diagnostic/failure/cleanup fields."""
import argparse
import base64
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(captures, fixture_root):
    def walk(value,key=''):
        if isinstance(value,dict):return {k:walk(v,k) for k,v in value.items()}
        if isinstance(value,list):return [walk(v,key) for v in value]
        if isinstance(value,str) and key in {'owner','project','file','message'}:
            return value.replace(str(fixture_root),'<fixtures>')
        return value
    return walk(captures)


def comparison_bridge(captures):
    defaults = captures[0]['rows']
    recorded = captures[1]['rows']
    encode = lambda value: base64.b64encode(value.encode('utf-8')).decode('ascii')
    rows = []
    for default, record in zip(defaults, recorded, strict=True):
        fixture = default['id']
        if record['id'] != fixture: raise RuntimeError('Native case order differs')
        evaluation = default['evaluation']
        prefix = '<fixtures>\\'+fixture+'\\'
        def relative(value):
            if not value.startswith(prefix):raise RuntimeError('Unexpected native fixture path')
            return value.removeprefix(prefix).replace('\\','/')
        disposition = 'CYCLE_REFUSAL' if fixture in {'BI03-two-file-cycle','BI07-prior-cycle','BI08-nonroot-cycle'} else 'MISSING' if fixture=='BI09-missing' else 'SUPPORTED'
        seen = set()
        duplicates = []
        for imported in record['evaluation'].get('duplicateImports') or []:
            if imported['project'] in seen: duplicates.append((relative(imported['owner']),relative(imported['project'])))
            seen.add(imported['project'])
        if disposition == 'SUPPORTED':
            if evaluation['properties'] != record['evaluation']['properties'] or evaluation['imports'] != record['evaluation']['imports']:
                raise RuntimeError('Default/recording property/import observations differ')
            if len(duplicates) != len(default['diagnostics']): raise RuntimeError('Native warning count differs')
            for duplicate, diagnostic in zip(duplicates,default['diagnostics'],strict=True):
                if diagnostic['code'] != 'MSB4011' or relative(diagnostic['file']) != duplicate[0]:
                    raise RuntimeError('Native warning identity differs')
        properties = evaluation.get('properties',{})
        files = '\n'.join(['main.proj']+[relative(i['project']) for i in evaluation.get('imports',[])])
        notices = '\n'.join('MSB4011|'+owner+'|'+target for owner,target in duplicates)
        rows.append('\t'.join([fixture, disposition, encode(properties.get('P','')),encode(properties.get('Q','')),encode(files),encode(notices),evaluation.get('code') or '']))
    return '\n'.join(rows)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('first',type=Path)
    parser.add_argument('second',type=Path)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--bridge',type=Path)
    args=parser.parse_args()
    root=Path(r'D:\AI\Implementation\dotj Frameworks')
    if args.out.exists() or not args.out.resolve().is_relative_to(root):raise RuntimeError('New D: output required')
    results=[]
    for path in [args.first,args.second]:
        data=json.loads(path.read_text())
        if data['status']!='PASS_NATIVE_IMPORT_OBSERVATIONS':raise RuntimeError('Native capture not passing')
        for c in data['commands']:
            for k in ['stdout','stderr','hostTrace']:
                if sha(Path(c[k]['path']))!=c[k]['sha256']:raise RuntimeError('Retained log drift')
        results.append(normalized(data['captures'],path.parent/'fixtures'))
    if results[0]!=results[1]:raise RuntimeError('Normalized observations differ')
    if args.bridge and args.bridge.read_text(encoding='utf-8') != comparison_bridge(results[0]):
        raise RuntimeError('Candidate comparison bridge differs from captured native observations')
    args.out.write_text(json.dumps({'status':'PASS_TWO_NATIVE_IMPORT_RUNS','normalization':'Exact fixture-root prefix only in owner/project/file/message fields; properties, diagnostics order/codes/locations, failures and cleanup unchanged',
        'inputs':[{'path':str(p),'sha256':sha(p)} for p in [args.first,args.second]],'observationsPerRun':27,'captures':results[0]},indent=2)+'\n')
    print('PASS 27 ordered observations identical across two pinned native runs')


if __name__=='__main__':main()
