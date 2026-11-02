"""Static/protocol synthetic controls only. No child execution or global patching."""
import ast, contextlib, copy, importlib.util, io, json, tempfile, unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('boolean_v1_protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
q=importlib.util.spec_from_file_location('boolean_v1_pair',Path(__file__).with_name('compare_pair.py'));pair=importlib.util.module_from_spec(q);q.loader.exec_module(pair)
class StaticControls(unittest.TestCase):
    def test_registry_and_all_groups(self):
        cases=p.read(p.HERE/'manifest.json')['cases'];private=p.read(p.HERE/'private-cases.json')['cases']
        self.assertEqual(len(cases),len({x['id'] for x in cases}));self.assertEqual({x['group'] for x in cases+private},{x['id'] for x in p.read(p.HERE/'source-trace.json')['groups']})
    def test_all_xml_and_fixture_ids(self):
        from xml.etree import ElementTree
        for folder,name in [('fixtures','manifest.json'),('private-fixtures','private-cases.json')]:
            cases=p.read(p.HERE/name)['cases'];self.assertEqual({x['id'] for x in cases},{x.name for x in (p.HERE/folder).iterdir()})
            for case in cases:ElementTree.parse(p.HERE/folder/case['id']/'main.proj')
    def test_source_anchors_resolve(self):
        anchors={a['path'] for a in p.read(p.HERE/'source-trace.json')['anchors']}
        for name in ['manifest.json','private-cases.json']:
            for c in p.read(p.HERE/name)['cases']:self.assertTrue(set(c['sourceAnchors'])<=anchors);self.assertTrue(c['requiredObservations'])
    def test_transition_native_case_binding(self):
        manifest={x['id']:x for x in p.read(p.HERE/'manifest.json')['cases']};t=p.read(p.HERE/'predecessor-transitions.json')
        self.assertEqual(len(t['transitions']),len({x['id'] for x in t['transitions']}))
        for x in t['transitions']:self.assertEqual(manifest[x['nativeCase']]['condition'],x['condition']);self.assertEqual(manifest[x['nativeCase']]['globals'],x['globals'])
    def test_aliases_twelve_have_property_and_literal_inputs(self):
        ids={x['id'] for x in p.read(p.HERE/'manifest.json')['cases']}
        for n in range(1,13):
            for kind in ['quoted','property','quoted-property','mixed']:self.assertIn(f'BOOL-ALIAS-{n:02}-{kind}',ids)
    def test_numeric_boundaries_are_unobserved(self):
        rows=[x for x in p.read(p.HERE/'manifest.json')['cases'] if x['id'].startswith('BOOL-NUM-')]
        self.assertTrue(rows);self.assertTrue(all(x['nativeOutcome']=='UNOBSERVED' for x in rows));self.assertTrue(any('1.0000000000000001110' in x['condition'] for x in rows))
    def test_verify_parser_rejects_selectors_and_abbreviations(self):
        base=['--receipt=x','--receipt-sha256=x','--lock-sha256=x']
        for bad in ['--mode=capture','--inner','--execute-reviewed','--execute','--out=x','--mode','--rece=x','--lock-sha=x']:
            with self.subTest(bad=bad),contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):p.verify_parser().parse_args(base+[bad])
    def test_capture_parser_rejects_mode_and_abbreviations(self):
        base=['--out=x','--lock-sha256=x','--review=x','--review-sha256=x']
        for bad in ['--mode=capture','--mode=java','--inner','--execute-reviewed','--rev=x','--lock-sha=x']:
            with self.subTest(bad=bad),contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):p.capture_parser().parse_args(base+[bad])
    def test_schemas_reject_bool_as_integer(self):
        with self.assertRaises(ValueError):p.validate(True,{'type':'integer'})
        with self.assertRaises(ValueError):p.validate(1,{'type':'boolean'})
    def test_schemas_reject_unknown_missing_and_wrong_types(self):
        schema={'type':'object','fields':{'x':{'type':'integer'}}}
        for value in [{},{'x':1,'extra':0},{'x':'1'},[]]:
            with self.assertRaises(ValueError):p.validate(value,schema)
    def test_failure_cannot_be_false_boolean_success(self):
        schema=p.read(p.HERE/'observation-schema.json')['observer']['fields']['rows']['items']['fields']['evaluation']
        for bad in [{'success':False},{'success':False,'properties':{'P':'','Q':''}},{'success':True,'type':'failure'}]:
            with self.assertRaises(ValueError):p.validate(bad,schema)
    def test_duplicate_json_rejected(self):
        with self.assertRaises(ValueError):json.loads('{"a":1,"a":2}',object_pairs_hook=p.unique_pairs)
    def test_bounded_reads(self):
        scratch=p.B/'agents/batch2516-build-boolean-native-preparation-v1/static-temp';scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as d:
            path=Path(d)/'x';path.write_bytes(b'12345')
            with self.assertRaises(ValueError):p.bounded(path,4)
            self.assertEqual(p.bounded(path,5),b'12345')
    def test_no_mode_forwarding_and_fixed_sibling_imports(self):
        for name in ['capture_native.py','verify_receipt.py','compare_pair.py']:
            text=(p.HERE/name).read_text();ast.parse(text);self.assertNotIn('sys.argv[1:]',text);self.assertIn("with_name('protocol.py')",text)
    def test_host_trace_has_no_unbounded_side_file(self):
        env=p.environment(Path('D:/example'));self.assertEqual(env['DOTNET_HOST_TRACE'],'1');self.assertNotIn('DOTNET_HOST_TRACEFILE',env);self.assertEqual(env['DOTNET_GCHeapHardLimit'],'8000000')
    def test_guard_pin_retained(self):self.assertEqual(p.sha(p.GUARD),p.GUARD_SHA)
    def test_normalization_does_not_touch_values_or_diagnostics(self):
        v={'rows':[{'globals':{'V':'D:/root'},'evaluation':{'success':False,'file':'D:/root/main.proj','message':'bad D:/root/main.proj','code':'MSB-X'},'diagnostics':[{'file':'D:/root/main.proj','message':'literal diagnostic','code':'MSB-Y'}]}]}
        n=pair.normalized(v,'D:/root');self.assertEqual(n['rows'][0]['globals']['V'],'D:/root');self.assertEqual(n['rows'][0]['evaluation']['code'],'MSB-X');self.assertEqual(n['rows'][0]['diagnostics'][0]['message'],'literal diagnostic');self.assertEqual(v['rows'][0]['evaluation']['file'],'D:/root/main.proj')
    def test_missing_or_boolean_pid_is_rejected(self):
        with self.assertRaises(ValueError):p.process({},[],Path('D:/x'),'native',30)
        r={key:None for key in p.PROCESS_FIELDS};r['processId']=True
        with self.assertRaisesRegex(ValueError,'positive PID'):p.process(r,[],Path('D:/x'),'native',30)
    def test_new_python_files_parse(self):
        for path in p.HERE.glob('*.py'):ast.parse(path.read_text(),filename=str(path))
    def test_observer_schema_accepts_real_immutable_predecessor_shape_only(self):
        prior=Path('C:/source/repos/dotj Frameworks/dotj-build/evaluation-candidate/condition-logic-v2/evidence/native-pass2-capture.json')
        old=p.read(prior)
        # Reading an old captured shape is not recapturing or adding observations.
        p.validate(old['payload'],p.read(p.HERE/'observation-schema.json')['observer'])
    def test_fix1_complete_python_distribution_and_native_dependencies(self):
        manifest=p.verify_python_runtime();names={Path(x['path']).name.lower() for x in manifest['files']}
        self.assertTrue({'python.exe','python313._pth','python313.zip','python313.dll','python3.dll','_ctypes.pyd','_hashlib.pyd','libffi-8.dll','libcrypto-3.dll','vcruntime140.dll','vcruntime140_1.dll'}<=names)
        self.assertEqual(manifest['fileCount'],len(manifest['files']))
        for binary in manifest['binaryImports']:
            self.assertTrue({x.lower() for x in binary['bundled']}<=names)
        self.assertFalse(manifest['configuration']['importSiteEnabled'])
    def test_fix1_python_digest_and_inventory_negatives(self):
        manifest=p.read(p.HERE/'python-runtime-manifest.json')
        wrong=copy.deepcopy(manifest);wrong['files'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'pin changed'):p.verify_python_runtime(wrong)
        omitted=copy.deepcopy(manifest);omitted['files'].pop()
        with self.assertRaisesRegex(ValueError,'inventory changed'):p.verify_python_runtime(omitted)
        outside=copy.deepcopy(manifest);outside['files'][0]['path']='C:/outside.dll'
        with self.assertRaisesRegex(ValueError,'payload path'):p.verify_python_runtime(outside)
    def test_fix1_python_manifest_and_every_payload_are_native_lock_bound(self):
        lock={x['path']:x for x in p.read(p.HERE/'native-input-lock.json')['pins']}
        descriptor=p.descriptor(p.HERE/'python-runtime-manifest.json');self.assertEqual(lock[descriptor['path']],descriptor)
        for item in p.read(p.HERE/'python-runtime-manifest.json')['files']:self.assertEqual(lock[item['path']],item)
        tree=ast.parse((p.HERE/'protocol.py').read_text());verify=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='verify_lock')
        self.assertTrue(any(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='verify_python_runtime' for x in ast.walk(verify)))
    def test_fix1_future_review_path_and_root_runtime_binding(self):
        proposal=p.read(p.HERE/'proposed-commands.json');wanted=p.descriptor(p.HERE/'python-runtime-manifest.json');self.assertEqual(proposal['pythonRuntimeManifest'],wanted)
        for command in proposal['commands']:
            self.assertEqual(command['pythonRuntimeManifest'],wanted)
            self.assertIn('--review='+str(p.B/'orchestration/two-frameworks/batch2516-native-fix1-review.json'),command['outerArgv'])
            self.assertEqual(command['outerTimeoutSeconds'],180);self.assertEqual(command['nativeTimeoutSeconds'],30)
            self.assertEqual(command['outerArgv'][0],str(p.B/'toolchains/python-3.13.9/python.exe'))
        self.assertEqual(p.sha(p.B/'orchestration/two-frameworks/batch2516-native-prelaunch-review.json'),'804161a56d35e1c8837dfd97f59a0b6f375ecc7375876d2dec12fe5ac614fc65')
    def test_fix1_exact_below_midpoint_decimal_and_both_operands(self):
        from xml.etree import ElementTree
        literal='0.'+'0'*323+'2';self.assertEqual(len(literal.split('.')[1]),324)
        self.assertLess(2*(2**1075),10**324)
        self.assertGreater(4*(2**1075),10**324);self.assertGreater(5*(2**1075),10**324)
        rows={x['id']:x for x in p.read(p.HERE/'manifest.json')['cases']}
        for order,(left,right) in enumerate([(literal,'0'),('0',literal)]):
            ident=f'BOOL-NUM-31-{order}';condition=repr(left)+'=='+repr(right);self.assertEqual(rows[ident]['condition'],condition)
            xml=ElementTree.parse(p.HERE/'fixtures'/ident/'main.proj');self.assertEqual(xml.find('PropertyGroup').attrib['Condition'],condition)
            self.assertEqual(rows[ident]['nativeOutcome'],'UNOBSERVED');self.assertIn(ident,p.read(p.HERE/'numeric-prerequisites.json')['requiredCaseIds'])
    def test_fix1_preserves_all_original_cases_and_fixture_bytes(self):
        archive=p.read(p.B/'agents/batch2516-build-boolean-native-preparation-v1/history/fix1-before/archive-manifest.json');mapping={x['originalPath']:x for x in archive['files']}
        before=p.read(mapping[str(p.HERE/'manifest.json')]['archivedPath']);after=p.read(p.HERE/'manifest.json')
        self.assertEqual(after['cases'][:len(before['cases'])],before['cases']);self.assertEqual(len(after['cases']),len(before['cases'])+2)
        for item in archive['files']:
            if Path(item['originalPath']).is_relative_to(p.HERE/'fixtures'):self.assertEqual(p.sha(item['originalPath']),item['sha256'])
    def test_fix1_reuses_unchanged_selected_native_pins_without_sdk_rescan(self):
        archive=p.read(p.B/'agents/batch2516-build-boolean-native-preparation-v1/history/fix1-before/archive-manifest.json');mapping={x['originalPath']:x for x in archive['files']}
        before=p.read(mapping[str(p.HERE/'native-input-lock.json')]['archivedPath']);old={x['path']:x for x in before['pins']};now={x['path']:x for x in p.read(p.HERE/'native-input-lock.json')['pins']}
        fingerprint=p.read(p.HERE/'native-fingerprint.json');self.assertEqual(p.sha(p.HERE/'native-fingerprint.json'),mapping[str(p.HERE/'native-fingerprint.json')]['sha256'])
        for item in fingerprint['files']:
            self.assertEqual(now[item['path']],old[item['path']]);self.assertTrue(Path(item['path']).is_file());self.assertEqual(Path(item['path']).stat().st_size,item['sizeBytes'])
    def test_fix1_predecessor_preservation_lock_unchanged(self):
        archive=p.read(p.B/'agents/batch2516-build-boolean-native-preparation-v1/history/fix1-before/archive-manifest.json');mapping={x['originalPath']:x for x in archive['files']}
        self.assertEqual(p.sha(p.HERE/'predecessor-preservation-lock.json'),mapping[str(p.HERE/'predecessor-preservation-lock.json')]['sha256'])
        for item in p.read(p.HERE/'predecessor-preservation-lock.json')['files']:p.pin(item)
    def test_fix1_actual_launch_count_survives_nonzero_and_guard_failure(self):
        spec=importlib.util.spec_from_file_location('boolean_capture_count_control',p.HERE/'capture_native.py');capture=importlib.util.module_from_spec(spec);spec.loader.exec_module(capture)
        for child,wanted in [({'launched':True,'exitCode':1},1),({'launched':True,'error':'assignment failed','exitCode':125},1),({'launched':False,'error':'admission unavailable','exitCode':None},0),({'launched':False,'error':'creation failed','exitCode':None},0)]:
            with self.subTest(child=child):
                record={'nativeExecutions':0,'status':'FAILED_OR_DEFERRED','raw':{'stderr':'retained'}};updates=[]
                capture.update_process(record,child,lambda:updates.append(dict(record)))
                self.assertEqual(record['nativeExecutions'],wanted);self.assertIs(record['process'],child);self.assertEqual(len(updates),1)
                self.assertEqual(record['status'],'FAILED_OR_DEFERRED');self.assertEqual(record['raw'],{'stderr':'retained'})
if __name__=='__main__':unittest.main(verbosity=2)
