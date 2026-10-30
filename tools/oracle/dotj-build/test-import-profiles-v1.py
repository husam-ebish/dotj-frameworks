"""Profile evidence refuses altered native fields; synthetic ends test transport only."""
import copy,json,runpy,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
class ProfileEvidenceTest(unittest.TestCase):
    def test_same_profile_bridge_and_malformed_rows(self):
        tool=HERE/'verify-import-profiles-v1.py'
        self.assertTrue(tool.exists(),'Missing selected-profile evidence validator')
        api=runpy.run_path(str(tool))
        captures=json.loads((REPO/'dotj-build/evaluation-candidate/evidence/native-import-observations-v1.json').read_text())['captures'][1:]
        captures=copy.deepcopy(captures)
        for c in captures:
            for r in c['rows']:
                for d in r['diagnostics']:d.update(endLine=7,endColumn=8)
                if not r['evaluation']['success']:r['evaluation'].update(endLine=7,endColumn=8)
        text=api['bridge'](captures)
        self.assertEqual(18,sum(x.startswith('CASE\t') for x in text.splitlines()))
        self.assertIn('\t7\t8\t',text,'New ends must survive without Default substitution')
        mutations=[lambda r:r['diagnostics'][0].pop('code'),lambda r:r['diagnostics'][0].update(line=99),lambda r:r['diagnostics'][0].update(file='borrowed-default'),lambda r:r['diagnostics'].pop(),lambda r:r['diagnostics'][0].update(code='MSB4011'),lambda r:r['diagnostics'].reverse(),lambda r:r['diagnostics'][0].pop('endColumn'),lambda r:r['diagnostics'][0].update(endLine=-1),lambda r:r['diagnostics'][0].update(endColumn='0'),lambda r:r['evaluation'].update(properties={'P':'invented'}),lambda r:r['cleanup'].update(loaded=1),lambda r:r.update(taskMarkerAbsent=False)]
        for mutation in mutations:
            bad=copy.deepcopy(captures);row=bad[1]['rows'][7];mutation(row)
            with self.assertRaises((ValueError,KeyError)):api['bridge'](bad)
        for mutation in [lambda e:e.pop('endColumn'),lambda e:e.update(endLine=-1),lambda e:e.update(endColumn='0'),lambda e:e.pop('code')]:
            bad=copy.deepcopy(captures);mutation(bad[1]['rows'][7]['evaluation'])
            with self.assertRaises((ValueError,KeyError)):api['bridge'](bad)
        for profile in ['Default','6','RecordDuplicateButNotCircularImports, RejectCircularImports','IgnoreMissingImports']:
            bad=copy.deepcopy(captures);bad[0]['profile']=profile
            with self.assertRaises(ValueError):api['bridge'](bad)
        bad=copy.deepcopy(captures);bad[0]['rows'][1]['evaluation']['duplicateImports'].reverse()
        with self.assertRaises(ValueError):api['bridge'](bad)
        bad=copy.deepcopy(captures);bad[0]['rows'][7]['evaluation']['duplicateImports'].append(copy.deepcopy(bad[0]['rows'][7]['evaluation']['imports'][0]))
        with self.assertRaises(ValueError):api['bridge'](bad)
        bad=copy.deepcopy(captures);bad[1]['rows'][0]['evaluation']['duplicateGetterFailure']=None
        with self.assertRaises(ValueError):api['bridge'](bad)
if __name__=='__main__':unittest.main()
