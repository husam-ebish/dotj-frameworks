// SPDX-License-Identifier: MIT

package org.dotj.internal.async;

import System.Action;

/** Per-instance, read-only await access. Java representation infrastructure, not native API. */
public abstract class TaskBridge {
    protected TaskBridge() { }

    public abstract boolean isCompleted();
    public abstract void awaitResult();
    public abstract void register(Action continuation);
}
