"""New-consumer forgery controls only; does not rerun unchanged historical mocks."""
import copy
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import product_support as p
import verify_product as v

def run():
    e=p.c.read(p.E/'public-task-delay-v1.json')
    result=v.validate(e)
    r=p.c.read(e['paired']['path']);original=r['commands'][0]
    passed=[]
    for label,change in [
      ('typed-pid',lambda x:x.update(processId=True)),
      ('ownership',lambda x:x.update(jobAssigned=False)),
      ('resume',lambda x:x.update(resumed=False)),
      ('exit-status',lambda x:x.update(exitCode=True)),
      ('timeout',lambda x:x.update(timedOut=True)),
      ('output-cap',lambda x:x.update(outputLimitExceeded=True)),
      ('freshness',lambda x:x.update(resourceSampleAgeSeconds=3)),
      ('commit-floor',lambda x:x['resources'][-1].update(freeVirtualBytes=0)),
      ('stream-limit',lambda x:x['outputLimitsBytes'].update(stderr=99999999)),
      ('raw-stream-hash',lambda x:x['streams']['stdout'].update(sha256='0'*64)),
      ('environment',lambda x:x['environment'].update(TEMP='C:/tmp'))]:
        forged=copy.deepcopy(original);change(forged)
        try:v.command(forged)
        except (ValueError,OSError):passed.append(label)
        else:raise AssertionError('accepted consumed-contract forgery '+label)
    p.c.require(not v.group_command({'label':'run-task-boundaries-0'},'task') and v.group_command({'label':'run-task-0'},'task'),'group identity prefix forgery')
    passed.append('group-identity-prefix')
    group=r['groups'][0]
    forged=copy.deepcopy(r['commands']);forged[0]['argv'].insert(-1,'-classpath')
    try:v.actual_group(group,forged,e['candidateJar']['path'])
    except ValueError:passed.append('consumer-argv')
    else:raise AssertionError('accepted extra consumer compile switch')
    source=(p.ROOT/'dotj-core/dotj-core-public/src/main/java/System/Threading/Tasks/Task.java').read_text(encoding='utf-8')
    for name,fragment in [
      ('no-token-int-forwarding','public static Task Delay(int millisecondsDelay) {\n        return delay(millisecondsDelay, CancellationToken.get_None(), null);\n    }'),
      ('no-token-span-forwarding','public static Task Delay(TimeSpan delay) {\n        return delay(delay, CancellationToken.get_None(), null);\n    }'),
      ('token-int-forwarding','public static Task Delay(int millisecondsDelay, CancellationToken cancellationToken) {\n        return delay(millisecondsDelay, cancellationToken, null);\n    }'),
      ('token-span-forwarding','public static Task Delay(TimeSpan delay, CancellationToken cancellationToken) {\n        return delay(delay, cancellationToken, null);\n    }')]:
        p.c.require(source.count(fragment)==1,'actual production wrapper forwarding '+name);passed.append(name)
    return dict(status='PASS_NEW_CONSUMED_CONTRACT_NEGATIVES',actualControls=len(passed),passed=passed,positiveActualEvidence=result,old69ControlsRerun=False,workloadChildren=0)

if __name__=='__main__':
    result=run();p.write(p.A/'changed-consumed-contract-controls-v1.json',result)
    print('PASS new consumed-contract negatives',result['actualControls'])
