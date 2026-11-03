"""Owned finite item-evaluation fixture definitions; expectations require native captures.

Scenario names and obligations come from adopted Task127. No reference outputs are
invented here. This module does not launch processes or write when imported.
"""
from pathlib import Path
import hashlib
import json
import sys

CASES = []

def case(identifier, body, *, files=None, properties=(), metadata=(), globals=None,
         attributes='', steps=None):
    tree = {'main.proj': '<Project'+attributes+'>'+body+'</Project>'}
    tree.update(files or {})
    CASES.append(dict(id=identifier, files=tree, queryProperties=list(properties),
        queryMetadata=list(metadata), queryBuiltIns=(['Identity','FullPath','RootDir','Filename','Extension','RelativeDir','Directory','RecursiveDir','DefiningProjectFullPath','DefiningProjectDirectory','DefiningProjectName','DefiningProjectExtension']
            if identifier in ('IM04','IM05','IG03','IG05','IG10') else []), globals=globals or {}, steps=steps or [],
        disposition='AWAITING_NATIVE_CAPTURE'))

case('IP01', '<PropertyGroup><Early>$(Late)</Early></PropertyGroup>'
    '<ItemGroup><Compile Include="$(Late)" Condition="\'$(Late)\' == \'a.cs\'" /></ItemGroup>'
    '<PropertyGroup><Late>a.cs</Late></PropertyGroup>', properties=('Early','Late'))
case('IP02', '<PropertyGroup><P>first</P></PropertyGroup><ItemGroup><I Include="root-$(P)" /></ItemGroup>'
    '<Import Project="sub/import.props" /><ItemGroup><I Include="last-$(P)" /></ItemGroup>'
    '<PropertyGroup><P>final</P></PropertyGroup>',
    files={'sub/import.props':'<Project><PropertyGroup><P>middle</P></PropertyGroup><ItemGroup><I Include="import-$(P)" /></ItemGroup></Project>'},properties=('P',))
case('IP03', '<Import Project="skipped.props" Condition="false" /><ItemGroup Condition="\'$(P)\' == \'yes\'"><I Include="reached" /></ItemGroup>'
    '<PropertyGroup><P>yes</P></PropertyGroup>',properties=('P',),metadata=('M',),
    files={'skipped.props':'<Project><ItemDefinitionGroup><I><M>unreached</M></I></ItemDefinitionGroup><ItemGroup><I Include="unreached"/></ItemGroup></Project>'})
case('IP04', '<PropertyGroup><P>local</P><Q>local</Q></PropertyGroup><ItemGroup><I Include="$(P)"><M>$(Q)</M></I></ItemGroup>',
    properties=('P','Q'), metadata=('M',),globals={'P':'global','Q':'global'},attributes=' TreatAsLocalProperty="P"')
case('IP05', '<PropertyGroup><V>@(Seed)</V><Escaped>%24(Late)</Escaped><Late>late</Late></PropertyGroup>'
    '<ItemGroup><Seed Include="a;b"/><I Include="$(V)"/><Seed Include="c"/><I Include="a;b;c;$(Escaped)" Exclude="$(V)"/></ItemGroup>',properties=('V','Escaped','Late'))
case('IP06', '<Import Project="sub/import.props"/><Import Project="sub/import.props"/>',
    files={'sub/import.props':'<Project><ItemGroup><I Include="once"/></ItemGroup></Project>'})

case('IO01', '<ItemGroup><I Include="a"/><Copy Include="@(I)"/><I Include="b"/><Copy Include="@(I)"/><I Include="@(I)"/></ItemGroup>')
case('IO02', '<ItemGroup><I Include="a.cs;b.cs;c.txt"/><Copy Include="@(I)"/><I Remove="a.cs"/><After Include="@(I)"/><I Remove="*.cs"/><Last Include="@(I)"/></ItemGroup>')
case('IO03', '<ItemGroup><I Include="a"><M>first</M></I><Copy Include="@(I)"/><I Update="a"><M>source</M></I><Copy Update="a"><N>destination</N></Copy></ItemGroup>',metadata=('M','N'))
case('IO04', '<ItemGroup><Seed Include="a"/><I Include="a;b" Exclude="@(Seed)"/><Seed Include="b"/><I Include="a;b;c" Exclude="@(Seed)" Condition="\'@(Seed)\' == \'a;b\'"/></ItemGroup>')
case('IO05', '<ItemGroup><I Include="a;a;b"/><I Include="a;c" Exclude="a"/><I Update="a"><M>both</M></I><I Update="missing"><M>none</M></I><I Remove="b;missing"/></ItemGroup>',metadata=('M',))
case('IO06', '<ItemGroup><I Include="@(Missing)"/><I Include="a"/><I Include="@(I);b"/><Copy Include="@(I)"/><I Remove="@(I)"/><After Include="@(I)"/></ItemGroup>')

