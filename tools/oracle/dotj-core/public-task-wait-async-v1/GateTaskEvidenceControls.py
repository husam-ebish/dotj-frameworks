"""Finite Python-only tests of the actual aggregate helper and retained records."""
import json,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import qualify as q
p=q.p;c=p.c
def main():
    out=Path(sys.argv[1]);c.confined(out);c.require(not out.exists(),'fresh aggregate controls');out.mkdir()
    gate=p.load('actual_wait_task_gate_binding',q.HERE.parent/'run-foundation-public-candidate-gate.py');original=gate.EVIDENCE;results=[]
    def mark(name):results.append(dict(control=name,passed=True))
    def selected(directory):
        gate.EVIDENCE=directory
        name=gate.selected_task_evidence_name(directory)
        return name,gate.read(name)
    def bind(directory,expected):
        name,data=selected(directory);assert data['candidateJar']['sha256']==expected;return name
    current=c.read(p.E/'foundation-product-candidate-v1.json')['jarSha256'];c.require(current=='1b3de7eba209fcb45d29f637fa2f1f3835095b51a9b52ac90efe06236383b8d7','actual final artifact');c.require(bind(original,current)=='public-task-wait-async-v1.json','real current selection');mark('actual-current-Wait-record-replacement')
    previous=p.B/'worktrees/dotj-core-task-run-cancellation-v1/planning/stage-2/repos/dotj-core/evidence';c.require(bind(previous,q.BASELINE_SHA)=='public-task-run-token-v1.json','actual retained predecessor selection');mark('actual-retained-Run-record-18f9')
    try:bind(previous,current)
    except AssertionError:mark('legacy-record-cannot-qualify-current-replacement')
    else:raise AssertionError('legacy qualified current')
    model=out/'model';model.mkdir();shutil.copyfile(previous/'public-task-run-token-v1.json',model/'public-task-run-token-v1.json');c.require(bind(model,q.BASELINE_SHA)=='public-task-run-token-v1.json','actual legacy-only bytes');mark('legacy-only-fallback')
    shutil.copyfile(original/'public-task-wait-async-v1.json',model/'public-task-wait-async-v1.json');c.require(bind(model,current)=='public-task-wait-async-v1.json','current takes precedence');mark('both-real-records-prefer-current')
    wrong=c.read(model/'public-task-wait-async-v1.json');wrong['candidateJar']['sha256']='0'*64;p.write(model/'public-task-wait-async-v1.json',wrong)
    try:bind(model,current)
    except AssertionError:mark('present-wrong-Wait-refuses-without-legacy-fallback')
    else:raise AssertionError('wrong Wait accepted')
    (model/'public-task-wait-async-v1.json').write_text('{malformed',encoding='utf-8')
    try:selected(model)
    except json.JSONDecodeError:mark('present-malformed-Wait-refuses-without-fallback')
    else:raise AssertionError('malformed Wait fell back')
    gate.EVIDENCE=original
    required=('public-task-wait-async-v1.json','public-task-wait-async-contract-v1.json','public-task-wait-async-preservation-v1.json','n01-selected-task-wait-async-v1.json')
    c.require(gate.WAIT_ASYNC_EVIDENCE_FILES==required and all((original/name).is_file() for name in required),'four actual noncircular current proof files');mark('four-actual-noncircular-Wait-proof-bindings')
    c.require(c.sha(p.ROOT/c.read(p.E/'foundation-product-candidate-v1.json')['jarPath'])==current,'actual current JAR hash retained');mark('actual-current-JAR-assertion')
    p.write(out/'receipt.json',dict(status='PASS',controls=results,source=c.descriptor(__file__),actualGate=c.descriptor(q.HERE.parent/'run-foundation-public-candidate-gate.py'),currentEvidence=c.descriptor(original/'public-task-wait-async-v1.json'),retainedEvidence=c.descriptor(previous/'public-task-run-token-v1.json'),actualNativeExecutions=0,actualJvmExecutions=0,actualFullGateExecutions=0))
    print('PASS actual gate task evidence binding',len(results),'controls')
if __name__=='__main__':main()
