// SPDX-License-Identifier: MIT

package org.dotj.internal.delegates;

/** Java lambda target for System.Action; callers pass a lambda and never name this type. */
@FunctionalInterface
public interface ActionBody {
    void Invoke();
}
