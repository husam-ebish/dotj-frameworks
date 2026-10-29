package org.dotj.internal.build.evaluation;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Selected same-input Default observations, with honest root/previous context absence. */
final class DefaultCycleTest {
    private static void require(boolean value,String message) { if(!value)throw new AssertionError(message); }
    private static String decode(String value) { return new String(Base64.getDecoder().decode(value),StandardCharsets.UTF_8); }
    private static Object field(Object object,String name) throws Exception {
        try { return object.getClass().getDeclaredMethod(name).invoke(object); }
        catch(NoSuchMethodException error) { throw new AssertionError("Missing Default-cycle context field: "+name,error); }
    }
    static void run(Path bridge,Path fixtures,Path output) throws Exception {
        Result result=null;Path directory=null;int index=0,expected=0,cases=0;
        List<String> rows=new ArrayList<>();
        for(String line:Files.readAllLines(bridge,StandardCharsets.UTF_8)) {
            String[] f=line.split("\t",-1);
            if(f[0].equals("CASE")) {
                if(result!=null)require(index==expected,"Missing cycle notice comparison");
                require(f.length==6,"Bad cycle case");
                directory=fixtures.resolve(f[1]);
                result=evaluate(directory.resolve("main.proj"),directory,Map.of());
                require(result.property("P").equals(decode(f[2])) && result.property("Q").equals(decode(f[3])),f[1]+" native cycle property/order mismatch");
                require(result.evaluatedFiles().equals(decode(f[4]).lines().map(directory::resolve).toList()),f[1]+" native cycle file order mismatch");
                index=0;expected=Integer.parseInt(f[5]);cases++;
                require(result.duplicateImports().size()==expected,f[1]+" native cycle notice count mismatch");
                require(evaluate(directory.resolve("main.proj"),directory,Map.of()).equals(result),"Cycle state leaked across calls");
                try { result.duplicateImports().clear();throw new AssertionError("Mutable cycle notices"); }
                catch(UnsupportedOperationException immutable) { }
                rows.add(f[1]+"\tNATIVE_DEFAULT_CYCLE_PROPERTIES_ORDER_CURRENT_CONTEXT\t"+expected);
            } else {
                require(f[0].equals("NOTICE") && f.length==13 && result!=null,"Bad cycle notice");
                var notice=result.duplicateImports().get(index++);
                require(notice.referenceCode().equals(f[2]) && notice.owner().equals(directory.resolve(f[3])) && notice.importedProject().equals(directory.resolve(f[4])),f[1]+" native cycle notice identity/order mismatch");
                Object current=field(notice,"current"),previous=field(notice,"previous"),root=field(notice,"rootContext");
                require(current!=null,"Missing cycle current position");
                for(int i=0;i<4;i++) {
                    String name=List.of("line","column","endLine","endColumn").get(i);
                    require(field(current,name).equals(Integer.valueOf(f[5+i])),f[1]+" cycle native current "+name+" mismatch");
                }
                if(f[9].equals("ROOT")) {
                    require(previous==null && root!=null && root.equals(directory.resolve(f[10])),f[1]+" root context must have root path and absent previous import");
                    require(f[11].equals("-") && f[12].equals("-"),"Root context invented previous coordinates");
                } else {
                    require(f[9].equals("PREVIOUS") && previous!=null && root==null,f[1]+" non-root context must have previous import and absent root context");
                    require(field(previous,"owner").equals(directory.resolve(f[10])) && field(previous,"line").equals(Integer.valueOf(f[11])) && field(previous,"column").equals(Integer.valueOf(f[12])),f[1]+" native first-import context mismatch");
                }
            }
        }
        require(result!=null && index==expected && cases==3,"Incomplete Default-cycle comparison");
        require(!Files.exists(fixtures.resolve("must-not-exist.txt")),"Cycle task marker executed");
        Files.write(output,rows,StandardCharsets.UTF_8);
    }
    public static void main(String[] args) throws Exception {
        run(Path.of(args[0]),Path.of(args[1]),Path.of(args[2]));
        System.out.println("PASS 3 selected Default cycles; root/previous context absence matched; no full chain or public ABI qualification");
    }
}
