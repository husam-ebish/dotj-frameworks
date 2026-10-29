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
class PrimitivePrivateFieldMetadataReadsProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String value(Object o,Type self){if(o==null)return null;if(o instanceof Type t)return t==self?"self":"type:"+t.ToString();if(o instanceof MemberTypes v)return Integer.toString(v.get_Value());if(o instanceof GenericParameterAttributes v)return Integer.toString(v.get_Value());if(o instanceof TypeCode v)return Integer.toString(v.get_Value());if(o.getClass().isArray()){StringJoiner j=new StringJoiner(";");for(int i=0;i<java.lang.reflect.Array.getLength(o);i++)j.add(value(java.lang.reflect.Array.get(o,i),self));return j.toString();}return o.toString();}
 static Type resolve(String name){return switch(name){case "null"->null;case "ListS"->Type.GetType("System.Collections.Generic.List`1").MakeGenericType(new Type[]{Type.GetType("System.String")});case "NullableInt"->Type.GetType("System.Nullable`1").MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType("System."+name);};}
 static String decode(String units){if(units.equals("~"))return null;StringBuilder b=new StringBuilder();if(!units.isEmpty())for(String p:units.split(","))b.append((char)Integer.parseInt(p));return b.toString();}
 static String metadata(FieldInfo f){List<String> parts=new ArrayList<>();parts.add(f.get_Name());parts.add(f.get_DeclaringType().get_FullName());parts.add(f.get_ReflectedType().get_FullName());parts.add(f.get_FieldType().get_FullName());parts.add(Integer.toString(f.get_Attributes().get_Value()));parts.add(f.ToString());boolean[] values={f.get_IsPublic(),f.get_IsPrivate(),f.get_IsFamily(),f.get_IsAssembly(),f.get_IsFamilyAndAssembly(),f.get_IsFamilyOrAssembly(),f.get_IsStatic(),f.get_IsInitOnly(),f.get_IsLiteral(),f.get_IsSpecialName(),f.get_IsNotSerialized(),f.get_IsPinvokeImpl(),f.get_IsCollectible()};for(boolean v:values)parts.add(Boolean.toString(v));return String.join("#",parts);}
 static Object ownerValue(String type,String text){return switch(type){case "Boolean"->Boolean.parseBoolean(text);case "Char"->text.charAt(0);case "Int16"->Short.parseShort(text);case "Int64"->Long.parseLong(text);case "UInt64"->new java.math.BigInteger(text);case "Single"->text.equals("NaN")?Float.intBitsToFloat(0xffc00000):Float.parseFloat(text);case "Double"->text.equals("NaN")?Double.longBitsToDouble(0xfff8000000000000L):Double.parseDouble(text);default->throw new AssertionError(type);};}
 static String scalar(Object value,String owner){if(value instanceof Boolean v)return "System.Boolean:"+v;if(value instanceof Character v)return "System.Char:"+(int)v;if(value instanceof Float v)return "System.Single:"+String.format(java.util.Locale.ROOT,"%08X",Float.floatToRawIntBits(v));if(value instanceof Double v)return "System.Double:"+String.format(java.util.Locale.ROOT,"%016X",Double.doubleToRawLongBits(v));return "System."+owner+":"+value;}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;try(var reader=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=reader.readLine())!=null){String[] p=line.split("\t",-1);String result=null,error="none",message=null,param=null;int hResult=0;try{Type type=resolve(p[2]);switch(p[1]){case "Fields"->{StringJoiner text=new StringJoiner(";");for(FieldInfo f:type.GetFields(BindingFlags.FromInt32(Integer.parseInt(p[3]))))text.add(metadata(f));result=text.toString();}case "Field"->{FieldInfo f=type.GetField("m_value",BindingFlags.FromInt32(Integer.parseInt(p[3])));if(f!=null)result=metadata(f);}case "Read"->{FieldInfo f=type.GetField("m_value",BindingFlags.NonPublic.or(BindingFlags.Instance));Object target=switch(p[5]){case "Null"->null;case "Object"->new Object();case "Owner"->ownerValue(p[2],decode(p[4]));case "Int32"->new Int32(17);case "String"->"text";case "Enum"->MemberTypes.Method;case "RuntimeType"->Type.GetType("System.Int32");default->throw new AssertionError(p[5]);};Object value=p[6].equals("Raw")?f.GetRawConstantValue():f.GetValue(target);result=scalar(value,p[2]);}default->throw new AssertionError(p[1]);}}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] actual={units(result),error,units(message),Integer.toString(hResult),units(param)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[7+i]))throw new AssertionError("id="+p[0]+" route="+p[1]+" type="+p[2]+" field="+i+" actual="+actual[i]+" expected="+p[7+i]);groups++;}calls++;}}java.lang.System.out.println("PASS integer private field reads calls="+calls+" groups="+groups);}
}
