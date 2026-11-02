"""New opt-in native entry point. Never invoked during preparation.

The owned 180-second controller starts BEFORE full closure hashing/admission.
Its actual conservative monotonic deadline is inherited by the inner process.
The only pre-parent hash is the bootstrap guard identity needed to own it.
"""
import argparse
import importlib.util
import shutil
import time
from pathlib import Path

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=load('ordering_protocol_runner',Path(__file__).with_name('protocol.py'))

def write_fresh(path,value):
    import json
    with Path(path).open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

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
def directories(out):
    p.require(not out.exists(),'fresh output only: '+str(out))
    for name in ['tmp','home','cache']:(out/name).mkdir(parents=True)
def phase_plan(phase):
    proposal=p.read(p.HERE/'execution-proposal.json')
    matches=[v for v in proposal['invocations'] if v['phase']==phase]
    p.require(len(matches)==1,'exact proposed phase');return proposal,matches[0]
def native_argv(phase):
    _,plan=phase_plan(phase);return plan['nativeArgv']
def validate_argv(argv,phase):p.require(p.same(argv,native_argv(phase)),'fixed native argv/manifest/output')
def review(path,digest,execution,phase):
    expected=p.B/'orchestration/two-frameworks'/('batch2518-ordering-'+phase+'-prelaunch-review-v1.json')
    p.require(Path(path)==expected,'phase-specific independent review path')
    p.require(p.sha(path)==digest,'external review digest');r=p.read(path);p.approval(r,execution,phase);return p.descriptor(path)
def guard():
    p.require(p.sha(p.GUARD)==p.GUARD_SHA,'exact qualified guard');return load('ordering_owned_guard',p.GUARD)

def inner(phase,execution,review_sha,ownership_handle):
    # The parent owns this process already; full hashing is inside its actual lifetime.
    started=time.monotonic();ownership=load('ordering_ownership_inner',p.HERE/'ownership.py')
    envelope,membership,deadline=ownership.consume(ownership_handle,p,phase,execution,review_sha)
    g=guard();history=load('ordering_history_inner',p.HERE/'history.py')
    proposal,plan=phase_plan(phase);out=Path(plan['output']);directories(out)
    receipt=dict(schemaVersion=1,status='FATAL_OR_CLEANUP_FAILURE',phase=phase,actualOuterDeadlineMonotonic=deadline,ownershipEnvelope=envelope,ownershipProof=membership,
                 innerStartedMonotonic=started,executionLockSha256=execution,review=None,process=None,
                 nativeExecutions=p.execution_count(None),newCompilerExecutions=0,resourceSamples=[],resourceAdmissions=[],raw={},progress=None,
                 outcomes=None,failure=None,fixtureRoot=str(out/'fixtures'),environment=environment(out))
    try:
        lock,reused=history.verify_execution(execution);receipt['binaryReuse']=reused
        receipt['review']=review(plan['reviewPath'],review_sha,execution,phase)
        # Materialize only immutable inputs in a fresh sandbox. No old producer invocation.
        (out/'fixtures').mkdir()
        selected=p.read(plan['partitionManifest'])
        for case in selected['cases']:
            for f in case['files']:
                target=out/'fixtures'/f['relativePath'];target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(p.HERE/'fixtures'/f['relativePath'],target)
                p.require(p.sha(target)==f['sha256'],'copied fixture digest')
        # wait_resources(+160) has its immutable effective120s cap, shortened by
        # the actual outer reserve. It may not consume the whole child+cleanup reserve.
        p.require(time.monotonic()+35<=deadline,'outer deadline after closure hashing')
        sampled,samples=g.wait_resources(min(time.monotonic()+160,deadline));receipt['resourceSamples'].extend(samples)
        p.admission(deadline,time.monotonic(),sampled,samples[-1],30)
        def prelaunch():
            begin=time.monotonic();sample=g.memory();end=time.monotonic()
            p.require(end-begin<=2,'fresh local resource query')
            receipt['resourceSamples'].append(sample);p.admission(deadline,end,begin,sample,30)
            receipt['resourceAdmissions'].append(dict(queryStartedMonotonic=begin,queryFinishedMonotonic=end,decisionMonotonic=end,actualOuterDeadlineMonotonic=deadline,sample=sample,childSeconds=30))
        def update(process):
            receipt['process']=process;receipt['nativeExecutions']=p.execution_count(process)
        argv=native_argv(phase);validate_argv(argv,phase)
        process=g.run(argv,out,receipt['environment'],'native',30,prelaunch=prelaunch,on_update=update)
        update(process)
        p.process_receipt(process,argv,out,30,'runtime')
        for stream in ['stdout','stderr']:receipt['raw'][stream]=p.descriptor(out/('native.'+stream))
        raw=p.bounded(out/'native.stderr',524288)
        p.require(len(raw)<=524288,'stderr cap')
        ids=[c['id'] for c in selected['cases']]
        receipt['progress']=p.progress(raw.decode('utf-8',errors='replace'),ids,True)
        value=p.loads(p.bounded(out/'native.stdout',2097152));receipt['outcomes']=p.observation(value,selected['cases'],proposal['fingerprint'])
        # Host trace must show the exact selected runtime and each actual module.
        trace=raw.decode('utf-8',errors='replace')
        for path in proposal['requiredHostTracePaths']:p.require(path.casefold() in trace.casefold(),'runtime host trace binding '+path)
        history.verify_execution(execution)
        receipt['status']='CAPTURED_PENDING_INDEPENDENT_ROOT_REVIEW'
    except BaseException as error:
        receipt['failure']={'type':type(error).__name__,'message':str(error)}
        raise
    finally:
        receipt['nativeExecutions']=p.execution_count(receipt['process'])
        for stream in ['stdout','stderr']:
            path=out/('native.'+stream)
            if path.exists():receipt['raw'][stream]=p.descriptor(path)
        receipt['innerSeconds']=time.monotonic()-started
        write_fresh(out/'receipt.json',receipt)

