"""Version3 prospective1200 consumer: one exact predecessor plus seven future phases.

No process launch. The exact exit1 predecessor additionally requires its
reviewed separate pure finalization; seven future phases require successful
corrected receipts. Two complete matching native passes remain mandatory.
"""
import argparse
import base64
import importlib.util
from pathlib import Path
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
p=load('ordering_protocol_freeze',Path(__file__).with_name('protocol.py'))
r=load('ordering_runner_freeze',p.HERE/'native_runner_v2.py')
h=load('ordering_history_freeze',p.HERE/'history.py')
binding=load('ordering_binding_freeze_v2',p.HERE/'runtime_binding.py')
predecessor=load('ordering_predecessor_freeze_v2',p.HERE/'archived_b169.py')

def verify_phase(plan,execution,predecessor_review_sha):
    out=Path(plan['output'])
    if plan['phase']==predecessor.PHASE:
        proof,value,review=predecessor.approved_finalization(execution,predecessor_review_sha)
        return proof['child'],value
    parent=p.read(Path(plan['controllerOutput'])/'parent-receipt.json');child=p.read(out/'receipt.json')

    r.policy.validate_attempt(plan)
    p.require(parent['attemptId']==child['attemptId']==plan['attemptId'] and p.same(parent['nativePolicy'],child['nativePolicy']) and p.same(parent['nativePolicy'],p.descriptor(p.HERE/'native-controller-policy-v2.json')),'fixed policy/attempt receipt binding')
    p.require(r.policy.finite(child['metadataStages']['preVerificationSeconds']) and child['metadataStages']['preVerificationSeconds']>=0 and r.policy.finite(child['metadataStages']['postVerificationSeconds']) and 0<=child['metadataStages']['postVerificationSeconds']<=480,'both full current verification stages actually complete')
    p.require(parent['status']=='COMPLETE_PENDING_INDEPENDENT_ROOT_REVIEW' and parent['failure'] is None,'parent success')
    p.require(child['status']=='CAPTURED_PENDING_INDEPENDENT_ROOT_REVIEW' and child['failure'] is None,'native success envelope')
    p.require(parent['phase']==child['phase']==plan['phase'] and parent['executionLockSha256']==child['executionLockSha256']==execution,'phase/closure binding')
    p.require(p.same(parent['controllerExecutions'],dict(state='KNOWN',value=1)) and p.same(child['nativeExecutions'],dict(state='KNOWN',value=1)),'typed actual parent/native executions')
    p.require(type(child['newCompilerExecutions']) is int and child['newCompilerExecutions']==0,'zero new compiles')
    p.pin(parent['innerReceipt']);p.require(parent['innerReceipt']['path']==str(out/'receipt.json'),'inner proof identity')
    deadline=parent['actualOuterDeadlineMonotonic'];p.require(child['actualOuterDeadlineMonotonic']==deadline and deadline==parent['outerStartedMonotonic']+1200,'actual deadline linkage')
    p.require(type(child['resourceAdmissions']) is list and len(child['resourceAdmissions'])==1,'actual native prelaunch admission')
    admission=child['resourceAdmissions'][0]
    p.require(admission['actualOuterDeadlineMonotonic']==deadline and admission['childSeconds']==30,'admission deadline/child identity')
    p.require(admission['queryStartedMonotonic']<=admission['queryFinishedMonotonic']<=admission['decisionMonotonic'],'query/decision order')
    r.policy.admission(deadline,admission['decisionMonotonic'],admission['queryStartedMonotonic'],admission['sample'])
    p.require(p.same(parent['ownershipEnvelope'],child['ownershipEnvelope']),'actual parent launch envelope linkage')
    ownership=load('ordering_ownership_freeze',p.HERE/'native_ownership_v2.py');envelope=child['ownershipEnvelope']
    r.policy.validate_envelope(envelope,phase=plan['phase'],attempt=plan['attemptId'],execution=execution,review=parent['reviewSha256'],guard_sha=p.GUARD_SHA,parent_pid=envelope['parentPid'],child_pid=parent['process']['processId'],now=child['innerStartedMonotonic'])
    proof=child['ownershipProof'];p.keys(proof,['actualParentPid','actualChildPid','actualJobMembershipVerified','parentExecutable','duplicatedJobHandleClosed'],'actual ownership proof')
    p.require(proof['actualParentPid']==envelope['parentPid'] and proof['actualChildPid']==envelope['childPid'] and proof['actualJobMembershipVerified'] is True and proof['duplicatedJobHandleClosed'] is True and proof['parentExecutable']==str(p.B/'toolchains/python-3.13.9/python.exe'),'actual OS parent/child/Job proof')
    argv=[str(p.B/'toolchains/python-3.13.9/python.exe'),'-B',str(p.HERE/'native_runner_v2.py'),'--inner','--phase='+plan['phase'],'--attempt-id='+plan['attemptId'],'--execution-lock-sha256='+execution,'--review-sha256='+parent['reviewSha256'],'--ownership-handle='+str(parent['ownershipPipeHandle'])]
    root=Path(plan['controllerOutput']);p.process_receipt(parent['process'],argv,root,1200,'controller')
    p.process_receipt(child['process'],plan['nativeArgv'],out,30,'runtime')
    p.require(p.same(parent['environment'],r.environment(root)) and p.same(child['environment'],plan['environment']),'exact environment')
    review=r.review(plan['reviewPath'],parent['reviewSha256'],execution,plan['phase']);p.require(p.same(child['review'],review),'new phase approval')
    for receipt,folder,label in [(parent,root,'controller'),(child,out,'native')]:
        p.keys(receipt['raw'],['stdout','stderr'],'complete raw streams')
        for stream in ['stdout','stderr']:
            d=receipt['raw'][stream];p.pin(d);p.require(d['path']==str(folder/(label+'.'+stream)),'raw file identity')
            p.require(d['sizeBytes']==receipt['process']['outputSizesBytes'][stream],'actual raw process size')
            p.require(d['sizeBytes']<=(2097152 if stream=='stdout' else 524288),'raw cap')
    manifest=p.read(plan['partitionManifest']);cases=manifest['cases'];expected=[c['id'] for c in cases]
    p.require(expected==plan['caseIds'],'partition identity/order')
    raw=p.bounded(out/'native.stderr',524288);progress=p.progress(raw.decode('utf-8',errors='replace'),expected,True)
    p.require(p.same(child['progress'],[list(x) for x in progress]),'serialized checkpoint proof')
    value=p.loads(p.bounded(out/'native.stdout',2097152));proposal=p.read(p.HERE/'execution-proposal.json')
    outcomes=p.observation(value,cases,proposal['fingerprint']);p.require(p.same(outcomes,child['outcomes']),'typed outcomes exactly retained')
    runtime=binding.verify(value,raw)
    p.require(p.same(child['runtimeBinding'],runtime),'captured strict corroborated runtime binding')
    # Fresh fixture copies may not change, grow or gain a task marker.
    actual={f.relative_to(out/'fixtures').as_posix() for f in (out/'fixtures').rglob('*') if f.is_file()}
    wanted={f['relativePath'] for c in cases for f in c['files']};p.require(actual==wanted,'fresh fixture exact inventory')
    for c in cases:
        for f in c['files']:
            file=out/'fixtures'/f['relativePath'];p.require(not file.is_symlink() and p.sha(file)==f['sha256'] and file.stat().st_size==f['sizeBytes'],'fresh exact fixture bytes')
    return child,value

