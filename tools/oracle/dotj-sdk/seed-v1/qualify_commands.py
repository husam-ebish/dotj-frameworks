"""Real shell commands on one explicit source-built SDK, with byte-level query checks."""
import argparse,json,sys,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture_native import descriptor,fixtures,inventory,save
from check_contract import validate
from test_seed import ps_command
from owned import Run,B

def check(case,code,out,err,native,platform):
    q=case['id'];expectedFailure=q in ['Q11','Q12','Q13','Q14','Q15','Q16']
    assert code==(1 if expectedFailure else 0),(q,case['variant'],code,out,err)
    if q in ['Q05','Q06','Q07','Q08','Q09','Q10']:
        assert out==Path(native['stdout']['path']).read_bytes(),(q,case['variant'],'raw stdout mismatch',out)
    if q=='Q10':assert b'MSB4210' in err and b'MSB4011' in err
    elif q in ['Q11','Q12','Q14','Q15']:
        assert not out and err
        if q=='Q11':assert b'XML_PROFILE' in err
        if q=='Q12':assert b'MSB4019' in err
        if q=='Q14' and case['variant']=='unexecuted-task':assert b'OUTSIDE_ADMITTED_PROFILE TARGET_DECLARATION_PROFILE' in err
        if q=='Q14' and case['variant']!='unexecuted-task':assert b'CAPABILITY_UNSUPPORTED' in err
        if q=='Q15':assert b'COMMAND_UNSUPPORTED' in err and b'Build succeeded' not in err
    elif q in ['Q13','Q16']:assert out and not err
    else:assert not err
    if q=='Q02':assert out==b'0.1.100-dev.1'+(b'\r\n' if platform=='windows' else b'\n')
    if q in ['Q01','Q04']:assert b'Usage: dotj' in out and b'Evaluation-only' in out
    if q=='Q03':assert b'0.1.100-dev.1' in out and b'Microsoft' in out and b'Source SHA256:' in out

def main():
    p=argparse.ArgumentParser();p.add_argument('--sdk',type=Path,required=True);p.add_argument('--attempt',type=Path,required=True);p.add_argument('--observations',type=Path,required=True);a=p.parse_args()
    own=Path(__file__).parent;contract=json.loads((own/'contract.json').read_text(encoding='utf-8'));validate(contract)
    native=json.loads(a.observations.read_text(encoding='utf-8'))
    references={(v['cohort'],v['variant']):v for v in native['rows'] if v['platform']=='windows'}
    run=Run(a.attempt);error=None
    try:
        run.env['JAVA_HOME']=str(B/'toolchains/jdk-qualified/jdk-21.0.12.1+1');run.env['PATH']='C:/Windows/System32'
        frozen=fixtures(contract,run.out/'fixtures');run.receipt.update(sdk=str(a.sdk),rows=[],fixturesBefore=frozen,observations=descriptor(a.observations),producer=descriptor(__file__))
        for index,case in enumerate(contract['cases']):
            argv=[s.replace('{fixtures}',str(run.out/'fixtures')) for s in case['argv']];label=f'query-{index:02}'
            run(label,ps_command(a.sdk/'dotj.ps1',argv),20,False);op=run.receipt['operations'][-1];process=op['process']
            assert not any(process.get(k) for k in ['timedOut','error','cleanupError','outputLimitExceeded'])
            out=(run.out/(label+'.stdout')).read_bytes();err=(run.out/(label+'.stderr')).read_bytes()
            check(case,process['exitCode'],out,err,references[(case['id'],case['variant'])],'windows')
            run.receipt['rows'].append(dict(case=case,logicalArgv=argv,operation=label,stdout=op['stdout'],stderr=op['stderr'],exitCode=process['exitCode'],status='EXPECTED_CAPABILITY_REFUSAL' if case['id'] in ['Q14','Q15'] else 'PASS_SELECTED_CONTRACT'))
            run.save()
        assert inventory(run.out/'fixtures')==frozen
        run.receipt['fixturesAfter']=inventory(run.out/'fixtures');run.receipt['cohorts']=16;run.receipt['invocations']=34
    except BaseException as caught:error=caught
    run.finish(error)
    if error:raise error
    print(json.dumps(dict(status='PASS_SELECTED_WINDOWS_COMMANDS',cohorts=16,invocations=34,receipt=descriptor(run.out/'receipt.json'))))
if __name__=='__main__':main()
