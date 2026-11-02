"""One externally bounded PURE two-full-current-check fit measurement.

No cached certificate or historical stage is executed. This is evidence for
independent prospective admission review, never an actual native launch proof.
"""
import argparse,importlib.util,json,time
from pathlib import Path

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
HERE=Path(__file__).resolve().parent
p=load('native_fit_protocol',HERE/'protocol.py')
n=load('native_fit_policy',HERE/'native_policy_v2.py')
h=load('native_fit_history',HERE/'history.py')

def measure(execution):
 out=p.A/'fix3-native-controller-fit-v1'
 p.require(out.is_dir() and not (out/'timing.json').exists(),'fresh externally owned fit output')
 started=time.monotonic();elapsed=[]
 for label in ['pre','post']:
  print(json.dumps(dict(stage=label,event='BEFORE',sourceLockSha256=execution)),flush=True)
  step=time.monotonic();h.verify_execution(execution);elapsed.append(time.monotonic()-step)
  print(json.dumps(dict(stage=label,event='AFTER',seconds=elapsed[-1],sourceLockSha256=execution)),flush=True)
 value=dict(schemaVersion=1,status='TWO_COMPLETE_CURRENT_CHECKS_FIT',sourceLockSha256=execution,policySha256=n.policy_sha(),completeChecks=2,preSeconds=elapsed[0],postSeconds=elapsed[1],fullMeasuredSeconds=time.monotonic()-started,remainingMetadataMarginSeconds=60)
 # Retain completed measurements even when fit is rejected; never label failure FIT.
 try:n.validate_fit(value,execution)
 except BaseException:
  value['status']='TWO_COMPLETE_CURRENT_CHECKS_FIT_REJECTED'
  with (out/'timing.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
  raise
 with (out/'timing.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status='PURE_FIT_VALIDATED_NOT_RUNTIME_ADMISSION',timing=p.descriptor(out/'timing.json'))),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument('--execution-lock-sha256',required=True)
 args=parser.parse_args();p.require(p.HEX.fullmatch(args.execution_lock_sha256),'external sourceLock SHA');measure(args.execution_lock_sha256)
