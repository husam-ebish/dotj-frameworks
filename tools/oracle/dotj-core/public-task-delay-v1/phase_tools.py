"""Dedicated phase implementation. Importing or preparing descriptors never launches."""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import time
from pathlib import Path
import contract as c

HERE=c.HERE
B=c.B
DOTNET=B/'toolchains/dotnet'
JDK=B/'toolchains/jdk-qualified/jdk-21.0.12.1+1'

def parser(phase):
    p=argparse.ArgumentParser(prog=phase,allow_abbrev=False)
    p.add_argument('--input-lock',required=True)
    p.add_argument('--input-lock-sha256',required=True)
    return p

def lock_inputs(args):
    c.require(c.sha(args.input_lock)==args.input_lock_sha256,'input lock hash')
    lock=c.read(args.input_lock)
    c.keys(lock,['version','profile','schema','manifest','sourceInputs','payload','producerFiles','runtimeconfig','guard','source','baselineSource','baselineJar','referenceAssemblies','nativeArtifactState'],'input lock')
    c.require(type(lock['version']) is int and lock['version']==1 and lock['profile']=='public-task-delay-v1','input lock identity')
    c.require(lock['nativeArtifactState']=='UNCOMPILED_HASH_MUST_BE_BOUND_AFTER_ACTUAL_COMPILE','premature artifact claim')
    for key in ['schema','manifest','sourceInputs','payload','runtimeconfig','guard','source','baselineSource','baselineJar']:
        c.validate_pin(lock[key])
    for item in lock['producerFiles']+lock['referenceAssemblies']:c.validate_pin(item)
    refs=sorted(str(x.resolve()) for x in (DOTNET/'packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll'))
    c.require(refs==sorted(x['path'] for x in lock['referenceAssemblies']),'reference inventory')
    c.require(c.sha(HERE/'schema.json')==lock['schema']['sha256'] and c.sha(HERE/'fixture-manifest.json')==lock['manifest']['sha256'],'profile binding')
    c.validate_manifest(c.read(lock['manifest']['path']))
    return lock

def environment(out):
    return {'SystemRoot':r'C:\Windows','WINDIR':r'C:\Windows','ComSpec':r'C:\Windows\System32\cmd.exe',
        'PATH':str(JDK/'bin')+';'+str(DOTNET)+r';C:\Windows\System32',
        'TEMP':str(out/'tmp'),'TMP':str(out/'tmp'),'TMPDIR':str(out/'tmp'),'HOME':str(out/'home'),'USERPROFILE':str(out/'home'),
        'HOMEDRIVE':'D:','HOMEPATH':str(out/'home')[2:],'APPDATA':str(out/'home/AppData/Roaming'),'LOCALAPPDATA':str(out/'home/AppData/Local'),
        'DOTNET_ROOT':str(DOTNET),'DOTNET_CLI_HOME':str(out/'home'),'DOTNET_MULTILEVEL_LOOKUP':'0','DOTNET_ROLL_FORWARD':'Disable',
        'DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_NOLOGO':'1','DOTNET_CLI_UI_LANGUAGE':'en-US','VSLANG':'1033',
        'DOTNET_GCHeapHardLimit':'8000000','DOTNET_gcServer':'0','DOTNET_PROCESSOR_COUNT':'2','DOTNET_EnableDiagnostics':'0',
        'DOTNET_DbgEnableMiniDump':'0','DOTNET_DbgMiniDumpName':str(out/'tmp/dotnet.dmp'),
        'DOTNET_HOST_TRACE':'1','DOTNET_HOST_TRACE_VERBOSITY':'3','DOTNET_HOST_TRACEFILE':str(out/'host-info.log'),
        'NUGET_PACKAGES':str(out/'cache/nuget'),'NUGET_HTTP_CACHE_PATH':str(out/'cache/http'),
        'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PYTHONUTF8':'1',
        'LANG':'en_US.UTF-8','LC_ALL':'en_US.UTF-8','JAVA_HOME':str(JDK)}

