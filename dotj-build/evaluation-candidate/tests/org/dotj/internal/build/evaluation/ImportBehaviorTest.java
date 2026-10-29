package org.dotj.internal.build.evaluation;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Same controlled bytes as the typed native import probe; cycles remain profile restrictions. */
final class ImportBehaviorTest {
    private static String decode(String value) { return new String(Base64.getDecoder().decode(value), StandardCharsets.UTF_8); }
    private static void require(boolean value,String message) { if(!value)throw new AssertionError(message); }
    static void run(Path bridge,Path fixtures,List<String> rows) throws Exception {
        int count=0;
        for(String line:Files.readAllLines(bridge,StandardCharsets.UTF_8)) {
            String[] f=line.split("\t",-1);require(f.length==7,"Bad native import bridge");
            String id=f[0];Path directory=fixtures.resolve(id),project=directory.resolve("main.proj");
            try {
                Result result=evaluate(project,directory,Map.of());
                require(f[1].equals("SUPPORTED"),id+" expected explicit cycle refusal or native missing failure");
                require(result.property("P").equals(decode(f[2])) && result.property("Q").equals(decode(f[3])),id+" native property mismatch");
                List<Path> expected=decode(f[4]).lines().map(directory::resolve).map(Path::toAbsolutePath).map(Path::normalize).toList();
                require(result.evaluatedFiles().equals(expected),id+" native import order mismatch");
                List<String> notices=result.duplicateImports().stream().map(n -> n.referenceCode()+"|"+directory.relativize(n.owner()).toString().replace('\\','/')+"|"+directory.relativize(n.importedProject()).toString().replace('\\','/')).toList();
                require(notices.equals(decode(f[5]).lines().toList()),id+" native notice code/owner/target/order mismatch");
                try { result.duplicateImports().add(new DuplicateImport("invalid",project,project));throw new AssertionError("Mutable notices"); }
                catch(UnsupportedOperationException expectedImmutable) { }
                Result fresh=evaluate(project,directory,Map.of());
                require(fresh.equals(result),id+" per-call import/property state leaked");
                rows.add(id+"\tNATIVE_ONCE_ONLY_PROPERTIES_ORDER_NOTICES\t"+f[2]+"\t"+f[4]);
            } catch(ProfileRejected error) {
                require(f[1].equals("CYCLE_REFUSAL") && error.code.equals("IMPORT_CYCLE_UNQUALIFIED"),id+" unexpected profile refusal "+error.code);
                rows.add(id+"\tEXPLICIT_CYCLE_GAP\t"+error.code);
            } catch(EvaluationFailure error) {
                require(f[1].equals("MISSING") && error.referenceCode.equals(f[6]) && error.project.equals(project) && error.missingImport.equals(directory.resolve("missing.props")),id+" native missing failure mismatch");
                rows.add(id+"\tNATIVE_MISSING_CODE_OWNER_PATH\t"+error.referenceCode);
            }
            count++;
        }
        require(count==9,"Missing import matrix case");
        require(!Files.exists(fixtures.resolve("must-not-exist.txt")),"Import task marker executed");
    }
}
