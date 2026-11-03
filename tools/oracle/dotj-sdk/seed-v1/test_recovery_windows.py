"""Real negative builds, boundary refusals and owned staging interruption."""
import argparse,json,sys,shutil,hashlib,re,threading,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from owned import Run,B,JDK,vm
from capture_native import descriptor,inventory
from test_seed import ps_command

def relock(source):
 p=source/'dotj-sdk/seed/sources.properties';lines=[]
 for line in p.read_text().splitlines():
  if line.startswith('sha256.'):
   key=line.split('=',1)[0];raw=(source/key[7:]).read_bytes()
   if key.endswith('.java'):raw=raw.replace(b'\r\n',b'\n')
   line=key+'='+hashlib.sha256(raw).hexdigest()
  lines.append(line)
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n');sha=descriptor(p)['sha256']
 for name in ['build.sh','build.ps1']:
  p=source/'dotj-sdk/seed'/name;p.write_text(re.sub('[a-f0-9]{64}',sha,p.read_text()),encoding='utf-8',newline='\n')

def main():
 p=argparse.ArgumentParser()
 for n in ['source','sdk','attempt']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();r=Run(a.attempt);error=None
 try:
  r.env['JAVA_HOME']=str(JDK.parent);r.env['PATH']='C:/Windows/System32'
  source=r.out/'source';sdk=r.out/'sdk';shutil.copytree(a.source,source);shutil.copytree(a.sdk,sdk)
  before=inventory(sdk);source_before=inventory(source);sibling=r.out/'sibling';sibling.mkdir();(sibling/'sentinel').write_bytes(b'preserve')
  r.receipt.update(producer=descriptor(__file__),sdkBefore=before,sourceBefore=source_before,cases=[])
  def negative(label,argv,needle,env=None,staging=False):
   old=dict(r.env)
   if env:
    for key,value in env.items():
     if value is None:r.env.pop(key,None)
     else:r.env[key]=value
   prior=set(r.out.glob('.dotj-stage-*'));r(label,argv,120,False);r.env=old
   op=r.receipt['operations'][-1];assert op['process']['exitCode']!=0 and not any(op['process'].get(k) for k in ['timedOut','error','cleanupError','outputLimitExceeded'])
   raw=(r.out/(label+'.stdout')).read_bytes()+(r.out/(label+'.stderr')).read_bytes();assert needle in raw,(label,raw)
   new=set(r.out.glob('.dotj-stage-*'))-prior;assert bool(new)==staging,(label,new)
   assert inventory(sdk)==before and inventory(sibling)['sentinel']['sha256']==hashlib.sha256(b'preserve').hexdigest()
   r.receipt['cases'].append(dict(label=label,expectedDiagnostic=needle.decode(),newStages=[str(x) for x in new],priorSdkUnchanged=True));r.save()
  build=lambda s:ps_command(s/'dotj-sdk/seed/build.ps1',[str(sdk)])
  launch=lambda tail:ps_command(sdk/'dotj.ps1',tail)
  negative('missing-java-home',build(source),b'JAVA_HOME_REQUIRED',{'JAVA_HOME':None})
  negative('missing-java',build(source),b'JDK_JAVA_MISSING',{'JAVA_HOME':str(r.out/'absent-jdk')})
  negative('unicode-jdk-admission',build(source),b'JDK_INSTALL_PATH_PROFILE',{'JAVA_HOME':str(r.out/'jdk\u6771\u4eac')})
  negative('ambient-classpath',build(source),b'AMBIENT_JAVA_ENVIRONMENT',{'CLASSPATH':str(r.out)})
  negative('build-root-conflict',build(source),b'DOTJ_ROOT_CONFLICT',{'DOTJ_ROOT':str(sibling)})
  negative('runtime-root-conflict',launch(['--help']),b'DOTJ_ROOT_CONFLICT',{'DOTJ_ROOT':str(sibling)})
  global_json=r.out/'global.json';global_json.write_text('{}')
  negative('build-global-json',build(source),b'GLOBAL_JSON_SELECTION_UNSUPPORTED')
  negative('runtime-global-json',launch(['--help']),b'GLOBAL_JSON_SELECTION_UNSUPPORTED')
  global_json.rename(r.out/'retained-global.json')
  for label,relative in [('source-mutation','dotj-sdk/src/org/dotj/internal/build/evaluation/SdkMain.java'),('manifest-mutation','dotj-sdk/seed/sources.properties')]:
   mutated=r.out/label;shutil.copytree(source,mutated);f=mutated/relative;f.write_bytes(f.read_bytes()+b'\n// changed\n')
   negative(label,build(mutated),b'SOURCE_IDENTITY' if label=='source-mutation' else b'SOURCE_MANIFEST_IDENTITY')
  jdk=r.out/'mutated-jdk';shutil.copytree(JDK.parent,jdk)
  for relative in ['release','bin/javac.exe','bin/jar.exe']:
   file=jdk/relative;raw=file.read_bytes();file.write_bytes(raw+b'\n')
   negative('jdk-mutation-'+file.stem,build(source),b'JDK_IDENTITY',{'JAVA_HOME':str(jdk)})
   file.write_bytes(raw)
  lock=descriptor(source/'dotj-sdk/seed/sources.properties')['sha256']
  negative('missing-jar-provider',[JDK/'java.exe',*vm(r.out),'--limit-modules','java.base,java.xml,jdk.compiler','-Ddotj.seed.script='+str(source/'dotj-sdk/seed/build.ps1'),'--source','21',source/'dotj-sdk/seed/Bootstrap.java',source,sdk,lock],b'JDK_TOOL_PROVIDER_MISSING')
  bad=r.out/'compiler-failure-source';shutil.copytree(source,bad);f=bad/'dotj-sdk/src/org/dotj/internal/build/evaluation/SdkMain.java';f.write_text(f.read_text()+'\nTHIS IS A DELIBERATE COMPILER FAILURE\n');relock(bad)
  negative('compile-failure',build(bad),b'COMPILATION_FAILED',staging=True)
  # The original, complete SDK remains runnable after a real provider failure.
  r('prior-after-compile-failure',launch(['--version']),20)
  assert (r.out/'prior-after-compile-failure.stdout').read_bytes()==b'0.1.100-dev.1\r\n'
  prior=set(r.out.glob('.dotj-stage-*'));event=threading.Event();observed=[];threads=[]
  class InterruptJob(r.guard.Job):
   def resume(self,process):
    super().resume(process)
    def watch():
     until=time.monotonic()+110
     while time.monotonic()<until and not event.wait(.01):
      new=set(r.out.glob('.dotj-stage-*'))-prior
      if new:
       observed.extend(str(x) for x in new);self.terminate();return
    thread=threading.Thread(target=watch);threads.append(thread);thread.start()
  label='controlled-interrupt';op={'label':label};r.receipt['operations'].append(op)
  _,samples=r.guard.wait_resources(time.monotonic()+120);r.receipt['resources'].extend(samples)
  def update(v):op['process']=v;r.save()
  try:r.guard.run(build(source),r.out,r.env,label,120,job_factory=InterruptJob,on_update=update,prelaunch=lambda: (_ for _ in ()).throw(ValueError('resource floor')) if not r.guard.resource_ready(r.guard.memory()) else None)
  finally:
   event.set()
   for t in threads:t.join(5)
  for stream in ['stdout','stderr']:op[stream]=descriptor(r.out/(label+'.'+stream))
  assert observed and op['process']['exitCode']==125 and not op['process'].get('cleanupError')
  assert inventory(sdk)==before and inventory(source)==source_before
  r.receipt['controlledInterruption']=dict(observedStages=observed,ownedJobTerminated=True,priorSdkUnchanged=True,sourceUnchanged=True)
  r('prior-after-interrupt',launch(['--version']),20)
  assert (r.out/'prior-after-interrupt.stdout').read_bytes()==b'0.1.100-dev.1\r\n'
  project=r.out/'unsupported.proj';project.write_text('<Project Sdk="Unqualified"><PropertyGroup><Probe>x</Probe></PropertyGroup></Project>')
  negative('sdk-style',launch(['msbuild',str(project),'-getProperty:Probe']),b'OUTSIDE_ADMITTED_PROFILE')
  alias=r.out/'sdk-alias';cmd="$ErrorActionPreference='Stop'; New-Item -ItemType Junction -Path '"+str(alias)+"' -Target '"+str(sdk)+"' | Out-Null"
  r('make-owned-junction',['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-Command',cmd],20)
  negative('junction-root',ps_command(alias/'dotj.ps1',['--help']),b'SYMLINK_PROFILE')
  r.receipt.update(sdkAfter=inventory(sdk),sourceAfter=inventory(source),siblingAfter=inventory(sibling))
 except BaseException as caught:error=caught
 r.finish(error)
 if error:raise error
 print(json.dumps(dict(status='PASS_WINDOWS_RECOVERY_BOUNDARIES',cases=len(r.receipt['cases']))))
if __name__=='__main__':main()
