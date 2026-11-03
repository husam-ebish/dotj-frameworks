"""Read retained Task128 executions; freeze the actual native contract, without launches.

Execution paths come from fixed artifact identities, never the reader's location.
Only declared fixture root relocation is normalized; values/order/diagnostics remain.
"""
from pathlib import Path
import hashlib
import json
import sys

B=Path('D:/AI/Implementation/dotj Frameworks')
A=B/'agents/batch2521-build-items-evaluation-v1'
IMAGE='mcr.microsoft.com/dotnet/aspnet@sha256:222759b391a1aaf241166672c8f99b2d4ada452e7b5319f3c6e8f265a37b5ad4'
OLD_JAR_SHA='6bc95bc7ed6d702ed58f455f10fe35ed0c71389dd175034afefaee2e259e089f'

def require(value,message):
    if not value: raise ValueError(message)

def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def desc(path):
    path=Path(path)
    return dict(path=str(path),sha256=sha(path),bytes=path.stat().st_size)
def check(d):
    p=Path(d['path'])
    require(sha(p)==d['sha256'] and p.stat().st_size==d.get('bytes',d.get('sizeBytes')), 'Artifact bytes differ: '+str(p))

def normalized(value,root,key=None):
    if isinstance(value,str):
        rootless=root[1:] if root.startswith('/') else root[3:]
        if key=='Directory' and value.startswith(rootless):
            return '{FIXTURE_ROOT_WITHOUT_ROOTDIR}'+value[len(rootless):]
        return value.replace(root,'{FIXTURE_ROOT}')
    if isinstance(value,list):return [normalized(v,root) for v in value]
    if isinstance(value,dict):return {k:normalized(v,root,k) for k,v in value.items()}
    return value

def expected_tree(source):
    return {p.relative_to(source).as_posix():sha(p) for p in source.rglob('*') if p.is_file()}

def after_tree(source,manifest,supplemental=False):
    values=expected_tree(source)
    if supplemental:return values
    for c in manifest['cases']:
        for step in c['steps']:
            prefix=c['id']+'/'
            if step['kind']=='filesystem-change':
                for path in step['delete']:del values[prefix+path]
                for path,text in step['write'].items():values[prefix+path]=hashlib.sha256(text.encode()).hexdigest()
            elif step['kind']=='evaluate-xml':values[prefix+step['owner']]=hashlib.sha256(step['xml'].encode()).hexdigest()
            elif step['kind']=='repeat-owner':values[prefix+step['owner']]=values[prefix+'main.proj']
    return values

