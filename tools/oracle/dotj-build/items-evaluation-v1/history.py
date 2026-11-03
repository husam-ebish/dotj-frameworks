"""Exact retained historical consumers with the sole native-backed NEG-items successor."""
import json
from pathlib import Path
import shutil
import zipfile
from product import A,B,JDK,MODULE,descriptor

def execute(run,out,vm,receipt,jar):
    prior=B/'agents/batch2518-build-ordering-preparation-v1'
    history=prior/'root-task108-historical-finaljar-attempt02/root-review-v2.json'
    ordering=prior/'task106-product-dev-attempt02/receipt.json'
    old_consumer=B/'validation/Batch-2516-boolean-product-green-v5/fixture-tests.jar'
    old_source=old_consumer.parent/'consumer-source/org/dotj/internal/build/evaluation/EvaluationBooleanProductTest.java'
    for path in (history,ordering,old_consumer,old_source):receipt['inputs'].append(descriptor(path))
    src=out/'successor-source';src.mkdir()
    shutil.copyfile(old_source,out/'EvaluationBooleanProductTest.original.java')
    original=old_source.read_text(encoding='utf-8-sig')
    before='negative(negatives,"items","<Project><ItemGroup><Compile Include=\\"*.java\\"/></ItemGroup></Project>","UNSUPPORTED_ELEMENT",Map.of());'
    after='nativeItems(negatives);'
    assert original.count(before)==1
    method='''
    private static void nativeItems(Path root) throws Exception {
        Path dir=root.resolve("items");Files.createDirectories(dir);
        Path file=dir.resolve("main.proj");
        String xml="<Project><ItemGroup><Compile Include=\\"*.java\\"/></ItemGroup></Project>";
        Files.writeString(file,xml);
        Result result=evaluate(file,dir,Map.of());
        require(result.items().isEmpty() && result.evaluatedFiles().equals(List.of(file))
            && result.imports().isEmpty() && result.duplicateImports().isEmpty() && result.conditionWarnings().isEmpty(),
            "NEG-items differs from frozen identical-input native empty-item transition");
        record("NEG-items\\tNATIVE_ITEM_TRANSITION_EMPTY\\tSUCCESS");
    }
'''
    successor=original.replace(before,after)
    end=successor.rfind('}')
    successor=successor[:end]+method+successor[end:]
    # Update only the prose count affected by this one documented row.
    successor=successor.replace('20 unchanged refusals','19 unchanged refusals + one native item transition')
    path=src/'EvaluationBooleanProductTest.java';path.write_text(successor,encoding='utf-8')
    receipt['legacyTransition']=dict(id='NEG-items',before='UNSUPPORTED_ELEMENT',after='NATIVE_ITEM_TRANSITION_EMPTY',
        original=descriptor(old_source),retained=descriptor(out/'EvaluationBooleanProductTest.original.java'),successor=descriptor(path),
        nativeContract=descriptor(A/'native-contract-v1.json'))
    run('compile-successor',[JDK/'javac.exe',*['-J'+v for v in vm],'--release','21','-implicit:none','-sourcepath',out/'empty',
        '--module-path',jar,'--patch-module',MODULE+'='+str(src)+';'+str(old_consumer),'-d',out/'classes',path])
    consumer=out/'historical-successor.jar';shutil.copyfile(old_consumer,consumer)
    run('package-successor',[JDK/'jar.exe',*['-J'+v for v in vm],'--update','--file',consumer,'--date=2020-01-01T00:00:00Z','-C',out/'classes','.'])
    with zipfile.ZipFile(consumer) as z:
        assert not any(n.rsplit('/',1)[-1].split('$')[0].removesuffix('.class') in
            ('ProjectEvaluationComponent','ItemEvaluator','ItemExpressions','ItemGlobs','ItemSnapshot') for n in z.namelist())
    receipt['consumer']=descriptor(consumer)
    historical=json.loads(history.read_text())['operations']
    order_ops=[op for op in json.loads(ordering.read_text())['commands'] if op['label'].startswith('runtime-')]
    old_jar=str(prior/'task106-product-dev-attempt02/dotj-build-evaluation-candidate.jar')
    old_outputs=str(prior/'task106-historical-finaljar-attempt02')
    old_order=str(prior/'task106-product-dev-attempt02')
    old_order_consumer=prior/'task106-product-dev-attempt02/consumer-classes'
    receipt['retainedOrderingClasses']=[descriptor(p) for p in sorted(old_order_consumer.rglob('*.class'))]
    assert not any(p.name.startswith('ProjectEvaluationComponent') for p in old_order_consumer.rglob('*.class'))
    (out/'outputs').mkdir()
    for op in order_ops+historical:
        argv=[]
        for arg in op['process']['argv']:
            # Replace explicit execution locations, never resolve relative to an importing reader.
            value=arg.replace(old_jar,str(jar)).replace(old_outputs,str(out))
            if op in order_ops:
                if old_order_consumer.as_posix().replace('/','\\') not in value:
                    value=value.replace(old_order,str(out))
            if op['label']=='packaged-current-base':value=value.replace(str(old_consumer),str(consumer))
            argv.append(value)
        argv.insert(5,'-XX:-UsePerfData')
        receipt['inputs'].extend(descriptor(Path(v)) for v in argv if Path(v).is_file())
        run(op['label'],argv,120)
    receipt['outputs']=[descriptor(p) for p in sorted(out.rglob('*.tsv'))]+[descriptor(consumer)]
