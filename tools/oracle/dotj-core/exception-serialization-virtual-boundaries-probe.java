import System.Exception;
import System.Type;
import System.Collections.IDictionary;
import System.InvalidOperationException;
import System.Runtime.Serialization.*;
import java.nio.file.*;
import java.util.*;
class ExceptionSerializationVirtualBoundariesProbe {
 static class Spy extends Exception {int calls,others;String mode;Spy(String message,String mode){super(message);this.mode=mode;}public String get_Source(){calls++;if(mode.equals("throw"))throw new InvalidOperationException("source failure");return mode.equals("text")?"virtual source":null;}public String get_Message(){others++;throw new AssertionError("Message");}public String get_HelpLink(){others++;throw new AssertionError("HelpLink");}public String get_StackTrace(){others++;throw new AssertionError("StackTrace");}public IDictionary get_Data(){others++;throw new AssertionError("Data");}}
 static String text(String s){if(s.equals("~"))return null;StringBuilder b=new StringBuilder();if(!s.isEmpty())for(String c:s.split(","))b.append((char)Integer.parseInt(c));return b.toString();}
 static String units(Object o){if(o==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:((String)o).toCharArray())j.add(Integer.toString(c));return j.toString();}
 public static void main(String[] args)throws java.lang.Exception {Spy e=null;int groups=0,calls=0;
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);int attempt=Integer.parseInt(p[5]);if(attempt==-1){e=new Spy(text(p[3]),p[4]);e.set_Source(text(p[1]));e.set_HelpLink(text(p[2]));}SerializationInfo info=attempt<0?null:new SerializationInfo(Type.GetType("System.Exception"),new FormatterConverter());String error="none";try{e.GetObjectData(info,new StreamingContext(StreamingContextStates.FromInt32(Integer.parseInt(p[6]))));}catch(Exception expected){error=expected.getClass().getName();}Map<String,Object> fields=new HashMap<>();if(info!=null){SerializationInfoEnumerator it=info.GetEnumerator();while(it.MoveNext()){SerializationEntry entry=it.get_Current();fields.put(entry.get_Name(),entry.get_Value());}}String[] actual={Integer.toString(e.calls),Integer.toString(e.others),Integer.toString(info==null?0:info.get_MemberCount()),error,units(fields.get("Source")),units(fields.get("HelpURL")),units(fields.get("Message")),units(fields.get("StackTraceString")),Boolean.toString(fields.get("Data")==null)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[7+i]))throw new AssertionError("case "+p[0]+" attempt "+attempt+" field "+i+": "+actual[i]+" != "+p[7+i]);groups++;}calls++;
 }java.lang.System.out.println("PASS serialization boundaries calls="+calls+" groups="+groups);}
}
