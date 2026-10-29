import System.DateTime;
import System.Globalization.NumberFormatInfo;
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
class IntegerPrivateFieldReadTargetDomainsProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String value(Object o,Type self){if(o==null)return null;if(o instanceof Type t)return t==self?"self":"type:"+t.ToString();if(o instanceof MemberTypes v)return Integer.toString(v.get_Value());if(o instanceof GenericParameterAttributes v)return Integer.toString(v.get_Value());if(o instanceof TypeCode v)return Integer.toString(v.get_Value());if(o.getClass().isArray()){StringJoiner j=new StringJoiner(";");for(int i=0;i<java.lang.reflect.Array.getLength(o);i++)j.add(value(java.lang.reflect.Array.get(o,i),self));return j.toString();}return o.toString();}
 static Type resolve(String name){return switch(name){case "null"->null;case "ListS"->Type.GetType("System.Collections.Generic.List`1").MakeGenericType(new Type[]{Type.GetType("System.String")});case "NullableInt"->Type.GetType("System.Nullable`1").MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType("System."+name);};}
 static Object target(String kind,int value){return switch(kind){case "Null"->null;case "Object"->new Object();case "Boolean"->true;case "Char"->'A';case "SByte"->new SByte(-17);case "Byte"->new Byte(17);case "Int16"->(short)-17;case "UInt16"->new UInt16(17);case "RawInt32"->Integer.valueOf(17);case "RawByte"->java.lang.Byte.valueOf((byte)value);case "Int32"->new Int32(-17);case "UInt32"->new UInt32(17);case "Int64"->-17L;case "UInt64"->java.math.BigInteger.valueOf(17);case "Single"->17.5f;case "Double"->17.5;case "Decimal"->new Decimal(175,0,0,false,1);case "DateTime"->DateTime.MinValue;case "String"->"text";case "DBNull"->DBNull.Value;case "RuntimeType"->Type.GetType("System.Int32");case "Nfi"->NumberFormatInfo.get_InvariantInfo();case "OtherEnum"->MemberTypes.Method;case "Int32Array"->new int[]{1,2};case "CharArray"->new char[]{'a','b'};case "ByteArray"->new Byte[]{new Byte(1),new Byte(2)};case "ObjectArray"->new Object[]{1,2};case "Enum"->FieldAttributes.FromInt32(value);default->throw new AssertionError(kind);};}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;try(var reader=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=reader.readLine())!=null){String[] p=line.split("\t",-1);String result=null,error="none",message=null,param=null;int hResult=0;try{FieldInfo field=resolve(p[1]).GetField("m_value",BindingFlags.NonPublic.or(BindingFlags.Instance));Object value=field.GetValue(target(p[2],Integer.parseInt(p[3])));result=value.getClass().getName()+":"+((IConvertible)value).ToString(null);}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] actual={units(result),error,units(message),Integer.toString(hResult),units(param)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[4+i]))throw new AssertionError("id="+p[0]+" type="+p[1]+" target="+p[2]+" field="+i+" actual="+actual[i]+" expected="+p[4+i]);groups++;}calls++;}}java.lang.System.out.println("PASS enum read target domains calls="+calls+" groups="+groups);}
}