def validate_capture(platform,passno,supplemental):
    kind='supplemental' if supplemental else 'native'
    suffix='v1' if supplemental else 'v2'
    out=A/f'{kind}-{platform}-pass{passno}-{suffix}'
    receipt=read(out/'receipt.json')
    require(receipt['status']=='CAPTURED_PENDING_CONTRACT_REVIEW','Unfinished capture')
    observer=A/('semantic-observer-v3' if supplemental else 'semantic-observer-v2')
    source=A/('supplemental-input-v1' if supplemental else 'corpus-input-v1')
    mode='supplemental' if supplemental else 'corpus'
    manifest=read(source/'manifest.json')
    for item in receipt['inputs']:check(item)
    slot=('supplemental-' if supplemental else '')+f'pass{passno}'
    if platform=='windows':
        root=str(out/'work/fixtures')
        raw=out/'native-windows.stdout'
        expected=[str(B/'toolchains/dotnet/dotnet.exe'),str(observer/'CaptureItemsV1.dll'),mode,root,str(out/'work/fixtures/manifest.json'),str(observer)]
        require(len(receipt['operations'])==1 and receipt['operations'][0]['process']['argv']==expected,'Exact Windows command differs')
        require(receipt['environmentOverrides']['DOTNET_ReadyToRun']=='0','Windows JIT profile differs')
        actual_root=out/'work/fixtures'
        before_root=actual_root
    else:
        root=f'/work/{slot}/fixtures'
        raw=out/('retained-output/supplemental.stdout' if supplemental else 'retained-output/native.stdout')
        c=receipt['container'];state=c['terminalInspect']['State'];host=c['terminalInspect']['HostConfig'];config=c['terminalInspect']['Config']
        require(c['image']==IMAGE and config['Image']==IMAGE and c['absenceVerified'],'Linux identity/cleanup differs')
        require(state['ExitCode']==0 and not state['OOMKilled'] and not state['Running'],'Linux terminal state differs')
        require(host['ReadonlyRootfs'] and host['NetworkMode']=='none' and host['Memory']==536870912 and host['MemorySwap']==536870912 and host['NanoCpus']==2000000000 and host['PidsLimit']==64,'Linux bounds differ')
        require(host['CapDrop']==['ALL'] and 'no-new-privileges' in host['SecurityOpt'],'Linux capabilities differ')
        require(config['Entrypoint']==['/usr/bin/timeout'] and config['Cmd']==['-s','KILL','25','/bin/sh','/run.sh',slot],'Linux inner argv differs')
        require(c['environment']['DOTNET_ReadyToRun']=='0' and c['environment']['MSBUILD_EXE_PATH']=='/observer/Microsoft.Build.dll','Linux managed profile differs')
        mounts={m['Destination']:m for m in c['terminalInspect']['Mounts']}
        require(mounts['/observer']['Source'].replace('\\','/').endswith(str(observer).replace('\\','/').split(':/',1)[-1]) or str(observer).replace('\\','/').lower() in mounts['/observer']['Source'].replace('\\','/').lower(),'Observer mount not bound')
        require(not mounts['/observer']['RW'] and not mounts['/corpus']['RW'] and not mounts['/run.sh']['RW'],'Readonly inputs differ')
        for pair in receipt['retainedOutputs']:
            check(pair['actual']);check(pair['retained'])
            require(pair['actual']['sha256']==pair['retained']['sha256'],'Retained raw copy differs')
        if not supplemental:
            profiles=(out/'retained-output/materialized-case-profile.tsv').read_text().splitlines()
            require(len(profiles)==42 and {line.split('\t')[0] for line in profiles}=={c['id'] for c in manifest['cases']} and all(line.endswith('\tfalse\tfalse') for line in profiles),'Actual copied-directory casing not proven')
        actual_root=A/'native-linux-corpus-root-v1'/slot/'fixtures'
        before_root=source
    for operation in receipt['operations']:
        process=operation['process'];label=operation['label']
        expected_exit=1 if label in ('container-initial','container-absence') else 0
        require(process['exitCode']==expected_exit and not process.get('timedOut') and not process.get('cleanupError') and not process.get('error') and not process.get('outputLimitExceeded'),'Process failure: '+label)
        check(operation['stdout']);check(operation['stderr'])
    before={Path(d['path']).relative_to(before_root).as_posix():d['sha256'] for d in receipt['corpusInputs']}
    require(before==expected_tree(source),'Initial corpus copy differs')
    actual=expected_tree(actual_root)
    require(actual==after_tree(source,manifest,supplemental),'Undeclared fixture mutation')
    payload=read(raw)
    require(payload['readyToRun']=='0' and payload['msbuild']['file']['sha256']=='96896c3c1e0843ea5c4cc03baac8df3a61587e3742599b6b29f99dbd25595eff','Loaded managed identity differs')
    rows=payload['observations']['rows']
    require([r['id'] for r in rows]==[c['id'] for c in manifest['cases']],'Case identity/order differs')
    if not supplemental:
        require(len(rows)==42 and payload['observations']['scenarioCount']==42,'Scenario count differs')
        require(all(r['retainedFirstSnapshotUnchanged'] and r['taskMarkerAbsent'] for r in rows),'Ownership/no-task markers differ')
        fs=payload['observations']['filesystem']
        require(fs['alternateExistsBefore']==(platform=='windows'),'Actual filesystem capability differs')
    for row in rows:
        evaluations=[row['evaluation']] if supplemental else [o for o in row['observations'] if 'result' in o]
        for evaluation in evaluations:
            require(evaluation['cleanup']['after']==0,'Collection not unloaded')
            ts=evaluation['toolsets']
            require(len(ts)==1 and ts[0]['ToolsVersion']=='Task128' and ts[0]['properties']=={},'Explicit toolset differs')
    return normalized(rows,root),dict(receipt=desc(out/'receipt.json'),raw=desc(raw),observerSource=desc(observer/'CaptureItemsV1.cs'),observerDll=desc(observer/'CaptureItemsV1.dll'),
        runtimeConfig=desc(observer/'CaptureItemsV1.runtimeconfig.json'),compiledInventory=desc(observer/'compiled-inventory.stdout'),
        exactExecutedArgv=[o['process']['argv'] for o in receipt['operations']],fixtureRoot=root,actualFixtureRoot=str(actual_root),
        runtime={k:payload[k] for k in ('os','runtime','readyToRun','host','core','msbuild','framework','loadedAssemblies')})

