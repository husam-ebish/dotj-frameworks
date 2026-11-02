"""Separate PURE recovery certificate, never admission for a runtime launch.

Future native_runner still calls the unchanged full inside-parent verifier.
Every unique descriptor is hashed by an independently bounded worker; explicit
semantic/inventory stages cover both exact locks, archives, reuse and fixtures.
"""
import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
p=load('segmented_closure_protocol',Path(__file__).with_name('protocol.py'))
h=load('segmented_closure_history',p.HERE/'history.py')
ROOT=p.A/'fix2-segmented-closure-v1'
OLD='35ef28faf73f6dd31596867f724c37ec5050163ad47ac18775ab362f6901897e'
SNAP='f3d1247be34b2267e062d09a2b64e9e7f24162d84e743622a2ebc372d96b6399'

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def fresh(path,value):
    with Path(path).open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
def metadata(execution):
    lockpath=p.HERE/'execution-lock.json';p.require(p.sha(lockpath)==execution,'current exact lock')
    lock=p.read(lockpath);c=p.read(p.HERE/'first-capture-predecessor.json');p.require(c['snapshot']['sha256']==SNAP and c['executionLockSha256']==OLD,'closed predecessor snapshot/lock')
    p.pin(c['snapshot']);snapshot=p.read(c['snapshot']['path']);entries=snapshot['profileEntries']
    oldentry=next(e for e in entries if e['repositoryRelativePath'].endswith('/execution-lock.json'));p.pin(oldentry['archived']);p.require(oldentry['archived']['sha256']==OLD,'exact archived old lock')
    old=p.read(oldentry['archived']['path'])
    def resolved(d,tiers):
        for tier in tiers:
            matches=[e['archived'] for e in tier if p.same(e['original'],d)]
            if matches:
                p.require(len(matches)==1,'one exact descriptor in selected archive tier');return matches[0]
        return d
    current_archive_d=lock['archiveLock'];p.pin(current_archive_d);archive=p.read(current_archive_d['path'])
    p.pin(archive['oldArchive']);older=p.read(archive['oldArchive']['path'])
    tiers=[entries,archive['entries'],older['entries']]
    def read_old(key):
        d=resolved(old[key],tiers);p.pin(d);return p.read(d['path']),d
    payload=p.read(lock['payloadLock']['path']);p.pin(lock['payloadLock']);oldpayload,oldpayload_d=read_old('payloadLock')
    p.require(p.same(payload,oldpayload),'unchanged complete old/current payload definitions')
    manifest=p.read(lock['manifest']['path']);p.pin(lock['manifest']);oldmanifest,oldmanifest_d=read_old('manifest')
    reuse=p.read(lock['reuseChain']['path']);p.pin(lock['reuseChain']);oldreuse,_=read_old('reuseChain');p.require(p.same(reuse,oldreuse),'unchanged exact binary reuse chain')
    return dict(lock=lock,old=old,c=c,snapshot=snapshot,archive=archive,older=older,tiers=tiers,resolved=resolved,payload=payload,manifest=manifest,oldmanifest=oldmanifest,oldmanifestDescriptor=oldmanifest_d,reuse=reuse)

