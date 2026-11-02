"""Data-only closed b169 predecessor. No old source import/execution or stage replay."""
import collections,hashlib,importlib.util,json
from pathlib import Path
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=load('archived_context_protocol',Path(__file__).with_name('protocol.py'))
ownership=load('legacy_literal180_primitive',p.HERE/'ownership.py')
binding=load('explicit_historical_binding',p.HERE/'runtime_binding.py')
ROOT=p.A/'fix2-segmented-closure-v1'
B169='b169ee19d9ab31d67f04d04cc4fc2dcdd48343488374dbe29b794e2fd2e4caa7'
OLD_LOCK='35ef28faf73f6dd31596867f724c37ec5050163ad47ac18775ab362f6901897e'
OLD=OLD_LOCK
OLD_APPROVAL='cb65a3c2c6589e3fdc87e79211ee87d52daecb4e345c585023199b3b786c0f00'
PHASE='pass1-part01'
STDOUT='dc06bcabd4314d837474b493fd75ae4eb7d6aba40591958b9ac46c9480ea1ca0'
STDERR='5464b7438af0c57b897858b64a529d795cd209520a646654707b33bdde50d7a4'
CERT='49ee36c1304b643b7d5f1dba4ece7ba6a67ffc283969105e7f6c2029c66c7f67'
PROOF='1a0564188c408ef2070ddbe87f0312da0d7803676962a74112f764836de2d4b2'
REVIEW='c26ac873862bd69f0898dce69801e1b0ae3581cc1e4a3cdc1e2f8d2f4099a6ff'
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
class Context:
 def __init__(self):
  self.lineage=p.read(p.HERE/'accepted-b169-lineage-v1.json');p.pin(self.lineage['snapshot'])
  p.require(self.lineage['snapshot']['sha256']=='db5870c9d87f8573baa169d66f5c25bc97b6ecb129682f54a235805f938c29f8','exact root-audited b169 snapshot')
  self.snapshot=p.read(self.lineage['snapshot']['path']);self.entries=self.snapshot['profileEntries']
  p.require(len(self.entries)==354 and self.snapshot['executionLockSha256']==B169,'exact b169 context')
  p.pin(self.lineage['certificate']);p.require(self.lineage['certificate']['sha256']==CERT,'exact accepted certificate')
  certificate=p.read(self.lineage['certificate']['path']);p.pin(certificate['plan']);accepted_plan=p.read(certificate['plan']['path'])
  self.external={row['descriptor']['path']:row['descriptor'] for row in accepted_plan['descriptors']}
 def resolve(self,d):
  p.check_descriptor(d)
  if Path(d['path']).is_relative_to(p.HERE):
   matches=[e for e in self.entries if p.same(e['original'],d)];p.require(len(matches)==1,'one exact b169 path/hash/size mapping, no live substitution')
   e=matches[0];p.require(e['archived']['sha256']==d['sha256'] and e['archived']['sizeBytes']==d['sizeBytes'],'hash-equivalent archived mapping');p.pin(e['archived']);return e['archived']
  return p.pin(d)
 def logical_descriptor(self,path):
  path=str(path);matches=[e for e in self.entries if e['original']['path']==path];p.require(len(matches)==1,'one logical archived source identity');self.resolve(matches[0]['original']);return matches[0]['original']
 def read_json(self,path):
  if Path(path).is_relative_to(p.HERE):return p.read(self.resolve(self.logical_descriptor(path))['path'])
  p.require(str(path) in self.external,'nonprofile historical path has an exact accepted descriptor');p.pin(self.external[str(path)])
  return p.read(path)
 def metadata(self):
  lock=self.read_json(p.HERE/'execution-lock.json');p.require(self.logical_descriptor(p.HERE/'execution-lock.json')['sha256']==B169,'b169 lock identity')
  c=self.read_json(p.HERE/'first-capture-predecessor.json');p.pin(c['snapshot']);snapshot=p.read(c['snapshot']['path']);entries=snapshot['profileEntries']
  oldentry=next(e for e in entries if e['repositoryRelativePath'].endswith('/execution-lock.json'));p.pin(oldentry['archived']);p.require(oldentry['archived']['sha256']==OLD,'old35 closure identity');old=p.read(oldentry['archived']['path'])
  p.pin(lock['archiveLock']);archive=p.read(lock['archiveLock']['path']);p.pin(archive['oldArchive']);older=p.read(archive['oldArchive']['path']);tiers=[entries,archive['entries'],older['entries']]
  def resolved(d,tiers):
   for tier in tiers:
    candidates=[e['archived'] for e in tier if p.same(e['original'],d)]
    if candidates:p.require(len(candidates)==1,'unambiguous exact historical tier');return candidates[0]
   return d
  def oldread(k):
   d=resolved(old[k],tiers);p.pin(d);return self.read_json(d['path']),d
  payload=self.read_json(lock['payloadLock']['path']);oldpayload,_=oldread('payloadLock');p.require(p.same(payload,oldpayload),'unchanged accepted old/current payload definition')
  manifest=self.read_json(lock['manifest']['path']);oldmanifest,oldmanifest_d=oldread('manifest');reuse=self.read_json(lock['reuseChain']['path']);oldreuse,_=oldread('reuseChain');p.require(p.same(reuse,oldreuse),'unchanged accepted reuse definition')
  return dict(lock=lock,old=old,c=c,snapshot=snapshot,archive=archive,older=older,tiers=tiers,resolved=resolved,payload=payload,manifest=manifest,oldmanifest=oldmanifest,oldmanifestDescriptor=oldmanifest_d,reuse=reuse)
