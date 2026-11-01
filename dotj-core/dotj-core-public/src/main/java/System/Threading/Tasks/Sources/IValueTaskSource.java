// SPDX-License-Identifier: MIT

package System.Threading.Tasks.Sources;

import System.Action_1;

/** Selected System.Threading.Tasks.Sources.IValueTaskSource contract. */
public interface IValueTaskSource {
    ValueTaskSourceStatus GetStatus(short token);

    void OnCompleted(Action_1<Object> continuation, Object state, short token, ValueTaskSourceOnCompletedFlags flags);

    void GetResult(short token);
}
