package org.dotj.internal.build.evaluation;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Compare live evaluation results to captured native values, never generated expected-case output. */
public final class ProjectEvaluationComponentTest {
    private static final List<String> rows = new ArrayList<>();
    private static void record(String row) { rows.add(row); System.out.println("PASS "+row.split("\t",-1)[0]); }
    private static String decode(String value) { return new String(Base64.getDecoder().decode(value), StandardCharsets.UTF_8); }
    private static void require(boolean ok, String why) { if(!ok)throw new AssertionError(why); }
    public static void main(String[] args) throws Exception {
        Path inputs=Path.of(args[0]),fixtureRoot=Path.of(args[1]),out=Path.of(args[2]);Files.createDirectories(out);
        require(ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI().equals(Path.of(args[4]).toUri()), "Evaluator did not load from candidate JAR");
        Module module = ProjectEvaluationComponent.class.getModule();
        require(module.isNamed() && module.getDescriptor().exports().isEmpty() && module.getDescriptor().opens().isEmpty(), "Candidate implementation exposed as public module API");
        require(!java.lang.reflect.Modifier.isPublic(ProjectEvaluationComponent.class.getModifiers()), "Candidate class must remain package-private");
        int nativeCases=0;
        for(String line:Files.readAllLines(inputs,StandardCharsets.UTF_8)) {
            String[] f=line.split("\t",-1);require(f.length==9,"Bad native bridge row");
            String id=f[0];Path relative=Path.of(decode(f[1]));Path project=fixtureRoot.resolve(relative);Map<String,String> globals=new LinkedHashMap<>();
            if(!f[7].isEmpty())globals.put(decode(f[7]),decode(f[8]));
            int exit=Integer.parseInt(f[2]);
            try {
                Result result=evaluate(project,project.getParent(),globals);
                require(exit==0,id+" expected native failure");
                String p=result.property("DotjProbeP"),q=result.property("DotjProbeQ");
                require(p.equals(decode(f[3]))&&q.equals(decode(f[4])),id+" captured native property mismatch: "+p+" / "+q);
                record(id+"\tNATIVE_PROPERTY_MATCH\t"+f[3]+"\t"+f[4]+"\t"+result.evaluatedFiles().size());
            } catch(EvaluationFailure missing) {
                require(exit!=0 && missing.referenceCode.equals(decode(f[5])),id+" unexpected import failure");
                Path expectedMissing=fixtureRoot.resolve(decode(f[6])).toAbsolutePath().normalize();
                require(missing.missingImport.equals(expectedMissing),id+" missing path mismatch");
                record(id+"\tNATIVE_ERROR_CODE_AND_PATH_MATCH\t"+missing.referenceCode+"\t<fixture-root>/"+fixtureRoot.relativize(missing.missingImport));
            }
            nativeCases++;
        }
        require(nativeCases==20,"Expected exact20 captured cases");
        ImportBehaviorTest.run(Path.of(args[5]),Path.of(args[6]),rows);
        Path negatives=out.resolve("negative-inputs");Files.createDirectories(negatives);
        negative(negatives,"sdk","<Project Sdk=\"Dotj.NoSdk\"/>","UNSUPPORTED_ATTRIBUTE",Map.of());
        negative(negatives,"items","<Project><ItemGroup><Compile Include=\"*.java\"/></ItemGroup></Project>","UNSUPPORTED_ELEMENT",Map.of());
        negative(negatives,"property-function","<Project><PropertyGroup><P>$([System.Environment]::GetEnvironmentVariable('HOME'))</P></PropertyGroup></Project>","PROPERTY_FUNCTION",Map.of());
        negative(negatives,"unicode-name","<Project><PropertyGroup><\u03bb>value</\u03bb></PropertyGroup></Project>","ASCII_PROPERTY_NAME",Map.of());
        negative(negatives,"unicode-comparison","<Project><PropertyGroup Condition=\"'\u03bb' == '\u039b'\"><P>value</P></PropertyGroup></Project>","UNICODE_COMPARISON",Map.of());
        negative(negatives,"numeric-comparison","<Project><PropertyGroup Condition=\"'1' == '1.0'\"><P>value</P></PropertyGroup></Project>","CONDITION_COERCION",Map.of());
        negative(negatives,"bool-coercion","<Project><PropertyGroup Condition=\"'true' == 'on'\"><P>value</P></PropertyGroup></Project>","CONDITION_COERCION",Map.of());
        negative(negatives,"or-operator","<Project><PropertyGroup Condition=\"true Or ()\"><P>value</P></PropertyGroup></Project>","CONDITION_PROFILE",Map.of());
        negative(negatives,"glob-import","<Project><Import Project=\"*.props\"/></Project>","IMPORT_PATH_PROFILE",Map.of());
        negative(negatives,"outside-import","<Project><Import Project=\"../outside.props\"/></Project>","IMPORT_BOUNDARY",Map.of());
        negative(negatives,"network-import","<Project><Import Project=\"https://example.invalid/file.props\"/></Project>","IMPORT_PATH_PROFILE",Map.of());
        negative(negatives,"unknown-escape","<Project><PropertyGroup><P>%41</P></PropertyGroup></Project>","ESCAPE_PROFILE",Map.of());
        previousImport(negatives,"duplicate-import","<Project><Import Project=\"one.props\"/><Import Project=\"one.props\"/></Project>","MSB4011",Map.of("one.props","<Project/>"),Path.of(args[6]).resolve("BI06-prior-duplicate"));
        previousImport(negatives,"cycle-import","<Project><Import Project=\"one.props\"/></Project>","MSB4210",Map.of("one.props","<Project><Import Project=\"main.proj\"/></Project>"),Path.of(args[6]).resolve("BI07-prior-cycle"));
        negative(negatives,"doctype","<!DOCTYPE Project [<!ENTITY x SYSTEM 'file:///C:/not-read'>]><Project/>","XML_PROFILE",Map.of());
        negative(negatives,"unknown-target-task","<Project><Target Name=\"T\"><Exec Command=\"never\"/></Target></Project>","TARGET_DECLARATION_PROFILE",Map.of());
        previousDynamicImport(negatives,Path.of(args[7]).resolve("NEG-dynamic-import"));
        negative(negatives,"false-hidden-function","<Project><PropertyGroup Condition=\"false\"><P>$([System.Environment]::GetEnvironmentVariable('HOME'))</P></PropertyGroup></Project>","PROPERTY_FUNCTION",Map.of());
        negative(negatives,"reserved-property","<Project><PropertyGroup><P>$(MSBuildThisFileDirectory)</P></PropertyGroup></Project>","RESERVED_PROPERTY_UNQUALIFIED",Map.of());
        // Removing static condition validation would silently accept these unsupported documents.
        negative(negatives,"skipped-unknown-condition","<Project><PropertyGroup Condition=\"false\"><P Condition=\"true Or ()\">value</P></PropertyGroup></Project>","CONDITION_PROFILE",Map.of());
        negative(negatives,"skipped-unknown-import-condition","<Project><ImportGroup Condition=\"false\"><Import Project=\"missing.props\" Condition=\"true Or ()\"/></ImportGroup></Project>","CONDITION_PROFILE",Map.of());
        negative(negatives,"skipped-unicode-condition","<Project><PropertyGroup Condition=\"false\"><P Condition=\"'λ' == 'Λ'\">value</P></PropertyGroup></Project>","UNICODE_COMPARISON",Map.of());
        negative(negatives,"skipped-function-condition","<Project><PropertyGroup Condition=\"false\"><P Condition=\"'$(P.ToUpper())' == 'X'\">value</P></PropertyGroup></Project>","ASCII_PROPERTY_NAME",Map.of());
        // No file-creation/process/task mechanism exists in evaluator. Confirm both sentinels remain absent.
        require(!Files.exists(fixtureRoot.resolve("BE19-no-target-execution/must-not-exist.txt")),"Copied target sentinel executed");
        require(!Files.exists(Path.of(args[3])),"Original reference sentinel modified");
        Files.write(out.resolve("case-results.tsv"),rows,StandardCharsets.UTF_8);
        System.out.println("PASS 20 original native cases + 20 unchanged refusals + one native import-path transition + prior duplicate/cycle now native-supported + 9 import-matrix cases; 0 product acceptance");
    }
    private static void previousDynamicImport(Path root,Path paired) throws Exception {
        Path directory=root.resolve("dynamic-import");Files.createDirectories(directory);
        for(String name:List.of("main.proj","one.props"))Files.copy(paired.resolve(name),directory.resolve(name));
        Result result=evaluate(directory.resolve("main.proj"),directory,Map.of());
        require(result.property("P").equals("one.props")&&result.property("Q").isEmpty()&&result.imports().size()==1&&result.duplicateImports().isEmpty(),"Exact legacy import path transition differs from native");
        require(result.imports().getFirst().owner().equals(directory.resolve("main.proj"))&&result.imports().getFirst().target().equals(directory.resolve("one.props")),"Legacy import identity changed");
        record("NEG-dynamic-import\tNATIVE_IMPORT_PATH_MATCH\tSUCCESS");
    }
    private static void previousImport(Path root,String id,String xml,String code,Map<String,String> extras,Path paired) throws Exception {
        Path directory=root.resolve(id);Files.createDirectories(directory);Path file=directory.resolve("main.proj");Files.writeString(file,xml);
        require(Files.readString(paired.resolve("main.proj")).equals(xml),"Prior import project bytes differ from native input");
        for(var entry:extras.entrySet()) {
            require(Files.readString(paired.resolve(entry.getKey())).equals(entry.getValue()),"Prior import bytes differ from native input");
            Files.writeString(directory.resolve(entry.getKey()),entry.getValue());
        }
        Result result=evaluate(file,directory,Map.of());
        require(result.evaluatedFiles().equals(List.of(file,directory.resolve("one.props"))) && result.property("P").isEmpty() && result.property("Q").isEmpty(),"Prior import native once-only mismatch");
        boolean cycle=code.equals("MSB4210");
        require(result.duplicateImports().size()==1 && result.duplicateImports().getFirst().referenceCode().equals(code)
            && result.duplicateImports().getFirst().owner().equals(cycle ? directory.resolve("one.props") : file)
            && result.duplicateImports().getFirst().importedProject().equals(cycle ? file : directory.resolve("one.props")),"Prior import native notice mismatch");
        record("NEG-"+id+"\tNOW_NATIVE_ONCE_ONLY_MATCH\t"+code);
    }
    private static void negative(Path root,String id,String xml,String expected,Map<String,String> extras) throws Exception {
        Path directory=root.resolve(id);Files.createDirectories(directory);Path file=directory.resolve("main.proj");Files.writeString(file,xml);
        for(var entry:extras.entrySet())Files.writeString(directory.resolve(entry.getKey()),entry.getValue());
        try {evaluate(file,directory,Map.of());throw new AssertionError(id+" unsupported input accepted");}
        catch(ProfileRejected error){require(error.code.equals(expected),id+" wrong rejection "+error.code);record("NEG-"+id+"\tPROFILE_REJECT\t"+error.code);}
    }
}
