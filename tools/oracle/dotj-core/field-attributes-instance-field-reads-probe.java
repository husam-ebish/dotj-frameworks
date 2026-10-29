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
class FieldAttributesInstanceFieldReadsProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String value(Object o,Type self){if(o==null)return null;if(o instanceof Type t)return t==self?"self":"type:"+t.ToString();if(o instanceof MemberTypes v)return Integer.toString(v.get_Value());if(o instanceof GenericParameterAttributes v)return Integer.toString(v.get_Value());if(o instanceof TypeCode v)return Integer.toString(v.get_Value());if(o.getClass().isArray()){StringJoiner j=new StringJoiner(";");for(int i=0;i<java.lang.reflect.Array.getLength(o);i++)j.add(value(java.lang.reflect.Array.get(o,i),self));return j.toString();}return o.toString();}
 static Type resolve(String name){return switch(name){case "null"->null;case "ListS"->Type.GetType("System.Collections.Generic.List`1").MakeGenericType(new Type[]{Type.GetType("System.String")});case "NullableInt"->Type.GetType("System.Nullable`1").MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType("System."+name);};}
 static String decode(String units){if(units.equals("~"))return null;StringBuilder b=new StringBuilder();if(!units.isEmpty())for(String p:units.split(","))b.append((char)Integer.parseInt(p));return b.toString();}
 static String metadata(FieldInfo f){List<String> parts=new ArrayList<>();parts.add(f.get_Name());parts.add(f.get_DeclaringType().get_FullName());parts.add(f.get_ReflectedType().get_FullName());parts.add(f.get_FieldType().get_FullName());parts.add(Integer.toString(f.get_Attributes().get_Value()));parts.add(f.ToString());boolean[] values={f.get_IsPublic(),f.get_IsPrivate(),f.get_IsFamily(),f.get_IsAssembly(),f.get_IsFamilyAndAssembly(),f.get_IsFamilyOrAssembly(),f.get_IsStatic(),f.get_IsInitOnly(),f.get_IsLiteral(),f.get_IsSpecialName(),f.get_IsNotSerialized(),f.get_IsPinvokeImpl(),f.get_IsCollectible()};for(boolean v:values)parts.add(Boolean.toString(v));return String.join("#",parts);}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;Type type=Type.GetType("System.Reflection.FieldAttributes");try(var reader=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=reader.readLine())!=null){String[] p=line.split("\t",-1);String result=null,error="none",message=null,param=null;int hResult=0;try{switch(p[1]){case "Fields"->{StringJoiner text=new StringJoiner(";");for(FieldInfo f:type.GetFields(BindingFlags.FromInt32(Integer.parseInt(p[2]))))text.add(metadata(f));result=text.toString();}case "Field"->{FieldInfo f=type.GetField("value__",BindingFlags.FromInt32(Integer.parseInt(p[2])));if(f!=null)result=metadata(f);}case "Read"->{FieldInfo f=type.GetField("value__");Object target=switch(p[3]){case "Null"->null;case "Object"->new Object();case "Int32"->new Int32(17);case "String"->"text";case "OtherEnum"->MemberTypes.Method;case "Enum"->FieldAttributes.FromInt32(Integer.parseInt(p[4]));default->throw new AssertionError(p[3]);};Object value=p[5].equals("Raw")?f.GetRawConstantValue():f.GetValue(target);result=value.getClass().getName()+":"+((IConvertible)value).ToString(null);}case "Ctor"->{Exception inner=Boolean.parseBoolean(p[9])?new Exception("inner"):null;String text=decode(p[8]);Exception e;if(p[6].equals("ApplicationException"))e=switch(p[7]){case "Default"->new ApplicationException();case "Text"->new ApplicationException(text);default->new ApplicationException(text,inner);};else e=switch(p[7]){case "Default"->new TargetException();case "Text"->new TargetException(text);default->new TargetException(text,inner);};result=e.getClass().getName()+"|"+e.get_Message()+"|"+e.get_HResult()+"|"+resolve(p[6]).get_BaseType().get_FullName()+"|"+(e.get_InnerException()==inner)+"|"+e.ToString();}default->throw new AssertionError(p[1]);}}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] actual={units(result),error,units(message),Integer.toString(hResult),units(param)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[10+i]))throw new AssertionError("id="+p[0]+" route="+p[1]+" field="+i+" actual="+actual[i]+" expected="+p[10+i]);groups++;}calls++;}}java.lang.System.out.println("PASS enum instance field reads calls="+calls+" groups="+groups);}
}
