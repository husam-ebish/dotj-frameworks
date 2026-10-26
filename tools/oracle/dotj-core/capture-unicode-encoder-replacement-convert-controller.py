"""Resume independent native cases after explicitly recorded bounded non-returns."""
import argparse,hashlib,json,os,subprocess,time,uuid
from pathlib import Path
BASE=Path('D:/AI/Implementation/dotj Frameworks');HERE=Path(__file__).resolve().parent;CORE='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--bound-seconds',type=float,default=3.0);a=p.parse_args();assert a.bound_seconds>=3
 work=BASE/'verification/unicode-encoder-replacement-convert-native'/uuid.uuid4().hex;work.mkdir(parents=True);config=work/'runtimeconfig.json';config.write_text('{"runtimeOptions":{"tfm":"net10.0","framework":{"name":"Microsoft.NETCore.App","version":"10.0.12"},"rollForward":"Disable"}}',encoding='utf-8');worker=HERE/'capture-unicode-encoder-replacement-convert-worker.ps1';entry=HERE/'capture-unicode-encoder-replacement-convert-contract.ps1';env=os.environ.copy();env.update(TEMP=str(BASE/'tmp'),TMP=str(BASE/'tmp'),DOTNET_ROOT=str(BASE/'toolchains/dotnet'),DOTNET_CLI_HOME=str(BASE/'cache/dotnet-home'),PSModuleAnalysisCachePath=str(BASE/'cache/powershell-analysis-preflight'));returned={};timeouts={};start=0;attempts=0
 while start<9216:
  attempt=work/f'attempt-{attempts:04d}';attempt.mkdir();result=attempt/'worker-completed.json';progress=work/'progress.json';progress.unlink(missing_ok=True)
  cmd=[str(BASE/'toolchains/dotnet/dotnet.exe'),'exec','--runtimeconfig',str(config),str(BASE/'toolchains/powershell-7.6.0-fxdependent/pwsh.dll'),'-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',str(worker),'-OutputPath',str(result),'-WorkRoot',str(work),'-StartAt',str(start)]
  with (attempt/'stdout.log').open('w',encoding='utf-8') as out,(attempt/'stderr.log').open('w',encoding='utf-8') as err:
   child=subprocess.Popen(cmd,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW);launch=time.monotonic();last=None;last_change=launch;observed=None;timed=None
   while child.poll() is None:
    try:current=json.loads(progress.read_text(encoding='utf-8'));token=current['utc']
    except (OSError,ValueError,KeyError):current=None;token=None
    if token is not None and token!=last:last=token;last_change=time.monotonic();observed=current
    if observed is not None and time.monotonic()-last_change>=a.bound_seconds:
     # Recheck that no result or process completion won the observation race.
     log=work/'returned.jsonl';last_returned=None
     if log.exists():
      with log.open('rb') as f:
       f.seek(max(0,log.stat().st_size-65536));lines=f.read().splitlines()
      if lines:
       try:last_returned=json.loads(lines[-1])['caseId']
       except (ValueError,KeyError):pass
     case_id=observed['context']['caseId']
     if child.poll() is None and (last_returned is None or last_returned<case_id):
      timed=dict(caseId=case_id,profile=observed['context']['profile'],bigEndian=observed['context']['bigEndian'],replacement=observed['context']['replacement'],status='OBSERVED_NO_RETURN_WITHIN_BOUND',context=observed['context'],lastCall=observed,observationSeconds=time.monotonic()-last_change,boundSeconds=a.bound_seconds,workerPid=child.pid,qualification='BOUNDED_OBSERVATION_ONLY; NOT_A_RETURN_VALUE_OR_PROOF_OF_INFINITE_EXECUTION');child.terminate();child.wait();break
    if observed is None and time.monotonic()-launch>30:
     child.terminate();child.wait();raise RuntimeError('Native worker did not reach a case; inspect '+str(attempt))
    time.sleep(.1)
   exit_code=child.wait()
  attempts+=1
  if timed is not None:
   timeouts[timed['caseId']]=timed;start=timed['caseId']+1
   with (work/'bounded-no-returns.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(timed,separators=(',',':'))+'\n')
   print(f"BOUNDED native no-return case={timed['caseId']} profile={timed['profile']} elapsed={timed['observationSeconds']:.2f}s; resume={start}",flush=True)
  elif exit_code==0:
   summary=json.loads(result.read_text());assert summary['totalCases']==9216 and summary['profiles']==18 and summary['runtimeVersion']=='10.0.12' and summary['coreLibSha256']==CORE;start=9216
  else:raise RuntimeError(f'Native worker exited {exit_code}; inspect {attempt}')
 log=work/'returned.jsonl'
 for line in log.read_text(encoding='utf-8').splitlines():
  row=json.loads(line);assert row['caseId'] not in returned and row['caseId'] not in timeouts;returned[row['caseId']]=dict(row,status='RETURNED')
 assert set(returned)|set(timeouts)==set(range(9216))
 profiles=[None]*18
 for row in list(returned.values())+list(timeouts.values()):
  pid=row['profile']
  if profiles[pid] is None:profiles[pid]=dict(bigEndian=row['bigEndian'],replacement=row['replacement'],rows=[])
  profiles[pid]['rows'].append(row)
 for profile in profiles:profile['rows'].sort(key=lambda r:r['caseId']);assert len(profile['rows'])==512
 record=dict(schemaVersion=2,runtimeVersion='10.0.12',coreLibSha256=CORE,oracleSha256=sha(entry),workerSha256=sha(worker),controllerSha256=sha(Path(__file__)),totalCases=9216,returnedCases=len(returned),boundedNoReturnCases=len(timeouts),boundSeconds=a.bound_seconds,workerAttempts=attempts,profiles=profiles,qualification='NATIVE_ENCODER_REPLACEMENT_CONVERT_REFERENCE_WITH_EXPLICIT_BOUNDED_NO_RETURN_OBSERVATIONS_ONLY; NO_JAVA_OR_FULL_NONTERMINATION_QUALIFICATION')
 a.output.write_text(json.dumps(record,separators=(',',':'))+'\n',encoding='utf-8',newline='\n');print(f'PASS bounded replacement edge capture: returned={len(returned)} boundedNoReturn={len(timeouts)} total=9216',flush=True)
if __name__=='__main__':main()
