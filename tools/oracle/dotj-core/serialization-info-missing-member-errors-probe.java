import System.Exception;
import System.ArgumentException;
import System.Type;
import System.Runtime.Serialization.*;
import java.nio.file.*;
import java.util.*;
class SerializationInfoMissingMemberErrorsProbe {
 static String text(String s){if(s.equals("~"))return null;StringBuilder b=new StringBuilder();if(!s.isEmpty())for(String c:s.split(","))b.append((char)Integer.parseInt(c));return b.toString();}
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static Object invoke(SerializationInfo info,String route,String name){return switch(route){
case "GetBoolean" -> info.GetBoolean(name);
case "GetByte" -> info.GetByte(name);
case "GetChar" -> info.GetChar(name);
case "GetDateTime" -> info.GetDateTime(name);
case "GetDecimal" -> info.GetDecimal(name);
case "GetDouble" -> info.GetDouble(name);
case "GetInt16" -> info.GetInt16(name);
case "GetInt32" -> info.GetInt32(name);
case "GetInt64" -> info.GetInt64(name);
case "GetSByte" -> info.GetSByte(name);
case "GetSingle" -> info.GetSingle(name);
case "GetString" -> info.GetString(name);
case "GetUInt16" -> info.GetUInt16(name);
case "GetUInt32" -> info.GetUInt32(name);
case "GetUInt64" -> info.GetUInt64(name);
case "GetValue:null"->info.GetValue(name,null);case "GetValue:Object"->info.GetValue(name,Type.GetType("System.Object"));case "GetValue:String"->info.GetValue(name,Type.GetType("System.String"));case "GetValue:Int32"->info.GetValue(name,Type.GetType("System.Int32"));default->throw new AssertionError(route);};}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);SerializationInfo info=new SerializationInfo(Type.GetType("System.Object"),new FormatterConverter());info.AddValue("present","sentinel",Type.GetType("System.String"));try{invoke(info,p[0],text(p[1]));throw new AssertionError("Missing lookup accepted");}catch(Exception expected){String[] actual={expected.getClass().getName(),units(expected.get_Message()),Integer.toString(expected.get_HResult()),units(expected instanceof ArgumentException argument?argument.get_ParamName():null),Integer.toString(info.get_MemberCount()),units(info.GetString("present"))};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[2+i]))throw new AssertionError(p[0]+" field "+i+": "+actual[i]+" != "+p[2+i]);groups++;}}calls++;}java.lang.System.out.println("PASS lookup errors calls="+calls+" groups="+groups);}
}