def context():return Context()
def reconstruct_plan(ctx):
    execution=B169;m=ctx.metadata();descriptors=[];by_path={};references=0
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
    add(ctx.logical_descriptor(p.HERE/'execution-lock.json'),'current-lock');add(m['c']['snapshot'],'old-snapshot')
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
    proposal=ctx.read_json(reuse['compilerProposal']['path']);compiled=ctx.read_json(reuse['compiledLock']['path'])
    for i,d in enumerate([proposal['source'],proposal['runtimeconfig']]+proposal['compilerReferences']+proposal['compilerInputs']):add(d,f'compiler-request[{i}]',True)
    for key in ['compileProof','controllerProof']:
        proof=ctx.read_json(reuse[key]['path'])
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

def environment(out):
    dotnet=p.B/'toolchains/dotnet';out=Path(out)
    env={'SystemRoot':r'C:\Windows','WINDIR':r'C:\Windows','ComSpec':r'C:\Windows\System32\cmd.exe',
         'PATH':str(dotnet)+r';C:\Windows\System32','TEMP':str(out/'tmp'),'TMP':str(out/'tmp'),
         'HOME':str(out/'home'),'USERPROFILE':str(out/'home'),'HOMEDRIVE':'D:','HOMEPATH':str(out/'home')[2:],
         'APPDATA':str(out/'home/AppData/Roaming'),'LOCALAPPDATA':str(out/'home/AppData/Local'),
         'DOTNET_ROOT':str(dotnet),'DOTNET_MULTILEVEL_LOOKUP':'0','DOTNET_ROLL_FORWARD':'Disable',
         'DOTNET_CLI_HOME':str(out/'home'),'DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','DOTNET_CLI_TELEMETRY_OPTOUT':'1',
         'DOTNET_NOLOGO':'1','DOTNET_CLI_UI_LANGUAGE':'en-US','VSLANG':'1033','MSBUILDDISABLENODEREUSE':'1',
         'MSBUILD_EXE_PATH':str(dotnet/'sdk/10.0.401/MSBuild.dll'),'MSBUILDUSEREXTENSIONSPATH':str(out/'home/msbuild-user'),
         'DOTNET_GCHeapHardLimit':'8000000','DOTNET_gcServer':'0','DOTNET_PROCESSOR_COUNT':'2','DOTNET_EnableDiagnostics':'0',
         'NUGET_PACKAGES':str(out/'cache/nuget'),'NUGET_HTTP_CACHE_PATH':str(out/'cache/http'),
         'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PYTHONUTF8':'1','DOTNET_HOST_TRACE':'1','DOTNET_HOST_TRACE_VERBOSITY':'3'}
    return env
