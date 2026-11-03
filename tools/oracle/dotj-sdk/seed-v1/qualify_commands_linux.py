"""Finite cohort containers exercising the exact Linux source-built SDK."""
import argparse,json,sys,shlex
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from owned import Run,B,container,docker_argv
from capture_native import descriptor,fixtures,inventory,save
from check_contract import validate
from qualify_commands import check

def main():
 p=argparse.ArgumentParser()
 for n in ['sdk','attempt','work-root','observations']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();a.attempt.mkdir();contract=json.loads((Path(__file__).parent/'contract.json').read_text(encoding='utf-8'));validate(contract)
 native=json.loads(a.observations.read_text(encoding='utf-8'));refs={(v['cohort'],v['variant']):v for v in native['rows'] if v['platform']=='linux'}
 manifest=dict(status='RUNNING',producer=descriptor(__file__),sdk=str(a.sdk),observations=descriptor(a.observations),cohorts=[])
 save(a.attempt/'manifest.json',manifest)
 for q in dict.fromkeys(c['id'] for c in contract['cases']):
  r=Run(a.attempt/q,True);error=None;slot=a.attempt.name+'-'+q.lower();cases=[c for c in contract['cases'] if c['id']==q]
  try:
   frozen=fixtures(contract,r.out/'fixtures');assert not (a.work_root/slot).exists()
   script='set -eu\nmkdir /work/'+slot+'\ncd /work/'+slot+'\nmkdir home tmp cache\n'
   rows=[]
   for i,c in enumerate(cases):
    argv=[s.replace('{fixtures}','/fixtures') for s in c['argv']];label=f'query-{i:02}'
    command=['/usr/bin/timeout','-s','KILL','20','/usr/bin/env','-i','JAVA_HOME=/jdk','LANG=C.UTF-8','LC_ALL=C.UTF-8','PATH=/nonexistent','HOME=/work/'+slot+'/home','TMPDIR=/work/'+slot+'/tmp','/bin/sh','/sdk/dotj',*argv]
    script+='set +e\n'+shlex.join(command)+' > '+label+'.stdout 2> '+label+'.stderr\nprintf "%s\\n" "$?" > '+label+'.exit\nset -e\n'
    rows.append(dict(case=c,logicalArgv=argv,command=command,label=label))
   sp=r.out/'run.sh';sp.write_text(script,encoding='utf-8',newline='\n')
   name='dotj-task136-'+slot
   argv=docker_argv(name,[(a.sdk,'/sdk',True),(B/'toolchains/jdk-linux21/jdk-21.0.12.1+1','/jdk',True),(r.out/'fixtures','/fixtures',True),(a.work_root,'/work',False)],dict(LANG='C.UTF-8',LC_ALL='C.UTF-8'),['/bin/sh','-c',script])
   r.receipt.update(producer=descriptor(__file__),script=descriptor(sp),rows=rows,fixturesBefore=frozen)
   container(r,name,argv)
   for row in rows:
    label=row['label'];work=a.work_root/slot;out=work/(label+'.stdout');err=work/(label+'.stderr');code=int((work/(label+'.exit')).read_text())
    c=row['case'];check(c,code,out.read_bytes(),err.read_bytes(),refs[(c['id'],c['variant'])],'linux')
    row.update(stdout=descriptor(out),stderr=descriptor(err),exit=descriptor(work/(label+'.exit')),exitCode=code,status='EXPECTED_CAPABILITY_REFUSAL' if q in ['Q14','Q15'] else 'PASS_SELECTED_CONTRACT')
   assert inventory(r.out/'fixtures')==frozen
   r.receipt['fixturesAfter']=inventory(r.out/'fixtures')
  except BaseException as caught:error=caught
  r.finish(error);manifest['cohorts'].append(descriptor(r.out/'receipt.json'));save(a.attempt/'manifest.json',manifest)
  if error:raise error
 manifest.update(status='PASS',cohortCount=16,invocations=34);save(a.attempt/'manifest.json',manifest)
 print(json.dumps(dict(status='PASS_LINUX_COMMANDS',cohorts=16,invocations=34,manifest=descriptor(a.attempt/'manifest.json'))))
if __name__=='__main__':main()
