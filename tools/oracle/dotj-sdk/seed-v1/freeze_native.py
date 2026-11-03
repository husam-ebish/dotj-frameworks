"""Check actual finite native observations and retain exact bytes; no product inputs."""
import argparse,json,sys,re,shlex
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture_native import descriptor,save
from check_contract import validate,EXPECTED,require

def raw(d):
 require(descriptor(d['path'])==d,'Observed stream identity')
 return Path(d['path']).read_text(encoding='utf-8-sig').replace('\r\n','\n')

def check(root,platform,contract):
 paths=sorted(root.glob('Q*/receipt.json'))
 require([p.parent.name for p in paths]==list(EXPECTED),'Exact native cohort receipt inventory')
 rows=[]
 for path in paths:
  r=json.loads(path.read_text(encoding='utf-8'));q=path.parent.name
  require(r['status']=='PASS' and r['cohort']==q and r['platform']==platform,'Capture outcome/profile')
  expected=[c for c in contract['cases'] if c['id']==q]
  require(len(r['invocations'])==len(expected) and [v['case'] for v in r['invocations']]==expected,'Exact invocation input/binding inventory '+q)
  require(r['nativeRole']=='ACTUAL_NATIVE_SDK_HOST' and r['nativeInputsUnchanged'],'Native tool role/input binding')
  require(r['fixturesBefore']==r['fixturesAfter'],'Fixture side effects')
  for sample in r['resources']:require(sample['freePhysicalBytes']>=512*1024**2 and sample['freeVirtualBytes']>=16*1024**3,'Resource floors')
  if platform=='linux':
   c=r['container'];h=c['createdInspect']['HostConfig']
   require(c['owner']=='task136' and c['cid'] and c['absenceVerified'] and c['lateAbsenceVerified'],'Container ownership/cleanup')
   require(h['NetworkMode']=='none' and h['ReadonlyRootfs'] and h['Memory']==536870912 and h['MemorySwap']==536870912 and h['PidsLimit']==64,'Container caps')
   require(r['filesystem']['caseDistinct'],'Measured case-sensitive work slot')
   require(r['systemTmpBefore']==[] and isinstance(r['systemTmpAfter'],list),'Private empty-before/full-after system tmp')
   create=next(o for o in r['operations'] if o['label']=='container-create')['process']['argv']
   require('/sdk/dotnet' in create[-1] and 'ReadyToRun' not in '\n'.join(create),'Actual Linux host, no fallback')
  else:require(r['network']['status']=='NETWORK_NOT_ISOLATED','Truthful Windows network facet')
  for index,v in enumerate(r['invocations']):
   case=v['case'];out=raw(v['stdout']);err=raw(v['stderr']);code=v['exitCode']
   require(v['operation']==f'native-{index:02}','Output operation binding')
   fixtureRoot=str(path.parent/'fixtures') if platform=='windows' else '/fixtures'
   exe='D:\\AI\\Implementation\\dotj Frameworks\\toolchains\\dotnet\\dotnet.exe' if platform=='windows' else '/sdk/dotnet'
   expectedArgv=[exe]+[s.replace('{fixtures}',fixtureRoot) for s in case['argv']]
   if case['argv'][0] in ('msbuild','build'):expectedArgv.append('-noAutoResponse')
   require(v['argv']==expectedArgv,'Expected operation argv binding')
   if platform=='windows':
    matches=[o for o in r['operations'] if o['label']==v['operation']]
    require(len(matches)==1,'Unique native operation')
    op=matches[0];require(op['stdout']==v['stdout'] and op['stderr']==v['stderr'] and op['process']['argv']==v['argv'] and op['process']['exitCode']==code,'Exact raw argv/output/exit binding')
   else:
    require(Path(v['stdout']['path']).name==v['operation']+'.stdout' and Path(v['stderr']['path']).name==v['operation']+'.stderr','Linux output-name binding')
    require(v['argv'][0]=='/sdk/dotnet','Linux native host argv')
    command=shlex.join(['/usr/bin/timeout','-s','KILL','20',*v['argv']])
    require(command+' > /parent/'+q+'/'+v['operation']+'.stdout 2> /parent/'+q+'/'+v['operation']+'.stderr' in create[-1],'Linux script/argv/stream binding')
   if case['argv'][0] in ('msbuild','build'):require(v['argv'][-1]=='-noAutoResponse','Native response-file guard')
   expectedFailure=q in ('Q11','Q12','Q13','Q16')
   require(code==(1 if expectedFailure else 0),'Native exit '+q)
   if case['expectation'].startswith('scalar:'):require(out==case['expectation'][7:]+'\n','Scalar value/order/channel '+q)
   if q=='Q07':
    value=json.loads(out);require(set(value)=={'Properties'},'Properties schema')
    props=value['Properties'];require(props['Escaped']=='quote " slash \\ tab\t line\n <>& café 東京','Sensitive JSON value')
    require(list(props)==(['Probe','probe','Escaped'] if case['variant']=='repeated-case' else ['Escaped','Probe']),'JSON query order/exact-key repetition')
    require(props.get('Probe')=='seed-baseline','JSON property')
   if q=='Q10':require('MSB4210' in err and 'MSB4011' in err,'Cycle/duplicate diagnostic stderr')
   if q in ('Q11','Q12'):require(out=='' and ('MSB4025' if q=='Q11' else 'MSB4019') in err,'Evaluation failure stderr')
   if q in ('Q13','Q16'):
    codeText='MSB1001' if q=='Q13' else 'MSB1003' if case['variant']=='zero' else 'MSB1008'
    require(codeText in out,'Command failure stdout')
   if q=='Q14':require(out==('inert\n' if case['variant']=='unexecuted-task' else 'seed-baseline\n'),'Harmless native evaluation/target result')
   if q=='Q15':require('Build succeeded.' in out and '0 Error(s)' in out,'Harmless no-op native build result')
   if q=='Q02':require(out=='10.0.401\n','Actual reference version')
   if q=='Q03':require('10.0.401' in out and ('win-x64' if platform=='windows' else 'linux-x64') in out,'Actual reference info')
   if q in ('Q01','Q04'):require(('Usage:' if q=='Q01' else 'Syntax:') in out,'Help output')
   stderrKind='empty' if not err else 'evaluation-diagnostic' if q in ('Q10','Q11','Q12') else 'host-first-use-information' if 'Welcome to .NET 10.0!' in err else 'other-retained'
   require(stderrKind!='other-retained','Unclassified stderr')
   rows.append(dict(platform=platform,cohort=q,variant=case['variant'],exitCode=code,argv=v['argv'],stdout=v['stdout'],stderr=v['stderr'],stderrKind=stderrKind,receipt=descriptor(path),candidateDisposition='CAPABILITY_REFUSAL_OUTSIDE_ADMITTED_PROFILE' if q in ('Q14','Q15') else 'FROZEN_NATIVE_CONTRACT',filesystem=r.get('filesystem',{}).get('type','Windows NTFS case-insensitive attempt directory'),network=r['network']))
 require(len(rows)==34,'Native observation cardinality')
 return rows

