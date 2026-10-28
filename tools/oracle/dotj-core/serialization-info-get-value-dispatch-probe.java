import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;
import System.Type;
import System.TypeCode;
import System.Int32;
import System.Byte;
import System.SByte;
import System.UInt16;
import System.UInt32;
import System.DateTime;
import System.Decimal;
import System.Runtime.Serialization.*;
import java.nio.file.*;
import java.util.*;
class SerializationInfoGetValueDispatchProbe {
 static class Spy implements IFormatterConverter {int calls;String last;boolean throwsConverter;Type seenType;Object marker=new String("converted marker");InvalidOperationException fail(String method){calls++;last=method;return new InvalidOperationException("converter sentinel");}
 public Object Convert(Object value,Type type){calls++;last="Convert:Type";seenType=type;if(throwsConverter)throw new InvalidOperationException("converter sentinel");return marker;}public Object Convert(Object value,TypeCode type){throw fail("Convert:TypeCode");}
public boolean ToBoolean(Object value){throw fail("ToBoolean");}
public short ToByte(Object value){throw fail("ToByte");}
public char ToChar(Object value){throw fail("ToChar");}
public DateTime ToDateTime(Object value){throw fail("ToDateTime");}
public Decimal ToDecimal(Object value){throw fail("ToDecimal");}
public double ToDouble(Object value){throw fail("ToDouble");}
public short ToInt16(Object value){throw fail("ToInt16");}
public int ToInt32(Object value){throw fail("ToInt32");}
public long ToInt64(Object value){throw fail("ToInt64");}
public byte ToSByte(Object value){throw fail("ToSByte");}
public float ToSingle(Object value){throw fail("ToSingle");}
public String ToString(Object value){throw fail("ToString");}
public int ToUInt16(Object value){throw fail("ToUInt16");}
public long ToUInt32(Object value){throw fail("ToUInt32");}
public java.math.BigInteger ToUInt64(Object value){throw fail("ToUInt64");}
 }
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static Object actual(String name,boolean owned){return switch(name){case "null"->null;case "Boolean"->true;case "Byte"->new Byte((short)42);case "Char"->'A';case "DateTime"->new DateTime(0L);case "Decimal"->new Decimal(42);case "Double"->1.25d;case "Int16"->(short)-42;case "Int32"->owned?new Int32(-42):Integer.valueOf(-42);case "Int64"->-42L;case "SByte"->new SByte((byte)-42);case "Single"->1.25f;case "String"->"sentinel";case "UInt16"->new UInt16(42);case "UInt32"->new UInt32(42L);case "UInt64"->java.math.BigInteger.valueOf(42);default->throw new AssertionError(name);};}
 static Object invoke(SerializationInfo info,String route){return switch(route){
case "GetBoolean"->info.GetBoolean("value");
case "GetByte"->info.GetByte("value");
case "GetChar"->info.GetChar("value");
case "GetDateTime"->info.GetDateTime("value");
case "GetDecimal"->info.GetDecimal("value");
case "GetDouble"->info.GetDouble("value");
case "GetInt16"->info.GetInt16("value");
case "GetInt32"->info.GetInt32("value");
case "GetInt64"->info.GetInt64("value");
case "GetSByte"->info.GetSByte("value");
case "GetSingle"->info.GetSingle("value");
case "GetString"->info.GetString("value");
case "GetUInt16"->info.GetUInt16("value");
case "GetUInt32"->info.GetUInt32("value");
case "GetUInt64"->info.GetUInt64("value");
default->throw new AssertionError(route);};}
 static String result(String route,Object value){if(value==null)return null;if(route.equals("GetChar"))return Integer.toString((Character)value);if(route.equals("GetDateTime"))return Long.toString(((DateTime)value).get_Ticks());if(route.equals("GetDecimal")){StringJoiner j=new StringJoiner(",");for(int bit:Decimal.GetBits((Decimal)value))j.add(Integer.toString(bit));return j.toString();}return value.toString();}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);for(int representation=0;representation<(p[0].equals("Int32")?2:1);representation++){Spy spy=new Spy();spy.throwsConverter=p[3].equals("throw");SerializationInfo info=new SerializationInfo(Type.GetType("System.Object"),spy);Type declared=Type.GetType(p[1].equals("NullableInt32")?"System.Nullable`1[System.Int32]":"System."+p[1]);Object original=actual(p[0],representation==1);info.AddValue("value",original,declared);Type target=p[2].equals("null")?null:Type.GetType(p[2].equals("NullableInt32")?"System.Nullable`1[System.Int32]":"System."+p[2]);String kind="none",error="none",message=null,param=null;int hResult=0;try{Object result=info.GetValue("value",target);kind=result==null?"null":result==original?"same":result==spy.marker?"converted":"other";}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] a={Integer.toString(spy.calls),units(spy.last),Boolean.toString(spy.seenType!=null&&spy.seenType==target),kind,error,units(message),Integer.toString(hResult),units(param),Integer.toString(info.get_MemberCount())};for(int i=0;i<a.length;i++){if(!a[i].equals(p[4+i]))throw new AssertionError(p[0]+" declared "+p[1]+" target "+p[2]+" mode "+p[3]+" field "+i+": "+a[i]+" != "+p[4+i]);groups++;}calls++;}}java.lang.System.out.println("PASS GetValue calls="+calls+" groups="+groups);}
}
