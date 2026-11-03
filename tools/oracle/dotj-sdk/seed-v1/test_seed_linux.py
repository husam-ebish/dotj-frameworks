"""Fresh Linux source-only build in measured case-enabled 9p/NTFS work slots."""
import argparse,json,sys,hashlib,zipfile,shlex
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture_native import descriptor,inventory
from owned import Run,B,container,docker_argv

def main():
 p=argparse.ArgumentParser()
 for n in ['source','attempt','work-root']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();run=Run(a.attempt,True);error=None;slot=a.attempt.name
 try:
  assert a.work_root.is_dir() and not (a.work_root/slot).exists()
  script=run.out/'run.sh'
  text='''set -eu
mkdir /work/SLOT
cd /work/SLOT
mkdir source-root home tmp cache empty
cp -R /source/. source-root/
touch CaseProbe caseprobe
test "$(find . -maxdepth 1 -name '*robe' | wc -l)" -eq 2
stat -f -c '%T' . > filesystem.txt
env -i JAVA_HOME=/jdk LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/nonexistent HOME=/work/SLOT/home TMPDIR=/work/SLOT/tmp /bin/sh /work/SLOT/source-root/dotj-sdk/seed/build.sh /work/SLOT/sdk > build.stdout 2> build.stderr
printf '%s\n' '<Project><PropertyGroup><Probe>seed-baseline</Probe></PropertyGroup></Project>' > probe.proj
env -i JAVA_HOME=/jdk LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/nonexistent HOME=/work/SLOT/home TMPDIR=/work/SLOT/tmp /bin/sh /work/SLOT/sdk/dotj --help > help.stdout 2> help.stderr
env -i JAVA_HOME=/jdk LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/nonexistent HOME=/work/SLOT/home TMPDIR=/work/SLOT/tmp /bin/sh /work/SLOT/sdk/dotj msbuild /work/SLOT/probe.proj '-getProperty:Probe' > query.stdout 2> query.stderr
'''.replace('SLOT',slot)
  script.write_text(text,encoding='utf-8',newline='\n')
  jdk=B/'toolchains/jdk-linux21/jdk-21.0.12.1+1'
  argv=docker_argv('dotj-task136-'+slot,[(a.source,'/source',True),(jdk,'/jdk',True),(a.work_root,'/work',False)],dict(HOME='/work/'+slot+'/home',TMPDIR='/work/'+slot+'/tmp',LANG='C.UTF-8',LC_ALL='C.UTF-8'),['/bin/sh','-c',text])
  run.receipt.update(producer=descriptor(__file__),script=descriptor(script),sourceInputs=inventory(a.source),sourceRoot=str(a.source),logicalBuildArgv=['/bin/sh','/work/'+slot+'/source-root/dotj-sdk/seed/build.sh','/work/'+slot+'/sdk'])
  container(run,'dotj-task136-'+slot,argv)
  work=a.work_root/slot;pointer=(work/'sdk/current').read_text().splitlines();jar=work/'sdk/versions'/pointer[0]/'dotj.jar'
  assert descriptor(jar)['sha256']==pointer[1]
  assert (work/'query.stdout').read_bytes()==b'seed-baseline\n' and not (work/'query.stderr').read_bytes()
  assert b'Usage: dotj' in (work/'help.stdout').read_bytes() and not (work/'help.stderr').read_bytes()
  with zipfile.ZipFile(jar) as z:classes={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.endswith('.class')}
  run.receipt.update(jar=descriptor(jar),classes=classes,work=str(work),outputs=inventory(work),filesystem=(work/'filesystem.txt').read_text().strip(),caseDistinct=True,sourceOnlyPath='/nonexistent')
 except BaseException as caught:error=caught
 run.finish(error)
 if error:raise error
 print(json.dumps(dict(status='PASS_LINUX_SOURCE_BUILD_HELP_QUERY',jar=descriptor(jar))))
if __name__=='__main__':main()
