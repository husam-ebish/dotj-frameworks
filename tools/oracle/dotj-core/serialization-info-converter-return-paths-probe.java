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
class SerializationInfoConverterReturnPathsProbe {
 static class Spy implements IFormatterConverter {int calls;String last;InvalidOperationException fail(String method){calls++;last=method;return new InvalidOperationException("converter sentinel");}
 public Object Convert(Object value,Type type){calls++;last="Convert:Type";return null;}public Object Convert(Object value,TypeCode type){calls++;last="Convert:TypeCode";return null;}
public boolean ToBoolean(Object value){calls++;last="ToBoolean";return true;}
public short ToByte(Object value){calls++;last="ToByte";return (short)42;}
public char ToChar(Object value){calls++;last="ToChar";return 'A';}
public DateTime ToDateTime(Object value){calls++;last="ToDateTime";return new DateTime(0L);}
public Decimal ToDecimal(Object value){calls++;last="ToDecimal";return new Decimal(42);}
public double ToDouble(Object value){calls++;last="ToDouble";return 1.25d;}
public short ToInt16(Object value){calls++;last="ToInt16";return (short)-42;}
public int ToInt32(Object value){calls++;last="ToInt32";return -42;}
public long ToInt64(Object value){calls++;last="ToInt64";return -42L;}
public byte ToSByte(Object value){calls++;last="ToSByte";return (byte)-42;}
public float ToSingle(Object value){calls++;last="ToSingle";return 1.25f;}
public String ToString(Object value){calls++;last="ToString";return "sentinel";}
public int ToUInt16(Object value){calls++;last="ToUInt16";return 42;}
public long ToUInt32(Object value){calls++;last="ToUInt32";return 42L;}
public java.math.BigInteger ToUInt64(Object value){calls++;last="ToUInt64";return java.math.BigInteger.valueOf(42);}
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
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);for(int representation=0;representation<(p[0].equals("Int32")?2:1);representation++){Spy spy=new Spy();SerializationInfo info=new SerializationInfo(Type.GetType("System.Object"),spy);Type declared=Type.GetType(p[1].equals("NullableInt32")?"System.Nullable`1[System.Int32]":"System."+p[1]);info.AddValue("value",actual(p[0],representation==1),declared);String value=null,error="none",message=null,param=null;int hResult=0;try{value=result(p[2],invoke(info,p[2]));}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] a={Integer.toString(spy.calls),units(spy.last),units(value),error,units(message),Integer.toString(hResult),units(param),Integer.toString(info.get_MemberCount())};for(int i=0;i<a.length;i++){if(!a[i].equals(p[3+i]))throw new AssertionError(p[0]+" declared "+p[1]+" route "+p[2]+" field "+i+": "+a[i]+" != "+p[3+i]);groups++;}calls++;}}java.lang.System.out.println("PASS typed dispatch calls="+calls+" groups="+groups);}
}