def jvm(out):
    return ['-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-Djava.io.tmpdir='+str(out/'tmp'),
        '-Duser.home='+str(out/'home'),'-Duser.language=en','-Duser.country=US',
        '-XX:ErrorFile='+str(out/'tmp/hs_err_pid%p.log'),'-XX:HeapDumpPath='+str(out/'tmp')]

def command(phase,out,lock,binding=None,partition=None,baseline_classes=None):
    if phase=='source-compile':
        return [str(DOTNET/'dotnet.exe'),'exec',str(DOTNET/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib',
            '-target:exe','-deterministic','-nullable:enable','-langversion:14','-warnaserror','-out:'+str(out/'PublicTaskDelayOracle.dll'),
            *['-r:'+x['path'] for x in lock['referenceAssemblies']],lock['source']['path']]
    if phase=='native-capture':
        c.require(binding is not None and partition in ['ordinary','async'],'native binding/partition')
        return [str(DOTNET/'dotnet.exe'),'exec','--runtimeconfig',binding['runtimeconfig']['path'],binding['dll']['path'],lock['manifest']['path'],partition]
    if phase=='baseline-compile':
        return [str(JDK/'bin/javac.exe'),*['-J'+x for x in jvm(out)],'-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),
            '--module-path',lock['baselineJar']['path'],'--add-modules','dotj.core.foundation.v1','-d',str(out/'classes'),lock['baselineSource']['path']]
    if phase=='baseline-red':
        c.require(baseline_classes is not None,'baseline classes binding')
        return [str(JDK/'bin/java.exe'),*jvm(out),'--module-path',lock['baselineJar']['path'],'--add-modules','dotj.core.foundation.v1',
            '-cp',str(baseline_classes),'PublicTaskDelayFixtures',lock['baselineJar']['path']]
    raise ValueError('unknown phase')

def prepare(phase):
    p=parser(phase+'-proposal');p.add_argument('--out',required=True);p.add_argument('--proposal',required=True)
    if phase=='native-capture':
        p.add_argument('--artifact-binding',required=True);p.add_argument('--artifact-binding-sha256',required=True)
        p.add_argument('--partition',choices=['ordinary','async'],required=True);p.add_argument('--pass-number',type=int,choices=[1,2],required=True)
    if phase=='baseline-red':
        p.add_argument('--baseline-binding',required=True);p.add_argument('--baseline-binding-sha256',required=True)
    a=p.parse_args();lock=lock_inputs(a);out=c.fresh_output(a.out)
    binding=None;binding_pin=None;baseline_classes=None
    if phase=='native-capture':
        c.require(c.sha(a.artifact_binding)==a.artifact_binding_sha256,'artifact binding hash');binding=c.read(a.artifact_binding)
        verify_binding(binding,lock,a.input_lock_sha256);binding_pin=c.descriptor(a.artifact_binding)
    if phase=='baseline-red':
        c.require(c.sha(a.baseline_binding)==a.baseline_binding_sha256,'baseline binding hash');binding=c.read(a.baseline_binding)
        for x in binding['classes']:c.validate_pin(x)
        from root_phase import consume_root
        compile_receipt=consume_root(binding['compileReceipt']['path'],binding['compileReceipt']['sha256'],'baseline-compile');c.successful(compile_receipt['command'])
        c.require(compile_receipt['phase']=='baseline-compile' and binding['inputLockSha256']==a.input_lock_sha256,'baseline compiler source binding')
        baseline_classes=c.confined(binding['classesDirectory']);binding_pin=c.descriptor(a.baseline_binding)
    argv=command(phase,out,lock,binding,getattr(a,'partition',None),baseline_classes)
    length=len(subprocess.list2cmdline(argv))+1;c.require(length<32767,'Windows command line length')
    descriptor={'version':1,'phase':phase,'inputLockSha256':a.input_lock_sha256,'argv':argv,'cwd':str(out),'outerEnvironment':environment(out),
        'timeoutSeconds':30 if phase=='native-capture' else 120,'parentTimeoutSeconds':180,
        'streamLimits':{'stdout':2*1024**2,'stderr':2*1024**2 if phase.endswith('compile') else 512*1024},
        'commandLineUtf16Units':len(subprocess.list2cmdline(argv).encode('utf-16-le'))//2+1,
        'artifactBinding':binding_pin,'partition':getattr(a,'partition',None),'passNumber':getattr(a,'pass_number',None),
        'status':'PROPOSAL_REQUIRES_INDEPENDENT_ROOT_REVIEW','resourceAdmission':'guard.wait_resources(time.monotonic()+160) before guard.run; freshness <=2s physical>=512MiB availablecommit>=16GiB'}
    c.write_new(c.confined(a.proposal),descriptor)

def verify_binding(binding,lock,lock_sha):
    c.keys(binding,['version','status','inputLockSha256','dll','runtimeconfig','compiledSource','compileReceipt','references'],'artifact binding')
    c.require(binding['status']=='ACTUAL_COMPILED_ARTIFACT_PENDING_ROOT_CAPTURE_APPROVAL' and binding['inputLockSha256']==lock_sha,'artifact stage')
    for k in ['dll','runtimeconfig','compiledSource','compileReceipt']:c.validate_pin(binding[k])
    c.require(binding['compiledSource']==lock['source'] and binding['references']==lock['referenceAssemblies'] and binding['runtimeconfig']['sha256']==lock['runtimeconfig']['sha256'],'artifact source/reference binding')
    from root_phase import consume_root
    receipt=consume_root(binding['compileReceipt']['path'],binding['compileReceipt']['sha256'],'source-compile');c.successful(receipt['command'])
    c.require(receipt['phase']=='source-compile' and receipt['inputLock']['sha256']==lock_sha and receipt['actualLaunches']==1,'compile receipt phase')
    compile_out=Path(receipt['command']['cwd']).resolve()
    c.require(Path(binding['dll']['path']).resolve()==compile_out/'PublicTaskDelayOracle.dll' and Path(binding['runtimeconfig']['path']).resolve()==compile_out/'PublicTaskDelayOracle.runtimeconfig.json','artifact path must be actual compiler output')
    c.require(receipt['compiledArtifacts']=={'dll':binding['dll'],'runtimeconfig':binding['runtimeconfig']},'artifact bytes differ from compile completion receipt')
    for item in receipt['streams'].values():c.validate_pin(item)
    c.validate_pin(receipt['approval']);c.validate_pin(receipt['commandDescriptor'])
    c.validate_approval(c.read(receipt['approval']['path']),'source-compile',lock_sha,receipt['commandDescriptor']['sha256'],None)
    expected=command('source-compile',Path(receipt['command']['cwd']),lock)
    c.require(receipt['command']['argv']==expected,'compiled argv binding')

def bind_artifact():
    p=parser('bind-artifact');p.add_argument('--compile-receipt',required=True);p.add_argument('--compile-receipt-sha256',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();lock=lock_inputs(a)
    from root_phase import consume_root
    receipt=consume_root(a.compile_receipt,a.compile_receipt_sha256,'source-compile')
    c.successful(receipt['command']);out=Path(receipt['command']['cwd'])
    binding={'version':1,'status':'ACTUAL_COMPILED_ARTIFACT_PENDING_ROOT_CAPTURE_APPROVAL','inputLockSha256':a.input_lock_sha256,
        'dll':c.descriptor(out/'PublicTaskDelayOracle.dll'),'runtimeconfig':c.descriptor(out/'PublicTaskDelayOracle.runtimeconfig.json'),
        'compiledSource':lock['source'],'compileReceipt':c.descriptor(a.compile_receipt),'references':lock['referenceAssemblies']}
    verify_binding(binding,lock,a.input_lock_sha256);c.write_new(c.confined(a.output),binding)

def bind_baseline():
    p=parser('bind-baseline');p.add_argument('--compile-receipt',required=True);p.add_argument('--compile-receipt-sha256',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();lock=lock_inputs(a)
    from root_phase import consume_root
    receipt=consume_root(a.compile_receipt,a.compile_receipt_sha256,'baseline-compile')
    c.successful(receipt['command']);out=Path(receipt['command']['cwd'])
    c.require(receipt['phase']=='baseline-compile' and receipt['actualLaunches']==1 and receipt['inputLock']['sha256']==a.input_lock_sha256,'baseline compile phase')
    c.require(receipt['command']['argv']==command('baseline-compile',out,lock),'baseline exact compiler arguments')
    c.validate_pin(receipt['approval']);c.validate_pin(receipt['commandDescriptor'])
    c.validate_approval(c.read(receipt['approval']['path']),'baseline-compile',a.input_lock_sha256,receipt['commandDescriptor']['sha256'],None)
    files=sorted((out/'classes').rglob('*'))
    classes=[c.descriptor(f) for f in files if f.is_file()]
    c.require(len(classes)==1 and Path(classes[0]['path']).name=='PublicTaskDelayFixtures.class','baseline class inventory')
    c.require(receipt['compiledArtifacts']==classes,'baseline artifact bytes differ from compile completion receipt')
    c.write_new(c.confined(a.output),{'version':1,'status':'ACTUAL_BASELINE_PROBE_COMPILED','inputLockSha256':a.input_lock_sha256,
        'compileReceipt':c.descriptor(a.compile_receipt),'classesDirectory':str(out/'classes'),'classes':classes,'compiledSource':lock['baselineSource'],'jar':lock['baselineJar']})

def check_full_payload(lock):
    payload=c.read(lock['payload']['path'])
    counts={}
    for name,closure in payload['payloads'].items():
        actual={str(f.resolve()) for f in Path(closure['root']).rglob('*') if f.is_file()}
        c.require(actual=={x['path'] for x in closure['files']},'full payload inventory '+name)
        for item in closure['files']:c.validate_pin(item)
        counts[name]=len(actual)
    sources=c.read(lock['sourceInputs']['path'])
    for item in sources['sources']:c.validate_pin(item['input'])
    for item in sources['licenses']:c.validate_pin(item)
    archive=c.read(sources['historicalArchive']['path'])
    for item in archive['entries']:
        c.require(item['status']=='RAW_ARCHIVED','missing historic archive')
        c.validate_pin(item['durable'])
    return counts

def payload_preflight():
    p=parser('payload-preflight');p.add_argument('--output',required=True)
    a=p.parse_args();started=time.monotonic();lock=lock_inputs(a);counts=check_full_payload(lock)
    c.write_new(c.confined(a.output),{'status':'PAYLOAD_BYTES_VERIFIED_STATIC_NO_CHILD','inputLock':c.descriptor(a.input_lock),'payload':lock['payload'],
        'counts':counts,'seconds':time.monotonic()-started,'actualChildLaunches':0,
        'parentBudgetPolicy':'Run static closure review as a separately bounded preflight; fresh full closure revalidation overhead is included in review before 180s phase admission. Never extend30s native/120s compiler or JDK deadlines.'})

def execution_parser(phase):
    p=parser(phase);p.add_argument('--descriptor',required=True);p.add_argument('--descriptor-sha256',required=True)
    p.add_argument('--approval',required=True);p.add_argument('--approval-sha256',required=True)
    p.add_argument('--outer-context',required=True);p.add_argument('--outer-context-sha256',required=True)
    return p

def execute(phase):
    from root_phase import context_check,reserve
    a=execution_parser(phase).parse_args();lock=lock_inputs(a)
    c.require(c.sha(a.descriptor)==a.descriptor_sha256 and c.sha(a.approval)==a.approval_sha256,'descriptor/approval hash')
    d=c.read(a.descriptor);approval=c.read(a.approval)
    c.require(c.sha(a.outer_context)==a.outer_context_sha256,'outer context hash');outer_context=c.read(a.outer_context)
    context_check(outer_context,phase,a.input_lock_sha256,a.descriptor_sha256,a.approval_sha256,d['cwd'],time.monotonic())
    c.require(outer_context['assessmentSha256']==approval['reviewReceiptSha256'],'inner assessment binding')
    for key in ['rootLauncher','outerImplementation']:
        c.validate_pin(outer_context[key]);c.require(outer_context[key] in lock['producerFiles'],'root launcher input-lock binding')
    c.keys(d,['version','phase','inputLockSha256','argv','cwd','outerEnvironment','timeoutSeconds','parentTimeoutSeconds','streamLimits','commandLineUtf16Units','artifactBinding','partition','passNumber','status','resourceAdmission'],'command descriptor')
    c.require(d['phase']==phase and d['inputLockSha256']==a.input_lock_sha256,'dedicated phase')
    binding_sha=d['artifactBinding']['sha256'] if d['artifactBinding'] else None
    c.require(outer_context['artifactBindingSha256']==binding_sha,'outer artifact binding')
    c.validate_approval(approval,phase,a.input_lock_sha256,a.descriptor_sha256,binding_sha)
    out=c.fresh_output(d['cwd']);binding=None;baseline_classes=None
    if d['artifactBinding']:
        c.validate_pin(d['artifactBinding']);binding=c.read(d['artifactBinding']['path'])
        if phase=='native-capture':verify_binding(binding,lock,a.input_lock_sha256)
        elif phase=='baseline-red':
            c.require(binding['inputLockSha256']==a.input_lock_sha256,'baseline binding lock')
            for x in binding['classes']:c.validate_pin(x)
            from root_phase import consume_root
            c.successful(consume_root(binding['compileReceipt']['path'],binding['compileReceipt']['sha256'],'baseline-compile')['command']);baseline_classes=binding['classesDirectory']
    c.require(d['argv']==command(phase,out,lock,binding,d['partition'],baseline_classes),'exact argv')
    c.require(d['outerEnvironment']==environment(out),'environment binding')
    c.require(type(d['timeoutSeconds']) is int and d['timeoutSeconds']==(30 if phase=='native-capture' else 120),'timeout')
    c.require(d['parentTimeoutSeconds']==180 and d['streamLimits']=={'stdout':2*1024**2,'stderr':2*1024**2 if phase.endswith('compile') else 512*1024},'resource caps')
    out.mkdir(parents=True)
    for relative in ['tmp','home/AppData/Roaming','home/AppData/Local','cache/nuget','cache/http','empty-sourcepath','classes']:(out/relative).mkdir(parents=True,exist_ok=True)
    if phase=='source-compile':shutil.copyfile(lock['runtimeconfig']['path'],out/'PublicTaskDelayOracle.runtimeconfig.json')
    spec=importlib.util.spec_from_file_location('batch2517_owned_guard',lock['guard']['path']);guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    receipt={'version':1,'phase':phase,'status':'PREPARING','actualLaunches':0,'partition':d['partition'],'passNumber':d['passNumber'],
        'inputLock':c.descriptor(a.input_lock),'approval':c.descriptor(a.approval),'commandDescriptor':c.descriptor(a.descriptor),'artifactBinding':d['artifactBinding'],'command':None,'streams':{},'resources':[],
        'outerContext':c.descriptor(a.outer_context),'payloadAdmission':None,'childAdmissionMonotonic':None,'finalized':False}
    def save():
        # Current invocation receipt is append-state evidence; frozen after phase end.
        (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    def update(record):
        receipt['command']=dict(record);receipt['actualLaunches']=c.count_attempt(record);save()
    save()
    try:
        payload_started=time.monotonic();counts=check_full_payload(lock);payload_finished=time.monotonic()
        c.require(payload_finished<outer_context['deadlineMonotonic'],'full closure exhausted actual outer budget')
        payload_record={'version':1,'status':'FULL_PAYLOAD_VERIFIED_FOR_THIS_OUTER_PHASE','outerContext':receipt['outerContext'],
            'inputLock':receipt['inputLock'],'descriptor':receipt['commandDescriptor'],'payload':lock['payload'],'counts':counts,
            'startedMonotonic':payload_started,'finishedMonotonic':payload_finished,'seconds':payload_finished-payload_started}
        c.write_new(out/'payload-admission.json',payload_record);receipt['payloadAdmission']=c.descriptor(out/'payload-admission.json');save()
        def query_resources():
            before=time.monotonic();sample=guard.memory()
            receipt['resources'].append({'sample':sample,'querySeconds':time.monotonic()-before,'outerElapsedSeconds':time.monotonic()-outer_context['startedMonotonic']});save()
            return sample
        sampled,samples=guard.wait_resources(time.monotonic()+160,query=query_resources)
        reserve(outer_context['deadlineMonotonic'],time.monotonic(),d['timeoutSeconds'])
        def prelaunch():
            c.require(time.monotonic()-sampled<=2,'stale admission sample')
            admission=time.monotonic();reserve(outer_context['deadlineMonotonic'],admission,d['timeoutSeconds'])
            receipt['childAdmissionMonotonic']=admission;save()
        record=guard.run(d['argv'],out,d['outerEnvironment'],'compile-'+phase if phase.endswith('compile') else phase,d['timeoutSeconds'],prelaunch=prelaunch,on_update=update,stream_limits=d['streamLimits'])
        # on_update counted the actual launch before interpreting its exit status.
        for stream in ['stdout','stderr']:receipt['streams'][stream]=c.descriptor(record[stream+'Path'])
        c.successful(record,23 if phase=='baseline-red' else 0)
        if phase=='native-capture':
            payload=c.wire(Path(record['stdoutPath']).read_bytes(),c.read(lock['schema']['path']),c.read(lock['manifest']['path']),d['partition']);c.invariants(payload,c.read(lock['manifest']['path']))
            receipt['status']='CAPTURED_PENDING_ROOT_REVIEW'
        elif phase=='baseline-red':
            raw=Path(record['stdoutPath']).read_text(encoding='utf-8')
            c.require(raw.count('MISSING_REQUIRED_MEMBER\t')==5 and 'BASELINE_REQUIRED_MEMBERS\t5\tMISSING\t5' in raw,'genuine five-member RED output')
            receipt['status']='GENUINE_PACKAGED_API_RED_PENDING_ROOT_REVIEW'
        else:
            receipt['compiledArtifacts']=({'dll':c.descriptor(out/'PublicTaskDelayOracle.dll'),'runtimeconfig':c.descriptor(out/'PublicTaskDelayOracle.runtimeconfig.json')}
                if phase=='source-compile' else [c.descriptor(f) for f in sorted((out/'classes').rglob('*')) if f.is_file()])
            receipt['status']='COMPILED_PENDING_ARTIFACT_BINDING'
    except BaseException as error:
        receipt['status']='FAILED_RETAINED' if receipt['actualLaunches'] else 'DEFERRED_NO_CHILD';receipt['failure']=str(error);raise
    finally:receipt['finalized']=True;save()

def verify_capture():
    p=argparse.ArgumentParser(prog='verify-native',allow_abbrev=False)
    p.add_argument('--receipts',nargs=4,required=True);p.add_argument('--receipt-sha256s',nargs=4,required=True);p.add_argument('--output',required=True)
    a=p.parse_args();schema=c.read(HERE/'schema.json');manifest=c.read(HERE/'fixture-manifest.json');passes={1:{},2:{}};seen=set()
    for path,digest in zip(a.receipts,a.receipt_sha256s):
        payload=c.consumed_capture(path,digest,schema,manifest);r=c.read(path);key=(r['passNumber'],r['partition'])
        c.require(key not in seen and key[0] in passes,'duplicate pass partition');seen.add(key)
        c.require(not set(passes[key[0]]) & set(payload),'duplicate global case identity');passes[key[0]].update(payload)
    c.require(seen=={(n,p) for n in [1,2] for p in ['ordinary','async']},'complete two-pass matrix')
    c.require(all(len(p)==manifest['caseCount'] for p in passes.values()),'full manifest')
    c.compare(passes[1],passes[2],manifest)
    c.write_new(c.confined(a.output),{'status':'TWO_COMPLETE_NATIVE_PASSES_VERIFIED_PENDING_ROOT_REVIEW','receipts':[c.descriptor(p) for p in a.receipts], 'casesPerPass':manifest['caseCount'],'acceptanceCredit':0})
