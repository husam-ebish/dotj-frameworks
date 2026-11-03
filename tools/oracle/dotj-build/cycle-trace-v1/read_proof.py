"""Pure, relocatable successor proof. Evidence resolves only inside this bundle; never by original paths."""
import argparse
import base64
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from compare import native_projection
from native_lock import flatten,normalize
from inherited_models import normalized,selected_native,selected_product,sort_result,boundary_result

def require(value,message):
    if not value:raise ValueError(message)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def descriptors(value):
    if isinstance(value,dict):
        if {'path','sha256','bytes'}<=value.keys():yield value
        for child in value.values():yield from descriptors(child)
    elif isinstance(value,list):
        for child in value:yield from descriptors(child)

class Bundle:
    def __init__(self,path,expected):
        self.root=Path(path).resolve().parent;raw=Path(path).read_bytes();require(digest(raw)==expected,'Proof hash')
        self.proof=json.loads(raw);self.cache={}
        for key,pin in self.proof['objects'].items():
            path=(self.root/pin['relative']).resolve()
            require(path.is_relative_to(self.root),'Object escapes bundle')
            raw=path.read_bytes();require(len(raw)==pin['bytes'] and digest(raw)==key,'Object bytes '+key)
            self.cache[key]=raw
    def raw(self,d):
        require(d['sha256'] in self.cache,'Missing object '+d['path'])
        raw=self.cache[d['sha256']];require(len(raw)==d['bytes'],'Descriptor length')
        return raw
    def text(self,d):return self.raw(d).decode('utf-8-sig')
    def json(self,d):return json.loads(self.text(d))

def process(op,pin):
    p=op['process'];require(op['label']==pin['label'] and p['argv']==pin['argv'] and p['exitCode']==pin['exitCode'],'Actual argv/exit differs')
    require(p.get('jobAssigned') and p.get('resumed') and p.get('launched'),'Owned launch')
    require(not any(p.get(k) for k in ('timedOut','outputLimitExceeded','cleanupError','error')) and p['cleanupSeconds']<=5,'Process terminal cleanup')
    require(0<p['timeoutSeconds']<=120,'Operation cap')

def owned_container(c):
    t=c['terminalInspect'];created=c['createdInspect'];h=created['HostConfig']
    require(c['absenceVerified'] and c['lateAbsenceVerified'],'Container absence')
    require(t['State']['ExitCode']==0 and not t['State']['OOMKilled'] and not t['State']['Running'],'Container terminal')
    require(t['Id']==created['Id']==c['cid'] and t['Name']=='/'+c['name'],'Container identity')
    require(t['Config']['Image']==c['image']=='mcr.microsoft.com/dotnet/aspnet@sha256:222759b391a1aaf241166672c8f99b2d4ada452e7b5319f3c6e8f265a37b5ad4','Pinned image')
    require(t['Config']['Labels']['dotj.owner']==c['owner']=='task132','Owned label')
    require(h['ReadonlyRootfs'] and h['NetworkMode']=='none' and h['Memory']==536870912 and h['MemorySwap']==536870912 and h['PidsLimit']==64,'Container resources')
    require(h['NanoCpus']==2000000000 and 'ALL' in h['CapDrop'] and any('no-new-privileges' in s for s in h['SecurityOpt']),'Container isolation')