def failed_parent_process(proc,argv,root):
    # Deliberately separate from successful process_receipt. No altered exit
    # value is ever passed to the success validator, returned or serialized.
    p.require(type(proc) is dict and p.same(proc.get('argv'),argv) and proc.get('cwd')==str(root),'predecessor parent exact argv/cwd')
    for key,wanted in [('timeoutSeconds',180),('cleanupLimitSeconds',5),('exitCode',1)]:p.require(type(proc.get(key)) is int and proc[key]==wanted,'predecessor parent '+key)
    for key in ['launched','jobAssigned','resumed']:p.require(proc.get(key) is True,'predecessor parent '+key)
    for key in ['timedOut','outputLimitExceeded']:p.require(proc.get(key) is False,'predecessor parent '+key)
    p.require(proc.get('error') is None and proc.get('cleanupError') is None,'predecessor parent has no runtime/cleanup error')
    p.integer(proc.get('processId'),'parent PID',1)
    p.require(proc.get('outputProfile')=='controller' and p.same(proc.get('outputLimitsBytes'),dict(stdout=2097152,stderr=524288)) and type(proc.get('outputPollSeconds')) in [int,float] and proc['outputPollSeconds']==0.1,'parent unchanged output caps/poll')
    p.require(type(proc.get('cleanupSeconds')) in [int,float] and 0<=proc['cleanupSeconds']<=5 and type(proc.get('seconds')) in [int,float] and 0<proc['seconds']<=185,'parent actual duration/cleanup bounds')

