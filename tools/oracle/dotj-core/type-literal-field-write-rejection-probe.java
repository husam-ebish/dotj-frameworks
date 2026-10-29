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
class TypeLiteralFieldWriteRejectionProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String value(Object o,Type self){if(o==null)return null;if(o instanceof Type t)return t==self?"self":"type:"+t.ToString();if(o instanceof MemberTypes v)return Integer.toString(v.get_Value());if(o instanceof GenericParameterAttributes v)return Integer.toString(v.get_Value());if(o instanceof TypeCode v)return Integer.toString(v.get_Value());if(o.getClass().isArray()){StringJoiner j=new StringJoiner(";");for(int i=0;i<java.lang.reflect.Array.getLength(o);i++)j.add(value(java.lang.reflect.Array.get(o,i),self));return j.toString();}return o.toString();}
 static Type resolve(String name){return switch(name){case "null"->null;case "ListS"->Type.GetType("System.Collections.Generic.List`1").MakeGenericType(new Type[]{Type.GetType("System.String")});case "NullableInt"->Type.GetType("System.Nullable`1").MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType("System."+name);};}
 static Object input(String kind){return switch(kind){case "Null"->null;case "Object"->new Object();case "Int32"->new Int32(17);case "Byte"->new Byte(17);case "SByte"->new SByte(-17);case "UInt16"->new UInt16(17);case "UInt32"->new UInt32(17);case "Int64"->17L;case "Double"->17.5;case "String"->"value";case "Enum"->MemberTypes.Method;case "DBNull"->DBNull.Value;case "Type"->Type.GetType("System.Int32");default->throw new AssertionError(kind);};}
 static String decode(String units){if(units.equals("~"))return null;StringBuilder b=new StringBuilder();if(!units.isEmpty())for(String p:units.split(","))b.append((char)Integer.parseInt(p));return b.toString();}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;try(var reader=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=reader.readLine())!=null){String[] p=line.split("\t",-1);String result=null,error="none",message=null,param=null,after=null;int hResult=0;try{if(p[1].equals("Write")){FieldInfo field=resolve(p[2]).GetField(p[3]);try{field.SetValue(input(p[4]),input(p[5]));}finally{Object value=field.GetRawConstantValue();after=value.getClass().getName()+":"+((IConvertible)value).ToString(null);}}else{Exception inner=Boolean.parseBoolean(p[8])?new Exception("inner"):null;String text=decode(p[7]);Exception e;if(p[2].equals("MemberAccessException")){e=switch(p[6]){case "Default"->new MemberAccessException();case "Text"->new MemberAccessException(text);default->new MemberAccessException(text,inner);};}else{e=switch(p[6]){case "Default"->new FieldAccessException();case "Text"->new FieldAccessException(text);default->new FieldAccessException(text,inner);};}result=e.getClass().getName()+"|"+e.get_Message()+"|"+e.get_HResult()+"|"+(e.get_InnerException()==inner)+"|"+resolve(p[2]).get_BaseType().get_FullName()+"|"+e.ToString();}}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] actual={units(result),error,units(message),Integer.toString(hResult),units(param),units(after)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[9+i]))throw new AssertionError("id="+p[0]+" route="+p[1]+" type="+p[2]+" field="+i+" actual="+actual[i]+" expected="+p[9+i]);groups++;}calls++;}}java.lang.System.out.println("PASS literal field write rejection calls="+calls+" groups="+groups);}
}
