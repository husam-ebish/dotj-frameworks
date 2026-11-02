"""Fixed prospective native metadata budget. Legacy180 and semantic caps stay separate."""
import importlib.util,math
from pathlib import Path
s=importlib.util.spec_from_file_location('native_policy_protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
POLICY=dict(schemaVersion=2,policyId='batch2518-native-full-verification-v2',controllerSeconds=1200,postverificationReserveSeconds=480,postFitMaxSeconds=400,metadataMarginSeconds=60,legacyControllerSeconds=180,nativeSeconds=30,jdkSeconds=120,cleanupSeconds=5,resourceWaitMaxSeconds=120,resourceFreshnessSeconds=2,freePhysicalBytes=536870912,availableCommitBytes=17179869184,pollSeconds=0.1,runtimeOutputBytes=dict(stdout=2097152,stderr=524288),compilerOutputBytes=dict(stdout=2097152,stderr=2097152))
def validate_policy(value):p.require(p.same(value,POLICY),'exact fixed prospective policy, no caller cap or missing/conflicting fields')
def policy():
 value=p.read(p.HERE/'native-controller-policy-v2.json');validate_policy(value);return value
def policy_sha():policy();return p.sha(p.HERE/'native-controller-policy-v2.json')
def finite(value):return type(value) in [int,float] and math.isfinite(value)
def validate_attempt(plan):
 phase=plan['phase'];p.require(phase!='pass1-part01' and phase in p.read(p.HERE/'execution-proposal.json')['remainingProducerPhases'],'only seven uncaptured logical phases')
 wanted=phase+('-attempt02' if phase=='pass1-part02' else '-attempt01')
 p.require(plan['attemptId']==wanted and plan['output']==str(p.A/'captures-v2'/wanted) and plan['controllerOutput']==str(p.A/'controllers-v2'/wanted) and plan['reviewPath']==str(p.B/'orchestration/two-frameworks'/('batch2518-ordering-'+wanted+'-prelaunch-review-v2.json')),'exact fresh attempt/controller/review path')
 p.require(plan['nativeArgv'][-2]==str(Path(plan['output'])/'fixtures'),'attempt fixture argv binding')
def admission(deadline,now,sampled,sample):
 p.require(all(finite(v) for v in [deadline,now,sampled]),'finite actual monotonic times')
 p.admission(deadline-480-60,now,sampled,sample,30)
def wait_deadline(deadline,now):
 p.require(finite(deadline) and finite(now),'finite wait deadline');return min(now+160,deadline-480-60)
def validate_envelope(e,*,phase,attempt,execution,review,parent_pid,child_pid,now,guard_sha=p.GUARD_SHA):
 legacy=__import__('importlib').util.spec_from_file_location('native_envelope_legacy',p.HERE/'ownership.py');m=__import__('importlib').util.module_from_spec(legacy);legacy.loader.exec_module(m)
 p.keys(e,list(m.FIELDS)+['attemptId','policyId','policySha256','controllerSeconds','postverificationReserveSeconds'],'native ownership envelope')
 p.require(e['attemptId']==attempt and e['policyId']==POLICY['policyId'] and e['policySha256']==policy_sha() and type(e['controllerSeconds']) is int and e['controllerSeconds']==1200 and type(e['postverificationReserveSeconds']) is int and e['postverificationReserveSeconds']==480,'bound fixed native policy/attempt')
 p.require(guard_sha==p.GUARD_SHA,'fixed qualified guard identity')
 for key,value in [('phase',phase),('executionLockSha256',execution),('reviewSha256',review),('guardSha256',guard_sha)]:p.require(e[key]==value,'native ownership '+key)
 for key,value in [('parentPid',parent_pid),('childPid',child_pid)]:p.require(type(e[key]) is int and e[key]==value and value>0,'actual native ownership '+key)
 p.require(type(e['schemaVersion']) is int and e['schemaVersion']==1 and type(e['parentJobHandle']) is int and e['parentJobHandle']>0,'native ownership scalar types')
 start=e['outerStartedMonotonic'];deadline=e['actualOuterDeadlineMonotonic'];p.require(all(finite(v) for v in [start,deadline,now]) and deadline==start+1200 and start<=now<deadline and deadline-now<=1200,'one actual start+1200 deadline')
 return deadline
def example_envelope():return dict(schemaVersion=1,phase='pass1-part02',attemptId='pass1-part02-attempt02',executionLockSha256='a'*64,reviewSha256='b'*64,outerStartedMonotonic=10,actualOuterDeadlineMonotonic=1210,parentPid=123,childPid=456,parentJobHandle=789,guardSha256=p.GUARD_SHA,policyId=POLICY['policyId'],policySha256=policy_sha(),controllerSeconds=1200,postverificationReserveSeconds=480)
def example_fit(execution):return dict(schemaVersion=1,status='TWO_COMPLETE_CURRENT_CHECKS_FIT',sourceLockSha256=execution,policySha256=policy_sha(),completeChecks=2,preSeconds=200.0,postSeconds=200.0,fullMeasuredSeconds=401.0,remainingMetadataMarginSeconds=60)
def validate_fit(f,execution):
 p.keys(f,['schemaVersion','status','sourceLockSha256','policySha256','completeChecks','preSeconds','postSeconds','fullMeasuredSeconds','remainingMetadataMarginSeconds'],'external two-check fit evidence')
 p.require(type(f['schemaVersion']) is int and f['schemaVersion']==1 and f['status']=='TWO_COMPLETE_CURRENT_CHECKS_FIT' and f['sourceLockSha256']==execution and f['policySha256']==policy_sha() and type(f['completeChecks']) is int and f['completeChecks']==2,'same frozen source/policy and two complete checks')
 p.require(all(finite(f[k]) and f[k]>=0 for k in ['preSeconds','postSeconds','fullMeasuredSeconds']) and f['fullMeasuredSeconds']>=f['preSeconds']+f['postSeconds'] and f['postSeconds']<=400,'actual complete post-equivalent<=400')
 p.require(type(f['remainingMetadataMarginSeconds']) is int and f['remainingMetadataMarginSeconds']==60 and f['fullMeasuredSeconds']+120+30+5+60<=1200,'full measured check budget plus worst-case wait/native/cleanup and explicit margin fits1200')
def validate_review(review,execution,plan):
 fields=['schemaVersion','independentReviewer','executionLockSha256','phase','nativeApproved','reuseObserverApproved','newCompilerExecutions','invocationCountApproved','attemptId','policyId','policySha256','controllerSeconds','postverificationReserveSeconds','fitEvidence']
 p.keys(review,fields,'prospective phase approval');validate_attempt(plan)
 p.approval({k:review[k] for k in fields[:8]},execution,plan['phase'])
 p.require(type(review['invocationCountApproved']) is int and review['invocationCountApproved']==1,'one fresh attempt only, no automatic retries')
 p.require(review['attemptId']==plan['attemptId'] and review['policyId']==POLICY['policyId'] and review['policySha256']==policy_sha() and type(review['controllerSeconds']) is int and review['controllerSeconds']==1200 and type(review['postverificationReserveSeconds']) is int and review['postverificationReserveSeconds']==480,'exact prospective approval policy/attempt')
 d=review['fitEvidence'];p.pin(d);p.require(d['path']==str(p.A/'fix3-native-controller-fit-v1/timing.json'),'fixed external fit proof path');validate_fit(p.read(d['path']),execution)
def retained_counts():
 r=p.read(p.A/'controllers/pass1-part02/parent-receipt.json');p.require(r['process']['timedOut'] is True and r['process']['exitCode']==125 and r['innerReceipt'] is None,'retained actual timeout unchanged')
 return dict(controllers=2,confirmedNative=1,secondAttemptNative=dict(state='UNKNOWN',value=None))
