// SPDX-License-Identifier: MIT

package System.Reflection;

import System.Type;

/** Selected parameter metadata for bounded method descriptors. */
public class ParameterInfo {
    private final String name;
    private final Type parameterType;
    private final int position;

    protected ParameterInfo(String name, Type parameterType, int position) {
        this.name = name;
        this.parameterType = parameterType;
        this.position = position;
    }

    public String get_Name() {
        return this.name;
    }

    public Type get_ParameterType() {
        return this.parameterType;
    }

    public int get_Position() {
        return this.position;
    }
}
