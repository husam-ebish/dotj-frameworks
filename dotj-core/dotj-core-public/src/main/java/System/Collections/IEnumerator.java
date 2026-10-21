// SPDX-License-Identifier: MIT

package System.Collections;

/** Selected non-generic cursor contract for serialization enumeration. */
public interface IEnumerator {
    Object get_Current();

    boolean MoveNext();

    void Reset();
}
