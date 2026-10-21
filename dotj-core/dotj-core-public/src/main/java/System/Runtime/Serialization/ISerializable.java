// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

/** Bounded serialization contract signature. */
public interface ISerializable {
    void GetObjectData(SerializationInfo info, StreamingContext context);
}
