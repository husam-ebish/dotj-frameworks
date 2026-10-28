import System.Exception;
import System.ArgumentException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.TypeLoadException;
import System.Int32;
import System.Type;
import System.Globalization.CultureNotFoundException;
import System.IO.FileNotFoundException;
import System.IO.FileLoadException;
import System.Runtime.Serialization.*;
import java.nio.file.*;
import java.util.*;
class DerivedExceptionSerializationCollisionsProbe {
 static String text(String s){if(s.equals("~"))return null;StringBuilder b=new StringBuilder();if(!s.isEmpty())for(String c:s.split(","))b.append((char)Integer.parseInt(c));return b.toString();}
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static void check(String a,String b,String context){if(!a.equals(b))throw new AssertionError(context+": "+a+" != "+b);}
 public static void main(String[] args)throws java.lang.Exception {SerializationInfoEnumerator it=null;int calls=0,groups=0;
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);if(p[0].equals("S")){String message=text(p[2]),param=text(p[3]);Exception e=switch(p[1]){case "Exception"->new Exception(message);case "ArgumentException"->new ArgumentException(message,param);case "ArgumentNullException"->new ArgumentNullException(param,message);case "ArgumentOutOfRangeException"->new ArgumentOutOfRangeException(param,42,message);case "CultureNotFoundException"->new CultureNotFoundException(param,1033,message);case "FileNotFoundException"->new FileNotFoundException(message,param);case "FileLoadException"->new FileLoadException(message,param);case "TypeLoadException"->new TypeLoadException(message);default->throw new AssertionError(p[1]);};if(p[6].equals("1"))e.get_Message();SerializationInfo info=new SerializationInfo(e.GetType(),new FormatterConverter());info.AddValue(p[4],"preseed",Type.GetType("System.String"));String error="none",errorMessage=null;int errorHResult=0;try{e.GetObjectData(info,new StreamingContext(StreamingContextStates.FromInt32(Integer.parseInt(p[5]))));}catch(Exception expected){error=expected.getClass().getName();errorMessage=expected.get_Message();errorHResult=expected.get_HResult();}check(Integer.toString(info.get_MemberCount()),p[7],line);check(error,p[8],line);check(units(errorMessage),p[9],line);check(Integer.toString(errorHResult),p[10],line);it=info.GetEnumerator();calls++;groups+=4;
 }else if(p[0].equals("E")){if(!it.MoveNext())throw new AssertionError("Missing entry");SerializationEntry entry=it.get_Current();check(entry.get_Name(),p[1],line);check(entry.get_ObjectType().get_FullName(),p[2],line);Object v=entry.get_Value();String value=v==null?"null|~":v instanceof String s?"text|"+units(s):v instanceof Int32 n?"int|"+n.get_Value():v instanceof Integer n?"int|"+n: "unsupported";check(value,p[3]+"|"+p[4],line);groups+=3;
 }else{if(it.MoveNext())throw new AssertionError("Extra entry");groups++;}}
 java.lang.System.out.println("PASS derived collisions calls="+calls+" groups="+groups);}
}
