"""Validate and transport bounded Default import-path observations without guessing errors."""
import argparse,base64,copy,hashlib,json
from pathlib import Path
ROOT=Path(r'D:\AI\Implementation\dotj Frameworks')
REPO=Path(__file__).resolve().parents[3]
BASE=REPO/'dotj-build/evaluation-candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def same_json(left,right):
    # Python otherwise equates True with 1 and False with 0 in nested containers.
    return json.dumps(left,sort_keys=True,separators=(',',':'))==json.dumps(right,sort_keys=True,separators=(',',':'))
def plan():return json.loads((BASE/'evidence/import-path-plan-v1.json').read_text())
def normalize(raw,root):
    result=copy.deepcopy(raw);prefix=str(root)+'\\'
    def path(s):
        if not isinstance(s,str) or not s.startswith(prefix):raise ValueError('Foreign native fixture path')
        return '<fixtures>\\'+s[len(prefix):]
    for row in result['rows']:
        ev=row['evaluation']
        for obj in row['diagnostics']+([] if ev['success'] else [ev]):
            obj['file']=path(obj['file'])
            obj['message']=obj['message'].replace(prefix,'<fixtures>\\')
        for key in ['imports','duplicateImports']:
            for edge in ev.get(key) or []:
                edge['owner']=path(edge['owner']);edge['project']=path(edge['project'])
    return result
def validate(capture):
    p=plan()
    if capture['profile']!='Default' or capture['runtime']!='.NET 10.0.12':raise ValueError('Unqualified native profile/runtime')
    if [r['id'] for r in capture['rows']] != [c['id'] for c in p['cases']]:raise ValueError('Case order/inventory')
    for row,case in zip(capture['rows'],p['cases']):
        if row['profile']!='Default' or row['globals']!=case['globals']:raise ValueError('Global/profile drift')
        if type(row['taskMarkerAbsent']) is not bool or not row['taskMarkerAbsent']:raise ValueError('Task marker')
        clean=row['cleanup']
        if type(clean['before']) is not int or clean['before']!=0 or type(clean['loaded']) is not int or clean['loaded']<0 or type(clean['afterUnload']) is not int or clean['afterUnload']!=0 or clean['disposed'] is not True:raise ValueError('Cleanup')
        ev=row['evaluation']
        if type(ev['success']) is not bool:raise ValueError('Success type')
        if ev['success']:
            if set(ev)!={'success','properties','imports','duplicateImports','duplicateGetterFailure'} or set(ev['properties'])!={'P','Q'} or any(type(v) is not str for v in ev['properties'].values()):raise ValueError('Success fields')
            if ev['duplicateImports'] is not None or set(ev['duplicateGetterFailure'])!={'type','message'} or ev['duplicateGetterFailure']['type']!='System.InvalidOperationException':raise ValueError('Getter availability')
            for edge in ev['imports']:
                if set(edge)!={'owner','project','line','column'}:raise ValueError('Edge fields')
                for k in ['owner','project']:relative(edge[k],row['id'])
                for k in ['line','column']:
                    if type(edge[k]) is not int or edge[k]<1:raise ValueError('Edge coordinate')
        elif set(ev)!={'success','type','code','file','line','column','endLine','endColumn','message','hresult'} or ev['type']!='Microsoft.Build.Exceptions.InvalidProjectFileException' or type(ev['hresult']) is not int:raise ValueError('Failure envelope')
        for obj in row['diagnostics']+([] if ev['success'] else [ev]):
            if 'code' not in obj or (obj['code'] is not None and type(obj['code']) is not str):raise ValueError('Nullable code key')
            relative(obj['file'],row['id'])
            if type(obj['message']) is not str:raise ValueError('Message')
            for k in ['line','column','endLine','endColumn']:
                if type(obj[k]) is not int or obj[k]<(1 if k in ['line','column'] else 0):raise ValueError('Coordinate')
    return capture
def relative(s,ident):
    prefix='<fixtures>\\'+ident+'\\'
    if not isinstance(s,str) or not s.startswith(prefix):raise ValueError('Foreign native path')
    tail=s[len(prefix):].replace('\\','/')
    if not tail or any(x in ['','..','.'] for x in tail.split('/')):raise ValueError('Unbounded path')
    return tail
def bridge(capture):
    validate(capture);lines=[];enc=lambda s:base64.b64encode(s.encode()).decode()
    for row in capture['rows']:
        ident=row['id'];ev=row['evaluation']
        lines.append('\t'.join(['CASE','Default',ident,str(ev['success']).lower(),enc(ev.get('properties',{}).get('P','')),enc(ev.get('properties',{}).get('Q',''))]))
        for k,v in row['globals'].items():lines.append('\t'.join(['GLOBAL',enc(k),enc(v)]))
        if ev['success']:
            lines.append('AVAIL\tfalse')
            for edge in ev['imports']:lines.append('\t'.join(map(str,['UNIQUE',relative(edge['owner'],ident),relative(edge['project'],ident),edge['line'],edge['column']])))
        for d in row['diagnostics']:
            if d['code']=='MSB4011':
                target=d['message'].split('"',2)[1];previous=next(e for e in ev['imports'] if e['project']==target)
                context='PREVIOUS'
            elif d['code']=='MSB4019':target=d['message'].split('"',2)[1];previous=None;context='MISSING'
            else:target=None;previous=None;context='INVALID'
            lines.append('\t'.join(map(str,['NOTICE',d['kind'],'NULL' if d['code'] is None else d['code'],relative(d['file'],ident),relative(target,ident) if target else '-',d['line'],d['column'],d['endLine'],d['endColumn'],context,relative(previous['owner'],ident) if previous else '-',previous['line'] if previous else '-',previous['column'] if previous else '-'])))
        if not ev['success']:
            missing=ev['code']=='MSB4019';target=row['diagnostics'][-1]['message'].split('"',2)[1] if missing else None
            lines.append('\t'.join(map(str,['FAILURE','MISSING_IMPORT' if missing else 'INVALID_IMPORT_EXPRESSION','NULL' if ev['code'] is None else ev['code'],relative(ev['file'],ident),relative(target,ident) if target else '-',ev['line'],ev['column'],ev['endLine'],ev['endColumn']])))
        lines.append('END')
    return '\n'.join(lines)+'\n'
