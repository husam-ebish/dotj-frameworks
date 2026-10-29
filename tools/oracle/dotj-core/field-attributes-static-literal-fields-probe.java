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
class FieldAttributesStaticLiteralFieldsProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String value(Object o,Type self){if(o==null)return null;if(o instanceof Type t)return t==self?"self":"type:"+t.ToString();if(o instanceof MemberTypes v)return Integer.toString(v.get_Value());if(o instanceof GenericParameterAttributes v)return Integer.toString(v.get_Value());if(o instanceof TypeCode v)return Integer.toString(v.get_Value());if(o.getClass().isArray()){StringJoiner j=new StringJoiner(";");for(int i=0;i<java.lang.reflect.Array.getLength(o);i++)j.add(value(java.lang.reflect.Array.get(o,i),self));return j.toString();}return o.toString();}
 static Type resolve(String name){return switch(name){case "null"->null;case "ListS"->Type.GetType("System.Collections.Generic.List`1").MakeGenericType(new Type[]{Type.GetType("System.String")});case "NullableInt"->Type.GetType("System.Nullable`1").MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType("System."+name);};}
 static String decode(String units){if(units.equals("~"))return null;StringBuilder b=new StringBuilder();if(!units.isEmpty())for(String p:units.split(","))b.append((char)Integer.parseInt(p));return b.toString();}
 static String value(Object v){return v==null?"~":v.getClass().getName()+":"+((IConvertible)v).ToString(null);}
 static String fieldText(FieldInfo f){Object first=f.GetValue(null),second=f.GetValue(new Object()),raw=f.GetRawConstantValue();return f.get_Name()+"#"+f.get_DeclaringType().get_FullName()+"#"+f.get_ReflectedType().get_FullName()+"#"+f.get_FieldType().get_FullName()+"#"+f.get_Attributes().get_Value()+"#"+f.ToString()+"#"+value(first)+"#"+value(second)+"#"+value(raw)+"#"+(first==second)+"#"+f.get_IsLiteral();}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;Type type=Type.GetType("System.Reflection.FieldAttributes");try(var reader=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=reader.readLine())!=null){String[] p=line.split("\t",-1);String result=null,error="none",message=null,param=null,after=null;int hResult=0;try{BindingFlags flags=BindingFlags.FromInt32(Integer.parseInt(p[3]));if(p[1].equals("Fields")){StringJoiner text=new StringJoiner(";");for(FieldInfo f:type.GetFields(flags))text.add(fieldText(f));result=text.toString();}else{FieldInfo f=type.GetField(decode(p[2]),flags);if(p[1].equals("Field")){if(f!=null)result=fieldText(f);}else{Object target=switch(p[4]){case "Null"->null;case "Enum"->FieldAttributes.Static;default->new Object();};try{f.SetValue(target,null);}finally{after=value(f.GetValue(null));}}}}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] actual={units(result),error,units(message),Integer.toString(hResult),units(param),units(after)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[5+i]))throw new AssertionError("id="+p[0]+" route="+p[1]+" field="+i+" actual="+actual[i]+" expected="+p[5+i]);groups++;}calls++;}}java.lang.System.out.println("PASS enum static literal fields calls="+calls+" groups="+groups);}
}