def main():
 p=argparse.ArgumentParser();p.add_argument('--windows',type=Path,required=True);p.add_argument('--linux',type=Path,required=True);p.add_argument('--contract',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 c=json.loads(a.contract.read_text(encoding='utf-8'));validate(c)
 rows=check(a.windows,'windows',c)+check(a.linux,'linux',c)
 a.out.mkdir(parents=True,exist_ok=False)
 result=dict(status='FROZEN_NATIVE_OBSERVATIONS_NOT_PRODUCT_QUALIFICATION',contract=descriptor(a.contract),reader=descriptor(__file__),cohorts=32,invocations=68,rows=rows,
  decisions=['Reference fresh-home welcome stderr retained, never blanket-stripped; owned help/version identity differs intentionally','Q07 repeated names retain exact case-sensitive JSON keys; duplicate exact spelling overwritten in insertion position','Native Q14 targets and unexecuted task and Q15 no-op build succeed; candidate explicit capability refusal is a gap, not parity','Q13/Q16 command diagnostics stdout; Q11/Q12 evaluation diagnostics stderr; Q10 warning stderr with clean query stdout','Windows network not isolated/offline facet NOT_QUALIFIED; Linux actual namespace network none'],productPasses=0)
 save(a.out/'observations.json',result);print(json.dumps(descriptor(a.out/'observations.json')))
if __name__=='__main__':main()
