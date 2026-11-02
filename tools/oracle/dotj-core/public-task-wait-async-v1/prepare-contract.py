"""Explicit narrow surface successors; frozen predecessor bytes stay unchanged."""
import hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import qualify as q
p=q.p;c=p.c
def main():
    old=HERE.with_name('public-task-run-token-v1');pairs=[]
    for name in ['TaskBoundaryControls.java','WorkTaskBoundaryControls.java','expected-public-surface-v1.txt','historical.py']:
        before=(old/name).read_text(encoding='utf-8');after=before
        if name=='TaskBoundaryControls.java':
            needle='} else check(selected.contains(method.getName()), "Task public surface: " + method);'
            replacement='''} else if (method.getName().equals("WaitAsync")) {
                    var parameters=java.util.Arrays.asList(method.getParameterTypes());
                    if (!(!Modifier.isStatic(method.getModifiers()) && method.getReturnType()==Task.class
                        && (parameters.equals(java.util.List.of(CancellationToken.class))
                            || parameters.equals(java.util.List.of(TimeSpan.class))
                            || parameters.equals(java.util.List.of(TimeSpan.class,CancellationToken.class)))))
                        throw new AssertionError("exact selected WaitAsync overload: " + method);
                } else check(selected.contains(method.getName()), "Task public surface: " + method);'''
            c.require(before.count(needle)==1,'exact Task surface extension');after=before.replace(needle,replacement)
        elif name=='WorkTaskBoundaryControls.java':
            delta=','.join('"method|public|instance|WaitAsync|'+descriptor+'LSystem/Threading/Tasks/Task;"' for descriptor in ['(LSystem/Threading/CancellationToken;)','(LSystem/TimeSpan;)','(LSystem/TimeSpan;LSystem/Threading/CancellationToken;)'])
            after=before.replace('exactPublicSurface(Task.class,Set.of(','exactPublicSurface(Task.class,Set.of('+delta+',')
        elif name=='expected-public-surface-v1.txt':
            additions=['System/Threading/Tasks/Task|M|WaitAsync|'+descriptor+'LSystem/Threading/Tasks/Task;|1' for descriptor in ['(LSystem/Threading/CancellationToken;)','(LSystem/TimeSpan;)','(LSystem/TimeSpan;LSystem/Threading/CancellationToken;)']]
            additions += ['System/TimeoutException|C|1','System/TimeoutException|M|<init>|()V|1','System/TimeoutException|M|<init>|(Ljava/lang/String;)V|1','System/TimeoutException|M|<init>|(Ljava/lang/String;LSystem/Exception;)V|1']
            after=before.rstrip('\n')+'\n'+'\n'.join(additions)+'\n'
        else:after=before.replace('import qualify as q','import batch2520_qualify as q')
        target=HERE/name;c.require(not target.exists(),'new successor destination');target.write_text(after,encoding='utf-8',newline='\n')
        pairs.append(dict(original=c.descriptor(old/name),successor=c.descriptor(target),allowedChange='Only exact three instance WaitAsync overloads and TimeoutException declared class/constructors; historical replay import points at this owned profile; no behavior assertion removed'))
    p.write(HERE/'historical-successors-v1.json',pairs)
    plan=p.B/'orchestration/two-frameworks/next-core-wait-async-scope-plan-v1.json'
    adopted=json.loads(plan.read_text(encoding='utf-8-sig'))
    contract=dict(version=1,batch=2520,scope='Complete nongeneric default-clock Task.WaitAsync family',adoptedPlan=c.descriptor(plan),sourcePins=adopted['evidencePins'],publicSurface=adopted['publicSurface'],sourceSemantics=adopted['sourceSemantics'],privateContract=adopted['minimalPrivateDesign'],matrix=c.descriptor(HERE/'matrix-v2.json'),matrixFreeze=c.descriptor(q.A/'matrix-freeze-v3.json'),actualNative=c.descriptor(q.A/'native-v2/receipt.json'),mapping=adopted['matrixBeforeFirstCapture']['sourceTestMapping'],javaAdaptations=adopted['publicSurface']['javaNullAdaptation'],unsupported=adopted['publicSurface']['explicitUnsupported'],acceptedTasks='0/1092 (0%)',openAcceptanceItems=1686,qualifiedFrameworks='0/66',acceptanceCredit=0,e01Decisions='All three OPEN',wholeProjectBatches='UNKNOWN',batch2519Integration=c.descriptor(p.B/'orchestration/two-frameworks/batch2519-integration-v1.json'))
    p.write(p.E/'public-task-wait-async-contract-v1.json',contract)
    print('PASS exact historical successors and selected WaitAsync contract')
if __name__=='__main__':main()