def validate_documents(ctx,parent,child,coord,approval,plan,value,raw):
    c=ctx.read_json(p.HERE/'first-capture-predecessor.json');oldproposal=ctx.read_json(c['oldProposal']['path']);oldplan=next(v for v in oldproposal['invocations'] if v['phase']==PHASE)
    p.require(p.same(plan,oldplan),'exact predecessor case/input/argv/environment plan')
    p.require(parent['phase']==child['phase']==coord['phase']==PHASE and parent['executionLockSha256']==child['executionLockSha256']==coord['executionLockSha256']==OLD_LOCK,'closed predecessor phase/lock')
    p.require(parent['reviewSha256']==coord['approvalSha256']==OLD_APPROVAL and child['review']==c['approval'],'closed predecessor approval')
    p.approval(approval,OLD_LOCK,PHASE)
    p.require(type(approval['invocationCountApproved']) is int and approval['invocationCountApproved']==1,'one predecessor invocation only')
    expected_error='runtime host trace binding '+oldproposal['fingerprint']['corePath']
    p.require(parent['status']==child['status']=='FATAL_OR_CLEANUP_FAILURE' and p.same(parent['failure'],dict(type='ValueError',message='process complete/cleanup')) and p.same(child['failure'],dict(type='ValueError',message=expected_error)) and parent['innerReceipt'] is None,'only exact original metadata failure accepted')
    p.require(p.same(parent['controllerExecutions'],dict(state='KNOWN',value=1)) and p.same(child['nativeExecutions'],dict(state='KNOWN',value=1)),'actual retained launch counts, never false zero/unknown')
    p.require(type(child['newCompilerExecutions']) is int and child['newCompilerExecutions']==0,'zero predecessor new compiles')
    p.require(coord['status']=='TERMINAL_NONZERO_INSPECT_NO_RETRY' and coord['commandInvoked'] is True and type(coord['exitCode']) is int and coord['exitCode']==1 and coord['nativeExecutions'] is None,'original coordinator failure/unknown retained')
    p.require(coord['reviewSha256']=='a04700d518b720f174e170c901dcb846a5f1bbcceb881540ce94b06884b68d08' and coord['adjudicationSha256']==c['adjudication']['sha256'] and coord['sourceSha256']==c['coordinatorSource']['sha256']=='94f463e4225c3dd8eda61ee812a42984b8e7b3c99eb984261ffa6b803ddf2dbe','coordinator old reviewed source/adjudication')
    out=Path(plan['output']);root=p.A/'controllers'/PHASE
    outerargv=[str(p.B/'toolchains/python-3.13.9/python.exe'),'-B',str(p.HERE/'native_runner.py'),'--phase='+PHASE,'--execution-lock-sha256='+OLD_LOCK,'--review-sha256='+OLD_APPROVAL]
    p.require(p.same(coord['command'],outerargv),'actual old outer command')
    innerargv=[str(p.B/'toolchains/python-3.13.9/python.exe'),'-B',str(p.HERE/'native_runner.py'),'--inner','--phase='+PHASE,'--execution-lock-sha256='+OLD_LOCK,'--review-sha256='+OLD_APPROVAL,'--ownership-handle='+str(parent['ownershipPipeHandle'])]
    failed_parent_process(parent['process'],innerargv,root);p.process_receipt(child['process'],plan['nativeArgv'],out,30,'runtime')
    p.require(p.same(parent['environment'],environment(root)) and p.same(child['environment'],plan['environment']),'exact original environments')
    deadline=parent['actualOuterDeadlineMonotonic'];envelope=child['ownershipEnvelope']
    p.require(p.same(parent['ownershipEnvelope'],envelope) and child['actualOuterDeadlineMonotonic']==deadline==parent['outerStartedMonotonic']+180==envelope['actualOuterDeadlineMonotonic'],'original owned deadline linkage')
    ownership.validate(envelope,phase=PHASE,execution=OLD_LOCK,review=OLD_APPROVAL,guard_sha=p.GUARD_SHA,parent_pid=envelope['parentPid'],child_pid=parent['process']['processId'],now=child['innerStartedMonotonic'])
    proof=child['ownershipProof'];p.keys(proof,['actualParentPid','actualChildPid','actualJobMembershipVerified','parentExecutable','duplicatedJobHandleClosed'],'actual predecessor ownership')
    p.require(proof['actualParentPid']==envelope['parentPid'] and proof['actualChildPid']==envelope['childPid'] and proof['actualJobMembershipVerified'] is True and proof['duplicatedJobHandleClosed'] is True and proof['parentExecutable']==str(p.B/'toolchains/python-3.13.9/python.exe'),'actual original OS parent/child/Job/duplicate closure')
    p.require(child['innerStartedMonotonic']+child['innerSeconds']<=deadline,'original inner completed inside owned deadline')
    p.require(type(child['resourceAdmissions']) is list and len(child['resourceAdmissions'])==1,'one actual predecessor admission')
    admission=child['resourceAdmissions'][0]
    p.require(admission['actualOuterDeadlineMonotonic']==deadline and type(admission['childSeconds']) is int and admission['childSeconds']==30 and admission['queryStartedMonotonic']<=admission['queryFinishedMonotonic']<=admission['decisionMonotonic'],'original admission timing/reserve')
    p.admission(deadline,admission['decisionMonotonic'],admission['queryStartedMonotonic'],admission['sample'],30)
    captured={d['path']:d for d in c['captureFiles']}
    for receipt,folder,label in [(parent,root,'controller'),(child,out,'native')]:
        p.keys(receipt['raw'],['stdout','stderr'],'original raw evidence')
        for stream in ['stdout','stderr']:
            path=str(folder/(label+'.'+stream));d=receipt['raw'][stream]
            p.require(path in captured and p.same(d,captured[path]),'closed original raw descriptor');p.pin(d)
            p.require(receipt['process'][stream+'Path']==path and type(receipt['process']['outputSizesBytes'][stream]) is int and receipt['process']['outputSizesBytes'][stream]==d['sizeBytes']<=(2097152 if stream=='stdout' else 524288),'raw path/size/output bound')
    p.require(type(raw) is bytes and hashlib.sha256(raw).hexdigest()==STDERR and len(raw)==298571,'exact original retained trace bytes')
    p.require(p.same(value,p.loads(p.bounded(out/'native.stdout',2097152))) and p.sha(out/'native.stdout')==STDOUT,'exact original retained native document')
    cases=ctx.read_json(plan['partitionManifest'])['cases'];ids=[v['id'] for v in cases];p.require(ids==plan['caseIds'] and len(ids)==72,'exact predecessor ordered72 case manifest')
    progress=p.progress(raw.decode('utf-8'),ids,True);p.require(p.same(child['progress'],[list(v) for v in progress]),'all144 exact original checkpoints')
    outcomes=p.observation(value,cases,oldproposal['fingerprint']);p.require(p.same(outcomes,child['outcomes']),'exact original typed outcome vector')
    p.require(dict(collections.Counter(outcomes))==dict(SUCCESS=56,PROJECT_ERROR=16),'closed original outcome count')
    p.require({f.relative_to(out/'fixtures').as_posix() for f in (out/'fixtures').rglob('*') if f.is_file()}=={f['relativePath'] for case in cases for f in case['files']},'exact original fixture inventory/no task marker')
    for case in cases:
        for f in case['files']:
            file=out/'fixtures'/f['relativePath'];p.require(not file.is_symlink() and p.sha(file)==f['sha256'] and file.stat().st_size==f['sizeBytes'],'original exact immutable fixture bytes')
    runtime=binding.verify_context(value,raw,ctx.read_json(p.HERE/'runtime-binding-contract.json'),ctx.read_json(p.HERE/'payload-lock.json'),ctx.read_json(p.HERE/'reuse-chain.json'),ctx.read_json(p.HERE/'execution-proposal.json')['fingerprint'])
    return dict(outcomeCounts=dict(collections.Counter(outcomes)),caseIds=ids,runtimeBinding=runtime,actualNativeExecutions=1,actualControllerExecutions=1,originalNativeExitCode=0,originalControllerExitCode=1,originalFailurePreserved=True)


