"""Bounded Linux preflight/failure/interruption controls against a prior usable SDK."""
import argparse,json,sys,shutil,shlex,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from owned import Run,B,container,docker_argv
from capture_native import descriptor,inventory,save
from test_recovery_windows import relock

def main():
 p=argparse.ArgumentParser()
 for n in ['source','sdk','attempt','work-root']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();a.attempt.mkdir();manifest=dict(status='RUNNING',producer=descriptor(__file__),groups=[]);save(a.attempt/'manifest.json',manifest)
 groups=['preflight','source','manifest','jdk-release','jdk-javac','jdk-jar','provider','compiler','interrupt','boundary']
 for group in groups:
  r=Run(a.attempt/group,True);error=None;slot=a.attempt.name+'-'+group;base='/work/'+slot;q=shlex.quote
  try:
   source=r.out/'source';shutil.copytree(a.source,source)
   if group=='source':(source/'dotj-sdk/src/org/dotj/internal/build/evaluation/SdkMain.java').write_bytes((source/'dotj-sdk/src/org/dotj/internal/build/evaluation/SdkMain.java').read_bytes()+b'\n// changed\n')
   if group=='manifest':
    f=source/'dotj-sdk/seed/sources.properties';f.write_bytes(f.read_bytes()+b'\n# changed\n')
   jdk=B/'toolchains/jdk-linux21/jdk-21.0.12.1+1'
   if group.startswith('jdk-'):
    original_jdk=jdk;jdk=r.out/'mutated-jdk';shutil.copytree(original_jdk,jdk)
    relative={'jdk-release':'release','jdk-javac':'bin/javac','jdk-jar':'bin/jar'}[group];f=jdk/relative;f.write_bytes(f.read_bytes()+b'\n')
   if group=='compiler':
    f=source/'dotj-sdk/src/org/dotj/internal/build/evaluation/SdkMain.java';f.write_bytes(f.read_bytes()+b'\nTHIS IS A DELIBERATE COMPILER FAILURE\n');relock(source)
   before=inventory(source);sdkbefore=inventory(a.sdk)
   env=['/usr/bin/env','-i','JAVA_HOME=/jdk','LANG=C.UTF-8','LC_ALL=C.UTF-8','PATH=/nonexistent','HOME='+base+'/home','TMPDIR='+base+'/tmp']
   build=env+['/bin/sh','/source/dotj-sdk/seed/build.sh',base+'/sdk'];launch=env+['/bin/sh',base+'/sdk/dotj']
   script='set -eu\nmkdir '+q(base)+'\ncd '+q(base)+'\nmkdir home tmp sibling\nprintf sentinel > sibling/sentinel\ncp -R /prior sdk\n'
   rows=[]
   def case(label,argv,needle,pre='',post='',success=False):
    nonlocal script
    script+=pre+'\nset +e\n'+shlex.join(['/usr/bin/timeout','-s','KILL','20',*argv])+' > '+label+'.stdout 2> '+label+'.stderr\nprintf "%s\\n" "$?" > '+label+'.exit\nset -e\n'+post+'\n'
    rows.append(dict(label=label,argv=argv,expectedDiagnostic=needle,success=success))
   if group=='preflight':
    case('missing-home',[v for v in build if v!='JAVA_HOME=/jdk'],'JAVA_HOME_REQUIRED')
    case('ambient-classpath',build[:2]+['CLASSPATH=/work']+build[2:],'AMBIENT_JAVA_ENVIRONMENT')
    case('root-conflict',build[:2]+['DOTJ_ROOT=/prior']+build[2:],'DOTJ_ROOT_CONFLICT')
    case('build-global',build,'GLOBAL_JSON_SELECTION_UNSUPPORTED',"printf '{}' > global.json",'mv global.json retained-global.json')
   elif group=='source':case('mutated-source',build,'SOURCE_IDENTITY')
   elif group=='manifest':case('mutated-manifest',build,'SOURCE_MANIFEST_IDENTITY')
   elif group.startswith('jdk-'):case(group,build,'JDK_IDENTITY')
   elif group=='provider':
    lock=descriptor(source/'dotj-sdk/seed/sources.properties')['sha256']
    case('missing-jar-provider',env+['/jdk/bin/java','-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=32m','-XX:-UsePerfData','-Djava.io.tmpdir='+base+'/tmp','-Duser.home='+base+'/home','-XX:ErrorFile='+base+'/tmp/hs_err_pid%p.log','-XX:HeapDumpPath='+base+'/tmp','--limit-modules','java.base,java.xml,jdk.compiler','-Ddotj.seed.script=/source/dotj-sdk/seed/build.sh','--source','21','/source/dotj-sdk/seed/Bootstrap.java','/source',base+'/sdk',lock],'JDK_TOOL_PROVIDER_MISSING')
   elif group=='compiler':case('compiler-failure',build,'COMPILATION_FAILED')
   elif group=='interrupt':
    script+=shlex.join(build)+' > interrupt.stdout 2> interrupt.stderr &\nchild=$!\nwhile [ "$(find . -maxdepth 1 -name \'.dotj-stage-*\' | wc -l)" -eq 0 ]; do /bin/sleep 0.01; done\nfind . -maxdepth 1 -name \'.dotj-stage-*\' > interrupted-stage.txt\nkill -KILL "$child"\nset +e\nwait "$child"\nprintf "%s\\n" "$?" > interrupt.exit\nset -e\n'
   else:
    case('runtime-global',launch+['--help'],'GLOBAL_JSON_SELECTION_UNSUPPORTED',"printf '{}' > global.json",'mv global.json retained-global.json')
    case('runtime-root-conflict',launch[:2]+['DOTJ_ROOT=/prior']+launch[2:]+['--help'],'DOTJ_ROOT_CONFLICT')
    case('symlink-root',env+['/bin/sh',base+'/alias/dotj','--help'],'SYMLINK_PROFILE','ln -s '+q(base+'/sdk')+' alias')
    case('sdk-style',launch+['msbuild','sdk.proj','-getProperty:Probe'],'OUTSIDE_ADMITTED_PROFILE',"printf '%s\\n' '<Project Sdk=\"Unqualified\" />' > sdk.proj")
   case('prior-after',[v.replace('JAVA_HOME=/jdk','JAVA_HOME=/valid-jdk') for v in launch]+['--version'],'0.1.100-dev.1',success=True)
   sp=r.out/'run.sh';sp.write_text(script,encoding='utf-8',newline='\n');name='dotj-task136-'+slot
   r.receipt.update(producer=descriptor(__file__),script=descriptor(sp),sourceBefore=before,sdkBefore=sdkbefore,rows=rows)
   container(r,name,docker_argv(name,[(source,'/source',True),(a.sdk,'/prior',True),(jdk,'/jdk',True),(B/'toolchains/jdk-linux21/jdk-21.0.12.1+1','/valid-jdk',True),(a.work_root,'/work',False)],dict(LANG='C.UTF-8',LC_ALL='C.UTF-8'),['/bin/sh','-c',script]))
   work=a.work_root/slot
   for row in rows:
    label=row['label'];code=int((work/(label+'.exit')).read_text());out=work/(label+'.stdout');err=work/(label+'.stderr')
    assert (code==0)==row['success'] and code not in [124,137],(label,code)
    assert row['expectedDiagnostic'].encode() in out.read_bytes()+err.read_bytes()
    row.update(exitCode=code,stdout=descriptor(out),stderr=descriptor(err),exit=descriptor(work/(label+'.exit')))
   if group=='interrupt':assert (work/'interrupt.exit').read_text().strip()=='137' and (work/'interrupted-stage.txt').read_text().strip()
   stages=list(work.glob('.dotj-stage-*'));assert bool(stages)==(group in ['compiler','interrupt'])
   actual=inventory(work/'sdk');assert {k:(v['bytes'],v['sha256']) for k,v in actual.items()}=={k:(v['bytes'],v['sha256']) for k,v in sdkbefore.items()}
   assert inventory(source)==before and (work/'sibling/sentinel').read_bytes()==b'sentinel'
   r.receipt.update(work=str(work),outputs={f.relative_to(work).as_posix():descriptor(f) for f in work.rglob('*') if not (getattr(f.lstat(),'st_file_attributes',0)&1024) and f.is_file()},sourceAfter=inventory(source),sdkAfter=actual,priorSdkUnchanged=True,sourceUnchanged=True,controlledInterruption=group=='interrupt')
  except BaseException as caught:error=caught
  r.finish(error);manifest['groups'].append(descriptor(r.out/'receipt.json'));save(a.attempt/'manifest.json',manifest)
  if error:raise error
 manifest['status']='PASS';save(a.attempt/'manifest.json',manifest);print(json.dumps(dict(status='PASS_LINUX_RECOVERY',groups=len(groups))))
if __name__=='__main__':main()
