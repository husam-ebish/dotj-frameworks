"""Compare the selected private value contract to immutable native observations.

Native exception classes/messages/HResult, toolsets and mutable ICollection identity
are not represented as Java ABI. Error mappings are exact case/step/code triples.
"""
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from native_contract import A,read,normalized,desc,require

ERRORS={('IC04',1):('MSB4100','CONDITION_NOT_BOOLEAN_CHILD'),('IS03',1):('MSB4113','CONDITION_NOT_BOOLEAN')}

def diagnostics(values):
    return [{k:v[k] for k in ('kind','Code','File','LineNumber','ColumnNumber')} for v in values]

def selected_native(row):
    observations=[]
    for index,value in enumerate(row['observations']):
        if 'action' in value:
            if value['action']=='private-snapshot-mutation-attempt':
                observations.append(dict(action=value['action'],refusals=4))
            else: observations.append(value)
            continue
        result=value['result']
        if result['success']:
            snapshot=dict(result['snapshot']);del snapshot['ToolsVersion']
            mutation=result['mutation']
            if mutation is not None:
                require(mutation['collectionMutation']['returned'] is False,'Native mutation probe changed')
                after=dict(mutation['after']);del after['ToolsVersion']
                mutation=dict(caller=mutation['caller'],collectionMutationRefused=True,after=after)
            observations.append(dict(result=dict(success=True,snapshot=snapshot,mutation=mutation),diagnostics=diagnostics(value['diagnostics'])))
        else:
            native,private=ERRORS[(row['id'],index)]
            require(result['ErrorCode']==native,'Unexpected native failure')
            observations.append(dict(result=dict(success=False,privateCode=private,file=result['ProjectFile'],line=result['LineNumber'],column=result['ColumnNumber']),
                diagnostics=diagnostics(value['diagnostics'])))
    return dict(id=row['id'],observations=observations,retainedFirstSnapshotUnchanged=row['retainedFirstSnapshotUnchanged'],taskMarkerAbsent=row['taskMarkerAbsent'])

def selected_product(row):
    row=json.loads(json.dumps(row))
    for index,value in enumerate(row['observations']):
        if 'result' in value and not value['result']['success']:
            result=value['result'];result.pop('message',None)
            if (row['id'],index) in ERRORS:
                native,private=ERRORS[(row['id'],index)]
                if result['privateCode']==private:
                    value['diagnostics'].append(dict(kind='error',Code=native,File=result['file'],LineNumber=result['line'],ColumnNumber=result['column']))
    return row

def differences(expected,actual,path=''):
    if type(expected)!=type(actual):return [dict(path=path,expected=expected,actual=actual)]
    if isinstance(expected,dict):
        if set(expected)!=set(actual):return [dict(path=path,expectedKeys=list(expected),actualKeys=list(actual))]
        return [d for k in expected for d in differences(expected[k],actual[k],path+'/'+k)]
    if isinstance(expected,list):
        if len(expected)!=len(actual):return [dict(path=path,expectedCount=len(expected),actualCount=len(actual),expected=expected,actual=actual)]
        return [d for i,(e,a) in enumerate(zip(expected,actual)) for d in differences(e,a,path+'/'+str(i))]
    return [] if expected==actual else [dict(path=path,expected=expected,actual=actual)]

def compare(raw,platform):
    product=read(raw);native=read(A/'native-contract-v1.json')
    require(product['scenarioCount']==42 and len(product['rows'])==42,'42 product scenarios required')
    actual=normalized(product['rows'],product['root'])
    require([r['id'] for r in actual]==[r['id'] for r in native['models'][platform]],'Scenario identities/order differ')
    rows=[]
    for expected,observed in zip(native['models'][platform],actual):
        difference=differences(selected_native(expected),selected_product(observed))
        rows.append(dict(id=expected['id'],passed=not difference,differences=difference))
    return dict(status='PASS' if all(r['passed'] for r in rows) else 'FAILED',scenarioCount=42,
        passed=sum(r['passed'] for r in rows),platform=platform,product=desc(raw),native=desc(A/'native-contract-v1.json'),rows=rows)

if __name__=='__main__':
    raw=Path(sys.argv[1]);out=Path(sys.argv[3])
    if out.exists():raise ValueError('New comparison output required')
    result=compare(raw,sys.argv[2]);out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed=result['passed'],failed=[r['id'] for r in result['rows'] if not r['passed']])))
    if result['status']!='PASS':sys.exit(1)
