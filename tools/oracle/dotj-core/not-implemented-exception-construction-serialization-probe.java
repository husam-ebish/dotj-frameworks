import System.Runtime.Serialization.*;
import System.Collections.IDictionary;
import System.NotImplementedException;
import System.Reflection.TargetException;
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
class NotImplementedExceptionConstructionSerializationProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String value(Object o,Type self){if(o==null)return null;if(o instanceof Type t)return t==self?"self":"type:"+t.ToString();if(o instanceof MemberTypes v)return Integer.toString(v.get_Value());if(o instanceof GenericParameterAttributes v)return Integer.toString(v.get_Value());if(o instanceof TypeCode v)return Integer.toString(v.get_Value());if(o.getClass().isArray()){StringJoiner j=new StringJoiner(";");for(int i=0;i<java.lang.reflect.Array.getLength(o);i++)j.add(value(java.lang.reflect.Array.get(o,i),self));return j.toString();}return o.toString();}
 static Type resolve(String name){return switch(name){case "null"->null;case "ListS"->Type.GetType("System.Collections.Generic.List`1").MakeGenericType(new Type[]{Type.GetType("System.String")});case "NullableInt"->Type.GetType("System.Nullable`1").MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType("System."+name);};}
 static String decode(String units){if(units.equals("~"))return null;StringBuilder b=new StringBuilder();if(!units.isEmpty())for(String p:units.split(","))b.append((char)Integer.parseInt(p));return b.toString();}
 static Exception create(String type,String ctor,String text,Exception inner){if(type.equals("NotImplementedException"))return switch(ctor){case "Default"->new NotImplementedException();case "Text"->new NotImplementedException(text);default->new NotImplementedException(text,inner);};return switch(ctor){case "Default"->new TargetException();case "Text"->new TargetException(text);default->new TargetException(text,inner);};}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;try(var reader=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=reader.readLine())!=null){String[] p=line.split("\t",-1);String result=null,error="none",message=null,param=null;int hResult=0;try{Type type=resolve(p[1]);Exception inner=Boolean.parseBoolean(p[4])?new Exception("inner"):null;Exception e=create(p[1],p[2],decode(p[3]),inner);e.set_Source(decode(p[5]));e.set_HelpLink(decode(p[6]));if(!p[8].equals("~"))e.set_HResult(Integer.parseInt(p[8]));IDictionary data=null;if(Boolean.parseBoolean(p[7])){data=e.get_Data();data.Add("key","value");}if(Boolean.parseBoolean(p[10]))e.get_Message();StreamingContext context=new StreamingContext(StreamingContextStates.FromInt32(Integer.parseInt(p[9])));SerializationInfo info=Boolean.parseBoolean(p[11])?null:new SerializationInfo(type,new FormatterConverter());e.GetObjectData(info,context);List<String> parts=new ArrayList<>();parts.add(info.get_FullTypeName());parts.add(info.get_AssemblyName());parts.add(Integer.toString(info.get_MemberCount()));SerializationInfoEnumerator en=info.GetEnumerator();while(en.MoveNext()){SerializationEntry entry=en.get_Current();Object v=entry.get_Value();String kind="null",text="~";if(v!=null){if(v==inner)kind="inner";else if(v==data)kind="data";else if(v instanceof String string){kind="text";text=units(string);}else if(v instanceof Integer n){kind="int";text=n.toString();}else if(v instanceof Int32 n){kind="int";text=n.ToString();}else throw new AssertionError(entry.get_Name()+" "+v.getClass().getName());}parts.add(entry.get_Name()+"#"+entry.get_ObjectType().get_FullName()+"#"+kind+"#"+text);}result=String.join("|",parts);}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] actual={units(result),error,units(message),Integer.toString(hResult),units(param)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[12+i]))throw new AssertionError("id="+p[0]+" type="+p[1]+" field="+i+" actual="+actual[i]+" expected="+p[12+i]);groups++;}calls++;}}java.lang.System.out.println("PASS access exception serialization calls="+calls+" groups="+groups);}
}
