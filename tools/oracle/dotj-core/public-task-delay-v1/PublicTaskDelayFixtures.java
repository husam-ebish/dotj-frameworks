// SPDX-License-Identifier: MIT
// Baseline-only packaged requirement probe. Never loads current product source.
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.net.URI;
import java.nio.file.Path;
import java.util.Arrays;

public final class PublicTaskDelayFixtures {
    private PublicTaskDelayFixtures() { }

    private static void require(boolean condition, String detail) {
        if (!condition) throw new IllegalStateException("INVALID_BASELINE_EVIDENCE " + detail);
    }

    private static void origin(Class<?> type, Path jar) throws Exception {
        URI location = type.getProtectionDomain().getCodeSource().getLocation().toURI();
        require(Path.of(location).toRealPath().equals(jar), "class origin " + type.getName());
        require(type.getModule().isNamed(), "named automatic JAR module " + type.getName());
        require("dotj.core.foundation.v1".equals(type.getModule().getName()), "module identity " + type.getName());
        require(type.getModule().getDescriptor().isAutomatic(), "automatic baseline module");
        java.lang.System.out.println("CLASS_ORIGIN\t" + type.getName() + "\t" + location + "\t" + type.getModule().getName());
    }

    public static void main(String[] args) throws Exception {
        require(args.length == 1, "one exact baseline JAR path required");
        Path jar = Path.of(args[0]).toRealPath();
        Class<?> task = Class.forName("System.Threading.Tasks.Task");
        Class<?> token = Class.forName("System.Threading.CancellationToken");
        Class<?> span = Class.forName("System.TimeSpan");
        // Resolve every dependency, module and argument type before testing absence.
        origin(task, jar); origin(token, jar); origin(span, jar);
        require(Modifier.isPublic(task.getModifiers()) && Modifier.isFinal(task.getModifiers()), "Task boundary");
        String[] names = {"FromCanceled", "Delay", "Delay", "Delay", "Delay"};
        Class<?>[][] parameters = {{token}, {int.class}, {int.class, token}, {span}, {span, token}};
        int missing = 0;
        for (int index = 0; index < names.length; index++) {
            String signature = "public static System.Threading.Tasks.Task " + names[index] + "("
                    + String.join(",", Arrays.stream(parameters[index]).map(Class::getName).toList()) + ")";
            try {
                Method method = task.getDeclaredMethod(names[index], parameters[index]);
                require(Modifier.isPublic(method.getModifiers()) && Modifier.isStatic(method.getModifiers())
                        && method.getReturnType() == task && method.getTypeParameters().length == 0,
                        "wrong existing exact signature " + signature);
                java.lang.System.out.println("PRESENT_REQUIRED_MEMBER\t" + signature);
            } catch (NoSuchMethodException absent) {
                missing++;
                java.lang.System.out.println("MISSING_REQUIRED_MEMBER\t" + signature);
            }
        }
        java.lang.System.out.println("BASELINE_REQUIRED_MEMBERS\t5\tMISSING\t" + missing);
        // Only all five correctly resolved exact missing members constitute proposed API RED.
        java.lang.System.exit(missing == 5 ? 23 : missing == 0 ? 0 : 24);
    }
}
