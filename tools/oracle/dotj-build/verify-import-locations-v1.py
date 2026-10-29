"""Derive bounded coordinate comparisons from Default-profile native fields only."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import runpy

ROOT=Path(r'D:\AI\Implementation\dotj Frameworks')
REPO=Path(__file__).resolve().parents[3]
BASE=REPO/'dotj-build/evaluation-candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
CYCLES={'BI03-two-file-cycle','BI07-prior-cycle','BI08-nonroot-cycle'}

def coordinate(value, positive=False):
    if type(value) is not int or value < (1 if positive else 0):
        raise ValueError('Malformed native coordinate')
    return value

def bridge(capture):
    if capture['profile']!='Default':raise ValueError('Locations require same Default profile')
    lines=[]
    for row in capture['rows']:
        if row['id'] in CYCLES or not row['evaluation']['success']:continue
        prefix='<fixtures>\\'+row['id']+'\\'
        def relative(path):
            if not isinstance(path,str) or not path.startswith(prefix):raise ValueError('Unexpected native owner/target')
            return path[len(prefix):].replace('\\','/')
        imports={}
        for imported in row['evaluation']['imports']:
            if imported['project'] in imports:raise ValueError('Default import list is not unique')
            coordinate(imported['line'],True);coordinate(imported['column'],True)
            imports[imported['project']]=imported
        lines.append('CASE\t'+row['id']+'\t'+str(len(row['diagnostics'])))
        for warning in row['diagnostics']:
            if warning['kind']!='warning' or warning['code']!='MSB4011':raise ValueError('Unexpected acyclic diagnostic')
            # Target is quoted in the retained English warning. Previous context is taken
            # from public Imports metadata in this SAME Default load, never from Java or
            # a recording-profile substitution. The native message provides a cross-check.
            message=warning['message']
            if not message.startswith('"'):raise ValueError('Unrecognized native target context')
            target=message.split('"',2)[1]
            previous=imports[target]
            context='"'+previous['owner']+' ('+str(previous['line'])+','+str(previous['column'])+')"'
            if 'It was already imported at '+context not in message:raise ValueError('Native previous context mismatch')
            values=[coordinate(warning[k],k in {'line','column'}) for k in ['line','column','endLine','endColumn']]
            lines.append('\t'.join(map(str,['NOTICE',row['id'],warning['code'],relative(warning['file']),relative(target),*values,relative(previous['owner']),previous['line'],previous['column']])))
    return '\n'.join(lines)+'\n'

def controls(capture):
    results=[]
    for name,mutation in [
        ('negative-current-line',lambda w:w.update(line=-1)),
        ('string-current-column',lambda w:w.update(column='2')),
        ('missing-end-coordinate',lambda w:w.pop('endColumn')),
        ('mismatched-previous-context',lambda w:w.update(message=w['message'].replace('It was already imported at','MISMATCH'))),
    ]:
        bad=copy.deepcopy(capture)
        warning=next(r['diagnostics'][0] for r in bad['rows'] if r['id']=='BI01-repeat')
        mutation(warning)
        try:bridge(bad)
        except (ValueError,KeyError):results.append({'control':name,'disposition':'REFUSED'})
        else:raise RuntimeError('Malformed coordinate evidence accepted: '+name)
    bad=copy.deepcopy(capture)
    first=next(r for r in bad['rows'] if r['id']=='BI01-repeat')['evaluation']['imports'][0]
    first['column']+=1
    try:bridge(bad)
    except ValueError:results.append({'control':'mismatched-same-profile-previous-coordinate','disposition':'REFUSED'})
    else:raise RuntimeError('Mismatched previous coordinate accepted')
    text=bridge(capture)
    wrong=text.replace('\t1\t154\t0\t0\t','\t1\t155\t0\t0\t',1)
    if wrong==text:raise RuntimeError('Coordinate control did not alter evidence')
    try:require_bridge(wrong,capture)
    except ValueError:results.append({'control':'mismatched-current-coordinate-bridge','disposition':'REFUSED'})
    else:raise RuntimeError('Mismatched current coordinate accepted')
    return results

def require_bridge(text,capture):
    if text!=bridge(capture):raise ValueError('Location bridge mismatch')

def verify_inputs():
    lock=BASE/'evidence/location-observation-lock-v1.json'
    data=json.loads(lock.read_text())
    for item in data['inputs']:
        anchor=ROOT if item['base']=='root' else REPO
        path=(anchor/item['path']).resolve(strict=True)
        if not path.is_relative_to(anchor) or sha(path)!=item['sha256']:raise RuntimeError('Location observation integrity mismatch: '+item['path'])
    observations=json.loads((BASE/'evidence/location-observations-v1.json').read_text())
    require_bridge((BASE/'evidence/location-comparison-v1.tsv').read_text(),observations['capture'])
    return observations

def main():
    p=argparse.ArgumentParser();p.add_argument('native',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists() or not a.out.resolve().is_relative_to(ROOT):raise RuntimeError('New private D: output required')
    raw=json.loads(a.native.read_text())
    if raw['status']!='PASS_NATIVE_LOCATION_OBSERVATIONS':raise RuntimeError('Native capture not passing')
    for command in raw['commands']:
        for key in ['stdout','stderr','hostTrace']:
            if sha(Path(command[key]['path']))!=command[key]['sha256']:raise RuntimeError('Native log drift')
    normalize=runpy.run_path(str(Path(__file__).with_name('verify-imports.py')))['normalized']
    capture=normalize(raw['captures'],a.native.parent/'fixtures')[0]
    old=json.loads((BASE/'evidence/native-import-observations-v1.json').read_text())['captures'][0]
    predecessor=copy.deepcopy(capture);predecessor['rows']=predecessor['rows'][:9]
    for row in predecessor['rows']:
        for warning in row['diagnostics']:
            warning.pop('endLine');warning.pop('endColumn')
        if not row['evaluation']['success']:
            row['evaluation'].pop('endLine');row['evaluation'].pop('endColumn')
    if predecessor!=old:raise RuntimeError('Prior Default observations changed beyond newly captured end fields')
    controls_result=controls(capture)
    text=bridge(capture)
    a.out.mkdir(parents=True)
    (a.out/'location-comparison-v1.tsv').write_text(text,encoding='utf-8')
    (a.out/'location-observations-v1.json').write_text(json.dumps({'schemaVersion':1,'status':'PASS_NATIVE_LOCATION_COMPARISON','raw':{'path':str(a.native),'sha256':sha(a.native)},'normalization':'Exact fixture-root prefix in owner/project/file/message only; all codes/coordinates/nulls/messages/failures/cleanup preserved','priorDefaultRowsPreserved':9,'controls':controls_result,'capture':capture},indent=2)+'\n')
    print('PASS native Default source locations; six malformed/coordinate/context controls refused')

if __name__=='__main__':main()
