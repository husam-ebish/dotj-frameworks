// SPDX-License-Identifier: MIT

package System.Reflection;

/** Java callback projection for the selected MemberFilter invocation contract. */
@FunctionalInterface
public interface MemberFilter {
    boolean Invoke(MemberInfo member, Object filterCriteria);
}