case('IM01', '<ItemGroup><I Include=" a ; ; b%3Bc;a;%253B " /></ItemGroup>')
case('IM02', '<ItemGroup><I Include="star%2A.txt;q%3F.txt;%40%28I%29;%24%28P%29;%27;%25" /></ItemGroup>',files={'starMATCH.txt':'not-enumerated'})
case('IM03', '<ItemGroup><I Include="a"><M>first</M><N>%(m)-%(I.M)</N><Empty/><m>last</m><After>%(M)</After></I></ItemGroup>',metadata=('M','m','N','Empty','Absent','After'))
case('IM04', '<ItemGroup><I Include="Dir/Mixed.Name.CS" /></ItemGroup>')
case('IM05', '<Import Project="sub/import.props"/><ItemGroup><Copy Include="@(I)"/><I Update="**/*.cs"><M>updated</M></I></ItemGroup>',
    files={'sub/import.props':'<Project><ItemGroup><I Include="src/**/*.cs"/></ItemGroup></Project>','src/one.cs':'x','src/nested/two.cs':'y'},metadata=('M',))
case('IM06', '<PropertyGroup><P>property</P><Injected>%25(M)</Injected></PropertyGroup><ItemGroup><Seed Include="a;b"/></ItemGroup><Import Project="sub/import.props"/>',
    files={'sub/import.props':'<Project><ItemGroup><I Include="one;two"><M>custom</M><N>%(M)-$(P)-@(Seed)</N><Escaped>%24(P)</Escaped><Stage>%(Escaped)</Stage><Injected>$(Injected)</Injected><Path>src\\file.txt</Path><Skipped Condition="false">bad</Skipped></I></ItemGroup></Project>'},
    properties=('P','Injected'),metadata=('M','N','Escaped','Stage','Injected','Path','Skipped'))

case('ID01', '<ItemDefinitionGroup><I><M>default</M></I></ItemDefinitionGroup><ItemGroup><I Include="a"/><I Include="b"><M>inline</M></I></ItemGroup>',metadata=('M',))
case('ID02', '<ItemGroup><I Include="a"/></ItemGroup><ItemDefinitionGroup><I><M>first</M></I></ItemDefinitionGroup><Import Project="defs.props"/><ItemDefinitionGroup><I><M>last</M></I></ItemDefinitionGroup>',
    files={'defs.props':'<Project><ItemDefinitionGroup><I><M>import</M><N>retained</N></I></ItemDefinitionGroup></Project>'},metadata=('M','N'))
case('ID03', '<PropertyGroup><P>yes</P></PropertyGroup><ItemDefinitionGroup Condition="\'$(P)\' == \'yes\'"><I><M>base</M></I><I Condition="\'%(M)\' == \'base\'"><N Condition="\'%(M)\' == \'base\'">%(M)-next</N></I></ItemDefinitionGroup><ItemGroup><I Include="a"/></ItemGroup>',metadata=('M','N'))
case('ID04', '<ItemDefinitionGroup><Source><M>source-default</M><N>source-only</N></Source><Destination><M>destination-default</M><D>destination-only</D></Destination></ItemDefinitionGroup><ItemGroup><Source Include="a"><M>source-direct</M></Source><Source Include="b"/><Destination Include="@(Source)"/></ItemGroup>',metadata=('M','N','D'))
case('ID05', '<ItemDefinitionGroup><A><M>default-a</M></A><B><M>default-b</M><N>b</N></B><C><M>default-c</M><Q>c</Q></C></ItemDefinitionGroup><ItemGroup><A Include="a"><M>%(M)-inline</M></A><B Include="@(A)"/><A Update="a"><M/></A><C Include="@(B)"/><B Update="a"><N/></B></ItemGroup>',metadata=('M','N','Q'))

