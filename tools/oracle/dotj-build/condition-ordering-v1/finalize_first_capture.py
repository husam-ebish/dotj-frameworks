"""Pure postcapture metadata finalization for one closed predecessor attempt.

The original parent exit1, child failure status and raw streams never change.
This is not a successful original coordinator receipt or permission to rerun it.
"""
import argparse
import collections
import hashlib
import importlib.util
import time
from pathlib import Path

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
p=load('first_finalization_protocol',Path(__file__).with_name('protocol.py'))
binding=load('first_finalization_binding',p.HERE/'runtime_binding.py')
history=load('first_finalization_history',p.HERE/'history.py')
runner=load('first_finalization_runner',p.HERE/'native_runner.py')
ownership=load('first_finalization_ownership',p.HERE/'ownership.py')
PHASE='pass1-part01'
OLD_LOCK='35ef28faf73f6dd31596867f724c37ec5050163ad47ac18775ab362f6901897e'
OLD_APPROVAL='cb65a3c2c6589e3fdc87e79211ee87d52daecb4e345c585023199b3b786c0f00'
FINDING='d356c5e99e44c68e550d5977928d3988e7e183c6cd7abd42b614d03c170b1173'
SNAPSHOT='f3d1247be34b2267e062d09a2b64e9e7f24162d84e743622a2ebc372d96b6399'
STDOUT='dc06bcabd4314d837474b493fd75ae4eb7d6aba40591958b9ac46c9480ea1ca0'
STDERR='5464b7438af0c57b897858b64a529d795cd209520a646654707b33bdde50d7a4'
FINAL=p.A/'first-capture-pure-finalization-v1/finalization-proof.json'
REVIEW=p.B/'orchestration/two-frameworks/batch2518-first-capture-pure-finalization-review-v1.json'

def contract():
    c=p.read(p.HERE/'first-capture-predecessor.json')
    p.keys(c,['schemaVersion','phase','executionLockSha256','snapshot','oldProposal','oldRunner','coordinatorSource','approval','finding','adjudication','coordination','captureFiles','finalizationPath'],'closed predecessor contract')
    p.require(type(c['schemaVersion']) is int and c['schemaVersion']==1 and c['phase']==PHASE and c['executionLockSha256']==OLD_LOCK,'only exact predecessor phase/lock')
    p.require(c['snapshot']['sha256']==SNAPSHOT and c['finding']['sha256']==FINDING and c['approval']['sha256']==OLD_APPROVAL and c['adjudication']['sha256']=='6f835f7bec11bba3cceccff121be08cf039d65e7085620d98d8aabe50a5022b2','exact predecessor authority allowlist')
    p.require(c['finalizationPath']==str(FINAL),'fixed versioned pure finalization output')
    expected=[('captures/pass1-part01/receipt.json','06b2ee75b4449a260a0bbcc1ed4eec6b9c50f399115122612b253972d251e64d',16581),
              ('captures/pass1-part01/native.stdout',STDOUT,66351),('captures/pass1-part01/native.stderr',STDERR,298571),
              ('controllers/pass1-part01/parent-receipt.json','e215a067adb03006823a28b441862692d6744691fd867b4645f6a1c4411561e0',5889),
              ('controllers/pass1-part01/controller.stdout','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',0),
              ('controllers/pass1-part01/controller.stderr','36ec7ae301563ed6abb658f22650bfbbef364a4c821c830eca35432d4d2b867f',1492)]
    p.require(p.same(c['captureFiles'],[dict(path=str(p.A/name),sha256=digest,sizeBytes=size) for name,digest,size in expected]),'only exact original failed-parent/exit0-child raw receipt allowlist')
    return c

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

def validate_documents(parent,child,coord,approval,plan,value,raw):
    c=contract();oldproposal=p.read(c['oldProposal']['path']);oldplan=next(v for v in oldproposal['invocations'] if v['phase']==PHASE)
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
    p.require(p.same(parent['environment'],runner.environment(root)) and p.same(child['environment'],plan['environment']),'exact original environments')
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
    cases=p.read(plan['partitionManifest'])['cases'];ids=[v['id'] for v in cases];p.require(ids==plan['caseIds'] and len(ids)==72,'exact predecessor ordered72 case manifest')
    progress=p.progress(raw.decode('utf-8'),ids,True);p.require(p.same(child['progress'],[list(v) for v in progress]),'all144 exact original checkpoints')
    outcomes=p.observation(value,cases,oldproposal['fingerprint']);p.require(p.same(outcomes,child['outcomes']),'exact original typed outcome vector')
    p.require(dict(collections.Counter(outcomes))==dict(SUCCESS=56,PROJECT_ERROR=16),'closed original outcome count')
    p.require({f.relative_to(out/'fixtures').as_posix() for f in (out/'fixtures').rglob('*') if f.is_file()}=={f['relativePath'] for case in cases for f in case['files']},'exact original fixture inventory/no task marker')
    for case in cases:
        for f in case['files']:
            file=out/'fixtures'/f['relativePath'];p.require(not file.is_symlink() and p.sha(file)==f['sha256'] and file.stat().st_size==f['sizeBytes'],'original exact immutable fixture bytes')
    runtime=binding.verify(value,raw)
    return dict(outcomeCounts=dict(collections.Counter(outcomes)),caseIds=ids,runtimeBinding=runtime,actualNativeExecutions=1,actualControllerExecutions=1,originalNativeExitCode=0,originalControllerExitCode=1,originalFailurePreserved=True)