def verify_lock(name):
    lock=json.loads((BASE/'evidence'/name).read_text())
    for item in lock['inputs']:
        anchor=ROOT if item['base']=='root' else REPO;p=(anchor/item['path']).resolve(strict=True)
        if not p.is_relative_to(anchor) or sha(p)!=item['sha256']:raise RuntimeError('Import-path integrity drift: '+item['path'])
def verify_plan_inputs():
    verify_lock('import-path-input-lock-v1.json')
    p=plan();root=BASE/'import-path-fixtures'
    if {x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file()}!={x['path'] for x in p['fixtures']}:raise ValueError('Fixture inventory')
    for x in p['fixtures']:
        if sha(root/x['path'])!=x['sha256'] or (root/x['path']).stat().st_size!=x['bytes']:raise ValueError('Fixture bytes')
def validate_raw(raw):
    if raw['status']!='PASS_NATIVE_IMPORT_PATH_OBSERVATIONS' or len(raw['captures'])!=2:raise ValueError('Native status/pass count')
    if raw['fixturesUnchanged'] is not True or raw['taskMarkersAbsent'] is not True:raise ValueError('Native fixture/marker status')
    if [c['label'] for c in raw['commands']]!=['compile-probe','Default-pass-1','Default-pass-2']:raise ValueError('Native command order')
    fixture_roots=[]
    for command in raw['commands'][1:]:
        fixture_root=Path(command['argv'][-2]).resolve(strict=True);manifest=Path(command['argv'][-1]).resolve(strict=True)
        if not fixture_root.is_relative_to(ROOT) or not manifest.is_relative_to(ROOT) or sha(manifest)!=sha(BASE/'evidence/import-path-plan-v1.json'):raise ValueError('Native fixture manifest drift')
        p=plan()
        if {x.relative_to(fixture_root).as_posix() for x in fixture_root.rglob('*') if x.is_file()}!={x['path'] for x in p['fixtures']}:raise ValueError('Native fixture inventory drift')
        for item in p['fixtures']:
            copied=fixture_root/item['path']
            if sha(copied)!=item['sha256'] or copied.stat().st_size!=item['bytes']:raise ValueError('Native copied fixture bytes drift')
        fixture_roots.append(fixture_root)
    if fixture_roots[0]!=fixture_roots[1]:raise ValueError('Native fixture roots differ')
    for command in raw['commands']:
        if type(command['exitCode']) is not int or command['exitCode']!=0:raise ValueError('Native command failed')
        for k in ['stdout','stderr','hostTrace']:
            path=Path(command[k]['path']).resolve(strict=True)
            if not path.is_relative_to(ROOT) or sha(path)!=command[k]['sha256']:raise ValueError('Raw log drift')
        if Path(command['stderr']['path']).read_bytes():raise ValueError('Native stderr present')
    # The report repeats the stdout data for convenience. It is never an independent oracle.
    for capture,command in zip(raw['captures'],raw['commands'][1:]):
        exact=json.loads(Path(command['stdout']['path']).read_bytes())
        if not same_json(capture,exact):raise ValueError('Embedded native capture differs from exact retained stdout')
    return raw
def verify_inputs():
    verify_plan_inputs();verify_lock('import-path-observation-lock-v1.json')
    data=json.loads((BASE/'evidence/import-path-observations-v1.json').read_text())
    raw=validate_raw(json.loads(Path(data['raw']['path']).read_text()))
    exact=[normalize(c,Path(data['raw']['path']).parent/'fixtures') for c in raw['captures']]
    if not same_json(data['captures'],exact):raise ValueError('Versioned observations differ from exact native stdout')
    if data['captures'][0]!=data['captures'][1]:raise ValueError('Native reproducibility')
    if bridge(data['captures'][0])!=(BASE/'evidence/import-path-comparison-v1.tsv').read_text():raise ValueError('Bridge drift')
    return data
def main():
    parser=argparse.ArgumentParser();parser.add_argument('native',type=Path);parser.add_argument('--out',required=True,type=Path);args=parser.parse_args()
    if args.out.exists() or not args.out.resolve().is_relative_to(ROOT) or args.out.resolve()==ROOT:raise RuntimeError('New private D output')
    verify_plan_inputs();raw=validate_raw(json.loads(args.native.read_text()))
    captures=[normalize(c,args.native.parent/'fixtures') for c in raw['captures']]
    if captures[0]!=captures[1]:raise ValueError('Fresh passes differ')
    text=bridge(captures[0]);args.out.mkdir(parents=True)
    (args.out/'import-path-comparison-v1.tsv').write_bytes(text.encode())
    data={'schemaVersion':1,'status':'PASS_NATIVE_IMPORT_PATH_COMPARISON','raw':{'path':str(args.native),'sha256':sha(args.native)},'normalization':'Exact fixture-root prefix only in path/message fields','captures':captures}
    (args.out/'import-path-observations-v1.json').write_bytes((json.dumps(data,indent=2)+'\n').encode())
    print('PASS eight Default cases; two fresh identical native passes')
if __name__=='__main__':main()