def check_native(bundle,contract):
    proof=bundle.proof;lock=bundle.json(proof['nativeLock']);recipe_runs={}
    for descriptor in proof['nativeRecipes']:
        recipe=bundle.json(descriptor)
        for run in recipe['runs']:recipe_runs[run['attempt']]=run
    observations={}
    for unit in lock['units']:
        raw=bundle.json(unit['stdout']);receipt=bundle.json(unit['receipt'])
        if unit['role']=='retained-completed-child':
            require(receipt['status']==unit['aggregateStatus'] and raw in receipt['captures'],'Completed native child raw/parsed/status')
            require(unit['unitExitCode']==0,'Native child exit')
            commands=[c for c in receipt['commands'] if c['label']==raw['profile']]
            require(len(commands)==1 and commands[0]['exitCode']==0,'Native child command')
            require(commands[0]['stdout']['sha256']==unit['stdout']['sha256'],'Native child stdout binding')
            if receipt['status']=='FAILED':require(unit['id']=='import-profiles-native-v1:RecordDuplicateButNotCircularImports','Only adopted FAILED child')
            platform='windows'
        else:
            require(receipt['status']=='PASS' and receipt['rawParsedEquality'] and receipt['fixturesUnchanged'],'New native execution')
            require(bundle.json(receipt['outputs'][1])==raw,'New native raw/parsed equality')
            selected=receipt['selection'];platform=selected['platform'];expected=recipe_runs[selected['attempt']]
            label='capture' if platform=='windows' else 'container-create'
            actual=next(o for o in receipt['operations'] if o['label']==label)
            require(actual['process']['argv']==expected['argv'],'Native actual approved argv')
            require([r['id'] for r in raw['rows']]==selected['ids'],'Native selected IDs')
            expected_files={c['id']+'/'+n:v['sha256'] for c in contract['cases'] if c['id'] in selected['ids'] for n,v in c['files'].items()}
            actual_files={d['path'].replace('\\','/').split('/fixtures/',1)[1]:d['sha256'] for d in receipt['fixtureInputs']}
            require(actual_files==expected_files,'Native exact input fixture closure')
            require({d['relative']:d['file']['sha256'] for d in proof['nativeFixtureAfter'][unit['id']]}==expected_files,'Native exact after fixture closure')
            if platform=='linux':
                owned_container(receipt['container'])
                require(bundle.text(receipt['caseProfile']).splitlines()==[id+'\tfalse\tfalse' for id in selected['ids']],'Native case profile')
                require(raw['msbuildPath']=='/sdk/Microsoft.Build.dll' and raw['frameworkPath']=='/sdk/Microsoft.Build.Framework.dll'
                    and raw['corePath']=='/usr/share/dotnet/shared/Microsoft.NETCore.App/10.0.12/System.Private.CoreLib.dll','Native Linux assembly origins')
            require(raw['runtime']=='.NET 10.0.12','Native runtime')
        for row in raw['rows']:
            require(row['cleanup']['before']==0 and row['cleanup']['afterUnload']==0 and row['cleanup']['disposed'] and row['taskMarkerAbsent'],'Native row cleanup')
            key=(platform,row['id'],row['profile'])
            observations.setdefault(key,[]).append((unit['id'],normalize(row,unit['fixtureRoot'])))
    require(len(lock['rows'])==114 and lock['newRowPasses']==190 and lock['requiredRowPasses']==228,'Native coverage size')
    byprofile={'DEFAULT':'Default','RECORD_DUPLICATES':'RecordDuplicateButNotCircularImports','REJECT_CIRCULAR':'RejectCircularImports'}
    for row in lock['rows']:
        entries=observations[(row['platform'],row['id'],byprofile[row['profile']])];values={}
        for unit,value in entries:
            for key,item in flatten(value).items():values.setdefault(key,[]).append((unit,item))
        require(set(values)==set(row['fields']),'Native field inventory')
        require(flatten(row['observation'])=={k:v['value'] for k,v in row['fields'].items()},'Native observation/fields binding')
        for field,pin in row['fields'].items():
            require(all(v==pin['value'] for _,v in values[field]) and sorted({u for u,_ in values[field]})==pin['units'] and len(pin['units'])>=2,'Native independent field passes')
        for diag in row['observation']['diagnostics']:require({'endLine','endColumn'}<=diag.keys(),'Native omitted end coordinates')
    return lock

