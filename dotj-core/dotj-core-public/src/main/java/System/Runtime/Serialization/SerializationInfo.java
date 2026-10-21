// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.ArgumentNullException;
import System.Type;

/** Bounded type identity for serialization method signatures. */
public class SerializationInfo {
    private final Type objectType;
    private final IFormatterConverter converter;

    public SerializationInfo(Type type, IFormatterConverter converter) {
        this(type, converter, false);
    }

    public SerializationInfo(Type type, IFormatterConverter converter,
            boolean requireSameTokenInPartialTrust) {
        if (type == null) {
            throw new ArgumentNullException("type");
        }
        if (converter == null) {
            throw new ArgumentNullException("converter");
        }
        this.objectType = type;
        this.converter = converter;
    }

    public Type get_ObjectType() {
        return this.objectType;
    }

    public String get_FullTypeName() {
        return this.objectType.get_FullName();
    }

    public int get_MemberCount() {
        return 0;
    }
}
