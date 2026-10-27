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
  primitive={'System.Boolean':'boolean','System.Int32':'int','System.String':'java.lang.String','System.Object':'java.lang.Object','System.IFormatProvider':'System.IFormatProvider','System.TypeCode':'System.TypeCode','TOther':'TOther','System.UInt64':'java.math.BigInteger','System.Globalization.NumberStyles':'System.Globalization.NumberStyles',owner:owner}
  methods=[];matched=set();selected=0;collapsed=0;parsing_bridges=set()
  for method in native['methods']:
   parameters=[v['type'] for v in method['parameters']];name=method['name'];is_selected=not method['isSpecialName'] and ((not method['isStatic'] and name in ['ToString','CompareTo','Equals','GetHashCode','GetTypeCode','TryFormat']) or (method['isStatic'] and name in ['Min','Max','Clamp','DivRem','BigMul','CreateChecked','CreateSaturating','CreateTruncating','LeadingZeroCount','TrailingZeroCount','PopCount','RotateLeft','RotateRight','IsEvenInteger','IsOddInteger','IsPow2','Log2','Sign'] or (owner=='System.SByte' and method['isStatic'] and name in ['Abs','Sign','CopySign','MaxMagnitude','MinMagnitude','IsPositive','IsNegative']) or (owner!='System.SByte' and method['isStatic'] and name=='Log2'))) or (method['isStatic'] and ((name=='Parse' and parameters in [['System.String'],['System.String','System.IFormatProvider'],['System.String','System.Globalization.NumberStyles'],['System.String','System.Globalization.NumberStyles','System.IFormatProvider']]) or (name=='TryParse' and parameters in [['System.String',owner+'&'],['System.String','System.IFormatProvider',owner+'&'],['System.String','System.Globalization.NumberStyles','System.IFormatProvider',owner+'&']])))
   is_span=method['isStatic'] and bool(parameters) and parameters[0] in ['System.ReadOnlySpan`1[System.Char]','System.ReadOnlySpan`1[System.Byte]'] and ((name=='Parse' and parameters[1:] in [['System.IFormatProvider'],['System.Globalization.NumberStyles','System.IFormatProvider']]) or (name=='TryParse' and parameters[1:] in [[owner+'&'],['System.IFormatProvider',owner+'&'],['System.Globalization.NumberStyles','System.IFormatProvider',owner+'&']]))
   is_selected=is_selected or is_span
   item=dict(nativeSignature=method['signature'],selected=is_selected)
   if is_selected:
    selected+=1
    def project(value):
     if is_span and value.startswith('System.ReadOnlySpan`1['):return 'System.ReadOnlySpan<T>'
     if value=='System.ValueTuple`2['+owner+','+owner+']':return 'System.ValueTuple<'+owner+', '+owner+'>'
     if value==owner+'&':return owner+'[]'
     if value=='System.Int32&':return 'int[]'
     if value=='System.Span`1[System.Char]':return 'char[]'
     if value=='System.Span`1[System.Byte]':return 'byte[]'
     if value=='System.ReadOnlySpan`1[System.Char]':return 'java.lang.String'
     assert value in primitive,(owner,name,value)
     return primitive[value]
    expected=dict(name=name,isStatic=method['isStatic'],genericArity=(1 if is_span else method['genericArity']),returnType=project(method['returnType']),parameters=[project(v) for v in parameters])
    found=[v for v in candidate if all(v[k]==v2 for k,v2 in expected.items())];assert len(found)==1,(owner,method,expected,found)
    item.update(status=('ERASURE_COLLAPSED_TYPED_SPAN' if is_span else 'PROJECTED_SELECTED_DECLARATION'),candidateDeclaration=found[0]['declaration'],projectedJava=expected);matched.add(found[0]['declaration'])
    if is_span:collapsed+=1;parsing_bridges.add(found[0]['declaration'])
   else:item['status']='OUTSIDE_SELECTED_PROJECTION_AUDIT'
   methods.append(item)
  assert selected==(52 if owner=='System.SByte' else 47 if owner=='System.UInt32' else 46),(owner,selected)
  assert collapsed==10 and len(parsing_bridges)==5,(owner,collapsed,parsing_bridges)
  bridge=[v for v in candidate if v['name']=='TryFormat' and v['genericArity']==1 and v['parameters']==['System.Span<T>','int[]','System.ReadOnlySpan<java.lang.Character>','System.IFormatProvider'] and v['returnType']=='boolean'];assert len(bridge)==1,(owner,bridge)
  matched.add(bridge[0]['declaration'])
  optional=[v for v in candidate if v['name']=='Parse' and v['isStatic'] and v['genericArity']==1 and v['parameters']==['System.ReadOnlySpan<T>'] and v['returnType']==owner];assert len(optional)==1,(owner,optional)
  fields=[dict(nativeField=v,candidateNamePresent=any(s.endswith(' '+v['name']+';') for s in declarations)) for v in native['fields']]
  records.append(dict(fullName=owner,nativeDeclaredMethodCount=len(native['methods']),selectedNativeMethodCount=selected,selectedProjectedMethodCount=selected-collapsed,erasureCollapsedNativeMethodCount=collapsed,typedParsingBridges=sorted(parsing_bridges),optionalDefaultSpanAdapter=optional[0]["declaration"],optionalAdapterStatus="JAVA_CONVENIENCE_FOR_NATIVE_STYLE_INTEGER_PROVIDER_NULL; NOT_AN_ADDITIONAL_CLR_DECLARATION",outsideSelectedMethodCount=len(methods)-selected,methods=methods,fields=fields,typedSpanBridge=bridge[0]['declaration'],typedSpanBridgeNativeOverloadCount=2,extraJavaPublicMethods=[v['declaration'] for v in candidate if v['declaration'] not in matched],javaPublicDeclarations=declarations))
 record=dict(schemaVersion=1,types=records,selectedNativeMethodCount=sum(v['selectedNativeMethodCount'] for v in records),erasureCollapsedNativeMethodCount=sum(v['erasureCollapsedNativeMethodCount'] for v in records),selectedProjectedMethodCount=sum(v['selectedProjectedMethodCount'] for v in records),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DECLARATION_AUDIT_ONLY; OUTSIDE_SCOPE_METHODS_FIELDS_GENERIC_INTERFACES_CLR_ABI_BEHAVIOR_TASK_ACCEPTANCE_AND_RELEASE_OPEN')
 (EVIDENCE/'small-integer-signatures-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n')
 print(f"PASS small-integer signature audit: {len(records)} types; {record['selectedProjectedMethodCount']} direct projections; {record['erasureCollapsedNativeMethodCount']} native parsing overloads through twenty typed bridges; four formatting bridges; remaining declarations/fields inventoried")
if __name__=='__main__':main()
