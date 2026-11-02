"""Focused PURE prospective-policy/archived-lineage controls; no runtime."""
import copy,importlib.util,math
from pathlib import Path
import unittest
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=load('policy_test_protocol',HERE/'protocol.py')
n=load('policy_tests',HERE/'native_policy_v2.py') if (HERE/'native_policy_v2.py').exists() else None
class NativePolicyControls(unittest.TestCase):
 def setUp(self):self.assertIsNotNone(n,'fixed prospective native policy is required')
 def test_fixed_policy_rejects_missing_conflicting_or_caller_caps(self):
  value=n.policy();n.validate_policy(value)
  for key,v in [('controllerSeconds',180),('controllerSeconds',True),('postverificationReserveSeconds',0),('nativeSeconds',120),('jdkSeconds',30)]:
   bad=copy.deepcopy(value);bad[key]=v
   with self.subTest(key=key),self.assertRaises(ValueError):n.validate_policy(bad)
  bad=copy.deepcopy(value);bad.pop('policyId')
  with self.assertRaises(ValueError):n.validate_policy(bad)
 def test_admission_reserves_postcheck_and_unchanged_child_cleanup(self):
  sample={'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3}
  n.admission(1200,500,499,sample)
  for deadline,now,stamp,s in [(1014,500,499,sample),(1200,500,497,sample),(1200,500,501,sample),(1200,500,499,dict(sample,freeVirtualBytes=0)),(math.inf,500,499,sample),(1200,True,0,sample)]:
   with self.subTest(deadline=deadline,now=now),self.assertRaises(ValueError):n.admission(deadline,now,stamp,s)
 def test_new_envelope_binds_policy_attempt_actual_parent_and_deadline(self):
  e=n.example_envelope();n.validate_envelope(e,phase='pass1-part02',attempt='pass1-part02-attempt02',execution='a'*64,review='b'*64,parent_pid=123,child_pid=456,now=11)
  for key,v in [('attemptId','other'),('controllerSeconds',180),('policySha256','0'*64),('actualOuterDeadlineMonotonic',190),('parentPid',True),('outerStartedMonotonic',math.nan)]:
   bad=dict(e);bad[key]=v
   with self.subTest(key=key),self.assertRaises(ValueError):n.validate_envelope(bad,phase='pass1-part02',attempt='pass1-part02-attempt02',execution='a'*64,review='b'*64,parent_pid=123,child_pid=456,now=11)
 def test_legacy_ownership_remains_literal180(self):
  legacy=load('legacy_180_only',HERE/'ownership.py');e=n.example_envelope();legacy_e={k:v for k,v in e.items() if k in legacy.FIELDS};legacy_e['actualOuterDeadlineMonotonic']=190
  legacy.validate(legacy_e,phase='pass1-part02',execution='a'*64,review='b'*64,guard_sha=p.GUARD_SHA,parent_pid=123,child_pid=456,now=11)
  legacy_e['actualOuterDeadlineMonotonic']=1210
  with self.assertRaises(ValueError):legacy.validate(legacy_e,phase='pass1-part02',execution='a'*64,review='b'*64,guard_sha=p.GUARD_SHA,parent_pid=123,child_pid=456,now=11)
 def test_fit_rejects_missing_checks_wrong_lock_and_excess_post_or_budget(self):
  f=n.example_fit('a'*64);n.validate_fit(f,'a'*64)
  for key,v in [('sourceLockSha256','0'*64),('postSeconds',401),('completeChecks',1),('postSeconds',True),('fullMeasuredSeconds',1100),('completeChecks',True)]:
   bad=dict(f);bad[key]=v
   with self.subTest(key=key),self.assertRaises(ValueError):n.validate_fit(bad,'a'*64)
 def test_fresh_attempt_paths_and_first_phase_exclusion(self):
  proposal=p.read(HERE/'execution-proposal.json')
  for plan in proposal['invocations'][1:]:
   n.validate_attempt(plan);self.assertIn('captures-v2',plan['output']);self.assertIn('controllers-v2',plan['controllerOutput'])
   bad=dict(plan,output=str(p.A/'captures/pass1-part02'))
   with self.assertRaises(ValueError):n.validate_attempt(bad)
 def test_second_timeout_native_count_remains_unknown(self):
  result=n.retained_counts();self.assertEqual(2,result['controllers']);self.assertEqual(1,result['confirmedNative']);self.assertEqual({'state':'UNKNOWN','value':None},result['secondAttemptNative'])
 def test_archived_b169_plan_and_approved_first_capture(self):
  a=load('closed_b169_test',HERE/'archived_b169.py');result=a.verify_accepted_first()
  self.assertEqual(72,result['rows']);self.assertEqual(1,result['originalParentExitCode']);self.assertEqual(104,result['stageReceiptCount']);self.assertEqual(11334,result['uniqueDescriptors'])
 def test_archived_resolver_rejects_missing_ambiguous_or_changed_bindings(self):
  a=load('closed_b169_resolver_test',HERE/'archived_b169.py');ctx=a.context();entry=ctx.entries[0]
  ctx.resolve(entry['original'])
  for changed in [dict(entry['original'],sha256='0'*64),dict(entry['original'],sizeBytes=True)]:
   with self.assertRaises(ValueError):ctx.resolve(changed)
  ctx.entries=ctx.entries+[entry]
  with self.assertRaises(ValueError):ctx.resolve(entry['original'])
 def test_new_transport_rejects_direct_inner_without_capability(self):
  transport=load('prospective_transport_control',HERE/'native_ownership_v2.py')
  for handle in [None,0,-1,True]:
   with self.subTest(handle=handle),self.assertRaises(ValueError):transport.consume(handle,p,'pass1-part02','pass1-part02-attempt02','a'*64,'b'*64)
  e=n.example_envelope()
  with self.assertRaises(ValueError):n.validate_envelope(e,phase=e['phase'],attempt=e['attemptId'],execution='a'*64,review='b'*64,guard_sha='0'*64,parent_pid=123,child_pid=456,now=11)
  for key,value in [('parentJobHandle',0),('childPid',999),('phase','pass2-part01'),('reviewSha256','0'*64),('executionLockSha256','0'*64)]:
   bad=dict(e);bad[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):n.validate_envelope(bad,phase=e['phase'],attempt=e['attemptId'],execution='a'*64,review='b'*64,guard_sha=p.GUARD_SHA,parent_pid=123,child_pid=456,now=11)
 def test_new_runner_and_consumer_bind_exact_attempt_review_and_caps(self):
  runner=load('prospective_runner_control',HERE/'native_runner_v2.py');consumer=load('prospective_consumer_control',HERE/'freeze_contract_v3.py')
  proposal,plan=runner.phase_plan('pass1-part02')
  self.assertEqual('pass1-part02-attempt02',plan['attemptId'])
  with self.assertRaises(ValueError):runner.validate_argv(plan['nativeArgv']+['--timeout=120'],'pass1-part02')
  with self.assertRaises(ValueError):runner.review(p.A/'old-review.json','b'*64,'a'*64,plan['phase'])
  # These are actual retained receipt shapes, used only as negative pure data.
  original=p.read(p.A/'controllers/pass1-part01/parent-receipt.json')['process'];proc=copy.deepcopy(original)
  proc.update(exitCode=0,error=None,timedOut=False,outputLimitExceeded=False,cleanupError=None,cleanupSeconds=0.01,timeoutSeconds=1200,seconds=1)
  p.process_receipt(proc,proc['argv'],proc['cwd'],1200,'controller')
  for key,value in [('timeoutSeconds',180),('cleanupLimitSeconds',6),('cleanupSeconds',5.01),('jobAssigned',False),('resumed',False),('outputLimitsBytes',dict(stdout=2097153,stderr=524288)),('outputSizesBytes',dict(stdout=0,stderr=524289))]:
   bad=copy.deepcopy(proc);bad[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):p.process_receipt(bad,proc['argv'],proc['cwd'],1200,'controller')
  # Consumer must reject a stale attempt before any raw observation can qualify.
  stale=dict(attemptId='pass1-part02-attempt01',nativePolicy=p.descriptor(HERE/'native-controller-policy-v2.json'))
  with patch.object(consumer.p,'read',side_effect=[stale,stale]):
   with self.assertRaises(ValueError):consumer.verify_phase(plan,'a'*64,'b'*64)
 def test_prospective_review_rejects_missing_conflicting_or_reused_attempt(self):
  plan=p.read(HERE/'execution-proposal.json')['invocations'][1];value=p.example_approval('a'*64,plan['phase'])
  value.update(attemptId=plan['attemptId'],policyId=n.POLICY['policyId'],policySha256=n.policy_sha(),controllerSeconds=1200,postverificationReserveSeconds=480,fitEvidence=dict(path=str(p.A/'fix3-native-controller-fit-v1/timing.json'),sha256='c'*64,sizeBytes=1))
  # Boundary-only artificial fit; no approval file or real fit output is written.
  original_read=n.p.read
  def read_control(path):return n.example_fit('a'*64) if Path(path)==Path(value['fitEvidence']['path']) else original_read(path)
  with patch.object(n.p,'pin'),patch.object(n.p,'read',side_effect=read_control):
   with patch.object(n,'validate_attempt'):
    n.validate_review(value,'a'*64,plan)
    for key,v in [('attemptId','pass1-part02-attempt01'),('policyId','legacy'),('controllerSeconds',180),('postverificationReserveSeconds',0),('phase','pass2-part02'),('executionLockSha256','0'*64),('invocationCountApproved',2)]:
     bad=copy.deepcopy(value);bad[key]=v
     with self.subTest(key=key),self.assertRaises(ValueError):n.validate_review(bad,'a'*64,plan)
    bad=copy.deepcopy(value);bad.pop('policySha256')
    with self.assertRaises(ValueError):n.validate_review(bad,'a'*64,plan)
 def test_closed_predecessor_rejects_forged_coverage_stages_and_other_failures(self):
  a=load('closed_predecessor_negative',HERE/'archived_b169.py');ctx=a.context();cert=p.read(ctx.lineage['certificate']['path']);plan=p.read(cert['plan']['path'])
  ids=[v['id'] for v in plan['descriptors']];a.validate_descriptor_coverage(plan,ids)
  for coverage in [ids[:-1],ids+[ids[0]],list(reversed(ids))]:
   with self.assertRaises(ValueError):a.validate_descriptor_coverage(plan,coverage)
  forged=copy.deepcopy(plan);forged['stages'][0]['kind']='FORGED'
  with self.assertRaises(ValueError):a.validate_stages(forged,cert['plan']['sha256'])
  original=p.read(p.A/'controllers/pass1-part01/parent-receipt.json')['process']
  for key,value in [('exitCode',125),('timedOut',True),('cleanupSeconds',6),('jobAssigned',False)]:
   bad=copy.deepcopy(original);bad[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):a.failed_parent_process(bad,original['argv'],Path(original['cwd']))
  with self.assertRaises(ValueError):a.approved_finalization('a'*64,'0'*64)
if __name__=='__main__':unittest.main(verbosity=2)
