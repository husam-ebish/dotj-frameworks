"""Physical source/JDK/SDK relocation and real Windows Unicode shell transport."""
import argparse,json,sys,shutil,hashlib,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from owned import Run,B
from capture_native import descriptor,inventory
from test_seed import ps_command

def main():
 p=argparse.ArgumentParser()
 for n in ['source','attempt']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();r=Run(a.attempt);error=None
 try:
  suffix=' spaces \u6771\u4eac & (owned)'
  source=r.out/('source'+suffix);jdk=r.out/'jdk spaces & (owned)';sdk=r.out/('sdk'+suffix)
  shutil.copytree(a.source,source);shutil.copytree(B/'toolchains/jdk-qualified/jdk-21.0.12.1+1',jdk)
  # This unlisted Java file must never enter the closed staged source inventory or JAR.
  ambient=source/'dotj-sdk/src/org/dotj/internal/build/evaluation/Ambient.java'
  ambient.write_text('package org.dotj.internal.build.evaluation; class Ambient { THIS MUST NOT COMPILE }\n')
  before=inventory(source);r.env['JAVA_HOME']=str(jdk);r.env['PATH']='C:/Windows/System32'
  r('build',ps_command(source/'dotj-sdk/seed/build.ps1',[str(sdk)]),120)
  pointer=(sdk/'current').read_text().splitlines();jar=sdk/'versions'/pointer[0]/'dotj.jar'
  with zipfile.ZipFile(jar) as z:
   assert not any('Ambient' in n for n in z.namelist())
   r.receipt['entries']=[dict(name=i.filename,date=list(i.date_time),bytes=i.file_size,sha256=hashlib.sha256(z.read(i)).hexdigest()) for i in z.infolist()]
  stages=list(r.out.glob('.dotj-stage-*'));assert len(stages)==1
  staged=inventory(stages[0]/'source');assert len(staged)==7
  r.receipt.update(sourceBefore=before,sourceAfter=inventory(source),stagedSources=staged,jar=descriptor(jar),producer=descriptor(__file__))
  assert r.receipt['sourceBefore']==r.receipt['sourceAfter']
  moved=r.out/('relocated sdk'+suffix);sdk.rename(moved)
  project=r.out/('project'+suffix+'.proj');project.write_text('<Project><PropertyGroup><Probe>original</Probe></PropertyGroup></Project>\n',encoding='utf-8')
  values=['caf\u00e9 \u6771\u4eac & | ^ < > ! "quoted" \\', '']
  for i,value in enumerate(values):
   label='unicode-scalar-'+str(i)
   r(label,ps_command(moved/'dotj.ps1',['msbuild',project.name,'-getProperty:Probe','-p:Probe='+value]),20)
   assert (r.out/(label+'.stdout')).read_bytes()==(value+'\r\n').encode('utf-8')
   assert not (r.out/(label+'.stderr')).read_bytes()
  r('empty-token',ps_command(moved/'dotj.ps1',['msbuild',project.name,'','-getProperty:Probe']),20,False)
  assert r.receipt['operations'][-1]['process']['exitCode']==1
  assert b'argument' in (r.out/'empty-token.stdout').read_bytes().lower()
  # Generate long user input inside PowerShell, avoiding its own EncodedCommand limit.
  test=r.out/'bound.ps1'
  test.write_text("$v=[string]::new([char]0x6771,8000)\n& '"+str(moved/'dotj.ps1').replace("'","''")+"' msbuild '"+str(project).replace("'","''")+"' '-getProperty:Probe' ('-p:Probe='+$v)\nexit $LASTEXITCODE\n",encoding='utf-8-sig')
  r('transport-bound',['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',test],20,False)
  assert r.receipt['operations'][-1]['process']['exitCode']==1
  assert b'WINDOWS_TRANSPORT_BOUND' in (r.out/'transport-bound.stderr').read_bytes()
  r.receipt.update(relocatedSdk=str(moved),relocatedJdk=str(jdk),sourceOnly=True,unlistedAmbientExcluded=True,strictUnicodeScalar=True,emptyTokenPreserved=True,explicitTransportBound=True)
 except BaseException as caught:error=caught
 r.finish(error)
 if error:raise error
 print(json.dumps(dict(status='PASS_WINDOWS_PHYSICAL_RELOCATION_TRANSPORT',jar=r.receipt['jar'])))
if __name__=='__main__':main()