def check_selected(bundle,contract,lock,entry):
    actual=bundle.json(entry['raw']);platform=entry['platform'];rows=normalize(actual['rows'],entry['fixtureRoot'])
    require(len(rows)==57 and len({(r['id'],r['profile']) for r in rows})==57,'Selected row inventory')
    expected_native={(r['id'],r['profile']):r['observation'] for r in lock['rows'] if r['platform']==platform}
    for row in rows:
        observed=row['observation'];key=row['id'],row['profile'];expected=native_projection(expected_native[key])
        require({k:v for k,v in observed.items() if k!='traces'}==expected,'Selected native projection '+str(key))
        case=next(c for c in contract['cases'] if c['id']==row['id']);sep='\\' if platform=='windows' else '/';prefix='<fixtures>'+sep+case['id']+sep
        path=lambda p:prefix+p.replace('/',sep)
        traces=[]
        for t in case['traces'][row['profile']]:
            require(2<=len(t['nodes'])<=17 and len(t['edges'])==len(t['nodes'])-1 and t['nodes'][t['cycleStartIndex']]==t['nodes'][-1],'Trace invariant')
            for i,e in enumerate(t['edges']):require(e['owner']==t['nodes'][i] and e['target']==t['nodes'][i+1],'Trace edge continuity')
            traces.append(dict(nodes=[path(n) for n in t['nodes']],edges=[dict(owner=path(e['owner']),target=path(e['target']),line=e['line'],column=e['column']) for e in t['edges']],
                cycleStartIndex=t['cycleStartIndex'],profile=row['profile'],diagnosticIndices=t['diagnosticIndices']))
        require(observed['traces']==traces,'Selected trace '+str(key))
    expected_origin=bundle.proof['jar']['path'] if platform=='windows' else '/product.jar'
    require(bundle.text(entry['origin']).strip()=='PRODUCT_ORIGIN\t'+expected_origin+'\t'+bundle.proof['jar']['sha256'],'Selected actual loaded origin')

def check_inherited(bundle):
    p=bundle.proof;inherited=p['inherited'];jarsha=p['jar']['sha256'];native=bundle.json(inherited['nativeContract'])
    for entry in inherited['items']:
        raw=bundle.json(entry['raw']);platform=entry['platform'];require(raw['scenarioCount']==len(raw['rows'])==42,'Inherited item count')
        actual=normalized(raw['rows'],raw['root']);expected=native['models'][platform]
        require(len(actual)==len(expected)==42 and [r['id'] for r in actual]==[r['id'] for r in expected],'Inherited item inventory')
        require(all(selected_native(e)==selected_product(a) for e,a in zip(expected,actual)),'Inherited native item semantics')
    private=[line for d in inherited['privateRows'] for line in bundle.text(d).splitlines()]
    require(len(private)==61 and all('\tPASS\t' in line for line in private),'Inherited private rows')
    require({r.split('-',1)[0] for r in private if r.startswith('IR')}=={'IR'+str(i).zfill(2) for i in range(1,15)},'Inherited 14 private groups')
    supplement=bundle.text(inherited['supplement']).splitlines();require(len(supplement)==4 and all('\tPASS\t' in r for r in supplement),'Supplement four')
    for entry in inherited['sort']:sort_result(bundle.json(entry['raw']),jarsha)
    for entry in inherited['boundary']:boundary_result([json.loads(line) for line in bundle.text(entry['raw']).splitlines()],jarsha,entry['platform'])
    require(bundle.text(inherited['sortCase'])=='fileAlias\tfalse\n' and bundle.text(inherited['boundaryCase'])=='directoryAlias\tfalse\n','Inherited regression case profiles')
    lines=bundle.text(inherited['itemsCase']).splitlines();require(len(lines)==42 and all(r.endswith('\tfalse\tfalse') for r in lines),'Inherited item case profile')
    stable=[]
    for entry in inherited['stable']:
        lines=bundle.text(entry['actual']).splitlines()
        if entry['name']=='import-path-results.tsv':lines.remove('NEG-dynamic-import\tNATIVE_IMPORT_PATH_MATCH\tSUCCESS')
        stable+=lines
    golden=bundle.text(inherited['stableGolden']).splitlines()
    require(len(stable)==len(golden)==94,'Stable94 inventory')
    require([(a,b) for a,b in zip(golden,stable) if a!=b]==[('NEG-items\tPROFILE_REJECT\tUNSUPPORTED_ELEMENT','NEG-items\tNATIVE_ITEM_TRANSITION_EMPTY\tSUCCESS')],'Sole NEG-items transition')
    for pair in inherited['unchanged']:require(bundle.text(pair['actual'])==bundle.text(pair['prior']),'Inherited unchanged row data')
    require('PASS_ORDERING_308 nativeSuccess=220 mappedErrors=81 restrictions=7' in bundle.text(inherited['ordering']) and 'M1-warning-before-error' in bundle.text(inherited['ordering']),'Ordering308/M1')
    require('PASS_BOOLEAN_CORPUS nativeIds=297 privateInputs=16 privateGroups=14' in bundle.text(inherited['boolean']),'Boolean297/private16/control14')

