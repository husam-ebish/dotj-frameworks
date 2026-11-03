"""Second independent Linux build with physical Unicode JDK/source/SDK relocation."""
import argparse,json,sys,shlex,hashlib,zipfile,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from owned import Run,B,container,docker_argv
from capture_native import descriptor,inventory

def main():
 p=argparse.ArgumentParser()
 for n in ['source','attempt','work-root']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();r=Run(a.attempt,True);error=None;slot=a.attempt.name
 try:
  base='/work/'+slot;suffix=' spaces \u6771\u4eac & (owned)';src=base+'/source'+suffix;jdk='/jdk'+suffix;sdk=base+'/sdk'+suffix;moved=base+'/relocated'+suffix;project=base+'/project'+suffix+'.proj'
  q=shlex.quote
  env=['/usr/bin/env','-i','JAVA_HOME='+jdk,'LANG=C.UTF-8','LC_ALL=C.UTF-8','PATH=/nonexistent','HOME='+base+'/home','TMPDIR='+base+'/tmp']
  script='set -eu\nmkdir '+q(base)+'\ncd '+q(base)+'\nmkdir home tmp\ncp -R /source '+q(src)+'\n'
  script+='printf "%s\\n" "package org.dotj.internal.build.evaluation; class Ambient { INVALID SOURCE }" > '+q(src+'/dotj-sdk/src/org/dotj/internal/build/evaluation/Ambient.java')+'\n'
  script+=shlex.join(env+['/bin/sh',src+'/dotj-sdk/seed/build.sh',sdk])+' > build.stdout 2> build.stderr\n'
  script+='mv '+q(sdk)+' '+q(moved)+'\nprintf "%s\\n" '+q('<Project><PropertyGroup><Probe>original</Probe></PropertyGroup></Project>')+' > '+q(project)+'\n'
  values=['caf\u00e9 \u6771\u4eac & | ^ < > ! "quoted" \\', '']
  for i,value in enumerate(values):
   script+=shlex.join(env+['/bin/sh',moved+'/dotj','msbuild',Path(project).name,'-getProperty:Probe','-p:Probe='+value])+f' > unicode-{i}.stdout 2> unicode-{i}.stderr\n'
  script+='set +e\n'+shlex.join(env+['/bin/sh',moved+'/dotj','msbuild',Path(project).name,'','-getProperty:Probe'])+' > empty.stdout 2> empty.stderr\nprintf "%s\\n" "$?" > empty.exit\nset -e\n'
  script+='touch CaseProbe caseprobe\ntest "$(find . -maxdepth 1 -name \'*robe\' | wc -l)" -eq 2\nstat -f -c "%T" . > filesystem.txt\n'
  relocated_jdk=r.out/('jdk'+suffix);shutil.copytree(B/'toolchains/jdk-linux21/jdk-21.0.12.1+1',relocated_jdk)
  r.receipt['relocatedJdkInputs']=inventory(relocated_jdk)
  sp=r.out/'run.sh';sp.write_text(script,encoding='utf-8',newline='\n');name='dotj-task136-'+slot
  r.receipt.update(producer=descriptor(__file__),script=descriptor(sp),sourceInputs=inventory(a.source))
  container(r,name,docker_argv(name,[(a.source,'/source',True),(relocated_jdk,jdk,True),(a.work_root,'/work',False)],dict(LANG='C.UTF-8',LC_ALL='C.UTF-8'),['/bin/sh','-c',script]))
  work=a.work_root/slot;actual=work/('relocated'+suffix);pointer=(actual/'current').read_text().splitlines();jar=actual/'versions'/pointer[0]/'dotj.jar'
  for i,value in enumerate(values):
   assert (work/f'unicode-{i}.stdout').read_bytes()==(value+'\n').encode('utf-8')
   assert not (work/f'unicode-{i}.stderr').read_bytes()
  assert (work/'empty.exit').read_text().strip()=='1' and b'EMPTY_ARGUMENT' in (work/'empty.stdout').read_bytes()
  with zipfile.ZipFile(jar) as z:
   assert not any('Ambient' in n for n in z.namelist())
   entries=[dict(name=i.filename,date=list(i.date_time),bytes=i.file_size,sha256=hashlib.sha256(z.read(i)).hexdigest()) for i in z.infolist()]
  stages=list(work.glob('.dotj-stage-*'));assert len(stages)==1 and len(inventory(stages[0]/'source'))==7
  r.receipt.update(jar=descriptor(jar),entries=entries,stagedSources=inventory(stages[0]/'source'),work=str(work),outputs=inventory(work),caseDistinct=True,filesystem=(work/'filesystem.txt').read_text().strip(),locale='C.UTF-8',physicalJdkRelocation=True)
 except BaseException as caught:error=caught
 r.finish(error)
 if error:raise error
 print(json.dumps(dict(status='PASS_LINUX_PHYSICAL_RELOCATION',jar=r.receipt['jar'])))
if __name__=='__main__':main()
