"""Exact read-only reuse/history resolver. No imports of old producer modules."""
import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('ordering_protocol_history',Path(__file__).with_name('protocol.py'))
p=importlib.util.module_from_spec(s);s.loader.exec_module(p)

def historical_pin(d,entries):
    p.check_descriptor(d)
    path=Path(d['path'])
    if path.is_file() and not path.is_symlink() and p.same(p.descriptor(path),d):return d
    selected=p.resolve_history(d,entries);p.pin(selected);return selected

def retained_authorities(entries):
    """New exact resolver check; never runs/imports any historical producer."""
    old=p.B/'worktrees/dotj-build-boolean-conditions-v1/tools/oracle/dotj-build'
    authorities=[old/'condition-boolean-v1/native-input-lock.json',old/'condition-boolean-capture-v2/execution-lock.json',old/'condition-boolean-observer-v3/execution-lock.json',p.B/'validation/Batch-2516-boolean-product-green-v5/receipt.json']
    checked=[];unresolved=[]
    def walk(value,authority,pointer=''):
        if type(value) is dict:
            if set(value)=={'path','sha256','sizeBytes'}:
                try:
                    resolved=historical_pin(value,entries);checked.append(dict(authority=str(authority),pointer=pointer,original=value,resolved=resolved))
                except (ValueError,OSError) as error:unresolved.append(dict(authority=str(authority),pointer=pointer,descriptor=value,error=str(error)))
            else:
                for key,item in value.items():walk(item,authority,pointer+'/'+key)
        elif type(value) is list:
            for index,item in enumerate(value):walk(item,authority,pointer+'/'+str(index))
    for path in authorities:
        p.require(path.is_file(),'retained historical authority exists '+str(path));walk(p.read(path),path)
    return dict(schemaVersion=1,status='VERIFIED_READ_ONLY' if not unresolved else 'EXPLICIT_UNRESOLVED_DESCRIPTORS',authorities=[p.descriptor(x) for x in authorities],checked=checked,unresolved=unresolved,oldProducerInvocations=0)

def verify_reuse(chain,entries):
    p.keys(chain,['schemaVersion','status','pins','source','runtimeconfig','dll','compiledLock','compileProof','controllerProof','compilerProposal','historicalExecutionLockSha256','historicalCompilerExecutions','newCompilerExecutions'],'reuse chain')
    p.require(type(chain['schemaVersion']) is int and chain['schemaVersion']==1 and chain['status']=='HISTORICAL_BINARY_REUSE_NEW_NATIVE_NOT_LAUNCHED','reuse version/status')
    p.require(type(chain['historicalCompilerExecutions']) is int and chain['historicalCompilerExecutions']==1 and type(chain['newCompilerExecutions']) is int and chain['newCompilerExecutions']==0,'historical/new compile distinction')
    for d in chain['pins']:historical_pin(d,entries)
    for name in ['source','runtimeconfig','dll','compiledLock','compileProof','controllerProof','compilerProposal']:historical_pin(chain[name],entries)
    lock=p.read(chain['compiledLock']['path']);proof=p.read(chain['compileProof']['path']);controller=p.read(chain['controllerProof']['path']);proposal=p.read(chain['compilerProposal']['path'])
    p.require(lock['executionLockSha256']==proof['executionLockSha256']==chain['historicalExecutionLockSha256'],'historical execution identity')
    for name,key in [('rootCompileProof','compileProof'),('rootControllerProof','controllerProof'),('source','source'),('compilerProposal','compilerProposal')]:p.require(p.same(lock[name],chain[key]),'compiled historical '+name)
    p.require(lock['compilerExecutions']==1 and type(lock['compilerExecutions']) is int and lock['nativeExecutions']==0 and type(lock['nativeExecutions']) is int,'historical compiled lock counts')
    p.require(proof['compilerExecutions']==1 and proof['nativeExecutions']==0 and proof['status']=='COMPILED_PENDING_BINDING' and proof['failure'] is None,'historical proof status')
    proc=proof['process']
    p.require(p.process_outcome(proc)=='PROCESS_COMPLETE' and proc['argv']==proposal['argv'] and proc['cwd']==proposal['cwd'],'historical actual compiler process/argv')
    p.require(proc['timeoutSeconds']==30 and proc['outputLimitsBytes']=={'stdout':2097152,'stderr':2097152},'historical compiler bounds')
    p.require(controller['status']=='COMPLETE_PENDING_ROOT_REVIEW' and controller['failure'] is None and p.process_outcome(controller['process'])=='PROCESS_COMPLETE','historical owned outer controller')
    p.require(p.same(proof['artifacts'],lock['artifacts']) and p.same(lock['artifacts'],[chain['dll'],chain['runtimeconfig']]),'binary artifacts chain')
    count=0
    for d in [proposal['source'],proposal['runtimeconfig']]+proposal['compilerReferences']+proposal['compilerInputs']:
        historical_pin(d,entries);count+=1
    for r in [proof,controller]:
        for d in r['raw'].values():historical_pin(d,entries)
    # Explicit legacy authority: these are retained source/proof bytes, never new launch authority.
    historical_pin(lock['review'],entries);historical_pin(proof['review'],entries)
    p.require(p.same(lock['review'],proof['review']) and proof['review']['sha256']==controller['review']['sha256'],'historical review binding')
    return dict(status='VERIFIED_READ_ONLY',compilerDescriptorsChecked=count,historicalCompilerExecutions=1,newCompilerExecutions=0,newNativeExecutions=0)