def build_plan(execution):
    m=metadata(execution);descriptors=[];by_path={};references=0
    def add(d,role,resolve=False):
        nonlocal references
        p.check_descriptor(d);original=d
        if resolve:d=m['resolved'](d,m['tiers'])
        p.check_descriptor(d);references+=1
        if d['path'] in by_path:
            row=descriptors[by_path[d['path']]];p.require(p.same(row['descriptor'],d),'no conflicting descriptor/path silently deduplicated')
        else:
            by_path[d['path']]=len(descriptors);row=dict(id=len(descriptors),descriptor=d,requiredBy=[]);descriptors.append(row)
        row['requiredBy'].append(dict(role=role,original=original))
    add(p.descriptor(p.HERE/'execution-lock.json'),'current-lock');add(m['c']['snapshot'],'old-snapshot')
    for tag,lock in [('current',m['lock']),('predecessor',m['old'])]:
        for index,d in enumerate(lock['pins']):add(d,f'{tag}.pins[{index}]',tag=='predecessor')
        for key in ['payloadLock','archiveLock','reuseChain','proposal','selectedSchema','manifest','transitionLedger']:add(lock[key],tag+'.'+key,tag=='predecessor')
    for tag in ['current','predecessor']:
        for i,d in enumerate(m['payload']['files']):add(d,f'{tag}.payload[{i}]')
    for tag,entries in [('current-archive',m['archive']['entries']),('old14',m['older']['entries']),('old-profile',m['snapshot']['profileEntries'])]:
        for i,e in enumerate(entries):
            add(e['archived'],f'{tag}[{i}].raw')
            if e['gitBlob'] is not None:add(e['gitBlob'],f'{tag}[{i}].git')
    for tag,entries in [('actual-capture',m['snapshot']['actualCaptureEntries']),('previous-evidence',m['snapshot']['preservedEvidence'])]:
        for i,e in enumerate(entries):add(e['original'],f'{tag}[{i}].original');add(e['archived'],f'{tag}[{i}].archived')
    reuse=m['reuse']
    for key in ['source','runtimeconfig','dll','compiledLock','compileProof','controllerProof','compilerProposal']:add(reuse[key],'reuse.'+key,True)
    for i,d in enumerate(reuse['pins']):add(d,f'reuse.pins[{i}]',True)
    proposal=p.read(reuse['compilerProposal']['path']);compiled=p.read(reuse['compiledLock']['path'])
    for i,d in enumerate([proposal['source'],proposal['runtimeconfig']]+proposal['compilerReferences']+proposal['compilerInputs']):add(d,f'compiler-request[{i}]',True)
    for key in ['compileProof','controllerProof']:
        proof=p.read(reuse[key]['path'])
        for stream,d in proof['raw'].items():add(d,key+'.raw.'+stream,True)
        add(proof['review'],key+'.review',True)
    add(compiled['review'],'compiled-review',True)
    stages=[]
    for index,start in enumerate(range(0,len(descriptors),128)):
        stages.append(dict(id=f'descriptors-{index:03}',kind='DESCRIPTORS',descriptorIds=list(range(start,min(start+128,len(descriptors))))))
    for kind in ['SCALAR_SCHEMA','ARCHIVE_RELATIONS','BINARY_REUSE','CURRENT_FIXTURES','ARCHIVED_FIXTURES','CAPTURE_SEMANTICS']:stages.append(dict(id=kind.lower().replace('_','-'),kind=kind))
    inventories=[dict(id='profile',root=str(p.HERE),files=sorted([*m['lock']['profileInventory'],str(p.HERE/'execution-lock.json')]))]
    for i,root in enumerate(m['payload']['roots']):inventories.append(dict(id=f'payload-{i}',root=root,files=sorted(d['path'] for d in m['payload']['files'] if Path(d['path']).is_relative_to(Path(root)))))
    oldroot=Path(m['oldmanifestDescriptor']['path']).parent
    inventories.append(dict(id='archived-profile',root=str(oldroot),files=sorted(e['archived']['path'] for e in m['snapshot']['profileEntries'])))
    for i,root in enumerate(m['snapshot']['actualCaptureRoots']):inventories.append(dict(id=f'actual-capture-{i}',root=root,files=sorted(e['original']['path'] for e in m['snapshot']['actualCaptureEntries'] if Path(e['original']['path']).is_relative_to(Path(root)))))
    for inv in inventories:stages.append(dict(id='final-inventory-'+inv['id'],kind='FINAL_INVENTORY',inventory=inv))
    return dict(schemaVersion=1,status='FROZEN_SEGMENTED_PURE_CLOSURE_PLAN_NOT_RUNTIME_ADMISSION',correctedExecutionLockSha256=execution,predecessorExecutionLockSha256=OLD,snapshot=m['c']['snapshot'],descriptors=descriptors,requiredDescriptorReferences=references,uniqueDescriptorCount=len(descriptors),stages=stages,pureWorkerLimitSeconds=120,workloadLimitsUnchanged=True,futureRuntimeAdmissionCredit=False)

def initialize(execution):
    p.require(not ROOT.exists(),'fresh segmented plan only');plan=build_plan(execution);ROOT.mkdir();fresh(ROOT/'plan.json',plan);return p.descriptor(ROOT/'plan.json')

