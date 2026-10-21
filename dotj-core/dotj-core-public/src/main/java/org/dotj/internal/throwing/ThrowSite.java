package org.dotj.internal.throwing;

import System.Exception;

/** Bounded hook for a future .j throw lowering; preserves exception identity. */
public final class ThrowSite {
    private static final StackTraceElement MARKER =
            new StackTraceElement("org.dotj.internal.throwing.ThrowSite", "captured", null, -1);

    private ThrowSite() {
    }

    public static <T extends Exception> T capture(T exception) {
        if (exception == null) {
            throw new NullPointerException("exception");
        }
        StackTraceElement caller = StackWalker.getInstance().walk(frames -> frames.skip(1)
                .findFirst().orElseThrow().toStackTraceElement());
        exception.setStackTrace(new StackTraceElement[] {MARKER, caller});
        return exception;
    }

    public static String stackText(Exception exception) {
        StackTraceElement[] frames = exception.getStackTrace();
        if (frames.length < 2 || !MARKER.equals(frames[0])) {
            return null;
        }
        StackTraceElement caller = frames[1];
        return "   at " + caller.getClassName() + "." + caller.getMethodName();
    }
}
