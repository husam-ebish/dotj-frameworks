import System.IFormatProvider;import System.IFormattable;import System.Exception;import System.ArgumentException;import System.InvalidOperationException;import System.Collections.*;import java.nio.file.*;import java.util.*;
class PrimitiveTextOracleKey {
 int id,equalsCalls,textCalls,textMode,fmtCalls;String lastFormat="unseen";IFormatProvider lastProvider;boolean accepts;String text;List<Integer> trace;
 PrimitiveTextOracleKey(int id,String text,int mode,boolean accepts,List<Integer> trace){this.id=id;this.text=text;textMode=mode;this.accepts=accepts;this.trace=trace;}
 @Override public boolean equals(Object other){equalsCalls++;return accepts;}
 @Override public int hashCode(){throw new InvalidOperationException("unexpected hash");}
 @Override public String toString(){textCalls++;trace.add(id);if(textMode==2)throw new InvalidOperationException("key text failure");return textMode==1?null:text;}
}
class FormattedPrimitiveTextKey extends PrimitiveTextOracleKey implements IFormattable {
 FormattedPrimitiveTextKey(int id,String text,int mode,boolean accepts,List<Integer> trace){super(id,text,mode,accepts,trace);}
 @Override public String ToString(String format,IFormatProvider provider){fmtCalls++;trace.add(100+id);lastFormat=format;lastProvider=provider;if(textMode==2)throw new InvalidOperationException("formatted key text failure");return textMode==1?null:"formatted stored";}
}
class ExceptionDataPrimitiveKeyTextProbe {
 interface Action{Object run();}
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String text(String units){StringBuilder b=new StringBuilder();if(!units.isEmpty())for(String u:units.split(","))b.append((char)Integer.parseInt(u));return b.toString();}
 static String normal(Object v){return v instanceof DictionaryEntry e?"K"+((PrimitiveTextOracleKey)e.get_Key()).id+"="+e.get_Value():v instanceof PrimitiveTextOracleKey k?"K"+k.id:v==null?"~":"V"+v;}
 static String outcome(Action a,String kind){try{Object v=a.run();return "OK|"+kind+"|"+(kind.equals("void")?"~":kind.equals("bool")?((Boolean)v?"1":"0"):kind.equals("current")?normal(v):v==null?"~":v.toString());}catch(Exception e){return "ERR|"+e.getClass().getName()+"|"+units(e.get_Message())+"|"+e.get_HResult()+"|"+units(e instanceof ArgumentException x?x.get_ParamName():null);}}
 static String contents(IDictionary d){StringJoiner j=new StringJoiner(";");IDictionaryEnumerator c=d.GetEnumerator();while(c.MoveNext())j.add(normal(c.get_Entry()));return j.toString();}
 static String calls(PrimitiveTextOracleKey k){return k.equalsCalls+","+k.textCalls+","+k.fmtCalls+"|"+units(k.lastFormat)+"|"+(k.fmtCalls==0?"unseen":k.lastProvider==null?"null":k.lastProvider.getClass().getName());}
 static void check(String a,String e,String c){if(!a.equals(e))throw new AssertionError(c+" actual="+a+" expected="+e);}
 static PrimitiveTextOracleKey key(int kind,int id,String text,int mode,boolean accepts,List<Integer> trace){return kind==0?new PrimitiveTextOracleKey(id,text,mode,accepts,trace):new FormattedPrimitiveTextKey(id,text,mode,accepts,trace);}
 static Object query(String kind,String value){return switch(kind){case "sbyte"->Byte.valueOf(value);case "short"->Short.valueOf(value);case "int"->Integer.valueOf(value);case "long"->Long.valueOf(value);case "bool"->value.equals("1");case "char"->Character.valueOf((char)Integer.parseInt(value));case "string"->text(value);case "float"->Float.valueOf(Float.intBitsToFloat(Integer.parseUnsignedInt(value,16)));case "double"->Double.valueOf(Double.longBitsToDouble(Long.parseUnsignedLong(value,16)));default->throw new AssertionError(kind);};}
 static String source(Object value,String kind){return switch(kind){case "float"->String.format(Locale.ROOT,"%08x",Float.floatToRawIntBits((Float)value));case "double"->String.format(Locale.ROOT,"%016x",Double.doubleToRawLongBits((Double)value));case "bool"->(Boolean)value?"1":"0";case "char"->Integer.toString((Character)value);case "string"->units((String)value);default->value.toString();};}
 public static void main(String[] args)throws java.lang.Exception{int cases=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);Object q=query(p[2],p[3]);check(source(q,p[2]),p[3],"source transport "+line);List<Integer> trace=new ArrayList<>();PrimitiveTextOracleKey s=key(Integer.parseInt(p[1]),1,"stored",0,true,trace);IDictionary d=new Exception("primitive key").get_Data();d.Add(s,"initial");check(outcome(()->{d.Add(q,"outer");return null;},"void"),p[4],"result "+line);check(Integer.toString(d.get_Count()),p[5],"count "+line);check(contents(d),p[6],"contents "+line);check(calls(s),p[7],"stored dispatch "+line);StringJoiner events=new StringJoiner(",");for(int id:trace)events.add(Integer.toString(id));check(events.toString(),p[8],"text order "+line);cases++;groups+=6;}java.lang.System.out.println("PASS primitive key text cases="+cases+" groups="+groups);}
}