def plan_read(plan_sha):
    p.require((ROOT/'plan.json').is_file() and p.sha(ROOT/'plan.json')==plan_sha,'external frozen plan digest')
    plan=p.read(ROOT/'plan.json');p.require(plan['predecessorExecutionLockSha256']==OLD and plan['snapshot']['sha256']==SNAP and p.sha(p.HERE/'execution-lock.json')==plan['correctedExecutionLockSha256'],'old/new lock and snapshot plan binding');return plan

def semantic(kind,m):
    if kind=='SCALAR_SCHEMA':
        for lock in [m['lock'],m['old']]:
            p.keys(lock,['schemaVersion','status','profileInventory','pins','payloadLock','archiveLock','reuseChain','proposal','selectedSchema','manifest','transitionLedger'],'closed execution lock')
            p.require(type(lock['schemaVersion']) is int and lock['schemaVersion']==1 and lock['status']=='PREPARATION_FROZEN_NOT_LAUNCHED','exact lock scalar/status')
        p.require(set(m['old']['profileInventory'])=={e['original']['path'] for e in m['snapshot']['profileEntries'] if not e['repositoryRelativePath'].endswith('/execution-lock.json')},'old exact snapshot inventory')
        p.manifest(m['manifest']);p.manifest(m['oldmanifest']);p.require(p.same(m['manifest'],m['oldmanifest']),'unchanged entire308-case manifest')
        schema=p.read(m['lock']['selectedSchema']['path']);p.pin(schema['emitter']);p.pin(schema['validator'])
        lines=Path(schema['emitter']['path']).read_text().splitlines()
        for field in schema['fields']:
            if field['availability']=='EMITTED':p.require(field['emitterLines'] and all(field['emitterText'] in lines[n-1] for n in field['emitterLines']),'exact emitted schema source anchors')
            else:p.require(field['path']=='ProjectError.stack' and field['availability']=='UNAVAILABLE_IN_REUSED_BINARY','only adopted unavailable field')
        return dict(currentAndOldLockScalars=True,manifestCases=len(m['manifest']['cases']),fieldTemplates=len(schema['fields']))
    if kind=='ARCHIVE_RELATIONS':
        count=0
        for entries in [m['archive']['entries'],m['older']['entries'],m['snapshot']['profileEntries']]:
            for e in entries:
                p.require(e['original']['sha256']==e['archived']['sha256'] and e['original']['sizeBytes']==e['archived']['sizeBytes'],'exact raw archive link')
                if e['gitBlob'] is not None and e['workingVsGitRelation']=='EXACT_RAW':p.require(e['gitBlob']['sha256']==e['archived']['sha256'] and e['gitBlob']['sizeBytes']==e['archived']['sizeBytes'],'exact raw/Git relation')
                elif e['gitBlob'] is not None and e['workingVsGitRelation']=='WORKTREE_CRLF_VS_GIT_LF':p.require(Path(e['archived']['path']).read_bytes().replace(b'\r\n',b'\n')==Path(e['gitBlob']['path']).read_bytes(),'explicit archived CRLF/Git LF relation')
                count+=1
        return dict(archiveEntriesChecked=count)
    if kind=='BINARY_REUSE':return h.verify_reuse(m['reuse'],m['archive']['entries']+m['older']['entries'])
    if kind=='CURRENT_FIXTURES':p.fixtures(m['manifest'],p.HERE/'fixtures');return dict(fixtureFiles=sum(len(c['files']) for c in m['manifest']['cases']))
    if kind=='ARCHIVED_FIXTURES':p.fixtures(m['oldmanifest'],Path(m['oldmanifestDescriptor']['path']).parent/'fixtures');return dict(fixtureFiles=sum(len(c['files']) for c in m['oldmanifest']['cases']))
    if kind=='CAPTURE_SEMANTICS':
        finalizer=load('segmented_capture_semantics',p.HERE/'finalize_first_capture.py');c=finalizer.contract();plan=next(v for v in p.read(c['oldProposal']['path'])['invocations'] if v['phase']==finalizer.PHASE);out=Path(plan['output'])
        return finalizer.validate_documents(p.read(p.A/'controllers/pass1-part01/parent-receipt.json'),p.read(out/'receipt.json'),p.read(c['coordination']['path']),p.read(c['approval']['path']),plan,p.read(out/'native.stdout'),p.bounded(out/'native.stderr',524288))
    raise ValueError('unknown semantic stage')