def finalize(execution,out,certificate_descriptor):
    p.require(out==FINAL.parent and not out.exists(),'separate fresh versioned PURE finalization only')
    c=contract()
    for name in ['snapshot','oldProposal','oldRunner','coordinatorSource','approval','finding','adjudication','coordination']:p.pin(c[name])
    for d in c['captureFiles']:p.pin(d)
    segmented=load('first_finalization_segmented',p.HERE/'segmented_closure.py')
    closure=segmented.verify_certificate(execution,certificate_descriptor)
    oldproposal=p.read(c['oldProposal']['path']);plan=next(v for v in oldproposal['invocations'] if v['phase']==PHASE)
    parent=p.read(p.A/'controllers'/PHASE/'parent-receipt.json');child=p.read(Path(plan['output'])/'receipt.json')
    value=p.read(Path(plan['output'])/'native.stdout');raw=p.bounded(Path(plan['output'])/'native.stderr',524288)
    validation=validate_documents(parent,child,p.read(c['coordination']['path']),p.read(c['approval']['path']),plan,value,raw)
    # Complete independently bounded PURE recovery, never a monolithic pass
    # or runtime admission credit to the failed original180-second parent.
    post=dict(status='SEGMENTED_PURE_FINALIZATION',certificate=certificate_descriptor,predecessorExecutionLockSha256=OLD_LOCK,correctedExecutionLockSha256=execution,allListedDescriptorsAndAssertionsCovered=True,futureRuntimeAdmissionCredit=False)
    for d in c['captureFiles']:p.pin(d)
    record=dict(schemaVersion=1,status='PURE_POSTCAPTURE_FINALIZED_PENDING_INDEPENDENT_REVIEW',phase=PHASE,correctedExecutionLockSha256=execution,predecessorExecutionLockSha256=OLD_LOCK,predecessorContract=p.descriptor(p.HERE/'first-capture-predecessor.json'),finding=c['finding'],adjudication=c['adjudication'],approval=c['approval'],snapshot=c['snapshot'],raw=c['captureFiles'],validation=validation,postCaptureClosure=post,currentCorrectedClosure=dict(executionLock=p.descriptor(p.HERE/'execution-lock.json'),segmentedCertificate=certificate_descriptor),newExecutionCounts=dict(native=0,compiler=0,jvm=0,product=0),retainedActualExecutionCounts=dict(native=1,controller=1),qualifiedCapture=False,launchApproval=False)
    out.mkdir();runner.write_fresh(FINAL,record);return record

def approved_finalization(execution,review_sha):
    p.require(REVIEW.is_file() and p.sha(REVIEW)==review_sha,'independent first-capture pure-finalization review required')
    review=p.read(REVIEW)
    p.keys(review,['schemaVersion','independentReviewer','firstCaptureFinalizationApproved','finalizationProof','correctedExecutionLockSha256','predecessorExecutionLockSha256','findingSha256'],'pure finalization review')
    p.require(type(review['schemaVersion']) is int and review['schemaVersion']==1 and type(review['independentReviewer']) is str and review['independentReviewer'].strip() and review['firstCaptureFinalizationApproved'] is True,'independent finalization authority')
    p.require(review['correctedExecutionLockSha256']==execution and review['predecessorExecutionLockSha256']==OLD_LOCK and review['findingSha256']==FINDING,'closed finalization review execution/finding')
    p.pin(review['finalizationProof']);p.require(review['finalizationProof']['path']==str(FINAL),'fixed predecessor PURE proof path')
    proof=p.read(FINAL)
    p.require(proof['status']=='PURE_POSTCAPTURE_FINALIZED_PENDING_INDEPENDENT_REVIEW' and proof['phase']==PHASE and proof['correctedExecutionLockSha256']==execution and proof['predecessorExecutionLockSha256']==OLD_LOCK and proof['finding']['sha256']==FINDING,'exact reviewed pure proof identity')
    p.require(p.same(proof['retainedActualExecutionCounts'],dict(native=1,controller=1)) and p.same(proof['newExecutionCounts'],dict(native=0,compiler=0,jvm=0,product=0)) and proof['validation']['originalControllerExitCode']==1 and proof['validation']['originalNativeExitCode']==0 and proof['validation']['originalFailurePreserved'] is True,'no predecessor failed-parent/launch count laundering')
    p.require(proof['postCaptureClosure']['status']=='SEGMENTED_PURE_FINALIZATION' and proof['postCaptureClosure']['predecessorExecutionLockSha256']==OLD_LOCK and proof['postCaptureClosure']['futureRuntimeAdmissionCredit'] is False,'skipped predecessor closure completed as PURE segmentation only')
    segmented=load('reviewed_first_segmented',p.HERE/'segmented_closure.py');segmented.verify_certificate(execution,proof['postCaptureClosure']['certificate'])
    c=contract()
    for d in c['captureFiles']:p.pin(d)
    plan=next(v for v in p.read(c['oldProposal']['path'])['invocations'] if v['phase']==PHASE)
    value=p.read(Path(plan['output'])/'native.stdout')
    actual=validate_documents(p.read(p.A/'controllers'/PHASE/'parent-receipt.json'),p.read(Path(plan['output'])/'receipt.json'),p.read(c['coordination']['path']),p.read(c['approval']['path']),plan,value,p.bounded(Path(plan['output'])/'native.stderr',524288))
    p.require(p.same(proof['validation'],actual),'independently reviewed exact retained validation')
    return proof,value,p.descriptor(REVIEW)

def main():
    parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument('--execution-lock-sha256',required=True);parser.add_argument('--out',required=True,type=Path);parser.add_argument('--segmented-certificate',required=True,type=Path);parser.add_argument('--segmented-certificate-sha256',required=True)
    args=parser.parse_args();p.require(p.sha(args.segmented_certificate)==args.segmented_certificate_sha256,'external segmented certificate digest');finalize(args.execution_lock_sha256,args.out,p.descriptor(args.segmented_certificate))
if __name__=='__main__':main()
