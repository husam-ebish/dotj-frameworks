// SPDX-License-Identifier: MIT

package System.Reflection;

import System.Type;

/** Bounded method reflection descriptor. */
public abstract class MethodInfo extends MethodBase {
    protected MethodInfo() {
    }

    public abstract Type get_ReturnType();
}