def check(proof_path,proof_sha,jar,source_root):
    bundle=Bundle(proof_path,proof_sha);p=bundle.proof
    for d in descriptors(p):bundle.raw(d)
    for name,pin in p['readerFiles'].items():require(digest((Path(__file__).parent/name).read_bytes())==pin,'Reader dependency bytes '+name)
    require(Path(jar).is_file() and digest(Path(jar).read_bytes())==p['jar']['sha256'],'Qualified explicit JAR required')
    root=Path(source_root)/'dotj-build/evaluation-candidate/src';sources={f.relative_to(root).as_posix():f for f in root.rglob('*.java')}
    require(set(sources)==set(p['source']),'Current source closure')
    for name,pin in p['source'].items():require(digest(sources[name].read_bytes().replace(b'\r\n',b'\n'))==pin['canonicalSha256'],'Current source bytes '+name)
    with zipfile.ZipFile(jar) as archive:
        require({n:digest(archive.read(n)) for n in archive.namelist() if n.endswith('.class')}==p['classes'],'Product class inventory')
    for d in p['consumers']:
        with zipfile.ZipFile(io.BytesIO(bundle.raw(d))) as z:
            require(not any(n.rsplit('/',1)[-1].split('$')[0].removesuffix('.class') in ('ProjectEvaluationComponent','ItemEvaluator','ItemExpressions','ItemGlobs','ItemSnapshot') for n in z.namelist()),'Consumer embeds product class')
    expected_names={'native-compile-v1','product-build-v1','abi-v1'}
    expected_names.update(f'native-{platform}-{profile}-{passno}-v1' for platform in ('windows','linux') for profile in ('default','record_duplicates','reject_circular') for passno in (1,2))
    expected_names.update(f'{mode}-{platform}-final-v1' for mode in ('selected','private') for platform in ('windows','linux'))
    expected_names.update('inherited-'+g+'-windows-v1' for g in ('items','private','junction','supplement','sort','boundary','history'))
    expected_names.update('inherited-'+g+'-linux-v1' for g in ('items','private','sort','boundary'))
    require({e['name'] for e in p['executions']}==expected_names and len(p['executions'])==len(expected_names),'Complete executed obligation inventory')
    actual_outputs=set();byname={}
    for entry in p['executions']:
        r=bundle.json(entry['receipt']);require(r['status']=='PASS','Execution not PASS')
        byname[entry['name']]=r
        actual_outputs.update(d['sha256'] for d in r.get('outputs',[]))
        actual_outputs.update(o[s]['sha256'] for o in r['operations'] for s in ('stdout','stderr'))
        require(len(r['operations'])==len(entry['expectedOperations']),'Operation inventory')
        for op,pin in zip(r['operations'],entry['expectedOperations']):process(op,pin)
        if 'container' in r:owned_container(r['container'])
        for sample in r['resources']:require(sample['freePhysicalBytes']>=512*1024**2 and sample['freeVirtualBytes']>=16*1024**3,'Resource floor')
        for op in r['operations']:
            argv=op['process']['argv']
            if Path(argv[0]).name.lower()=='java.exe':
                expected_jar=p['abi']['baselineJar']['path'] if entry['name']=='abi-v1' and op['label']=='baseline-legacy' else p['jar']['path']
                require('--module-path' in argv and argv[argv.index('--module-path')+1]==expected_jar,'Runtime uses qualified JAR')
    history=next(e for e in p['executions'] if e['name']=='inherited-history-windows-v1')
    require([o['label'] for o in history['expectedOperations']]==p['historyGroups'] and len(p['historyGroups'])==14,'All 14 retained runtime groups')
    old=bundle.json(p['contractOriginal']);contract=bundle.json(p['contract']);expected=copy.deepcopy(old)
    count=0
    for case in expected['cases']:
        for traces in case['traces'].values():
            for trace in traces:
                for edge in trace['edges']:edge['column']-=1;count+=1
    require(expected==contract and count==190,'Only adopted coordinate amendment')
    for case in contract['cases']:
        for name,pin in case['files'].items():require(digest(base64.b64decode(pin['base64']))==pin['sha256'],'Frozen fixture bytes')
    lock=check_native(bundle,contract)
    require({e['platform'] for e in p['selected']}=={'windows','linux'},'Both selected platforms')
    for entry in p['selected']:
        require(entry['raw']['sha256'] in actual_outputs and entry['origin']['sha256'] in actual_outputs,'Selected execution binding')
        check_selected(bundle,contract,lock,entry)
    wanted={c['id'] for c in contract['controls']} - {'CC12-proof-binding','CC13-relocation'}
    require({e['platform'] for e in p['private']}=={'windows','linux'} and len(p['private'])==2,'Both private platforms')
    for entry in p['private']:
        require(entry['raw']['sha256'] in actual_outputs and entry['origin']['sha256'] in actual_outputs,'Private execution binding')
        require(set(bundle.json(entry['raw'])['groups'])==wanted,'Private control groups')
        expected_origin=p['jar']['path'] if entry['platform']=='windows' else '/product.jar'
        require(bundle.text(entry['origin']).strip()=='PRODUCT_ORIGIN\t'+expected_origin+'\t'+p['jar']['sha256'],'Private loaded origin')
    for pair in p['abi']['pairs']:require(bundle.raw(pair['baseline'])==bundle.raw(pair['successor']),'Legacy javap ABI')
    require('PASS\tCC06-abi' in bundle.text(p['abi']['consumer']),'Old compiled legacy consumer')
    inherited=p['inherited']
    output_descriptors=[e['raw'] for family in ('items','sort','boundary') for e in inherited[family]]
    output_descriptors+=inherited['privateRows']+[inherited['supplement'],inherited['ordering'],inherited['boolean']]
    output_descriptors += [e['actual'] for family in ('stable','unchanged') for e in inherited[family]]
    require(all(d['sha256'] in actual_outputs for d in output_descriptors),'Inherited actual output binding')
    red=bundle.json(p['baselineRed']);require(red['status']=='PASS' and red['expectedFeatureRed'],'Actual packaged baseline RED')
    redop=next(o for o in red['operations'] if o['label']=='consumer')
    require(redop['process']['exitCode']!=0 and 'FEATURE_RED: required trace-aware sidecar absent' in bundle.text(redop['stderr']),'Baseline RED reason')
    check_inherited(bundle)
    require(bundle.json(p['legacyResult'])['evidenceFiles']==1760 and p['legacyProof']['sha256']=='1165c51b1c2d6f2fcc952d26dc6a7e8ee242696d483238a4bfe1ee8cb8738aa5','1760 historical lineage')
    return dict(status='PASS_BOUNDED_PRIVATE_CYCLE_TRACE',graphs=19,profiles=3,platforms=2,nativeRowPasses=228,
        selectedRows=114,privateGroups=14,inheritedItemsPerPlatform=42,inheritedPrivateRows=61,historyGroups=14,stableRows=94,
        legacyEvidenceFiles=1760,evidenceObjects=len(bundle.cache),acceptedTasksAdded=0)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for field in ('proof','sha256','jar','source-root'):parser.add_argument('--'+field,required=True)
    a=parser.parse_args();print(json.dumps(check(a.proof,a.sha256,a.jar,a.source_root)))
