import System.ApplicationException;
import System.Reflection.TargetException;
import System.MemberAccessException;
import System.FieldAccessException;
import System.Byte;
import System.SByte;
import System.UInt16;
import System.UInt32;
import System.DBNull;
import System.Reflection.FieldInfo;
import System.Globalization.NumberFormatInfo;
import System.InvalidOperationException;
import System.IFormatProvider;
import System.Decimal;
import System.Int32;
import System.Reflection.FieldAttributes;
import System.Reflection.FieldInfo;
import System.IConvertible;
import System.Reflection.MemberInfo;
import System.Reflection.MemberTypes;
import System.Reflection.MemberFilter;
import System.Reflection.TypeFilter;
import System.Reflection.MethodInfo;
import System.Reflection.ParameterInfo;
import System.Reflection.BindingFlags;
import System.Type;
import System.Exception;
import System.ArgumentException;
import System.Reflection.BindingFlags;
import System.Reflection.MemberTypes;
import System.Reflection.GenericParameterAttributes;
import System.TypeCode;
import java.nio.file.*;
import java.util.*;
class PrimitiveStaticFieldValueIdentityProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String value(Object o,Type self){if(o==null)return null;if(o instanceof Type t)return t==self?"self":"type:"+t.ToString();if(o instanceof MemberTypes v)return Integer.toString(v.get_Value());if(o instanceof GenericParameterAttributes v)return Integer.toString(v.get_Value());if(o instanceof TypeCode v)return Integer.toString(v.get_Value());if(o.getClass().isArray()){StringJoiner j=new StringJoiner(";");for(int i=0;i<java.lang.reflect.Array.getLength(o);i++)j.add(value(java.lang.reflect.Array.get(o,i),self));return j.toString();}return o.toString();}
 static Type resolve(String name){return switch(name){case "null"->null;case "ListS"->Type.GetType("System.Collections.Generic.List`1").MakeGenericType(new Type[]{Type.GetType("System.String")});case "NullableInt"->Type.GetType("System.Nullable`1").MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType("System."+name);};}
 static String decode(String units){if(units.equals("~"))return null;StringBuilder b=new StringBuilder();if(!units.isEmpty())for(String p:units.split(","))b.append((char)Integer.parseInt(p));return b.toString();}
 static String metadata(FieldInfo f){List<String> parts=new ArrayList<>();parts.add(f.get_Name());parts.add(f.get_DeclaringType().get_FullName());parts.add(f.get_ReflectedType().get_FullName());parts.add(f.get_FieldType().get_FullName());parts.add(Integer.toString(f.get_Attributes().get_Value()));parts.add(f.ToString());boolean[] values={f.get_IsPublic(),f.get_IsPrivate(),f.get_IsFamily(),f.get_IsAssembly(),f.get_IsFamilyAndAssembly(),f.get_IsFamilyOrAssembly(),f.get_IsStatic(),f.get_IsInitOnly(),f.get_IsLiteral(),f.get_IsSpecialName(),f.get_IsNotSerialized(),f.get_IsPinvokeImpl(),f.get_IsCollectible()};for(boolean v:values)parts.add(Boolean.toString(v));return String.join("#",parts);}
 static Object ownerValue(String type,String text){return switch(type){case "Boolean"->Boolean.parseBoolean(text);case "Char"->text.charAt(0);case "Int16"->Short.parseShort(text);case "Int64"->Long.parseLong(text);case "UInt64"->new java.math.BigInteger(text);case "Single"->text.equals("NaN")?Float.intBitsToFloat(0xffc00000):Float.parseFloat(text);case "Double"->text.equals("NaN")?Double.longBitsToDouble(0xfff8000000000000L):Double.parseDouble(text);default->throw new AssertionError(type);};}
 static String scalar(Object value,String owner){if(value instanceof String v)return "System.String:"+v;if(value instanceof Boolean v)return "System.Boolean:"+v;if(value instanceof Character v)return "System.Char:"+(int)v;if(value instanceof Float v)return "System.Single:"+String.format(java.util.Locale.ROOT,"%08X",Float.floatToRawIntBits(v));if(value instanceof Double v)return "System.Double:"+String.format(java.util.Locale.ROOT,"%016X",Double.doubleToRawLongBits(v));return "System."+owner+":"+value;}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);String value=null,error="none",message=null,param=null;int hResult=0;try{FieldInfo field=resolve(p[1]).GetField(p[2]);Object target=switch(p[3]){case "Null"->null;case "Object"->new Object();case "String"->"target";case "RuntimeType"->Type.GetType("System.Int32");default->throw new AssertionError(p[3]);};Object first=null,second=null;switch(p[4]){case "ValueValue"->{first=field.GetValue(target);second=field.GetValue(target);}case "RawRaw"->{first=field.GetRawConstantValue();second=field.GetRawConstantValue();}case "ValueRaw"->{first=field.GetValue(target);second=field.GetRawConstantValue();}default->throw new AssertionError(p[4]);}value=scalar(first,p[1])+"|"+scalar(second,p[1])+"|"+(first==second);}catch(Exception e){error=e.getClass().getName();message=e.get_Message();hResult=e.get_HResult();if(e instanceof ArgumentException a)param=a.get_ParamName();}String[] actual={units(value),error,units(message),Integer.toString(hResult),units(param)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[5+i]))throw new AssertionError("id="+p[0]+" owner="+p[1]+" field="+p[2]+" route="+p[4]+" index="+i+" actual="+actual[i]+" expected="+p[5+i]);groups++;}calls++;}java.lang.System.out.println("PASS primitive static value identity calls="+calls+" groups="+groups);}
}
