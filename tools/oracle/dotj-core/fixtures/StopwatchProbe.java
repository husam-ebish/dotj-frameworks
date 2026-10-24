import System.Diagnostics.Stopwatch;

public class StopwatchProbe {
    private static final class Derived extends Stopwatch {
    }

    public static void main(String[] args) throws java.lang.Exception {
        Stopwatch watch = null;
        for (String operation : args) {
            switch (operation) {
                case "new": watch = new Stopwatch(); break;
                case "start": watch.Start(); break;
                case "stop": watch.Stop(); break;
                case "reset": watch.Reset(); break;
                case "restart": watch.Restart(); break;
                case "startNew": watch = Stopwatch.StartNew(); break;
                default:
                    if (!operation.startsWith("sleep:")) { throw new AssertionError("Unknown operation"); }
                    Thread.sleep(Long.parseLong(operation.substring(6)));
            }
            long before = watch.get_ElapsedTicks();
            long span = watch.get_Elapsed().get_Ticks();
            long milliseconds = watch.get_ElapsedMilliseconds();
            String text = watch.ToString();
            String javaText = watch.toString();
            long after = watch.get_ElapsedTicks();
            java.lang.System.out.println("{\"record\":\"state\",\"operation\":\""+operation+"\",\"running\":"+watch.get_IsRunning()
                +",\"before\":"+before+",\"after\":"+after+",\"spanTicks\":"+span+",\"milliseconds\":"+milliseconds
                +",\"text\":\""+text+"\",\"javaText\":\""+javaText+"\"}");
        }
        long previous = Stopwatch.GetTimestamp();
        boolean nondecreasing = true;
        boolean advanced = false;
        for (int index = 0; index < 10000; index++) {
            long next = Stopwatch.GetTimestamp();
            nondecreasing &= next >= previous;
            advanced |= next > previous;
            previous = next;
        }
        long start = Stopwatch.GetTimestamp();
        long oneArgumentTicks = Stopwatch.GetElapsedTime(start).get_Ticks();
        long end = Stopwatch.GetTimestamp();
        Derived derived = new Derived(); derived.Start(); derived.Reset();
        java.lang.System.out.println("{\"record\":\"counter\",\"frequency\":"+Stopwatch.Frequency+",\"highResolution\":"+Stopwatch.IsHighResolution
            +",\"nondecreasing\":"+nondecreasing+",\"advanced\":"+advanced+",\"start\":"+start+",\"end\":"+end
            +",\"oneArgumentTicks\":"+oneArgumentTicks+",\"derivedReset\":"+(!derived.get_IsRunning() && derived.get_ElapsedTicks()==0L)+"}");
    }
}
