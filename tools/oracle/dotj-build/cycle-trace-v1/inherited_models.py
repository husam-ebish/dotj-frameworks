"""Pure inherited semantic predicates, retained verbatim from the 303 proof lineage."""

import json

ERRORS={('IC04',1):('MSB4100','CONDITION_NOT_BOOLEAN_CHILD'),('IS03',1):('MSB4113','CONDITION_NOT_BOOLEAN')}

def require(value,message):
    if not value: raise ValueError(message)

def normalized(value,root,key=None):
    if isinstance(value,str):
        rootless=root[1:] if root.startswith('/') else root[3:]
        if key=='Directory' and value.startswith(rootless):
            return '{FIXTURE_ROOT_WITHOUT_ROOTDIR}'+value[len(rootless):]
        return value.replace(root,'{FIXTURE_ROOT}')
    if isinstance(value,list):return [normalized(v,root) for v in value]
    if isinstance(value,dict):return {k:normalized(v,root,k) for k,v in value.items()}
    return value

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

def sort_result(value,jar_sha):
    require(value['id']=='T129-IMPORTANT-01' and value['status']=='PASS','Raw-sort disposition')
    require(value['pair']==['a0.cs','a@.cs'],'Raw-sort pair order')
    expected=['a@.cs','a%40.cs','a0.cs','a@.cs','a%40.cs','a0.cs','a@.cs']
    require(value['fragmentsAndDuplicates']==expected and value['vectorOrder']==expected,'Raw-sort fragment/vector order')
    require(value['identityEscaping'] and value['retainedSnapshot'] and value['jarSha256']==jar_sha,'Raw-sort identity/provenance')

def boundary_result(rows,jar_sha,platform):
    require(len(rows)==3 and [r['id'] for r in rows]==['T130-IMPORTANT-01','T130-IMPORTANT-02','T130-IMPORTANT-03'],'Boundary family inventory')
    require(all(r['status']=='PASS' and r['jarSha256']==jar_sha and r['platform']==platform for r in rows),'Boundary provenance')
    prefix,selectors,extension=rows
    sep='\\' if platform=='windows' else '/'
    expected=['a@'+sep+'x.cs','a%40'+sep+'x.cs','a@'+sep+'x.cs']
    require(prefix['identities']==prefix['copy']==expected and prefix['metadata']==['at','percent','at']
        and prefix['exclude']==[expected[1]] and prefix['remove']==[expected[0],expected[2]] and prefix['inlineIdentity'],'Escaped-prefix boundary')
    require(selectors['identities']==['./a.cs','a.cs','d/../a.cs','missing/../a.cs','other.cs','p%40.cs','p@.cs']
        and selectors['metadata']==['updated','updated','updated','updated','','percent','at']
        and selectors['excludeCount']==0 and selectors['remove']==['other.cs']
        and all(selectors[k] for k in ('absolute','mixedSeparators','nonexistentPaths','copyUnchanged','invalidFallback','trailingSeparator')),'Normalized-selector boundary')
    require(extension['identities']==['name.','plain','file.cs','.hidden','multi.part.']
        and extension['direct']==extension['inline']==['','','.cs','.hidden','']
        and extension['definingProject'] and extension['nonexistentLiteral'],'Trailing-dot boundary')
