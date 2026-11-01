// SPDX-License-Identifier: MIT

package org.dotj.internal.async;

import System.Action;
import System.Threading.Tasks.ValueTask;
import System.Threading.Tasks.Sources.ValueTaskSourceOnCompletedFlags;

/** Lets the awaiter types use ValueTask state without adding public members that .NET does not have. */
public final class ValueTaskBridge {
    /** Implemented once, inside ValueTask, where its private state is visible. */
    public interface Access {
        void register(ValueTask task, Action continuation, ValueTaskSourceOnCompletedFlags flags);

        void awaitResult(ValueTask task);
    }

    private static volatile Access access;

    private ValueTaskBridge() {
    }

    public static void install(Access installed) {
        if (access != null) {
            throw new IllegalStateException("ValueTask access is already installed");
        }
        access = installed;
    }

    public static void register(ValueTask task, Action continuation, ValueTaskSourceOnCompletedFlags flags) {
        access.register(task, continuation, flags);
    }

    public static void awaitResult(ValueTask task) {
        access.awaitResult(task);
    }
}
