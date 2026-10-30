"""Bridge new same-profile coordinates while preserving every original native field."""
import argparse,base64,copy,hashlib,json,runpy
from pathlib import Path
ROOT=Path(r'D:\AI\Implementation\dotj Frameworks')
REPO=Path(__file__).resolve().parents[3]
BASE=REPO/'dotj-build/evaluation-candidate'
PROFILES=['RecordDuplicateButNotCircularImports','RejectCircularImports']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def validate(captures):
    old=json.loads((BASE/'evidence/native-import-observations-v1.json').read_text())['captures'][1:]
    if [c['profile'] for c in captures]!=PROFILES:raise ValueError('Only individual selected profiles observed')
    prior=copy.deepcopy(captures)
    for capture in prior:
        for row in capture['rows']:
            for obj in row['diagnostics']+([] if row['evaluation']['success'] else [row['evaluation']]):
                for key in ['line','column','endLine','endColumn']:
                    if type(obj[key]) is not int or obj[key] < (1 if key in ['line','column'] else 0):raise ValueError('Malformed native coordinate')
                obj.pop('endLine');obj.pop('endColumn')
    if prior!=old:raise ValueError('Prior same-profile observations changed beyond new end coordinates')
def bridge(captures):
    validate(captures)
    lines=[]
    encode=lambda s:base64.b64encode(s.encode()).decode()
    for capture in captures:
        for row in capture['rows']:
            ident=row['id'];ev=row['evaluation'];prefix='<fixtures>\\'+ident+'\\'
            def relative(s):
                if not s.startswith(prefix):raise ValueError('Foreign native path')
                return s[len(prefix):].replace('\\','/')
            lines.append('\t'.join(['CASE',capture['profile'],ident,str(ev['success']).lower(),encode(ev.get('properties',{}).get('P','')),encode(ev.get('properties',{}).get('Q',''))]))
            if ev['success']:
                lines.append('AVAIL\t'+str(ev['duplicateImports'] is not None).lower())
                for kind,key in [('UNIQUE','imports'),('RECORDED','duplicateImports')]:
                    for edge in ev[key] or []:lines.append('\t'.join(map(str,[kind,relative(edge['owner']),relative(edge['project']),edge['line'],edge['column']])))
            for d in row['diagnostics']:
                code=d['code'];target=d['message'].split('"',2)[1]
                context='ROOT' if code=='MSB4210' else 'PREVIOUS' if code=='MSB4011' else 'CIRCULAR' if code is None else 'MISSING'
                previous=next((i for i in ev.get('imports',[]) if i['project']==target),None) if context=='PREVIOUS' else None
                lines.append('\t'.join(map(str,['NOTICE',d['kind'],'NULL' if code is None else code,relative(d['file']),relative(target),d['line'],d['column'],d['endLine'],d['endColumn'],context,relative(previous['owner']) if previous else '-',previous['line'] if previous else '-',previous['column'] if previous else '-'])))
            if not ev['success']:lines.append('\t'.join(map(str,['FAILURE','CIRCULAR_IMPORT' if ev['code'] is None else 'MISSING_IMPORT','NULL' if ev['code'] is None else ev['code'],relative(ev['file']), relative(row['diagnostics'][-1]['message'].split('"',2)[1]),ev['line'],ev['column'],ev['endLine'],ev['endColumn']])))
            lines.append('END')
    return '\n'.join(lines)+'\n'
def verify_inputs():
    lock=json.loads((BASE/'evidence/profile-observation-lock-v1.json').read_text())
    for item in lock['inputs']:
        anchor=ROOT if item['base']=='root' else REPO;p=(anchor/item['path']).resolve(strict=True)
        if not p.is_relative_to(anchor) or sha(p)!=item['sha256']:raise RuntimeError('Profile evidence drift: '+item['path'])
    data=json.loads((BASE/'evidence/profile-observations-v1.json').read_text())
    if bridge(data['captures'])!=(BASE/'evidence/profile-comparison-v1.tsv').read_text():raise RuntimeError('Profile bridge drift')
    return data
def verify_plan_inputs():
    lock=json.loads((BASE/'evidence/profile-input-lock-v1.json').read_text())
    for item in lock['inputs']:
        anchor=ROOT if item['base']=='root' else REPO
        path=(anchor/item['path']).resolve(strict=True)
        if not path.is_relative_to(anchor) or sha(path)!=item['sha256']:raise RuntimeError('Profile input drift: '+item['path'])
    old=json.loads((BASE/'evidence/native-import-observations-v1.json').read_text())
    normalize=runpy.run_path(str(Path(__file__).with_name('verify-imports.py')))['normalized']
    for source in old['inputs']:
        path=Path(source['path'])
        if sha(path)!=source['sha256']:raise RuntimeError('Original native report drift')
        raw=json.loads(path.read_text())
        if normalize(raw['captures'],path.parent/'fixtures')!=old['captures']:raise RuntimeError('Original native rows drift')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('native',type=Path);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    if args.out.exists() or not args.out.resolve().is_relative_to(ROOT) or args.out.resolve()==ROOT:raise RuntimeError('New private D: output required')
    verify_plan_inputs()
    raw=json.loads(args.native.read_text())
    if raw['status']!='PASS_NATIVE_PROFILE_OBSERVATIONS':raise RuntimeError('Native capture not passing')
    for c in raw['commands']:
        for k in ['stdout','stderr','hostTrace']:
            if sha(Path(c[k]['path']))!=c[k]['sha256']:raise RuntimeError('Native log drift')
    normalize=runpy.run_path(str(Path(__file__).with_name('verify-imports.py')))['normalized']
    captures=normalize(raw['captures'],args.native.parent/'fixtures');text=bridge(captures)
    args.out.mkdir(parents=True)
    (args.out/'profile-comparison-v1.tsv').write_text(text,encoding='utf-8')
    (args.out/'profile-observations-v1.json').write_text(json.dumps({'schemaVersion':1,'status':'PASS_NATIVE_PROFILE_COMPARISON','raw':{'path':str(args.native),'sha256':sha(args.native)},'normalization':'Exact copied fixture-root prefix only in path/message fields; all prior fields preserved','priorSameProfileRowsPreserved':18,'captures':captures},indent=2)+'\n')
    print('PASS 18 same-profile native rows preserved; new ends transported')
if __name__=='__main__':main()