def verify_execution(expected):
    lock_path=p.HERE/'execution-lock.json';p.require(p.sha(lock_path)==expected,'external new execution lock digest')
    lock=p.read(lock_path)
    p.keys(lock,['schemaVersion','status','profileInventory','pins','payloadLock','archiveLock','reuseChain','proposal','selectedSchema','manifest','transitionLedger'],'execution lock')
    p.require(type(lock['schemaVersion']) is int and lock['schemaVersion']==1 and lock['status']=='PREPARATION_FROZEN_NOT_LAUNCHED','new execution version')
    for d in lock['pins']:p.pin(d)
    actual={str(x) for x in p.HERE.rglob('*') if x.is_file() and x!=lock_path}
    p.require(actual==set(lock['profileInventory']),'complete new profile inventory')
    for k in ['payloadLock','archiveLock','reuseChain','proposal','selectedSchema','manifest','transitionLedger']:p.pin(lock[k])
    payload=p.read(lock['payloadLock']['path'])
    for d in payload['files']:p.pin(d)
    for root in payload['roots']:
        files={str(x) for x in Path(root).rglob('*') if x.is_file()}
        p.require(files=={d['path'] for d in payload['files'] if Path(d['path']).is_relative_to(Path(root))},'closed full payload inventory '+root)
    archive=p.read(lock['archiveLock']['path'])
    entries=archive['entries']
    for e in entries:
        p.check_descriptor(e['original']);p.pin(e['archived'])
        p.require(e['original']['sha256']==e['archived']['sha256'] and e['original']['sizeBytes']==e['archived']['sizeBytes'],'new archive exact raw')
        if e['gitBlob'] is not None:p.pin(e['gitBlob'])
    old=p.read(archive['oldArchive']['path']);p.pin(archive['oldArchive'])
    for e in old['entries']:
        p.pin(e['archived']);p.pin(e['gitBlob'])
    # No blanket fallback: each requested original descriptor must equal one explicit entry.
    result=verify_reuse(p.read(lock['reuseChain']['path']),entries+old['entries'])
    p.fixtures(p.read(lock['manifest']['path']),p.HERE/'fixtures')
    return lock,result

def verify_archived_execution(expected,snapshot_descriptor):
    """Fresh postcapture closure through a separately pinned exact archive.

    No old module import, producer retarget, global fallback or path mutation.
    The caller closes the snapshot descriptor and predecessor execution digest.
    """
    import time
    started=time.monotonic();p.pin(snapshot_descriptor);snapshot=p.read(snapshot_descriptor['path'])
    entries=snapshot['profileEntries'];lock_entries=[e for e in entries if Path(e['repositoryRelativePath']).name=='execution-lock.json']
    p.require(len(lock_entries)==1,'single archived execution lock');archived=lock_entries[0]['archived'];p.pin(archived)
    p.require(archived['sha256']==expected==snapshot['previousExecutionLockSha256'],'exact predecessor execution digest')
    lock=p.read(archived['path'])
    p.keys(lock,['schemaVersion','status','profileInventory','pins','payloadLock','archiveLock','reuseChain','proposal','selectedSchema','manifest','transitionLedger'],'archived execution lock')
    p.require(type(lock['schemaVersion']) is int and lock['schemaVersion']==1 and lock['status']=='PREPARATION_FROZEN_NOT_LAUNCHED','archived original lock status')
    p.require(set(lock['profileInventory'])=={e['original']['path'] for e in entries if e is not lock_entries[0]},'archived exact profile inventory')
    for e in entries:
        p.check_descriptor(e['original']);p.pin(e['archived']);p.pin(e['gitBlob'])
        p.require(e['original']['sha256']==e['archived']['sha256']==e['gitBlob']['sha256'] and e['original']['sizeBytes']==e['archived']['sizeBytes']==e['gitBlob']['sizeBytes'],'archived exact raw/Git bytes')
    resolutions=[historical_pin(d,entries) for d in lock['pins']]
    def read_bound(name):return p.read(historical_pin(lock[name],entries)['path'])
    payload=read_bound('payloadLock')
    for d in payload['files']:p.pin(d)
    for root in payload['roots']:
        p.require({str(f) for f in Path(root).rglob('*') if f.is_file()}=={d['path'] for d in payload['files'] if Path(d['path']).is_relative_to(Path(root))},'archived actual full payload inventory')
    current_archive=read_bound('archiveLock');old_entries=current_archive['entries']
    for e in old_entries:
        p.pin(e['archived'])
        if e['gitBlob'] is not None:p.pin(e['gitBlob'])
    p.pin(current_archive['oldArchive']);older=p.read(current_archive['oldArchive']['path'])
    for e in older['entries']:p.pin(e['archived']);p.pin(e['gitBlob'])
    reused=verify_reuse(read_bound('reuseChain'),old_entries+older['entries'])
    manifest=read_bound('manifest');manifest_path=Path(historical_pin(lock['manifest'],entries)['path'])
    p.fixtures(manifest,manifest_path.parent/'fixtures')
    return dict(status='FRESH_ARCHIVED_PREDECESSOR_POSTCAPTURE_CLOSURE_VERIFIED',executionLock=archived,snapshot=snapshot_descriptor,profileFiles=len(entries),pinsVerified=len(resolutions),payloadFiles=len(payload['files']),binaryReuse=reused,readOnlySeconds=time.monotonic()-started,newNativeExecutions=0,newCompilerExecutions=0,newJvmExecutions=0)
