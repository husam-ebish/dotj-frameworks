"""Strict raw-bound native And evidence checker. Never runs a compiler or JVM."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(r'D:\AI\Implementation\dotj Frameworks')
REPO = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
DATA = REPO/'dotj-build/evaluation-candidate/and-conditions-v1'
EVIDENCE = DATA/'evidence'
CASE_IDS = ['BA01-literal-truth-table','BA02-balanced-nesting','BA03-token-case-and-boundaries',
            'BA04-lazy-right-exists','BA05-owner-relative-exists','BA06-encounter-time-properties',
            'BA07-import-groups-and-no-task-execution','BA08-malformed-right-side-parsed']


def require(condition, message):
    if not condition: raise ValueError(message)


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    def unique(pairs):
        obj={}
        for key,value in pairs:
            require(key not in obj,'duplicate JSON key: '+key)
            obj[key]=value
        return obj
    return json.loads(Path(path).read_bytes(),object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON: '+x)))


def read_pinned(path, expected):
    require(isinstance(expected,str) and re.fullmatch('[a-f0-9]{64}',expected),'external SHA256 required')
    require(sha(path)==expected,'external pin mismatch: '+str(path))
    return read(path)


def typed_equal(left, right):
    if type(left) is not type(right): return False
    if type(left) is dict:
        return left.keys()==right.keys() and all(typed_equal(left[k],right[k]) for k in left)
    if type(left) is list:
        return len(left)==len(right) and all(typed_equal(a,b) for a,b in zip(left,right))
    return left == right


def keys(obj, fields):
    require(type(obj) is dict and set(obj)==set(fields),'unexpected/missing fields: '+str(fields))


def scalar(obj, field, kind):
    require(field in obj and type(obj[field]) is kind,'typed field mismatch: '+field)


def edge(edge):
    keys(edge,['owner','project','line','column'])
    for key in ['owner','project']: scalar(edge,key,str)
    for key in ['line','column']:
        scalar(edge,key,int);require(edge[key]>=0,'negative edge location')


def diagnostic(d):
    keys(d,['kind','code','file','line','column','endLine','endColumn','message'])
    require(d['kind'] in ['warning','error'],'unknown diagnostic kind')
    for key in ['code','file','message']: require(d[key] is None or type(d[key]) is str,'diagnostic string')
    for key in ['line','column','endLine','endColumn']: scalar(d,key,int)


def validate_payload(data):
    keys(data,['runtime','msbuildAssembly','msbuildPath','frameworkPath','corePath','profile','rows'])
    require(data['runtime']=='.NET 10.0.12' and data['profile']=='Default','runtime/profile drift')
    for key in ['runtime','msbuildAssembly','msbuildPath','frameworkPath','corePath','profile']:scalar(data,key,str)
    require(type(data['rows']) is list,'rows must be list')
    require([r.get('id') for r in data['rows']]==CASE_IDS,'exact ordered eight-case coverage required')
    for index,row in enumerate(data['rows']):
        keys(row,['id','globals','profile','evaluation','diagnostics','cleanup','taskMarkerAbsent'])
        require(row['profile']=='Default','row profile drift')
        require(typed_equal(row['globals'],{'EmptyPath':''} if index==3 else {}),'globals differ')
        require(row['taskMarkerAbsent'] is True,'task marker evidence missing')
        cleanup=row['cleanup'];keys(cleanup,['before','loaded','afterUnload','disposed'])
        for key in ['before','loaded','afterUnload']:scalar(cleanup,key,int)
        require(cleanup['before']==0 and cleanup['loaded']>=0 and cleanup['afterUnload']==0 and cleanup['disposed'] is True,'cleanup incomplete')
        ev=row['evaluation'];scalar(ev,'success',bool)
        if ev['success']:
            keys(ev,['success','properties','imports','duplicateImports','duplicateGetterFailure'])
            keys(ev['properties'],['P','Q'])
            for key in ['P','Q']:scalar(ev['properties'],key,str)
            require(type(ev['imports']) is list,'imports type')
            for value in ev['imports']:edge(value)
            require(ev['duplicateImports'] is None or type(ev['duplicateImports']) is list,'duplicate imports type')
            if ev['duplicateImports'] is not None:
                for value in ev['duplicateImports']:edge(value)
            if ev['duplicateGetterFailure'] is not None:
                keys(ev['duplicateGetterFailure'],['type','message'])
                for key in ['type','message']:scalar(ev['duplicateGetterFailure'],key,str)
        else:
            keys(ev,['success','type','code','file','line','column','endLine','endColumn','message','hresult'])
            require(ev['type']=='Microsoft.Build.Exceptions.InvalidProjectFileException','untyped native failure')
            for key in ['code','file','message']: require(ev[key] is None or type(ev[key]) is str,'exception string')
            for key in ['line','column','endLine','endColumn','hresult']:scalar(ev,key,int)
        require(type(row['diagnostics']) is list,'diagnostics type')
        for d in row['diagnostics']:diagnostic(d)


def normalize(data, fixture_root):
    result=copy.deepcopy(data);root=str(fixture_root).rstrip('\\/')
    require(root and root!='<FIXTURE_ROOT>','invalid fixture root')
    # Boundary prevents fixtures-other matching fixtures. Replacement is exact and case-sensitive.
    pattern=re.compile(r'(?<![\w\\/:.-])'+re.escape(root)+r'(?=$|[\\/])')
    def replace(value, message=False):
        if type(value) is not str:return value
        if message:return pattern.sub(lambda _: '<FIXTURE_ROOT>',value)
        if value==root or value.startswith((root+'\\',root+'/')):return '<FIXTURE_ROOT>'+value[len(root):]
        return value
    for row in result['rows']:
        ev=row['evaluation']
        if ev['success']:
            for group in ['imports','duplicateImports']:
                for item in ev[group] or []:
                    for field in ['owner','project']:item[field]=replace(item[field])
            if ev['duplicateGetterFailure'] is not None:
                ev['duplicateGetterFailure']['message']=replace(ev['duplicateGetterFailure']['message'],True)
        else:
            for field in ['file','message']:ev[field]=replace(ev[field],field=='message')
        for d in row['diagnostics']:
            for field in ['file','message']:d[field]=replace(d[field],field=='message')
    return result


def owned_path(path, root):
    path=Path(path).resolve(strict=True);root=Path(root).resolve(strict=True)
    require(path.is_relative_to(root) and path!=root,'path escapes owned root')
    return path


def bind_stdout(descriptor, payload, capture_root):
    keys(descriptor,['path','sha256'])
    path=owned_path(descriptor['path'],capture_root)
    raw=read_pinned(path,descriptor['sha256'])
    require(typed_equal(raw,payload),'raw typed stdout differs from envelope payload')
    return raw


def verify_fixtures(root, entries):
    root=Path(root).resolve(strict=True)
    require(type(entries) is list and len({x['path'] for x in entries})==len(entries),'fixture lock duplicates')
    require({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}=={x['path'] for x in entries},'fixture coverage differs')
    for item in entries:
        path=owned_path(root/item['path'],root)
        require(sha(path)==item['sha256'] and path.stat().st_size==item['bytes'],'fixture changed: '+item['path'])


def verify_inputs(expected, lock_path=None):
    lock_path=Path(lock_path or EVIDENCE/'input-lock.json')
    lock=read_pinned(lock_path,expected)
    seen=set()
    for item in lock['inputs']:
        identity=(item['base'],item['path']);require(identity not in seen,'duplicate input');seen.add(identity)
        root={'repo':REPO,'root':ROOT}[item['base']]
        path=owned_path(root/item['path'],root)
        require(sha(path)==item['sha256'],'input changed: '+str(path))
    plan=read(EVIDENCE/'plan.json')
    require([x['id'] for x in plan['cases']]==CASE_IDS,'plan coverage differs')
    verify_fixtures(DATA/'fixtures',plan['fixtures'])
    # Later observation/candidate artifacts and their coordinator are not native inputs.
    # Enumerate the consumed static corpus, never an evolving evidence directory.
    native_paths=[DATA/'.gitattributes',EVIDENCE/'plan.json',EVIDENCE/'grammar.json',EVIDENCE/'capture.schema.json']
    native_paths += [DATA/'fixtures'/x['path'] for x in plan['fixtures']]
    native_paths += [HERE/name for name in ['capture.py','verify.py','test_verify.py']]
    required={('repo',p.relative_to(REPO).as_posix()) for p in native_paths}
    require(required.issubset(seen),'new owned input coverage missing')
    require(not any('ProjectEvaluationComponent.java' in x['path'] or x['path'].endswith('.jar') for x in lock['inputs']),'native lock must exclude future candidate changes')
    return lock


def verify_checkpoint(path, expected, input_sha):
    checkpoint=read_pinned(path,expected)
    require(checkpoint['inputLockSha256']==input_sha,'checkpoint input lock differs')
    require(checkpoint['phase']=='STATIC_PREPARED_ROOT_REVIEW_REQUIRED','checkpoint phase differs')
    require(checkpoint['briefSha256']=='3c7141f6888fd44ff3a8820d36d0f42f1a126b54632a6d42241ee242e3951a9f','checkpoint brief differs')
    return checkpoint


def classify(payload):
    successful=[r['id'] for r in payload['rows'][:7] if r['evaluation']['success'] is True]
    require(len(successful)==7,'one or more supported-case native outcomes failed; revise scope before candidate proof')
    return {'successfulNativeComparisons':len(successful),'successfulIds':successful,
            'malformedEvidence':[{'id':payload['rows'][7]['id'],'nativeSuccess':payload['rows'][7]['evaluation']['success'],
                                  'privateCandidateDisposition':'PROFILE_REFUSAL_REQUIRED','exactExceptionParity':False}],
            'candidateComparisonsPerformed':0,'acceptedTasksAdded':0,'numberedBatchCredit':0}


def validate_resources(record):
    labels=[x['label'] for x in record['commands']]
    require([w['before'] for w in record['resourceWaits']]==labels,'resource wait coverage differs')
    for wait in record['resourceWaits']:
        require(wait['status']=='READY' and type(wait['limitSeconds']) is int and wait['limitSeconds']==120
                and type(wait['pollSeconds']) is int and wait['pollSeconds']==5,'resource wait bounds/status differ')
        require(type(wait['seconds']) in (int,float) and 0<=wait['seconds']<120,'resource deadline exceeded')
        readings=[r for r in record['resources'] if r['before']==wait['before']]
        require(readings,'missing resource reading')
        for field in ['freePhysicalKiB','freeVirtualKiB']:
            require(all(type(r.get(field)) is int and r[field]>=0 for r in readings),'invalid resource query')
        require(readings[-1]['freePhysicalKiB']>=524288 and readings[-1]['freeVirtualKiB']>=16777216,'resource floor not met')
        require(type(readings[-1]['waitSeconds']) in (int,float) and 0<=readings[-1]['waitSeconds']<120,'resource query deadline exceeded')
    require(all(r['before'] in labels for r in record['resources']),'unknown resource reading')


def validate_capture(path, input_sha, checkpoint_path, checkpoint_sha):
    verify_checkpoint(checkpoint_path,checkpoint_sha,input_sha)
    lock=verify_inputs(input_sha);path=Path(path).resolve(strict=True);record=read(path);out=path.parent
    require(out.is_relative_to(ROOT) and out!=ROOT,'capture outside project base')
    require(type(record['schemaVersion']) is int and record['schemaVersion']==1 and record['status']=='PASS_NATIVE_AND_CAPTURE','capture incomplete')
    require(type(record['runId']) is str and record['runId'],'capture run ID missing')
    require(record['inputLockSha256']==input_sha and record['checkpointSha256']==checkpoint_sha,'capture pins differ')
    fixture_root=owned_path(record['fixtureRoot'],out)
    require(fixture_root==out/'fixtures','unexpected copied fixture root')
    verify_fixtures(fixture_root,read(EVIDENCE/'plan.json')['fixtures'])
    require(len(record['commands'])==2,'one compiler and one eight-collection native process required')
    require([x['label'] for x in record['commands']]==['compile-probe','native-eight-cases'],'command coverage')
    for command in record['commands']:
        require(type(command['exitCode']) is int and command['exitCode']==0 and not command.get('timeout') and not command.get('cleanupError'),'command failed')
        for key in ['stdout','stderr','hostTrace']:
            info=command[key];log=owned_path(info['path'],out)
            require(sha(log)==info['sha256'],'log hash differs')
        require(Path(command['stderr']['path']).read_bytes()==b'','native stderr retained but capture rejected')
        require(type(command['nativeTimeoutSeconds']) is int and command['nativeTimeoutSeconds']==30 and command['cwd']==str(out),'native bounds/cwd differ')
        env=command['environmentOverrides']
        require(env['DOTNET_GCHeapHardLimit']=='8000000' and env['DOTNET_PROCESSOR_COUNT']=='2' and env['DOTNET_ROLL_FORWARD']=='Disable','native environment differs')
    expected_copies={x['target']:x for x in lock['copiedInputs']}
    require({x['target'] for x in record['copiedInputs']}==set(expected_copies),'copied input coverage differs')
    for item in record['copiedInputs']:
        expected=expected_copies[item['target']];file=owned_path(out/item['target'],out)
        require(item['sha256']==expected['sha256'] and sha(file)==expected['sha256'],'copied native input differs')
    for field in ['binary','runtimeConfig']:
        info=record[field];file=owned_path(info['path'],out);require(sha(file)==info['sha256'],'binary/config hash differs')
    require(typed_equal(read(record['runtimeConfig']['path']),lock['runtimeConfig']),'runtime configuration differs')
    command=record['commands'][1]
    expected_args=[str(ROOT/'toolchains/dotnet/dotnet.exe'),'exec','--runtimeconfig',record['runtimeConfig']['path'],
                   '--depsfile',str(ROOT/'toolchains/dotnet/sdk/10.0.401/MSBuild.deps.json'),record['binary']['path'],str(fixture_root),str(out/'plan.json')]
    require(command['argv']==expected_args,'native consumption command differs')
    compile_expected=[str(ROOT/'toolchains/dotnet/dotnet.exe'),'exec',str(ROOT/'toolchains/dotnet/sdk/10.0.401/Roslyn/bincore/csc.dll'),
                      '/nologo','/noconfig','/nostdlib+','/target:exe','/nullable:enable','/deterministic+','/langversion:14',
                      '/out:'+record['binary']['path'],*['/reference:'+str(ROOT/p) for p in lock['compilerReferences']],str(out/'CaptureImportPathsV1.cs')]
    require(record['commands'][0]['argv']==compile_expected,'compiler source/reference lineage differs')
    payload=bind_stdout(command['stdout'],record['payload'],out)
    validate_payload(payload)
    for field,rel in lock['resolvedAssemblies'].items():
        require(payload[field]==str(ROOT/rel),'resolved native assembly differs')
    require(payload['msbuildAssembly']==lock['msbuildAssembly'],'resolved native assembly identity differs')
    require(typed_equal(record['limits'],lock['limits']),'declared native resource limits differ')
    require(len(record['resourceWaits'])==2 and len(record['resources'])>=2,'resource observations incomplete')
    validate_resources(record)
    classify(payload)
    return record,normalize(payload,fixture_root)


def compare_pair(paths, input_sha, checkpoint_path, checkpoint_sha):
    require(len(paths)==2 and Path(paths[0]).resolve()!=Path(paths[1]).resolve(),'two distinct retained captures required')
    left,lnorm=validate_capture(paths[0],input_sha,checkpoint_path,checkpoint_sha)
    right,rnorm=validate_capture(paths[1],input_sha,checkpoint_path,checkpoint_sha)
    require(left['runId']!=right['runId'] and left['fixtureRoot']!=right['fixtureRoot'],'fresh independent captures required')
    require(typed_equal(lnorm,rnorm),'fresh typed native captures disagree')
    return {'schemaVersion':1,'status':'PAIRED_NATIVE_AND_EVIDENCE','inputLockSha256':input_sha,'checkpointSha256':checkpoint_sha,
            'captures':[{'path':str(Path(p).resolve()),'sha256':sha(p)} for p in paths],
            'normalizedPayload':lnorm,'classification':classify(lnorm),'candidateState':'NOT_RUN'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('captures',nargs=2,type=Path)
    parser.add_argument('--input-lock-sha256',required=True)
    parser.add_argument('--checkpoint',required=True,type=Path)
    parser.add_argument('--checkpoint-sha256',required=True)
    parser.add_argument('--observation-lock',type=Path)
    parser.add_argument('--observation-lock-sha256')
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args();out=args.out.resolve()
    require(out.is_relative_to(ROOT) and out!=ROOT and not out.exists(),'new owned output required')
    out.mkdir(parents=True)
    result={'status':'FAILED','candidateComparisonsPerformed':0,'acceptedTasksAdded':0}
    try:
        pair=compare_pair(args.captures,args.input_lock_sha256,args.checkpoint,args.checkpoint_sha256)
        if args.observation_lock:
            locked=read_pinned(args.observation_lock,args.observation_lock_sha256)
            require(typed_equal(locked,pair),'externally pinned observation lock differs')
            result.update(status='PASS_EXTERNALLY_PINNED_NATIVE_AND_PAIR',observationLockSha256=sha(args.observation_lock))
        else:
            require(args.observation_lock_sha256 is None,'observation path missing')
            (out/'observation-lock.json').write_bytes((json.dumps(pair,indent=2)+'\n').encode())
            result.update(status='PAIR_VERIFIED_PENDING_EXTERNAL_OBSERVATION_PIN',observationLockSha256=sha(out/'observation-lock.json'))
        result['classification']=pair['classification']
    except Exception as error:
        result['error']=str(error);raise
    finally:(out/'verification.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result))


if __name__=='__main__':main()
