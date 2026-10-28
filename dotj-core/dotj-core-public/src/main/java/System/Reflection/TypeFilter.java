// SPDX-License-Identifier: MIT

package System.Reflection;

import System.Type;

/** Java callback projection for the selected TypeFilter invocation contract. */
@FunctionalInterface
public interface TypeFilter {
    boolean Invoke(Type type, Object filterCriteria);
}
