"""Check the finite retained lifecycle ledger and owned reference evidence."""
import argparse
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
EVIDENCE = REPO / 'planning/stage-2/repos/dotj-build/evidence'
ROOT = Path(r'D:\AI\Implementation\dotj Frameworks')
RAW_SHA = '3187a8e9de73bd701c4d9389ae24e86fb193a942ce7110ae700e4cb938f6ea1f'
INPUT_LOCK_SHA = '1bbf88a7b75cf8f31c53b84dcce8df5652be27cd8703b0714ebdc556549a13b7'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read(path):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result: raise ValueError('duplicate JSON key: '+key)
            result[key]=value
        return result
    return json.loads(Path(path).read_bytes(),object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def strict(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=True,allow_nan=False,separators=(',',':'))

def require(condition, reason):
    if not condition: raise ValueError(reason)

def linked(item, base=REPO):
    path=(base/item['path']).resolve(strict=True)
    require(path.is_relative_to(base.resolve()),'evidence path escape')
    require(sha(path)==item['sha256'],'evidence/input bytes differ: '+item['path'])
    return path

def validate_ledger(ledger):
    rawpath=EVIDENCE/'compiled-lifecycle-raw-v1.json'
    require(sha(rawpath)==RAW_SHA,'retained inventory raw bytes differ')
    raw=read(rawpath)
    expected={'callables':[],'properties':[],'identities':raw['directContracts']}
    for t in raw['types']:
        expected['callables']+=t['methods']
        expected['properties']+=t['properties']
        for p in t['properties']: expected['callables']+=p['accessors']
    for category,records in expected.items():
        actual=[strict(r['metadata']) for r in ledger[category]]
        want=[strict(r) for r in records]
        require(len(actual)==len(set(actual)) and sorted(actual)==sorted(want),
                'retained inventory differs: '+category)
        for row in ledger[category]:
            m=row['metadata']
            module=raw['moduleVersionId'] if category!='identities' or m['assembly']==raw['assembly'] else None
            require(row['moduleVersionId']==module,'retained module identity differs')
            representation=row['representation']
            require(representation['status']=='BLOCKED' and representation['java'] is None
                    and isinstance(representation['gaps'],list) and all(type(x) is str and x for x in representation['gaps'])
                    and bool(representation['gaps']),'unapproved representation')
            if m.get('public') is False:
                require(row['profile']['included'] is False,'nonpublic representation promoted')
            require(type(row['profile']['included']) is bool and bool(row['profile']['reason']), 'representation profile')
            require(bool(row['semanticObligation']) and bool(row['ownershipStateRequirement']) and bool(row['downstream']), 'representation obligation')
            require(row['evidence']==[{'path':str(rawpath.relative_to(REPO)).replace('\\','/'),'sha256':RAW_SHA}], 'evidence lineage')
            for item in row['evidence']: linked(item)
    require(ledger['publicPromotion']=='BLOCKED' and type(ledger['acceptedTasksAdded']) is int
            and ledger['acceptedTasksAdded']==0 and type(ledger['numberedBatchCredit']) is int
            and ledger['numberedBatchCredit']==0 and len(ledger['openGates'])>=8,'representation promotion gate')
    return {'callables': 47, 'properties': 2, 'identities': 24}

def validate_payload(data, scenario):
    require(set(data)=={'schemaVersion','id','runtime','msbuildPath','frameworkPath','corePath','actions'}
            and type(data['schemaVersion']) is int and data['schemaVersion']==1
            and data['id']==scenario['id'] and data['runtime']=='.NET 10.0.12'
            and all(type(data[k]) is str for k in ['msbuildPath','frameworkPath','corePath'])
            and type(data['actions']) is list and len(data['actions'])==len(scenario['actions']),'output schema header/actions')
    kinds={'null':type(None),'bool':bool,'string':str,'dictionary':dict}
    for actual,planned in zip(data['actions'],scenario['actions']):
        require(type(actual) is dict,'output schema action must be an object')
        require(actual.get('id')==planned['id'] and type(actual.get('cleanup')) is bool
                and actual['cleanup']==planned['cleanup'] and type(actual.get('success')) is bool,'output schema action order/type')
        if actual['success']:
            require(set(actual)=={'id','cleanup','success','value'} and type(actual['value']) is kinds[planned['valueKind']], 'output schema value type/absence')
            if planned['valueKind']=='dictionary':
                require(all(type(k) is str and type(v) is str for k,v in actual['value'].items()),'output schema dictionary')
        else:
            require(set(actual)=={'id','cleanup','success','exception'},'output schema exception/absence')
            e=actual['exception']
            require(type(e) is dict and set(e)=={'type','hresult','message','diagnostic'} and type(e['type']) is str
                    and type(e['hresult']) is int and type(e['message']) is str,'output schema exception types')
            if e['diagnostic'] is not None:
                d=e['diagnostic']
                require(type(d) is dict and set(d)=={'code','file','line','column','endLine','endColumn'}
                        and all(type(d[k]) is int for k in ['line','column','endLine','endColumn'])
                        and all(d[k] is None or type(d[k]) is str for k in ['code','file']), 'output schema diagnostic')
    return data

def bind_capture(path):
    report=read(path)
    capture_root=Path(report['fixtureRoot']).resolve().parent
    # Bind duplicate observations before consulting any report-provided normalization roots.
    for command in report['commands']:
        if 'parsed' not in command: continue
        stdout=Path(command['stdout']['path'])
        require(stdout.resolve().is_relative_to(capture_root),'raw stdout binding path')
        require(sha(stdout)==command['stdout']['sha256'],'raw stdout binding bytes')
        require(strict(read(stdout))==strict(command['parsed']),'raw stdout binding parsed differs')
    return report

def verify_fixtures(root):
    root=Path(root).resolve(strict=True)
    trusted=HERE/'fixtures/manifest-v1.json'
    lock=read(EVIDENCE/'lifecycle-behavior-input-lock-v1.json')
    require(sha(EVIDENCE/'lifecycle-behavior-input-lock-v1.json')==INPUT_LOCK_SHA,'fixture trusted input lock differs')
    expected=next(x['sha256'] for x in lock['inputs'] if x['path'].endswith('/fixtures/manifest-v1.json'))
    require(sha(trusted)==expected and sha(root/'manifest-v1.json')==expected,'fixture trusted manifest differs')
    manifest=read(trusted)
    require({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}==
            {'manifest-v1.json',*[x['path'] for x in manifest['fixtures']]},'fixture file set differs')
    for item in manifest['fixtures']:
        p=(root/item['path']).resolve()
        require(p.is_relative_to(root) and p.is_file() and sha(p)==item['sha256'],'fixture bytes differ: '+item['path'])
    require(all(not (root/p).exists() for p in manifest['absent']),'fixture missing-file precondition')

def verify_inputs():
    path=EVIDENCE/'lifecycle-behavior-input-lock-v1.json'
    require(sha(path)==INPUT_LOCK_SHA,'trusted input lock differs')
    lock=read(path)
    for item in lock['inputs']: linked(item,ROOT if item['base']=='root' else REPO)
    verify_fixtures(HERE/'fixtures')
    return lock

def normalize(value, fixture_root):
    if type(value) is str: return value.replace(str(fixture_root),'<FIXTURE_ROOT>')
    if type(value) is list: return [normalize(x,fixture_root) for x in value]
    if type(value) is dict: return {k:normalize(v,fixture_root) for k,v in value.items()}
    return value

def validate_resource_waits(report,labels):
    require(type(report) is dict and 'resourceWaits' in report and 'resources' in report,'resource wait report shape')
    waits=report['resourceWaits'];readings=report['resources']
    require(type(waits) is list and type(readings) is list and all(type(w) is dict for w in waits)
            and all(type(r) is dict for r in readings) and [w.get('before') for w in waits]==labels,'resource wait group coverage/order')
    cursor=0
    def seconds(value):return type(value) in (int,float) and 0<=value<120 and math.isfinite(value)
    for wait,label in zip(waits,labels):
        require(set(wait)=={'before','limitSeconds','pollSeconds','seconds','status'}
                and type(wait['limitSeconds']) is int and wait['limitSeconds']==120
                and type(wait['pollSeconds']) is int and wait['pollSeconds']==5
                and wait['status']=='READY' and seconds(wait['seconds']),'resource wait bounds/status')
        group=[]
        while cursor<len(readings) and readings[cursor].get('before')==label:
            row=readings[cursor];cursor+=1
            require(set(row)=={'before','utc','waitSeconds','freePhysicalKiB','freeVirtualKiB'}
                    and type(row['utc']) is str and seconds(row['waitSeconds'])
                    and all(type(row[k]) is int and row[k]>=0 for k in ['freePhysicalKiB','freeVirtualKiB']), 'resource wait reading types')
            group.append(row)
        require(bool(group),'resource wait missing readings')
        times=[r['waitSeconds'] for r in group]
        require(times==sorted(times) and wait['seconds']>=times[-1],'resource wait elapsed chronology')
        ready=lambda r:r['freePhysicalKiB']>=524288 and r['freeVirtualKiB']>=16777216
        require(ready(group[-1]) and not any(ready(r) for r in group[:-1]),'resource wait fabricated READY boundary')
    require(cursor==len(readings),'resource wait extra or out-of-order readings')

def validate_capture(path):
    path=Path(path).resolve(strict=True)
    report=bind_capture(path)
    base=Path(report['fixtureRoot']).resolve().parent
    require(base.is_relative_to(ROOT) and base!=ROOT,'native capture private root')
    require(report['status']=='PASS_NATIVE_LIFECYCLE_PASS' and report['inputLockSha256']==INPUT_LOCK_SHA,'native pass/input status')
    require(type(report['schemaVersion']) is int and report['schemaVersion']==1 and type(report['runId']) is str
            and type(report['acceptedTasksAdded']) is int and report['acceptedTasksAdded']==0
            and report['publicQualification'] is False,'native report schema/credit')
    root=(base/'fixtures').resolve()
    require(report['fixtureRoot']==str(root),'fixture root is not the declared capture root')
    verify_fixtures(root)
    lock=verify_inputs();plan=read(EVIDENCE/'lifecycle-behavior-plan-v1.json')
    require(report['limits']=={'heapMiB':128,'processors':2,'timeoutSeconds':30,'queryTimeoutSeconds':20,
            'minFreePhysicalKiB':524288,'minFreeVirtualKiB':16777216,'resourceWaitSeconds':120,
            'resourcePollSeconds':5,'aggregateCaptureSeconds':540,'nativeCleanupReserveSeconds':35},'native resource limits')
    commands=report['commands']
    require([x['label'] for x in commands]==['compile']+[s['id'] for s in plan['scenarios']],'native command coverage/order')
    validate_resource_waits(report,[c['label'] for c in commands])
    for key in ['binary','runtimeConfig']:
        item=report[key];p=Path(item['path']).resolve(strict=True)
        require(p.is_relative_to(base) and sha(p)==item['sha256'],'native generated input bytes')
    require(strict(read(report['runtimeConfig']['path']))==strict(lock['runtimeConfig']),'native runtime configuration')
    values=[]
    for index,command in enumerate(commands):
        require(command.get('exitCode')==0 and type(command.get('exitCode')) is int
                and not command.get('timeout') and type(command.get('processId')) is int
                and type(command.get('nativeTimeoutSeconds')) is int and command['nativeTimeoutSeconds']==30,'native process status')
        for stream in ['stdout','stderr','hostTrace']:
            item=command[stream];p=Path(item['path']).resolve(strict=True)
            require(p.is_relative_to(base) and sha(p)==item['sha256'],'native raw log bytes')
        require(Path(command['stderr']['path']).read_bytes()==b'','native stderr is nonempty')
        environment=command['environmentOverrides']
        require(environment['DOTNET_GCHeapHardLimit']=='8000000' and environment['DOTNET_PROCESSOR_COUNT']=='2'
                and environment['DOTNET_ROLL_FORWARD']=='Disable','native environment limits')
        if index:
            scenario=plan['scenarios'][index-1]
            data=validate_payload(command['parsed'],scenario)
            require(all(data[k]==v for k,v in lock['assemblyPaths'].items()),'native resolved assembly identity')
            require(command['argv'][-2:]==[str(root),scenario['id']],'native fixture command input')
            values.append(data)
    return report,values

def validate_observation_lock(path, expected_sha, report_paths, reports):
    require(type(expected_sha) is str and len(expected_sha)==64 and sha(path)==expected_sha,
            'observation externally supplied SHA required or differs')
    lock=read(path)
    require(type(lock['schemaVersion']) is int and lock['schemaVersion']==1
            and lock['status']=='LOCKED_NATIVE_LIFECYCLE_PAIR' and lock['inputLockSha256']==INPUT_LOCK_SHA,
            'observation lock lineage')
    require(len(lock['passes'])==len(reports)==len(report_paths)==2
            and len({p['runId'] for p in reports})==2,'observation pair coverage')
    for entry,path,report in zip(lock['passes'],report_paths,reports):
        root=Path(entry['root']).resolve(strict=True)
        require(root.is_relative_to(ROOT) and report['runId']==entry['runId']
                and report['fixtureRoot']==str(root/'fixtures') and sha(path)==entry['reportSha256'],
                'observation report/root identity')
        require(bool(entry['files']) and len({x['path'] for x in entry['files']})==len(entry['files']),
                'observation file coverage')
        for item in entry['files']:
            p=(root/item['path']).resolve(strict=True)
            require(p.is_relative_to(root) and sha(p)==item['sha256'],'observation retained raw/input bytes differ')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture',action='append',type=Path,default=[])
    parser.add_argument('--ledger',type=Path,required=True)
    parser.add_argument('--static',action='store_true')
    parser.add_argument('--resource-telemetry',type=Path,help='Static schema control only; never qualifies native observations')
    parser.add_argument('--observation-lock',type=Path,default=EVIDENCE/'lifecycle-behavior-observations-v1.json')
    parser.add_argument('--observation-lock-sha256')
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();out=args.out.resolve()
    require(out.is_relative_to(ROOT) and out!=ROOT and not out.exists(),'new private D: output required')
    out.mkdir(parents=True)
    result={'schemaVersion':1,'status':'REFUSED','publicPromotion':'BLOCKED','acceptedTasksAdded':0,'numberedBatchCredit':0}
    code=0
    try:
        result['coverage']=validate_ledger(read(args.ledger));verify_inputs()
        result['ledgerSha256']=sha(args.ledger);result['inputLockSha256']=INPUT_LOCK_SHA
        if args.static:
            require(not args.capture,'static mode cannot accept captures')
            if args.resource_telemetry:
                labels=['compile']+[s['id'] for s in read(EVIDENCE/'lifecycle-behavior-plan-v1.json')['scenarios']]
                validate_resource_waits(read(args.resource_telemetry),labels)
                result['resourceTelemetrySchema']='PASS_STATIC_SCHEMA_ONLY'
            result.update(status='PASS_STATIC_ONLY',nativeOutcomes='UNOBSERVED')
        else:
            require(args.resource_telemetry is None,'resource telemetry schema controls require static mode')
            require(len(args.capture)==2 and len({p.resolve() for p in args.capture})==2,'two distinct native pass reports required')
            passes=[validate_capture(p) for p in args.capture]
            validate_observation_lock(args.observation_lock,args.observation_lock_sha256,args.capture,[p[0] for p in passes])
            require(passes[0][0]['runId']!=passes[1][0]['runId'],'distinct fresh process passes required')
            normalized=[normalize(values,report['fixtureRoot']) for report,values in passes]
            require(strict(normalized[0])==strict(normalized[1]),'native passes differ after fixture-root-only normalization')
            result.update(status='PASS_BOUNDED_EVIDENCE',nativeScenarios=8,nativeProcesses=16,
                          captures=[{'path':str(p.resolve()),'sha256':sha(p)} for p in args.capture],
                          observationLock={'path':str(args.observation_lock.resolve()),'sha256':args.observation_lock_sha256},observations=normalized[0])
        result['openGates']=read(args.ledger)['openGates']
    except (ValueError,KeyError,TypeError,OSError,StopIteration) as error:
        result['error']=str(error);code=1
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'report':str(out/'verification.json')}))
    return code

if __name__=='__main__': raise SystemExit(main())