def worker(plan_sha,stage_id):
    started=time.monotonic();plan=plan_read(plan_sha);matches=[s for s in plan['stages'] if s['id']==stage_id];p.require(len(matches)==1,'exact bounded stage')
    stage=matches[0];out=ROOT/stage_id;p.require(out.is_dir() and not (out/'result.json').exists(),'fresh stage result')
    if stage['kind']=='DESCRIPTORS':
        for i in stage['descriptorIds']:p.pin(plan['descriptors'][i]['descriptor'])
        evidence=dict(validatedDescriptorIds=stage['descriptorIds'])
    elif stage['kind']=='FINAL_INVENTORY':
        inv=stage['inventory'];actual=sorted(str(f) for f in Path(inv['root']).rglob('*') if f.is_file());p.require(actual==inv['files'],'complete final inventory '+inv['id']);evidence=dict(inventoryId=inv['id'],fileCount=len(actual),inventorySha256=hashlib.sha256(canonical(actual)).hexdigest())
    else:evidence=semantic(stage['kind'],metadata(plan['correctedExecutionLockSha256']))
    record=dict(schemaVersion=1,status='SEGMENTED_PURE_STAGE_VERIFIED',stage=stage,planSha256=plan_sha,correctedExecutionLockSha256=plan['correctedExecutionLockSha256'],predecessorExecutionLockSha256=OLD,startedMonotonic=started,finishedMonotonic=time.monotonic(),evidence=evidence,newExecutionCounts=dict(native=0,compiler=0,jvm=0,product=0))
    fresh(out/'result.json',record);print(stage_id,'VERIFIED')

def validate_descriptor_coverage(plan,coverage):
    p.require(type(plan['uniqueDescriptorCount']) is int and plan['uniqueDescriptorCount']>0,'typed positive descriptor count')
    p.require(p.same(coverage,list(range(plan['uniqueDescriptorCount']))) and len(set(coverage))==len(coverage),'complete coverage, no missing/duplicate/reordered/bool-alias descriptors')

def validate_stages(plan,plan_sha):
    receipts=[];results=[];coverage=[];last_finished=None
    for stage in plan['stages']:
        folder=ROOT/stage['id'];r=p.read(folder/'command-result.json');p.require(type(r['exitCode']) is int and r['exitCode']==0 and r['timedOut'] is False and r['timeoutSeconds']==120,'every pure stage actual bounded exit0, no retry')
        p.require(r['launched'] is True,'actual pure worker launch');p.integer(r['processId'],'pure worker PID',1)
        expected=[str(p.B/'toolchains/python-3.13.9/python.exe'),'-B',str(p.HERE/'segmented_closure.py'),'worker','--plan-sha256='+plan_sha,'--stage='+stage['id']]
        p.require(p.same(r['command'],expected) and r['cwd']==str(p.HERE),'exact pure stage argv/cwd')
        for key in ['stdout','stderr','result']:p.pin(r[key])
        p.require(r['result']['path']==str(folder/'result.json'),'exact stage result path')
        value=p.read(folder/'result.json');p.require(value['status']=='SEGMENTED_PURE_STAGE_VERIFIED' and p.same(value['stage'],stage) and value['planSha256']==plan_sha and value['correctedExecutionLockSha256']==plan['correctedExecutionLockSha256'] and value['predecessorExecutionLockSha256']==OLD,'exact old/new stage identity')
        p.require(p.same(value['newExecutionCounts'],dict(native=0,compiler=0,jvm=0,product=0)) and type(value['startedMonotonic']) in [int,float] and type(value['finishedMonotonic']) in [int,float] and 0<=value['finishedMonotonic']-value['startedMonotonic']<=120,'pure stage execution/duration')
        p.require(last_finished is None or last_finished<=value['startedMonotonic'],'actual ordered independent stage sequence');last_finished=value['finishedMonotonic']
        if stage['kind']=='DESCRIPTORS':p.require(p.same(value['evidence']['validatedDescriptorIds'],stage['descriptorIds']),'exact ordered per-stage coverage');coverage.extend(stage['descriptorIds'])
        if stage['kind']=='FINAL_INVENTORY':p.require(value['evidence']['inventorySha256']==hashlib.sha256(canonical(stage['inventory']['files'])).hexdigest(),'exact complete final inventory proof')
        receipts.append(p.descriptor(folder/'command-result.json'));results.append(value)
    validate_descriptor_coverage(plan,coverage)
    return receipts,results

