// SPDX-License-Identifier: MIT

package System.Collections;

/** Selected non-generic CLR dictionary enumerator contract. */
public interface IDictionaryEnumerator extends IEnumerator {
    DictionaryEntry get_Entry();

    Object get_Key();

    Object get_Value();
}
