import System.Exception;
import System.ArgumentException;
import System.ArgumentOutOfRangeException;
import System.Collections.*;
import java.lang.reflect.Array;
import java.nio.file.*;
import java.util.*;
class ExceptionDataCopyToProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String normal(Object v){if(v==null)return "N";if(v instanceof DictionaryEntry e)return "E("+normal(e.get_Key())+","+normal(e.get_Value())+")";if(v instanceof String s)return "S:"+units(s);return (v instanceof Integer?"Int32":v instanceof Long?"Int64":v instanceof Byte?"Byte":v.getClass().getSimpleName())+":"+v;}
 static IDictionary data(int p){IDictionary d=new Exception("copy").get_Data();Object[][] pairs=switch(p){case 0->new Object[0][0];case 1->new Object[][]{{"k",7}};case 2->new Object[][]{{1,1},{"x","text"}};case 3->new Object[][]{{1,1},{2,"text"},{3,3}};case 4->new Object[][]{{"a",null},{"b","text"},{"c",1}};case 5->new Object[][]{{"a","one"},{"b","two"},{"c","three"}};default->throw new AssertionError();};for(Object[] pair:pairs)d.Add(pair[0],pair[1]);return d;}
 static Object array(String k){return switch(k){case "null"->null;case "object"->new Object[]{"guard","guard","guard"};case "entry"->new DictionaryEntry[]{new DictionaryEntry("guard",99),new DictionaryEntry("guard",99),new DictionaryEntry("guard",99)};case "string"->new String[]{"guard","guard","guard"};case "int"->new int[]{99,99,99};case "long"->new long[]{99,99,99};case "byte"->new byte[]{99,99,99};case "rank2"->new Object[][]{{"guard","guard"},{"guard","guard"}};default->throw new AssertionError();};}
 static String snapshot(Object a){if(a==null)return "~";StringJoiner j=new StringJoiner(";");if(a instanceof Object[][] rows){for(Object[] row:rows)for(Object v:row)j.add(normal(v));}else for(int i=0;i<Array.getLength(a);i++)j.add(normal(Array.get(a,i)));return j.toString();}
 static String contents(IDictionary d){StringJoiner j=new StringJoiner(";");IDictionaryEnumerator e=d.GetEnumerator();while(e.MoveNext())j.add(normal(e.get_Entry()));return j.toString();}
 static String copy(ICollection c,Object a,int i){try{c.CopyTo(a,i);return "OK";}catch(Exception e){return String.join("|","ERR",e.getClass().getName(),units(e.get_Message()),Integer.toString(e.get_HResult()),units(e instanceof ArgumentException x?x.get_ParamName():null),e instanceof ArgumentOutOfRangeException x?normal(x.get_ActualValue()):"~");}}
 static void check(String actual,String expected,String context){if(!actual.equals(expected))throw new AssertionError(context+" actual="+actual+" expected="+expected);}
 public static void main(String[] args)throws java.lang.Exception{int cases=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);IDictionary d=data(Integer.parseInt(p[0]));ICollection c=switch(p[1]){case "dictionary"->d;case "keys"->d.get_Keys();case "values"->d.get_Values();default->throw new AssertionError();};Object a=array(p[2]);check(copy(c,a,Integer.parseInt(p[3])),p[4],"outcome "+line);check(snapshot(a),p[5],"destination "+line);check(Integer.toString(d.get_Count()),p[6],"count "+line);check(contents(d),p[7],"contents "+line);cases++;groups+=4;}java.lang.System.out.println("PASS Data CopyTo cases="+cases+" groups="+groups);}
}
