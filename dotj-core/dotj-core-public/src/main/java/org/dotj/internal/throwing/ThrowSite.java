// SPDX-License-Identifier: MIT

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
        StackTraceElement caller = targetFrame(exception);
        if (caller == null) {
            return null;
        }
        return "   at " + caller.getClassName() + "." + caller.getMethodName();
    }

    public static StackTraceElement targetFrame(Exception exception) {
        StackTraceElement[] frames = exception.getStackTrace();
        return frames.length < 2 || !MARKER.equals(frames[0]) ? null : frames[1];
    }
}
