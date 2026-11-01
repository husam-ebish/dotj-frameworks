// SPDX-License-Identifier: MIT

package System.Runtime.CompilerServices;

import System.Action;

/** Selected System.Runtime.CompilerServices.INotifyCompletion contract. */
public interface INotifyCompletion {
    void OnCompleted(Action continuation);
}