def freeze(output):
    output=Path(output)
    require(not output.exists(),'New contract file required')
    result=dict(schemaVersion=1,status='FROZEN_NATIVE_CONTRACT_PENDING_ROOT_REVIEW',scenarioCount=42,semanticRows=168,
        supplementalDefinitions=4,supplementalRepeatedRows=16,privateControlGroups=14,privateGroupsExecuted=0,
        productEditsAuthorized=False,acceptedTasksAdded=0,models={},captures={},supplementalModels={},supplementalCaptures={})
    for supplemental in (False,True):
        for platform in ('windows','linux'):
            one,e1=validate_capture(platform,1,supplemental);two,e2=validate_capture(platform,2,supplemental)
            require(one==two,'Native repeated pass mismatch: '+platform)
            result['supplementalModels' if supplemental else 'models'][platform]=one
            result['supplementalCaptures' if supplemental else 'captures'][platform]=[e1,e2]
    result['normalization']='Only exact declared fixture-root relocation in strings; selected built-in Directory uses the same root with filesystem RootDir removed. No case/separator/order/value/error normalization.'
    result['sourceRoles']={'semantic':'Sealed semantic-observer-v2 source/DLL executed all168 semantic rows. Repository primary source is byte-identical.',
        'supplemental':'Sealed semantic-observer-v3 executed only supplemental mode. Repository supplemental-source contains its exact source; never claimed executed for semantic rows.'}
    reference=B/'references/msbuild/b44cdcec4c79c50c67560876707d57d4f635fa3b/source'
    findings=[('src/Build/Evaluation/Evaluator.cs','725-729','Final surviving lazy items added after source-element ordering'),
        ('src/Build/Evaluation/LazyItemEvaluator.cs','500-503','GetAllItemsDeferred orders final survivors by ElementOrder'),
        ('src/Build/Collections/ItemDictionary.cs','23,164-167,383-404','Final materialization builds per-type lists; Items enumerates those lists'),
        ('src/Build/Evaluation/Expander.cs','251-264','Metadata then properties then items then MaybeAdjustFilePath'),
        ('src/Build/Definition/ToolsetReader.cs','255-264,280-326','Local-only bootstrap avoids None framework-path fallback'),
        ('src/Build/Definition/ToolsetLocalReader.cs','20-43','Explicit local directory defines bootstrap Current properties'),
        ('src/Framework/BuildEnvironmentHelper.cs','123-129,336-348','Explicit MSBUILD_EXE_PATH uses an existing owned assembly path')]
    result['sourceRefinements']=[dict(file=desc(reference/path),lines=lines,finding=finding) for path,lines,finding in findings]
    result['orderingRulingProposed']='Preserve internal final source-element order and multiplicity. Project.Items observation groups by type in first-surviving-materialization order, not first-ever-operation order. GetItems preserves surviving order within type. No public collection ABI claim.'
    result['legacyTransition']={'id':'NEG-items','input':desc(A/'supplemental-input-v1/NEG-items/main.proj'),'old':'UNSUPPORTED_ELEMENT','new':'SUCCESS_EMPTY_ITEMS','unchangedHistoricalRows':93}
    red=read(A/'genuine-baseline-red-v1/receipt.json')
    require(red['status']=='GENUINE_BASELINE_RED' and red['inputs'][0]['sha256']==OLD_JAR_SHA,'Genuine RED missing')
    result['baselineRed']=desc(A/'genuine-baseline-red-v1/receipt.json')
    result['abi']=desc(A/'genuine-baseline-red-v1/old-result-abi.stdout')
    result['abiPreservation']='Keep old six-argument Result constructor and all accessor descriptors; add private item state/accessors with immutable deep snapshots.'
    result['inputManifest']=desc(A/'corpus-input-v1/manifest.json')
    result['supplementalInputManifest']=desc(A/'supplemental-input-v1/manifest.json')
    result['reader']=desc(__file__)
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],contract=desc(output))))

if __name__=='__main__':freeze(sys.argv[1])
