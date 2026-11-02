"""Pin the selected source contract and exact historical surface successors."""
import hashlib,json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import qualify as q
p=q.p;c=p.c

def main():
    source=p.B/'reference/upstream/runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6'
    task=source/'src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/Task.cs'
    tests=source/'src/libraries/System.Runtime/tests/System.Threading.Tasks.Tests/Task/TaskRtTests.cs'
    c.require(c.sha(task)=='5b0d6892267269233dcf5c6191f357b0ba6c4257d1e757ca4d2fe93272b29d9b' and c.sha(tests)=='27fa4f56273d730d5cb0266947ac10281b78ec73471281673c55721034c11366','pinned upstream source')
    old=p.HERE;rows=[]
    for name in ['TaskBoundaryControls.java','WorkTaskBoundaryControls.java','expected-public-surface-v1.txt']:
        before=(old/name).read_text(encoding='utf-8');after=(q.HERE/name).read_text(encoding='utf-8')
        if name=='TaskBoundaryControls.java':
            needle='!java.util.Arrays.equals(method.getParameterTypes(), new Class<?>[]{parameter})'
            expected=before.replace(needle,'(!java.util.Arrays.equals(method.getParameterTypes(), new Class<?>[]{parameter}) && !(method.getName().equals("Run") && java.util.Arrays.equals(method.getParameterTypes(), new Class<?>[]{Action.class,CancellationToken.class})))')
        elif name=='WorkTaskBoundaryControls.java':expected=before.replace('exactPublicSurface(Task.class,Set.of(','exactPublicSurface(Task.class,Set.of("method|public|static|Run|(LSystem/Action;LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;",')
        else:expected=before.rstrip('\n')+'\n'+q.ADDITION+'\n'
        c.require(after==expected,'exact one-overload successor '+name)
        rows.append(dict(original=c.descriptor(old/name),successor=c.descriptor(q.HERE/name),allowedChange='Exactly one static Task.Run(Action,CancellationToken) surface entry; all behavior checks and original counts preserved'))
    p.write(q.HERE/'historical-successors-v1.json',rows)
    cases=[]
    for name in ['PublicTaskRunTokenOracle.cs','SupplementRunTokenOracle.cs']:
        for value in re.findall(r'"([a-z]+(?:-[a-z]+)+|none|default|live|precanceled)"',(q.HERE/name).read_text()):
            if value not in cases and value not in ['utf-8']:cases.append(value)
    contract=dict(version=1,batch=2519,selectedApi='public static System.Threading.Tasks.Task Run(System.Action action, System.Threading.CancellationToken cancellationToken)',publicDelta=q.ADDITION,
        adoptedPlan=dict(path=str(p.O/'next-core-run-token-scope-plan-v1.json'),sha256='4bda2ea05f65010517d72575f50358ca84869cf3b0dd4b265be856a456a8b726'),
        runtimeSource=c.descriptor(task),upstreamTests=c.descriptor(tests),runtimeRevision='4271d88e0aebf3d04f188f1334c2220d80555ef6',
        sourceAnchors=dict(nullAction='Task.cs507-522',noRegistration='Task.cs605-650 QueuedByRuntime exclusion; InternalStartNew1141-1156',queue='Task.cs1658-1691',entry='Task.cs2238-2296',matchingOce='Task.cs2413-2434',publicRun='Task.cs5525-5546'),
        upstreamMapping=[dict(method='TaskRtTests.RunRunTests',assertions='Selected Action live-token body invocation and RanToCompletion; no upstream generic/AttachedToParent execution',designedCases=['live','none','default']),dict(method='TaskRtTests.RunRunTests_Cancellation_Negative',assertions='Selected precanceled Action suppression and IsCanceled; await replaces unsupported public Wait',designedCases=['precanceled'])],
        designedFixtureSources=[c.descriptor(q.HERE/name) for name in ['PublicTaskRunTokenOracle.cs','PublicTaskRunTokenFixtures.java','SupplementRunTokenOracle.cs','SupplementRunTokenFixtures.java','TaskRunTokenControls.java']],
        semantics=['Validate action before Java token null','Always queue including requested tokens; no return-time status contract','Worker checks requested token once before invoking action','Cancellation after entry neither interrupts nor forces cancellation','Only associated requested token equal to thrown OCE token cancels; original OCE retained for repeated awaits','Unrequested/default/foreign/null Java OCE token faults; ordinary failures fault despite requests','No Run registration/CTR/timer ownership; completion dispatch outside action catch','Old Run(Action) keeps all-OCE-fault behavior'],
        fieldNormalization=dict(repeatIdentity='For synthesized skip TaskCanceledException with no original action exception, this is a vacuous original-identity assertion. No synthesized exception object reuse is claimed. Matching action OCE and fault identities are compared directly.',taskIdentity='TaskCanceledException payload identity; other exceptions vacuous',heldRunning='Only emitted while an entered action is blocked; never status at Run return'),
        javaAdaptations=['Java null token validation and null OCE token faults are separate representation controls','No inheritable JVM state from creator at fresh daemon construction is a correction to the predecessor shared helper; it is source-derived predecessor behavior, not an observed predecessor run','Cached workers are not cleared of arbitrary task-written ThreadLocals; no CLR ExecutionContext capture claim','Foreign Java Throwable wrapped with original cause','Rejected executor reports on new daemon and invokes work in finally; catastrophic thread creation failures remain outside delivery guarantee','Private held executor/after-entry barrier gives source-supported ordering, not a CLR scheduling observation'],
        exclusions=['generic Task/TCS/ValueTask arity','Func/unwrap Run','custom scheduler/creation options','ExecutionContext parity','public .j execution','CTS/CTR/Delay redesign','whole WP02/N01/NF acceptance','E01 release rights'],
        acceptanceCredit=0,acceptedTasks='0/1092 (0%)',openAcceptanceItems=1686,qualifiedFrameworks='0/66',wholeProjectRemainingBatches='UNKNOWN',e01Decisions='All three OPEN')
    p.write(p.E/'public-task-run-token-contract-v1.json',contract)
    p.write(p.E/'n01-selected-task-run-token-v1.json',dict(version=1,api=contract['selectedApi'],java='System.Threading.Tasks.Task.Run(System.Action,System.Threading.CancellationToken)',historicalLedger='n01-public-method-dispositions-v10.0.12.json',historicalDisposition='INDIVIDUAL_SYNTAX_ONLY Batch422/909; original bytes preserved',selectedContract=c.descriptor(p.E/'public-task-run-token-contract-v1.json'),wholeN01Qualified=False,acceptanceCredit=0))
    print('PASS selected contract/source pins and three exact surface successors')

if __name__=='__main__':main()