def outer(phase,execution,review_sha):
    g=guard() # Minimal bootstrap hash only. Full input hashing belongs to owned child.
    # A fixed lexical phase is checked before any proposal read or payload hash.
    import re
    p.require(re.fullmatch(r'pass[12]-part[0-9]{2}',phase),'phase grammar')
    out=p.A/'controllers'/phase;directories(out)
    record=dict(schemaVersion=1,status='FATAL_OR_CLEANUP_FAILURE',phase=phase,executionLockSha256=execution,
                reviewSha256=review_sha,process=None,controllerExecutions=p.execution_count(None),innerReceipt=None,raw={},failure=None,environment=environment(out))
    ownership=load('ordering_ownership_outer',p.HERE/'ownership.py')
    started=time.monotonic();deadline=started+180
    capability=ownership.LaunchCapability(g,p,phase,execution,review_sha,started,deadline)
    argv=[str(p.B/'toolchains/python-3.13.9/python.exe'),'-B',str(p.HERE/'native_runner.py'),'--inner',
          '--phase='+phase,'--execution-lock-sha256='+execution,'--review-sha256='+review_sha,'--ownership-handle='+str(capability.handle)]
    try:
        def update(process):record.update(process=process,controllerExecutions=p.execution_count(process))
        result=g.run(argv,out,environment(out),'controller',180,on_update=update,launch=capability.launch,job_factory=capability.job_factory)
        update(result);p.process_receipt(result,argv,out,180,'controller')
        _,plan=phase_plan(phase);receipt=Path(plan['output'])/'receipt.json';p.require(receipt.exists(),'inner receipt required')
        record['innerReceipt']=p.descriptor(receipt)
        value=p.read(receipt);p.require(value['status']=='CAPTURED_PENDING_INDEPENDENT_ROOT_REVIEW','inner completion')
        record['status']='COMPLETE_PENDING_INDEPENDENT_ROOT_REVIEW'
    except BaseException as error:
        record['failure']={'type':type(error).__name__,'message':str(error)};raise
    finally:
        record['ownershipEnvelope']=capability.record;record['ownershipPipeHandle']=capability.handle
        capability.close()
        record['outerStartedMonotonic']=started;record['actualOuterDeadlineMonotonic']=deadline
        record['controllerExecutions']=p.execution_count(record['process'])
        for stream in ['stdout','stderr']:
            path=out/('controller.'+stream)
            if path.exists():record['raw'][stream]=p.descriptor(path)
        write_fresh(out/'parent-receipt.json',record)

def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--inner',action='store_true');parser.add_argument('--phase',required=True)
    parser.add_argument('--execution-lock-sha256',required=True);parser.add_argument('--review-sha256',required=True)
    parser.add_argument('--ownership-handle',type=int)
    args=parser.parse_args()
    for digest in [args.execution_lock_sha256,args.review_sha256]:p.require(p.HEX.fullmatch(digest),'external SHA256')
    if args.inner:
        p.require(args.ownership_handle is not None,'inherited owned-launch capability required')
        inner(args.phase,args.execution_lock_sha256,args.review_sha256,args.ownership_handle)
    else:
        p.require(args.ownership_handle is None,'outer creates its actual capability/deadline')
        outer(args.phase,args.execution_lock_sha256,args.review_sha256)
if __name__=='__main__':main()