case('IC01', '<Import Project="sub/import.props"/>',files={'root.txt':'root','sub/import.props':'<Project><ItemGroup Condition="Exists(\'root.txt\') Or false And false"><I Include="a" Condition="Exists(\'root.txt\')"><M Condition="Exists(\'root.txt\')">root</M></I></ItemGroup></Project>'},metadata=('M',))
case('IC02', '<ItemGroup><I Include="a" Condition="\'@(Seed)\' == \'a\' And \'$(P)\' == \'yes\' Or false"/><Seed Include="a"/><I Include="b" Condition="\'@(Seed)\' == \'a\' And \'$(P)\' == \'yes\' Or false"/></ItemGroup>',
    globals={'P':'yes'},properties=('P',),steps=[{'kind':'repeat-owner','owner':'other.proj','globals':{'P':'no'}}])
case('IC03', '<ItemGroup><I Include="a"><M>yes</M><N Condition="\'%(M)\' == \'yes\'">accepted</N></I><I Include="b"><M>no</M><N Condition="\'%(M)\' == \'yes\'">accepted</N></I></ItemGroup>',metadata=('M','N'),steps=[{'kind':'repeat-owner','owner':'other.proj'}])
case('IC04', '<ItemGroup Condition="true Or false And true"><I Include="a"><M Condition="true Or false And true">yes</M></I></ItemGroup>',metadata=('M',),
    steps=[{'kind':'evaluate-xml','owner':'failed.proj','xml':'<Project><ItemGroup Condition="true And invalid Or false"><I Include="a"/></ItemGroup></Project>'},
           {'kind':'repeat-owner','owner':'recovered.proj'}])
case('IC05', '<ItemGroup Condition="false"><I Include="missing/**/*.cs"/></ItemGroup><ItemGroup><I Include="missing/**/*.cs" Condition="false"/><I Include="valid"/></ItemGroup>')
case('IC06', '<ItemGroup><I Include="evaluated"/></ItemGroup><Target Name="Never"><WriteLinesToFile File="must-not-exist.txt" Lines="executed"/><Error Text="never"/></Target>',attributes=' InitialTargets="Never" DefaultTargets="Never"')

GLOB_FILES={'lower.cs':'a','Upper.CS':'b','zero.cs':'c','a.cs':'d','ab.cs':'e','plain':'f','.hidden':'g',
    'Dir/one.cs':'h','Dir/Upper.CS':'i','Dir/nested/two.cs':'j','Other/three.cs':'k','x/a.cs':'l','x/x/b.CS':'m','deep/x/nest/c.cs':'n'}
case('IG01','<ItemGroup><I Include="*.cs;literal.cs;*.none;missing/*.cs"/></ItemGroup>',files=GLOB_FILES)
case('IG02','<ItemGroup><I Include="?.cs;a?.cs"/></ItemGroup>',files=GLOB_FILES)
case('IG03','<ItemGroup><I Include="**/*.cs"/></ItemGroup>',files=GLOB_FILES)
case('IG04','<ItemGroup><I Include="D*/*.cs"/></ItemGroup>',files=GLOB_FILES)
case('IG05','<ItemGroup><I Include="**/x/**/*.cs"/></ItemGroup>',files=GLOB_FILES)
case('IG06','<ItemGroup><I Include="dir/*.cs;d*/*.cs"/></ItemGroup>',files=GLOB_FILES)
case('IG07','<ItemGroup><Star Include="*"/><StarDotStar Include="*.*"/></ItemGroup>',files=GLOB_FILES)
case('IG08','<ItemGroup><First Include="*.cs" Exclude="a.cs"/><Second Include="*.cs" Exclude="ab.cs"/></ItemGroup>',files=GLOB_FILES)
case('IG09','<ItemGroup><Seed Include="a.cs"/><I Include="*.cs" Exclude="@(Seed);ab.cs;zero*"/><I Include="missing/one.cs;missing/two.txt"/><I Update="missing/*.cs"><M>matched</M></I><I Remove="missing/*.txt"/></ItemGroup>',files=GLOB_FILES,metadata=('M',))
case('IG10','<ItemGroup><I Include="./*.cs;**/*.cs" Exclude="Dir/**"/></ItemGroup>',files=GLOB_FILES)

