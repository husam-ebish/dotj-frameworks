"""Pure full-coordinate native evidence reader, including the adopted completed child."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from corpus import descriptor, sha, read_contract, PROFILES, verify_fixtures

def checked(item):
    p=Path(item['path'])
    assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'], str(p)
    return p

def flatten(value,prefix=''):
    if isinstance(value,dict):
        return {k:v for key,item in value.items() for k,v in flatten(item,prefix+'.'+key).items()}
    if isinstance(value,list):
        result={prefix+'.$length':len(value)}
        for i,item in enumerate(value):result.update(flatten(item,prefix+'['+str(i)+']'))
        return result
    return {prefix:value}

def normalize(value,root):
    if isinstance(value,str):return value.replace(root,'<fixtures>')
    if isinstance(value,list):return [normalize(v,root) for v in value]
    if isinstance(value,dict):return {k:normalize(v,root) for k,v in value.items()}
    return value

def process_ok(op):
    p=op['process']
    assert p['exitCode']==0 and not any(p.get(k) for k in ('timedOut','outputLimitExceeded','cleanupError','error'))
    assert p.get('jobAssigned') is True and p.get('resumed') is True and p['cleanupSeconds']<=5
    checked(op['stdout']);checked(op['stderr'])

def build(contract_path,artifacts,replacements=None):
    contract=read_contract(contract_path)
    cov=next(i for i in contract['inputs'] if i['path'].endswith('task131-native-projection-coverage-v1.json'))
    coverage=json.loads(checked(cov).read_text())
    observations={};units=[];new_count=0
    input_bindings=[]
    def input_checked(item):
        path=Path(item['path'])
        if not path.is_file() or sha(path)!=item['sha256']:
            snapshot=Path(artifacts)/'executed-native-v1'/path.name
            assert snapshot.is_file() and sha(snapshot)==item['sha256'], 'Missing executed source snapshot '+str(path)
            input_bindings.append(dict(original=item,retained=descriptor(snapshot)))
        else:
            checked(item);input_bindings.append(dict(original=item,retained=item))
    def add(platform,unit,raw,root):
        if platform=='windows':
            expected={'msbuildPath':('toolchains/dotnet/sdk/10.0.401/Microsoft.Build.dll','96896c3c1e0843ea5c4cc03baac8df3a61587e3742599b6b29f99dbd25595eff'),
                'frameworkPath':('toolchains/dotnet/sdk/10.0.401/Microsoft.Build.Framework.dll','58a2da163e77baa35719982597f92384d8ae442479070df97b4747b1093f5a2f'),
                'corePath':('toolchains/dotnet/shared/Microsoft.NETCore.App/10.0.12/System.Private.CoreLib.dll','1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678')}
            base=Path('D:/AI/Implementation/dotj Frameworks')
            for field,(relative,digest) in expected.items():
                assert Path(raw[field])==base/relative and sha(raw[field])==digest
        else:
            assert raw['msbuildPath']=='/sdk/Microsoft.Build.dll' and raw['frameworkPath']=='/sdk/Microsoft.Build.Framework.dll'
            assert raw['corePath']=='/usr/share/dotnet/shared/Microsoft.NETCore.App/10.0.12/System.Private.CoreLib.dll'
        for row in raw['rows']:
            assert row['cleanup']['afterUnload']==0 and row['cleanup']['disposed'] and row['taskMarkerAbsent']
            normalized=normalize(row,root)
            observations.setdefault((platform,row['id'],row['profile']),[]).append((unit,normalized))
    for source in coverage['sources']:
        receipt=json.loads(checked(source['receipt']).read_text())
        assert receipt['status']==source['aggregateStatus']
        for item in source['sameInputFixtureDescriptors']:checked(item)
        for field in ('binary','runtimeConfig'):
            checked(source[field])
        for child in source['passes']:
            assert child['exitCode']==0
            raw=json.loads(checked(child['stdout']).read_text(encoding='utf-8-sig'))
            assert raw in receipt['captures'], 'Raw/parsed child differs'
            command=next(c for c in receipt['commands'] if c['label']==child['profile'])
            assert command['exitCode']==0 and command['argv']==child['argv']
            assert raw['profile']==child['profile'] and raw['runtime']=='.NET 10.0.12'
            if source['aggregateStatus']=='FAILED':
                assert source['id']=='import-profiles-native-v1' and child['profile']==PROFILES['RECORD_DUPLICATES']
            root=child['argv'][-2]
            units.append(dict(id=child['id'],aggregateStatus=receipt['status'],unitExitCode=0,
                              receipt=source['receipt'],stdout=child['stdout'],fixtureRoot=root,role='retained-completed-child'))
            add('windows',child['id'],raw,root)
    for selection in contract['nativeSchedule']['runs']:
        out=Path((replacements or {}).get(selection['attempt'],Path(artifacts)/selection['attempt']))
        receipt=json.loads((out/'receipt.json').read_text())
        assert receipt['status']=='PASS' and receipt['selection']==selection
        for item in receipt['inputs']:input_checked(item)
        for sample in receipt['resources']:
            assert sample['freePhysicalBytes']>=512*1024**2 and sample['freeVirtualBytes']>=16*1024**3
        assert receipt['fixturesUnchanged'] and receipt['rawParsedEquality']
        outputs=receipt['outputs'];raw=json.loads(checked(outputs[0]).read_text(encoding='utf-8-sig'))
        assert raw==json.loads(checked(outputs[1]).read_text())
        assert [r['id'] for r in raw['rows']]==selection['ids']
        verify_fixtures(contract,out/'fixtures',selection['ids'])
        for op in receipt['operations']:
            if op['label'] not in ('container-initial','container-absence','container-late-absence'):
                process_ok(op)
        if selection['platform']=='linux':
            c=receipt['container'];assert c['absenceVerified'] and c['lateAbsenceVerified']
            terminal=c['terminalInspect'];assert terminal['State']['ExitCode']==0 and not terminal['State']['OOMKilled'] and not terminal['State']['Running']
            assert terminal['Id']==c['cid'] and terminal['Config']['Labels']['dotj.owner']=='task132'
            verify_fixtures(contract,Path(receipt['actualFixturePath']),selection['ids'])
            checked(receipt['caseProfile'])
            assert Path(receipt['caseProfile']['path']).read_text().splitlines()==[id+'\tfalse\tfalse' for id in selection['ids']]
            host=c['createdInspect']['HostConfig']
            assert host['ReadonlyRootfs'] and host['NetworkMode']=='none' and host['Memory']==536870912 and host['MemorySwap']==536870912 and host['PidsLimit']==64
        new_count+=len(raw['rows'])
        unit=selection['attempt'];units.append(dict(id=unit,receipt=descriptor(out/'receipt.json'),stdout=outputs[0],
            fixtureRoot=receipt['fixtureRoot'],aggregateStatus='PASS',unitExitCode=0,role='new-capture'))
        add(selection['platform'],unit,raw,receipt['fixtureRoot'])
    assert new_count==190
    rows=[]
    for platform in ('windows','linux'):
        for case in contract['cases']:
            for profile,native in PROFILES.items():
                entries=observations[(platform,case['id'],native)]
                # Union per-field evidence: omitted end coordinates contribute no observation.
                fields={}
                for unit,row in entries:
                    for key,value in flatten(row).items():
                        values=fields.setdefault(key,[])
                        assert not values or values[0][1]==value, (platform,case['id'],profile,key,values,value)
                        values.append((unit,value))
                best=max(entries,key=lambda item:len(flatten(item[1])))
                assert set(flatten(best[1]))==set(fields)
                for key,values in fields.items():assert len({v[0] for v in values})>=2,(platform,case['id'],profile,key)
                for diag in best[1]['diagnostics']:assert {'endLine','endColumn'}<=diag.keys()
                if not best[1]['evaluation']['success']:assert {'endLine','endColumn'}<=best[1]['evaluation'].keys()
                rows.append(dict(platform=platform,id=case['id'],profile=profile,observation=best[1],
                    fields={k:dict(value=v[0][1],units=sorted({x[0] for x in v})) for k,v in fields.items()}))
    return dict(status='PASS_NATIVE_FULL_COORDINATE_TWO_PASS',contract=descriptor(contract_path),coverage=cov,
                rows=rows,units=units,newRowPasses=new_count,requiredRowPasses=228,chainRole='source-derived only',replacements=replacements or {},inputBindings=input_bindings)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--contract',type=Path,required=True)
    p.add_argument('--artifacts',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--replacements',type=Path)
    a=p.parse_args();value=build(a.contract,a.artifacts,json.loads(a.replacements.read_text()) if a.replacements else None);assert not a.output.exists()
    a.output.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=value['status'],rows=len(value['rows']),**descriptor(a.output))))
