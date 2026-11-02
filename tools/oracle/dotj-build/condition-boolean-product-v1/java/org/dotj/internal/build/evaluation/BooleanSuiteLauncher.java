package org.dotj.internal.build.evaluation;
import java.nio.file.Path;
import java.util.Arrays;
import java.lang.reflect.*;
final class BooleanSuiteLauncher {
    static void identity(Path jar) throws Exception {
        Class<?> type=ProjectEvaluationComponent.class;Module module=type.getModule();
        if(!type.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri())||!module.isNamed()||!module.getName().equals("org.dotj.build.evaluation.candidate")||!module.getDescriptor().exports().isEmpty()||!module.getDescriptor().opens().isEmpty()||Modifier.isPublic(type.getModifiers()))throw new AssertionError("JAR_MODULE_IDENTITY");
        if(!module.getDescriptor().requires().stream().map(x->x.name()).collect(java.util.stream.Collectors.toSet()).equals(java.util.Set.of("java.base","java.xml")))throw new AssertionError("RUNTIME_DEPENDENCIES");
        System.out.println("BOOLEAN_PRODUCT_IDENTITY jar="+jar+" module="+module.getName()+" exports=0 opens=0");
    }
    public static void main(String[] args) throws Exception {
        identity(Path.of(args[0]));
        try {Class.forName("org.dotj.internal.build.evaluation."+args[1]).getMethod("main",String[].class).invoke(null,(Object)Arrays.copyOfRange(args,2,args.length));}
        catch(InvocationTargetException e){if(e.getCause() instanceof Exception x)throw x;throw (Error)e.getCause();}
    }
}