case('IS01','<ItemGroup><I Include="*.cs"/></ItemGroup>',files={'old.cs':'old'},steps=[{'kind':'filesystem-change','write':{'new.cs':'new'},'delete':['old.cs']},{'kind':'repeat-owner','owner':'main.proj'}])
case('IS02','<ItemGroup><I Include="$(P)"/></ItemGroup>',globals={'P':'first'},properties=('P',),
    steps=[{'kind':'caller-global-mutation','name':'P','value':'mutated'}, {'kind':'private-snapshot-mutation-attempt'}, {'kind':'repeat-owner','owner':'other.proj'}])
case('IS03','<ItemGroup Condition="false"><I Include="missing/*.cs"/></ItemGroup><ItemGroup><I Include="valid"/></ItemGroup>',
    steps=[{'kind':'evaluate-xml','owner':'failed.proj','xml':'<Project><ItemGroup><I Include="a" Condition="invalid"/></ItemGroup></Project>'}, {'kind':'repeat-owner','owner':'recovered.proj'}])

def materialize(out):
    if len(CASES)!=42 or len({c['id'] for c in CASES})!=42:
        raise ValueError('Adopted finite scenario identity count differs')
    out=Path(out)
    if out.exists(): raise ValueError('New corpus root required')
    out.mkdir(parents=True)
    files=[]
    for c in CASES:
        for relative,text in c['files'].items():
            path=out/c['id']/relative
            path.parent.mkdir(parents=True,exist_ok=True)
            data=text.encode('utf-8');path.write_bytes(data)
            files.append(dict(path=path.relative_to(out).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    manifest=dict(schemaVersion=1,status='DRAFT_NOT_NATIVE_FROZEN',scenarioCount=42,
        cases=[{k:v for k,v in c.items() if k!='files'} for c in CASES],files=files)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

def supplemental(out):
    out=Path(out)
    if out.exists(): raise ValueError('New supplemental root required')
    original=Path('D:/AI/Implementation/dotj Frameworks/agents/batch2518-build-ordering-preparation-v1/task106-historical-finaljar-attempt02/outputs/negative-inputs/items/main.proj')
    legacy=original.read_bytes()
    if hashlib.sha256(legacy).hexdigest()!='ed0dfaf3dc50842bf3a5a5630817600701108d7dbaca65e9399c1b1e4bbd4a43':
        raise ValueError('Historical item refusal input differs')
    if [p.name for p in original.parent.iterdir()]!=['main.proj']:
        raise ValueError('Historical item directory changed')
    values={'NEG-items':legacy,
        'IR03-definition-vector':b'<Project><ItemDefinitionGroup><I><M>@(Seed)</M></I></ItemDefinitionGroup><ItemGroup><I Include="a"/></ItemGroup></Project>',
        'IR03-property-condition':b'<Project><PropertyGroup Condition="\'@(I)\' == \'\'"><P>value</P></PropertyGroup></Project>',
        'IR05-built-in-assignment':b'<Project><ItemGroup><I Include="a"><Filename>forbidden</Filename></I></ItemGroup></Project>'}
    out.mkdir(parents=True); files=[]
    for id,data in values.items():
        folder=out/id;folder.mkdir();(folder/'main.proj').write_bytes(data)
        files.append(dict(path=id+'/main.proj',bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    (out/'manifest.json').write_text(json.dumps(dict(schemaVersion=1,cases=[dict(id=id) for id in values],files=files,
        legacyOriginal=dict(path=str(original),sha256=hashlib.sha256(legacy).hexdigest(),directoryFiles=['main.proj']),
        qualification='Supplemental transition/refusal evidence; not extra semantic scenarios'),indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    if sys.argv[1]=='--supplemental': supplemental(sys.argv[2])
    else: materialize(sys.argv[1])
