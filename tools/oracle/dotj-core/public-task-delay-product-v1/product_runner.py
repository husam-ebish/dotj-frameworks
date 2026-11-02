"""Guarded Java-only successor. No SDK/native/prechange execution modes exist."""
import argparse, sys, time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import product_support as p
c=p.c

def inner(args):
    s=p.Session(args.out,args.mode,args.jar)
    try:
        if args.mode=='build':
            builder=p.load('delay_candidate_builder',p.TOOLS/'build-foundation-product-candidate.py')
            s.record['sourceClosure']=[c.descriptor(x) for x in builder.SOURCES];s.save()
            classes=builder.build_product(s.jdk)
            artifact=dict(schemaVersion=1,productSources=[dict(path=x.relative_to(p.ROOT).as_posix(),sha256=c.sha(x)) for x in builder.SOURCES],
                jarPath=builder.JAR.relative_to(p.ROOT).as_posix(),jarSha256=c.sha(builder.JAR),licensePath=builder.LICENSE.relative_to(p.ROOT).as_posix(),
                licenseSha256=c.sha(builder.LICENSE),licenseEntry='META-INF/LICENSE',jarEntries=['META-INF/MANIFEST.MF','META-INF/LICENSE',*classes],
                classSha256={name:c.sha(builder.CLASSES/name) for name in classes},status='BUILT_STAGED_CANDIDATE; Batch2517 qualification and integration pending')
            p.write(p.E/'foundation-product-candidate-v1.json',artifact)
            s.record.update(candidateJar=c.descriptor(builder.JAR),surface=p.check_surface(builder.JAR))
            p.load('delay_bind_file_map',p.TOOLS/'bind-foundation-file-map.py').main()
            p.load('delay_distribution',p.TOOLS/'verify-foundation-distribution.py').main(s.jdk)
        elif args.mode=='bind':
            p.check_surface(args.jar)
            p.load('delay_bind_file_map',p.TOOLS/'bind-foundation-file-map.py').main()
            p.load('delay_distribution',p.TOOLS/'verify-foundation-distribution.py').main(s.jdk)
        elif args.mode=='paired':
            manifest,schema,passes=p.prerequisites();s.record['surface']=p.check_surface(args.jar)
            group,records=s.java_group('paired',[p.HERE/'PublicTaskDelayProductFixtures.java'],'PublicTaskDelayProductFixtures',
                [('PublicTaskDelayProductFixtures',[str(p.FROZEN/'fixture-manifest.json'),str(p.HERE/'case-inputs.tsv'),part,str(args.jar)]) for part in ['ordinary','async']],args.jar,module=True)
            actual={}
            for rec,part in zip(records,['ordinary','async']):actual.update(c.wire(Path(rec['stdoutPath']).read_bytes(),schema,manifest,part))
            for native in passes:c.compare(actual,native,manifest)
            group.update(cases=len(actual),fields=sum(len(x) for x in actual.values()),comparedNativePasses=2,rawWinners={k:v['winner'] for k,v in actual.items() if v['winner']})
        elif args.mode=='private':
            group,records=s.java_group('private',[p.HERE/'TaskDelayProductControls.java'],'System.Threading.Tasks.TaskDelayProductControls',
                [('System.Threading.Tasks.TaskDelayProductControls',[str(args.jar),str(n)]) for n in range(1,10)],args.jar)
            markers=[]
            for rec in records:markers.extend(Path(rec['stdoutPath']).read_text(encoding='utf-8').splitlines())
            wanted={f'J{n:02}\tb\ttrue' for n in range(1,31)}
            c.require(len(markers)==30 and set(markers)==wanted,'all 30 actual private controls in nine groups')
            group.update(actualControls=len(markers),actualGroups=len(records))
        elif args.mode=='sample':
            s.java_group('sample',[p.HERE/'DelayCancellationSample.java'],'DelayCancellationSample',
                [('DelayCancellationSample',[str(args.jar)])],args.jar)
        elif args.mode=='historical':
            from historical_replay import replay
            replay(s,args.jar,args.only)
        elif args.mode=='audits':
            for name in ['audit-foundation-rights-inputs.py','audit-foundation-source-provenance.py','compare-foundation-upstream-text.py','build-foundation-notice-review-queue.py','audit-throw-site-upstream-adjacency.py','build-foundation-e01-review-packet.py','verify-differential-oracle-provenance.py']:
                s.step('audit-'+name,[str(p.PYTHON),'-B',str(p.TOOLS/name)])
        else:raise ValueError('unknown phase')
        if args.jar:c.require(c.descriptor(args.jar)==s.record['candidateJar'],'identical final JAR throughout phase')
        s.record.update(status='PASS_'+args.mode.upper(),sessionsEnded=True);s.save()
    except BaseException as error:
        s.record.update(status='FAILED_STOP_NO_RETRY',error=repr(error),sessionsEnded=True);s.save();raise

def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--mode',choices=['build','bind','paired','private','sample','historical','audits'],required=True)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--jar',type=Path);parser.add_argument('--inner',action='store_true')
    parser.add_argument('--only')
    args=parser.parse_args();c.confined(args.out)
    if args.inner:inner(args);return
    if args.mode not in ['build','audits']:c.require(args.jar is not None,'candidate JAR required')
    launch=args.out.with_name(args.out.name+'-outer');p.prepare(launch)
    # Pin all actual runtime/import inputs before starting the absolute parent budget.
    # The child uses its own 540s work envelope within this explicit 1800s phase.
    pins=p.payload_lock()+[c.descriptor(x) for x in sorted(p.HERE.glob('*')) if x.is_file()]
    p.write(launch/'inputs.json',pins)
    deadline=time.monotonic()+1965
    argv=[str(p.PYTHON),'-B',str(Path(__file__).resolve()),*sys.argv[1:],'--inner']
    def update(record):p.write(launch/'controller.json',record)
    record=p.checked_launch(argv,launch,'controller',1800,deadline,update)
    update(record);c.successful(record)
    result=c.read(args.out/'receipt.json');c.require(result['status']=='PASS_'+args.mode.upper(),'actual phase status')
    print(result['status'],c.sha(args.out/'receipt.json'))

if __name__=='__main__':main()
