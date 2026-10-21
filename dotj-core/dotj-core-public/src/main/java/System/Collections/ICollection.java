// SPDX-License-Identifier: MIT

package System.Collections;

/** Selected non-generic CLR collection contract. */
public interface ICollection extends IEnumerable {
    int get_Count();

    boolean get_IsSynchronized();

    Object get_SyncRoot();

    void CopyTo(Object array, int index);
}
