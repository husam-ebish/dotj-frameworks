"""Deterministic designed inputs only; no expected native outputs or launches."""
from xml.sax.saxutils import escape, quoteattr

GROUPS=['all-four-numeric','all-four-versions','both-mixed-paths','dispatch-priority',
        'nonnumeric-and-observable-errors','grammar-and-xml','one-pass-and-reached-order',
        'sites-imports-globals-and-lifecycle','cache-and-warning-owner',
        'version-component-reachability','private-bounds-and-isolation','historical-transition']
MARKER='<Target Name="Never"><Error Text="must never execute"/><WriteLinesToFile File="must-not-exist.txt" Lines="bad"/></Target>'

def design():
    rows=[];files={}
    def add(group,label,condition,*,globals=None,site='PropertyGroup',before='',after='',imports=None,scope='SELECTED',purpose='',anchor='NumericComparisonExpressionNode.cs:36-65',raw=None):
        case_id='ORD-'+label
        if site=='PropertyGroup':body='<PropertyGroup Condition='+quoteattr(condition)+'><P>yes</P><Q>taken</Q></PropertyGroup>'
        elif site=='Property':body='<PropertyGroup><P Condition='+quoteattr(condition)+'>yes</P><Q>taken</Q></PropertyGroup>'
        elif site=='Import':body='<Import Project="nested/child.proj" Condition='+quoteattr(condition)+'/>'
        else:body='<ImportGroup Condition='+quoteattr(condition)+'><Import Project="nested/child.proj"/></ImportGroup>'
        xml=raw if raw is not None else '<Project>'+before+body+after+MARKER+'</Project>\n'
        content={'main.proj':xml.encode('utf-8')}
        if site in ['Import','ImportGroup']:content['nested/child.proj']=b'<Project><PropertyGroup><P>yes</P><Q>taken</Q></PropertyGroup></Project>\n'
        for name,value in (imports or {}).items():content[name]=value.encode('utf-8')
        rows.append(dict(id=case_id,group=group,globals=globals or {},condition=condition,site=site,
                         purpose=purpose or label,sourceAnchor=anchor,nativeStatus='NOT_LAUNCHED_NOT_OBSERVED',
                         productScope=scope,files=[],historicalId=None))
        files[case_id]=content
    ops=[('LT','<'),('LE','<='),('GT','>'),('GE','>=')]
    numeric=[('less','1','2'),('equal','2','2'),('greater','3','2'),('signed','+4','-4'),
             ('zero','-0','0'),('decimal','-.5','+.25'),('hex','0xFFFFFFFF','0'),('hexzero','0x00000001','1'),
             ('large',"'999999999999999999999999999999999999999'",'0'),('nan-left',"'NaN'",'0'),
             ('nan-right','0',"'NaN'"),('nan-trim',"' NaN '",'0'),('exponent',"'1e2'",'2'),
             ('infinity',"'Infinity'",'0'),('suffix',"'1d'",'0'),('hexfloat',"'0x1p1'",'0'),
             ('property',"'$(N)'",'2'),('quoted',"'01.50'","'2.0'")]
    for tag,op in ops:
        for label,left,right in numeric:add(GROUPS[0],f'NUM-{tag}-{label}',f'{left}{op}{right}',globals={'N':'1'} if label=='property' else None)
    versions=[('major','1.2.3','2.0.0'),('minor','6.1.0','6.2.0'),('build','6.2.1','6.2.2'),
              ('revision','6.2.1.1','6.2.1.2'),('equal','6.2.1.1','6.2.1.1'),('two-three','6.0','6.0.0'),
              ('three-four','6.0.0','6.0.0.0'),('max','2147483647.2147483647.2147483647.2147483647','1.0.0'),
              ('overflow','2147483648.0.0','1.0.0'),('negative','6.-1.0','1.0.0'),('empty','6..0','1.0.0'),
              ('fifth','6.0.0.0.0','1.0.0'),('plus','+6.+0.+0','6.0.0'),('negative-zero','6.-0.-0','6.0.0'),
              ('space',' 6 . 0 . 0 ','6.0.0'),('sign-space','6.+ 0.0','6.0.0'),('nonnumeric','v6.0.0','6.0.0'),
              ('exponent','6.0e0.0','6.0.0'),('hex','6.0x0.0','6.0.0')]
    for tag,op in ops:
        for label,left,right in versions:add(GROUPS[1],f'VER-{tag}-{label}',f"'{left}'{op}'{right}'",anchor='Version.cs:357-442')
    for tag,op in ops:
        # Equal-major must avoid numeric/numeric; fractional must avoid the
        # higher-priority version/version path. Minor5000000000 exceeds Int32,
        # while invariant decimal conversion still yields the finite number6.5.
        for label,num,ver in [('less','5','6.0.0'),('equal-major','6','6.0.0'),('greater','7','6.0.0'),
                              ('fractional','6.5000000000','6.0.0'),('negative','-1','0.0.0'),('large','999999999999','6.0.0'),
                              ('nan',"'NaN'",'6.0.0'),('hex','0xFFFFFFFF','0.0.0')]:
            add(GROUPS[2],f'MIX-{tag}-NV-{label}',f"{num}{op}'{ver}'")
            add(GROUPS[2],f'MIX-{tag}-VN-{label}',f"'{ver}'{op}{num}")
        for label,left,right in [('version-priority','6.1','6.2.0'),('numeric-priority','6.10','6.2'),
                                  ('upstream-priority','8.1','8.0.16.23'),('reverse-version','6.2.0','6.1')]:
            add(GROUPS[3],f'DISPATCH-{tag}-{label}',f"'{left}'{op}'{right}'")
    invalid=[('left',"'bad'<1"),('right',"1<'bad'"),('source-error-side',"'6.0.0'<'bad'"),
             ('both',"'bad'<'worse'"),('empty',"''<1"),('undefined',"'$(Missing)'<1"),('boolean',"'true'<1"),
             ('exists',"Exists('')<1"),('slash',"HasTrailingSlash('bad')<1"),('not',"!1<2"),
             ('nested',"(Exists('')==true)<1"),('bad-global-left',"'$(L)'<'$(R)'"),
             ('bad-global-right',"'$(R)'<'$(L)'"),('version-only-right',"'bad'<'6.0.0'")]
    for label,condition in invalid:add(GROUPS[4],'ERROR-'+label,condition,globals={'L':'bad','R':'worse'} if 'global' in label else None)
    grammar=[('group','!(1<2)'),('precedence','false Or 1<2 And false'),('short-or',"true Or 'bad'<1"),
             ('short-and',"false And 'bad'<1"),('separate-le','1< =2'),('separate-ge','1> =2'),
             ('missing-left','<2'),('missing-right','1<'),('chain','1<2<3'),('chain-eq','1<2==true'),
             ('chain-reverse','true==1<2'),('double','1<<2'),('unclosed','(1<2'),('trailing','1<2 junk'),
             ('not-factor','!1<2'),('nested-group','((1<2))'),('and-or','1<2 And false Or true')]
    for label,condition in grammar:add(GROUPS[5],'GRAMMAR-'+label,condition)
    add(GROUPS[5],'GRAMMAR-skipped-malformed','1<',before='<PropertyGroup Condition="false">',after='</PropertyGroup>',site='Property')
    # Avoid nested PropertyGroup XML: valid outer false ImportGroup, malformed inner Import.
    rows.pop();files.pop('ORD-GRAMMAR-skipped-malformed')
    add(GROUPS[5],'GRAMMAR-skipped-malformed','1<',raw='<Project><ImportGroup Condition="false"><Import Project="absent.proj" Condition="1&lt;"/></ImportGroup>'+MARKER+'</Project>\n',site='Import')
    expansion=[('global',"'$(N)'<2",{'N':'1'}),('escaped-dollar',"'$(N)'<2",{'N':'%24(M)'}),
               ('residual',"'$(N)'<2",{'N':'$(M)','M':'1'}),('operator-data',"'$(N)'<2",{'N':'1<2'}),
               ('quote-data',"'$(N)'<2",{'N':"1' Or true Or '1"}),('unicode-left',"'$(L)'<'$(R)'",{'L':'é','R':'bad'}),
               ('unicode-right',"'$(R)'<'$(L)'",{'L':'é','R':'bad'}),('skip-or',"true Or '$(N)'<2",{'N':'bad'}),
               ('skip-and',"false And '$(N)'<2",{'N':'bad'})]
    for label,condition,global_values in expansion:add(GROUPS[6],'EXPAND-'+label,condition,globals=global_values,scope='SOURCE_OR_NATIVE_RESTRICTION_REVIEW' if 'unicode' in label else 'SELECTED')
    add(GROUPS[6],'EXPAND-encounter-order',"'$(N)'<2",before='<PropertyGroup><N>1</N></PropertyGroup>',after='<PropertyGroup><N>3</N><Q Condition="\'$(N)\'&gt;2">after</Q></PropertyGroup>')
    for site in ['Property','PropertyGroup','Import','ImportGroup']:
        add(GROUPS[7],'SITE-'+site,"'$(N)'<2",site=site,globals={'N':'1'})
    add(GROUPS[7],'SITE-global-immutable',"'$(N)'<2",globals={'N':'1'},before='<PropertyGroup><N>3</N></PropertyGroup>')
    add(GROUPS[7],'SITE-global-local',"'$(N)'<2",globals={'N':'1'},raw='<Project TreatAsLocalProperty="N"><PropertyGroup><N>3</N></PropertyGroup><PropertyGroup Condition="\'$(N)\'&lt;2"><P>yes</P><Q>taken</Q></PropertyGroup>'+MARKER+'</Project>\n')
    for label,condition,path in [('false-missing','2<1','absent.proj'),('true-missing','1<2','absent.proj'),('false-expanded','2<1','$(Missing)')]:
        add(GROUPS[7],'IMPORT-'+label,condition,raw='<Project><Import Project='+quoteattr(path)+' Condition='+quoteattr(condition)+'/>'+MARKER+'</Project>\n',site='Import')
    add(GROUPS[7],'IMPORT-duplicate','1<2',site='Import',after='<Import Project="nested/child.proj" Condition="2&gt;1"/>')
    add(GROUPS[7],'IMPORT-cycle','1<2',site='Import',imports={'nested/child.proj':'<Project><Import Project="../main.proj" Condition="1&lt;2"/></Project>\n'})
    add(GROUPS[7],'IMPORT-nested-owner','1<2',site='Import',imports={'nested/child.proj':'<Project><PropertyGroup Condition="1&lt;2"><P>yes</P><Q>taken</Q></PropertyGroup><Import Project="grand.proj" Condition="1&lt;2"/></Project>\n','nested/grand.proj':'<Project><PropertyGroup><Q>nested</Q></PropertyGroup></Project>\n'})
    # Keep these consecutive in one partition: process-shared raw AST/cache, per-row owner/state.
    for index,value in enumerate(['bad','1','3','1']):
        add(GROUPS[8],f'CACHE-fail-valid-{index}',"'$(CacheN)' < 2718",globals={'CacheN':'3000' if value=='3' else value})
    for index,condition in enumerate(['2718<3000 And true Or false','2718<3000 And true Or false','2718 < 3000 And true Or false','2718<3000 and true or false']):
        add(GROUPS[8],f'CACHE-owner-{index}',condition,site='Import' if index==1 else 'PropertyGroup')
    add(GROUPS[8],'CACHE-skipped-first','2719<3000 And true Or false',raw='<Project><PropertyGroup Condition="false"><P Condition="2719&lt;3000 And true Or false">skipped</P></PropertyGroup><Import Project="nested/child.proj"/>'+MARKER+'</Project>\n',imports={'nested/child.proj':'<Project><PropertyGroup Condition="2719&lt;3000 And true Or false"><P>yes</P><Q>taken</Q></PropertyGroup></Project>\n'})
    reachable=[('escaped-nul',{'V':'6.0.0%00'}),('global-nul',{'V':'6.0.0\0'}),('space-then-nul',{'V':'6.0.0 \0'}),
               ('nul-then-space',{'V':'6.0.0\0 '}),('tab',{'V':'6.\t0.0'}),('newline',{'V':'6.\n0.0'}),
               ('vertical-tab',{'V':'6.\x0b0.0'}),('form-feed',{'V':'6.\x0c0.0'}),('carriage',{'V':'6.\r0.0'}),
               ('nbsp',{'V':'6.\u00a00.0'}),('unicode-digit',{'V':'6.٠.0'}),('escaped-tab',{'V':'6.%090.0'})]
    for label,global_values in reachable:add(GROUPS[9],'REACH-'+label,"'$(V)'<'7.0.0'",globals=global_values,scope='REACHABILITY_AND_RESTRICTION_REVIEW',anchor='Version.cs:357-442; Number.Parsing.Common.cs:302-309')
    # Native inputs witness shared grammar; strict private limits are Java-only below.
    add(GROUPS[10],'BOUND-group64','('*64+'1<2'+')'*64)
    add(GROUPS[10],'BOUND-group65','('*65+'1<2'+')'*65,scope='PRIVATE_DESIGN_REFUSAL')
    add(GROUPS[10],'BOUND-node256','!'+' And '.join(['1<2']*64),scope='PRIVATE_BOUNDARY_REVIEW')
    add(GROUPS[10],'BOUND-node257','!!'+' And '.join(['1<2']*64),scope='PRIVATE_DESIGN_REFUSAL')
    add(GROUPS[11],'HISTORY-BOOL-BOUND-ordering','1<2')
    rows[-1]['historicalId']='BOOL-BOUND-ordering'
    java_only=[dict(id='JAVA-VERSION-INTEGER-BOUNDARIES',nativeParityCredit=0,values=['+0','-0','2147483647','2147483648','-1','\t+0\r','+ 0','0 \0','0\0 ','٠','\u00a00']),
               dict(id='JAVA-PRIVATE-GROUP-64-65',nativeParityCredit=0,accepted=64,refused=65),
               dict(id='JAVA-PRIVATE-NODE-256-257',nativeParityCredit=0,accepted=256,refused=257),
               dict(id='JAVA-RAW-AST-SNAPSHOT-ISOLATION',nativeParityCredit=0,purpose='immutable raw nodes, fresh globals/owner/error and snapshots; behavior before field inspection'),
               dict(id='JAVA-CACHE-3000-CLEAR',nativeParityCredit=0,purpose='unchanged >3000 private clear policy; no native eviction equivalence')]
    rows.sort(key=lambda row:GROUPS.index(row['group']))
    return rows,files,java_only
