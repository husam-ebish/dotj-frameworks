"""Bind completed selected phases. Foundation completion is recorded separately."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import qualify as q
p=q.p;c=p.c

def main():
    roots={'baseline':'baseline-v1','native':'native-v1','nativeSupplement':'native-supplement-v1','build':'build-v2','paired':'paired-v1','pairedSupplement':'paired-supplement-v1','private':'private-v1','historicalPartial':'historical-v1','historicalTail':'historical-tail-v2','audits':'audits-v1'}
    phases={key:c.descriptor(q.A/name/'receipt.json') for key,name in roots.items()}
    jar=c.read(phases['build']['path'])['candidateJar'];c.validate_pin(jar)
    versions=[]
    for key,pin in phases.items():
        r=c.read(pin['path']);outer=Path(pin['path']).parent.with_name(Path(pin['path']).parent.name+'-outer')
        producer=next(x for x in r['inputs'] if x['original']['path'].endswith('qualify.py'))
        versions.append(dict(phase=key,executedProducer=producer['durable'],outerInvocation=c.descriptor(outer/'invocation.json'),outerController=c.descriptor(outer/'controller.json'),helperVersion=r.get('helpers','Retrospective immutable helper pins recorded in implementation report; native1/build2/private1 loaded earlier producer versions')))
    evidence=dict(schemaVersion=1,status='SELECTED_BEHAVIOR_CHECKS_PASSED',candidateJar=jar,publicSurface=q.surface(Path(jar['path'])),contract=c.descriptor(p.E/'public-task-run-token-contract-v1.json'),**phases,
        executedProducerVersions=versions,failedNoChildBuild=c.descriptor(q.A/'build-v1-outer/controller.json'),launchControls=c.descriptor(q.A/'launch-admission-controls-v3.stdout'),
        foundationQualification='Separate public-task-run-token-foundation-v1.json records the actual foundation gate after it completes; no gate success is asserted here',
        historicalSuccessors=c.descriptor(q.HERE/'historical-successors-v1.json'),nativeCases=25,nativeFields=300,nativePassesPerMatrix=2,privateControls=23,historicalFieldsAndControls=3475,delayCases=113,delayFields=3955,delayPrivateControls=30,
        acceptanceCredit=0,acceptedTasks='0/1092 (0%)',openAcceptanceItems=1686,qualifiedFrameworks='0/66',wholeProjectRemainingBatches='UNKNOWN',e01Decisions='All three OPEN',integration='Root independent reviews and terminal merge/push not asserted')
    p.write(p.E/'public-task-run-token-v1.json',evidence)
    from verify_candidate import validate
    print(validate(evidence))

if __name__=='__main__':main()