def verify_accepted_first():
 ctx=context();lineage=ctx.lineage
 for key,sha in [('acceptedProof',PROOF),('acceptedReview',REVIEW),('certificate',CERT)]:
  p.require(lineage[key]['sha256']==sha,'closed qualified predecessor '+key);p.pin(lineage[key])
 proof=p.read(lineage['acceptedProof']['path']);review=p.read(lineage['acceptedReview']['path']);cert=p.read(lineage['certificate']['path']);plan=p.read(cert['plan']['path']);p.pin(cert['plan'])
 p.require(review['firstCaptureFinalizationApproved'] is True and review['correctedExecutionLockSha256']==B169 and review['predecessorExecutionLockSha256']==OLD and p.same(review['finalizationProof'],lineage['acceptedProof']),'exact existing independent finalization approval')
 p.require(proof['correctedExecutionLockSha256']==B169 and proof['predecessorExecutionLockSha256']==OLD and proof['phase']==PHASE and proof['validation']['originalControllerExitCode']==1 and proof['validation']['originalNativeExitCode']==0,'retained first180 metadata failure identity')
 for e in ctx.entries:
  p.pin(e['archived']);p.pin(e['gitBlob']);p.require(e['original']['sha256']==e['archived']['sha256']==e['gitBlob']['sha256'] and e['original']['sizeBytes']==e['archived']['sizeBytes']==e['gitBlob']['sizeBytes'],'all354 exact raw/Git historical sources')
 expected=reconstruct_plan(ctx);p.require(p.same(expected,plan),'same complete archived b169 plan, not live HERE')
 receipts,results=validate_stages(plan,cert['plan']['sha256'])
 p.require(len(receipts)==104 and plan['uniqueDescriptorCount']==11334 and plan['requiredDescriptorReferences']==20011 and p.same(receipts,cert['allStageReceipts']) and p.same(cert['semanticStages'],[r for r in results if r['stage']['kind']!='DESCRIPTORS']),'all accepted104 stage/scalar/inventory/reuse/archive/fixture/schema data, no replay')
 p.require(cert['allListedDescriptorsAndAssertionsCovered'] is True and cert['finalInventoryRechecksComplete'] is True and cert['futureRuntimeAdmissionCredit'] is False and p.same(cert['retainedActualExecutionCounts'],dict(native=1,controller=1)),'closed historical coverage/counters only')
 c=ctx.read_json(p.HERE/'first-capture-predecessor.json')
 for key in ['snapshot','oldProposal','oldRunner','coordinatorSource','approval','finding','adjudication','coordination']:p.pin(c[key])
 for d in c['captureFiles']:p.pin(d)
 proposal=ctx.read_json(c['oldProposal']['path']);caseplan=next(v for v in proposal['invocations'] if v['phase']==PHASE);out=Path(caseplan['output']);value=p.read(out/'native.stdout')
 actual=validate_documents(ctx,p.read(p.A/'controllers/pass1-part01/parent-receipt.json'),p.read(out/'receipt.json'),p.read(c['coordination']['path']),p.read(c['approval']['path']),caseplan,value,p.bounded(out/'native.stderr',524288))
 p.require(p.same(actual,proof['validation']),'same strict first72 legacy180/ownedJob/raw/fingerprint evidence')
 return dict(status='QUALIFIED_FIRST72_FROM_EXACT_ARCHIVED_B169_DATA',rows=len(value['rows']),originalParentExitCode=1,originalNativeExitCode=0,stageReceiptCount=len(receipts),uniqueDescriptors=11334,requiredReferences=20011,oldLock=OLD,acceptedLock=B169,acceptedProof=lineage['acceptedProof'],acceptedReview=lineage['acceptedReview'],certificate=lineage['certificate'],value=value,child=p.read(out/'receipt.json'),futureRuntimeAdmissionCredit=False,stageExecutions=0,nativeExecutions=0)
def approved_finalization(execution,review_sha):
 p.require(review_sha==REVIEW and p.sha(p.HERE/'execution-lock.json')==execution,'new current sourceLock separate from exact old review')
 result=verify_accepted_first();return result,result['value'],result['acceptedReview']
