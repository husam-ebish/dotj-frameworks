// SPDX-License-Identifier: MIT

package System.Runtime.CompilerServices;

import System.Action;

/** Selected System.Runtime.CompilerServices.ICriticalNotifyCompletion contract. */
public interface ICriticalNotifyCompletion extends INotifyCompletion {
    void UnsafeOnCompleted(Action continuation);
}
