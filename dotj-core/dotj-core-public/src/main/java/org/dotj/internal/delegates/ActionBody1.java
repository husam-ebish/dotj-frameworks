// SPDX-License-Identifier: MIT

package org.dotj.internal.delegates;

/** Java lambda target for System.Action_1; callers pass a lambda and never name this type. */
@FunctionalInterface
public interface ActionBody1<T> {
    void Invoke(T arg);
}
