"""Verify current retained WorkTask and legacy groups; never launch a process."""
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def main():
    spec=importlib.util.spec_from_file_location('current_same_jar',Path(__file__).with_name('verify-public-valuetask-task.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    e=module.c.read(module.E/'public-worktask-cancelasync-v1.json')
    module.c.require(module.c.sha(module.E/e['currentEvidence'])==e['currentEvidenceSha256'],'current evidence binding')
    module.c.require(module.c.sha(module.E/e['historicalEvidence'])==e['historicalEvidenceSha256'],'historical evidence retained')
    module.c.require(e['candidateJar']==module.c.read(module.E/e['currentEvidence'])['candidateJar'],'current WorkTask same JAR')
    module.main(legacy=True)
if __name__=='__main__':main()
