import System.IFormatProvider;import System.IFormattable;import System.Exception;import System.ArgumentException;import System.InvalidOperationException;import System.Collections.*;import java.nio.file.*;import java.util.*;
class FormattableOracleKey {
 int id,equalsCalls,textCalls,textMode,fmtCalls;String lastFormat="unseen";IFormatProvider lastProvider;boolean accepts;String text;List<Integer> trace;
 FormattableOracleKey(int id,String text,int mode,boolean accepts,List<Integer> trace){this.id=id;this.text=text;textMode=mode;this.accepts=accepts;this.trace=trace;}
 @Override public boolean equals(Object other){equalsCalls++;return accepts;}
 @Override public int hashCode(){throw new InvalidOperationException("unexpected hash");}
 @Override public String toString(){textCalls++;trace.add(id);if(textMode==2)throw new InvalidOperationException("key text failure");return textMode==1?null:text;}
}
class FormattedOracleKey extends FormattableOracleKey implements IFormattable {
 FormattedOracleKey(int id,String text,int mode,boolean accepts,List<Integer> trace){super(id,text,mode,accepts,trace);}
 @Override public String ToString(String format,IFormatProvider provider){fmtCalls++;trace.add(100+id);lastFormat=format;lastProvider=provider;if(textMode==2)throw new InvalidOperationException("formatted key text failure");return textMode==1?null:"F:"+text.substring(2);}
}
class ExceptionDataFormattableKeyTextProbe {
 interface Action{Object run();}
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String text(String units){StringBuilder b=new StringBuilder();if(!units.isEmpty())for(String u:units.split(","))b.append((char)Integer.parseInt(u));return b.toString();}
 static String normal(Object v){return v instanceof DictionaryEntry e?"K"+((FormattableOracleKey)e.get_Key()).id+"="+e.get_Value():v instanceof FormattableOracleKey k?"K"+k.id:v==null?"~":"V"+v;}
 static String outcome(Action a,String kind){try{Object v=a.run();return "OK|"+kind+"|"+(kind.equals("void")?"~":kind.equals("bool")?((Boolean)v?"1":"0"):kind.equals("current")?normal(v):v==null?"~":v.toString());}catch(Exception e){return "ERR|"+e.getClass().getName()+"|"+units(e.get_Message())+"|"+e.get_HResult()+"|"+units(e instanceof ArgumentException x?x.get_ParamName():null);}}
 static String contents(IDictionary d){StringJoiner j=new StringJoiner(";");IDictionaryEnumerator c=d.GetEnumerator();while(c.MoveNext())j.add(normal(c.get_Entry()));return j.toString();}
 static String calls(FormattableOracleKey k){return k.equalsCalls+","+k.textCalls+","+k.fmtCalls+"|"+units(k.lastFormat)+"|"+(k.fmtCalls==0?"unseen":k.lastProvider==null?"null":k.lastProvider.getClass().getName());}
 static void check(String a,String e,String c){if(!a.equals(e))throw new AssertionError(c+" actual="+a+" expected="+e);}
 static FormattableOracleKey key(int kind,int id,String text,int mode,boolean accepts,List<Integer> trace){return kind==0?new FormattableOracleKey(id,text,mode,accepts,trace):new FormattedOracleKey(id,text,mode,accepts,trace);}
 public static void main(String[] args)throws java.lang.Exception{int cases=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);List<Integer> trace=new ArrayList<>();FormattableOracleKey s=key(Integer.parseInt(p[1]),1,text(p[6]),Integer.parseInt(p[3]),true,trace),q=p[5].equals("1")?s:key(Integer.parseInt(p[2]),2,text(p[7]),Integer.parseInt(p[4]),false,trace);IDictionary d=new Exception("formattable text").get_Data();d.Add(s,"initial");IEnumerator[] cursors={d.GetEnumerator(),d.get_Keys().GetEnumerator(),d.get_Values().GetEnumerator()};for(int i=0;i<3;i++){final IEnumerator c=cursors[i];check(outcome(c::MoveNext,"bool"),p[8+i],"before "+line);groups++;}check(outcome(()->{d.Add(q,"outer");return null;},"void"),p[11],"result "+line);groups++;
 for(int i=0;i<3;i++){final IEnumerator c=cursors[i];int o=17+i*3;check(outcome(c::get_Current,"current"),p[o],"current "+line);check(outcome(c::MoveNext,"bool"),p[o+1],"move "+line);check(outcome(()->{c.Reset();return null;},"void"),p[o+2],"reset "+line);groups+=3;}
 check(Integer.toString(d.get_Count()),p[12],"count "+line);check(contents(d),p[13],"contents "+line);check(calls(s),p[14],"stored dispatch "+line);check(calls(q),p[15],"query dispatch "+line);StringJoiner events=new StringJoiner(",");for(int id:trace)events.add(Integer.toString(id));check(events.toString(),p[16],"text order "+line);groups+=5;cases++;}java.lang.System.out.println("PASS formattable key text cases="+cases+" groups="+groups);}
}
