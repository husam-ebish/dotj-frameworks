// SPDX-License-Identifier: MIT

package System;

import System.Threading.Tasks.ValueTask;

/** A resource with an explicit .NET-style asynchronous disposal operation. */
public interface IAsyncDisposable {
    ValueTask DisposeAsync();
}
