"""Inventory four numeric carriers without granting native signature or task parity."""
import argparse,hashlib,importlib.util,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'

def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 oracle_path=EVIDENCE/'small-integer-signatures-contract-v10.0.12.json';j=json.loads(oracle_path.read_text())
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-small-integer-signatures-contract.ps1').read_bytes()).hexdigest()
 spec=importlib.util.spec_from_file_location('int32_signature_parser',Path(__file__).with_name('audit-int32-declared-signatures.py'));parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)
 owners=['System.SByte','System.Byte','System.UInt16','System.UInt32'];assert [t['fullName'] for t in j['types']]==owners
 records=[]
 for native in j['types']:
  owner=native['fullName'];output=subprocess.run(['javap','-public','-classpath',str(a.jar),owner],check=True,text=True,capture_output=True).stdout
  declarations=[s.strip() for s in output.splitlines() if s.strip().startswith('public ')];candidate=[v for s in declarations if (v:=parser.java_method(s)) is not None]
  primitive={'System.Boolean':'boolean','System.Int32':'int','System.String':'java.lang.String','System.Object':'java.lang.Object','System.IFormatProvider':'System.IFormatProvider','System.TypeCode':'System.TypeCode',owner:owner}
  methods=[];matched=set();selected=0
  for method in native['methods']:
   parameters=[v['type'] for v in method['parameters']];name=method['name'];is_selected=not method['isSpecialName'] and ((not method['isStatic'] and name in ['ToString','CompareTo','Equals','GetHashCode','GetTypeCode','TryFormat']) or (method['isStatic'] and name in ['Min','Max','Clamp','LeadingZeroCount','TrailingZeroCount','PopCount','RotateLeft','RotateRight','IsEvenInteger','IsOddInteger','IsPow2'] or (owner=='System.SByte' and method['isStatic'] and name in ['Abs','Sign','CopySign','MaxMagnitude','MinMagnitude'])))
   item=dict(nativeSignature=method['signature'],selected=is_selected)
   if is_selected:
    selected+=1
    def project(value):
     if value=='System.Int32&':return 'int[]'
     if value=='System.Span`1[System.Char]':return 'char[]'
     if value=='System.Span`1[System.Byte]':return 'byte[]'
     if value=='System.ReadOnlySpan`1[System.Char]':return 'java.lang.String'
     assert value in primitive,(owner,name,value)
     return primitive[value]
    expected=dict(name=name,isStatic=method['isStatic'],genericArity=0,returnType=project(method['returnType']),parameters=[project(v) for v in parameters])
    found=[v for v in candidate if all(v[k]==v2 for k,v2 in expected.items())];assert len(found)==1,(owner,method,expected,found)
    item.update(status='PROJECTED_SELECTED_DECLARATION',candidateDeclaration=found[0]['declaration'],projectedJava=expected);matched.add(found[0]['declaration'])
   else:item['status']='OUTSIDE_SELECTED_PROJECTION_AUDIT'
   methods.append(item)
  assert selected==(28 if owner=='System.SByte' else 23),(owner,selected)
  bridge=[v for v in candidate if v['name']=='TryFormat' and v['genericArity']==1 and v['parameters']==['System.Span<T>','int[]','System.ReadOnlySpan<java.lang.Character>','System.IFormatProvider'] and v['returnType']=='boolean'];assert len(bridge)==1,(owner,bridge)
  matched.add(bridge[0]['declaration'])
  fields=[dict(nativeField=v,candidateNamePresent=any(s.endswith(' '+v['name']+';') for s in declarations)) for v in native['fields']]
  records.append(dict(fullName=owner,nativeDeclaredMethodCount=len(native['methods']),selectedProjectedMethodCount=selected,outsideSelectedMethodCount=len(methods)-selected,methods=methods,fields=fields,typedSpanBridge=bridge[0]['declaration'],typedSpanBridgeNativeOverloadCount=2,extraJavaPublicMethods=[v['declaration'] for v in candidate if v['declaration'] not in matched],javaPublicDeclarations=declarations))
 record=dict(schemaVersion=1,types=records,selectedProjectedMethodCount=sum(v['selectedProjectedMethodCount'] for v in records),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DECLARATION_AUDIT_ONLY; OUTSIDE_SCOPE_METHODS_FIELDS_GENERIC_INTERFACES_CLR_ABI_BEHAVIOR_TASK_ACCEPTANCE_AND_RELEASE_OPEN')
 (EVIDENCE/'small-integer-signatures-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n')
 print(f"PASS small-integer signature audit: {len(records)} types; {record['selectedProjectedMethodCount']} selected native declarations; four typed span erasure bridges; remaining declarations/fields inventoried")
if __name__=='__main__':main()
