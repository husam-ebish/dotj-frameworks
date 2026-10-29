package org.dotj.internal.build.evaluation;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Native coordinates are transported verbatim; no coordinate is computed from fixture text here. */
final class ImportLocationTest {
    private static void require(boolean value,String message) { if(!value)throw new AssertionError(message); }
    private static Object field(Object object,String name) throws Exception {
        try { return object.getClass().getDeclaredMethod(name).invoke(object); }
        catch(NoSuchMethodException error) { throw new AssertionError("Missing native source coordinates: "+name,error); }
    }
    static void run(Path bridge,Path fixtures,Path output) throws Exception {
        List<String> rows=new ArrayList<>();Result result=null;Path directory=null;int index=0,expected=0,cases=0;
        for(String line:Files.readAllLines(bridge,StandardCharsets.UTF_8)) {
            String[] f=line.split("\t",-1);
            if(f[0].equals("CASE")) {
                if(result!=null)require(index==expected,"Missing native notice comparison");
                require(f.length==3,"Bad location case");
                directory=fixtures.resolve(f[1]);result=evaluate(directory.resolve("main.proj"),directory,Map.of());
                index=0;expected=Integer.parseInt(f[2]);cases++;
                require(result.duplicateImports().size()==expected,f[1]+" native notice count mismatch");
                require(evaluate(directory.resolve("main.proj"),directory,Map.of()).equals(result),"Location state leaked between calls");
                rows.add(f[1]+"\tNATIVE_DEFAULT_CURRENT_AND_PREVIOUS_LOCATIONS\t"+expected);
            } else {
                require(f[0].equals("NOTICE") && f.length==12 && result!=null,"Bad location notice");
                var notice=result.duplicateImports().get(index++);
                require(notice.referenceCode().equals(f[2]) && notice.owner().equals(directory.resolve(f[3])) && notice.importedProject().equals(directory.resolve(f[4])),f[1]+" native notice identity/order mismatch");
                Object current=field(notice,"current"),previous=field(notice,"previous");
                require(current!=null && previous!=null,"Missing actual native location/context");
                for(int i=0;i<4;i++) {
                    String name=List.of("line","column","endLine","endColumn").get(i);
                    require(field(current,name).equals(Integer.valueOf(f[5+i])),f[1]+" native current "+name+" mismatch: "+field(current,name)+" != "+f[5+i]);
                }
                require(field(previous,"owner").equals(directory.resolve(f[9])) && field(previous,"line").equals(Integer.valueOf(f[10])) && field(previous,"column").equals(Integer.valueOf(f[11])),f[1]+" same-profile previous owner/location mismatch");
            }
        }
        require(result!=null && index==expected && cases==10,"Incomplete native location matrix");
        Files.write(output,rows,StandardCharsets.UTF_8);
    }
    public static void main(String[] args) throws Exception {
        run(Path.of(args[0]),Path.of(args[1]),Path.of(args[2]));
        System.out.println("PASS 10 Default-profile location cases; no public ABI qualification");
    }
}