def aggregate(plan_sha):
    plan=plan_read(plan_sha);p.require(p.same(plan,build_plan(plan['correctedExecutionLockSha256'])),'reconstructed same complete closure plan, no skipped assertion')
    receipts,results=validate_stages(plan,plan_sha)
    for row in plan['descriptors']:
        d=row['descriptor']
        if Path(d['path']).is_relative_to(p.HERE) and '/fixtures/' not in d['path'].replace('\\','/'):p.pin(d)
    # Final stages rechecked inventories after all byte/scalar checks. Recheck
    # exact lock and plan metadata identities here; no earlier certificate is
    # accepted by any runtime launch path.
    p.require(p.sha(p.HERE/'execution-lock.json')==plan['correctedExecutionLockSha256'] and p.sha(ROOT/'plan.json')==plan_sha,'completion lock/plan identities')
    proof=dict(schemaVersion=1,status='SEGMENTED_PURE_CLOSURE_COMPLETE_NOT_RUNTIME_ADMISSION',plan=p.descriptor(ROOT/'plan.json'),correctedExecutionLockSha256=plan['correctedExecutionLockSha256'],predecessorExecutionLockSha256=OLD,snapshot=plan['snapshot'],uniqueDescriptorsVerified=plan['uniqueDescriptorCount'],requiredDescriptorReferences=plan['requiredDescriptorReferences'],allStageReceipts=receipts,semanticStages=[r for r in results if r['stage']['kind']!='DESCRIPTORS'],allListedDescriptorsAndAssertionsCovered=True,finalInventoryRechecksComplete=True,pureWorkerLimitSeconds=120,futureRuntimeAdmissionCredit=False,retainedActualExecutionCounts=dict(native=1,controller=1),newExecutionCounts=dict(native=0,compiler=0,jvm=0,product=0),monolithicPassClaim=False,original180SecondRuntimeSuccessClaim=False)
    fresh(ROOT/'certificate.json',proof);return p.descriptor(ROOT/'certificate.json')

def verify_certificate(execution,d):
    p.pin(d);p.require(d['path']==str(ROOT/'certificate.json'),'fixed segmented PURE recovery certificate')
    proof=p.read(d['path']);p.require(proof['status']=='SEGMENTED_PURE_CLOSURE_COMPLETE_NOT_RUNTIME_ADMISSION' and proof['correctedExecutionLockSha256']==execution and proof['predecessorExecutionLockSha256']==OLD and proof['snapshot']['sha256']==SNAP and proof['futureRuntimeAdmissionCredit'] is False and proof['monolithicPassClaim'] is False and proof['original180SecondRuntimeSuccessClaim'] is False,'segmented recovery only, not runtime admission')
    p.pin(proof['plan']);plan=plan_read(proof['plan']['sha256']);p.require(p.same(plan,build_plan(execution)),'same complete old/current closure plan at finalization')
    receipts,results=validate_stages(plan,proof['plan']['sha256'])
    for row in plan['descriptors']:
        d=row['descriptor']
        if Path(d['path']).is_relative_to(p.HERE) and '/fixtures/' not in d['path'].replace('\\','/'):p.pin(d)
    p.require(p.same(receipts,proof['allStageReceipts']) and proof['uniqueDescriptorsVerified']==plan['uniqueDescriptorCount'] and proof['requiredDescriptorReferences']==plan['requiredDescriptorReferences'] and proof['allListedDescriptorsAndAssertionsCovered'] is True and proof['finalInventoryRechecksComplete'] is True,'exact completed full segmented closure')
    p.require(p.same(proof['retainedActualExecutionCounts'],dict(native=1,controller=1)) and p.same(proof['newExecutionCounts'],dict(native=0,compiler=0,jvm=0,product=0)),'typed actual/new execution counts')
    return proof

def main():
    parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument('action',choices=['plan','worker','aggregate']);parser.add_argument('--execution-lock-sha256');parser.add_argument('--plan-sha256');parser.add_argument('--stage');args=parser.parse_args()
    if args.action=='plan':print(json.dumps(initialize(args.execution_lock_sha256),indent=2))
    elif args.action=='worker':worker(args.plan_sha256,args.stage)
    else:print(json.dumps(aggregate(args.plan_sha256),indent=2))
if __name__=='__main__':main()