def freeze(execution,review_path,review_sha,out,predecessor_review_sha):
    lock,reuse=h.verify_execution(execution);proposal=p.read(p.HERE/'execution-proposal.json')
    expected_review=p.B/'orchestration/two-frameworks/batch2518-ordering-contract-freeze-review-v3.json'
    p.require(review_path==expected_review and p.sha(review_path)==review_sha,'independent contract freeze review')
    review=p.read(review_path);p.keys(review,['schemaVersion','independentReviewer','executionLockSha256','contractFreezeApproved','phaseParentReceipts','predecessorFinalizationReview'],'contract freeze review')
    p.require(type(review['schemaVersion']) is int and review['schemaVersion']==1 and type(review['independentReviewer']) is str and review['independentReviewer'].strip() and review['executionLockSha256']==execution and review['contractFreezeApproved'] is True,'freeze authority')
    parent_files=[(p.A/'controllers'/v['phase'] if v['phase']==predecessor.PHASE else Path(v['controllerOutput']))/'parent-receipt.json' for v in proposal['invocations']]
    p.require(p.same(review['phaseParentReceipts'],[p.descriptor(x) for x in parent_files]),'independently reviewed exact captures')
    p.require(p.same(review['predecessorFinalizationReview'],predecessor.context().lineage['acceptedReview']) and review['predecessorFinalizationReview']['sha256']==predecessor_review_sha,'closed independently approved predecessor finalization review')
    predecessor.approved_finalization(execution,predecessor_review_sha)
    by_pass={1:[],2:[]};proofs=[]
    for phase in proposal['invocations']:
        child,value=verify_phase(phase,execution,predecessor_review_sha);normalized=p.normalize(value,child['fixtureRoot'])
        by_pass[phase['passNumber']].extend(normalized['rows'])
        proofs.append(dict(parent=p.descriptor((p.A/'controllers'/phase['phase'] if phase['phase']==predecessor.PHASE else Path(phase['controllerOutput']))/'parent-receipt.json'),child=p.descriptor(Path(phase['output'])/'receipt.json'),sourceKind='EXACT_PREDECESSOR_VIA_APPROVED_PURE_METADATA_FINALIZATION' if phase['phase']==predecessor.PHASE else 'CORRECTED_PRODUCER_SUCCESS',pureFinalization=predecessor.context().lineage['acceptedProof'] if phase['phase']==predecessor.PHASE else None))
    p.require(p.same(by_pass[1],by_pass[2]),'two independent complete typed passes exactly match selected fields')
    expected=[c['id'] for c in p.read(p.HERE/'manifest.json')['cases']];p.require([x['id'] for x in by_pass[1]]==expected,'full ordered IDs')
    witness=next(x for x in by_pass[1] if x['id']=='ORD-HISTORY-BOOL-BOUND-ordering')
    p.require(p.row(witness,witness['id'],{})=='SUCCESS','historical transition genuinely observed SUCCESS')
    ev=witness['evaluation'];p.require(ev['properties']=={'P':'yes','Q':'taken'} and ev['imports']==[] and witness['diagnostics']==[],'historical selected witness fields')
    p.require(out==p.A/'frozen-native-contract-v3' and not out.exists(),'one fresh fixed freeze output');out.mkdir()
    r.write_fresh(out/'contract.json',dict(schemaVersion=1,status='OBSERVED_PENDING_PRODUCT_IMPLEMENTATION',executionLockSha256=execution,review=p.descriptor(review_path),proofs=proofs,rows=by_pass[1],acceptanceCredit=0))
    bridge='ORDERING_NATIVE_SUCCESS_BRIDGE_V1\n'+witness['id']+'\t'+'\t'.join(base64.b64encode(ev['properties'][k].encode()).decode() for k in ['P','Q'])+'\n'
    with (out/'baseline-success-bridge.tsv').open('x',encoding='ascii',newline='\n') as f:f.write(bridge)

def main():
    parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument('--execution-lock-sha256',required=True)
    parser.add_argument('--predecessor-finalization-review-sha256',required=True);parser.add_argument('--review',required=True,type=Path);parser.add_argument('--review-sha256',required=True);parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args();freeze(args.execution_lock_sha256,args.review,args.review_sha256,args.out,args.predecessor_finalization_review_sha256)
if __name__=='__main__':main()
