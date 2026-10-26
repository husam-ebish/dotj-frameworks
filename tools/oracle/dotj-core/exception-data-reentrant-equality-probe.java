import System.Exception;import System.ArgumentException;import System.InvalidOperationException;import System.Collections.*;import java.nio.file.*;import java.util.*;
class ReentrantOracleKey {
 int id,calls,mode;boolean accepts,fired;IDictionary dictionary;ReentrantOracleKey tail,fresh;
 ReentrantOracleKey(int id){this.id=id;}
 @Override public boolean equals(Object other){calls++;if(mode!=0&&!fired){fired=true;switch(mode){case 1->{}case 2->dictionary.Clear();case 3->{dictionary.Clear();dictionary.Add(fresh,"nested");}case 4->dictionary.Add(fresh,"nested");case 5->dictionary.set_Item(this,"nested");case 6->dictionary.Remove(this);case 7->dictionary.Remove(tail);default->throw new AssertionError(mode);}}return id==1?accepts:other instanceof ReentrantOracleKey k&&id==k.id;}
 @Override public int hashCode(){throw new InvalidOperationException("unexpected hash");}
 @Override public String toString(){return "K"+id;}
}
class ExceptionDataReentrantEqualityProbe{
 interface Action{Object run();}
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String normal(Object v){return v instanceof DictionaryEntry e?e.get_Key()+"="+e.get_Value():v instanceof ReentrantOracleKey?v.toString():v==null?"~":"V"+v;}
 static String outcome(Action a,String kind){try{Object v=a.run();return "OK|"+kind+"|"+(kind.equals("void")?"~":kind.equals("bool")?((Boolean)v?"1":"0"):kind.equals("current")?normal(v):v==null?"~":v.toString());}catch(Exception e){return "ERR|"+e.getClass().getName()+"|"+units(e.get_Message())+"|"+e.get_HResult()+"|"+units(e instanceof ArgumentException x?x.get_ParamName():null);}}
 static String contents(IDictionary d){StringJoiner j=new StringJoiner(";");IDictionaryEnumerator c=d.GetEnumerator();int n=0;while(c.MoveNext()){if(++n>16)throw new AssertionError("cycle");j.add(normal(c.get_Entry()));}return j.toString();}
 static void check(String a,String e,String c){if(!a.equals(e))throw new AssertionError(c+" actual="+a+" expected="+e);}
 public static void main(String[] args)throws java.lang.Exception{int cases=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);int size=Integer.parseInt(p[0]);IDictionary d=new Exception("reentrant").get_Data();ReentrantOracleKey h=new ReentrantOracleKey(1),t=new ReentrantOracleKey(2),third=new ReentrantOracleKey(3),fresh=new ReentrantOracleKey(9),q=new ReentrantOracleKey(Integer.parseInt(p[3]));d.Add(h,"initial1");if(size>=2)d.Add(t,"initial2");if(size>=3)d.Add(third,"initial3");h.calls=t.calls=third.calls=0;h.accepts=p[2].equals("1");h.dictionary=d;h.tail=t;h.fresh=fresh;h.mode=Integer.parseInt(p[1]);ICollection keys=d.get_Keys(),values=d.get_Values();IEnumerator[] cursors={d.GetEnumerator(),keys.GetEnumerator(),values.GetEnumerator()};for(int i=0;i<3;i++){final IEnumerator c=cursors[i];check(outcome(c::MoveNext,"bool"),p[5+i],"before move "+line);groups++;}
 String r=switch(p[4]){case "read"->outcome(()->d.get_Item(q),"value");case "contains"->outcome(()->d.Contains(q),"bool");case "write"->outcome(()->{d.set_Item(q,"outer");return null;},"void");case "add"->outcome(()->{d.Add(q,"outer");return null;},"void");case "remove"->outcome(()->{d.Remove(q);return null;},"void");default->throw new AssertionError();};check(r,p[8],"result "+line);groups++;
 for(int i=0;i<3;i++){final IEnumerator c=cursors[i];int o=15+i*3;check(outcome(c::get_Current,"current"),p[o],"current "+line);check(outcome(c::MoveNext,"bool"),p[o+1],"move "+line);check(outcome(()->{c.Reset();return null;},"void"),p[o+2],"reset "+line);groups+=3;}
 check(Integer.toString(d.get_Count()),p[9],"dictionary count "+line);check(Integer.toString(keys.get_Count()),p[10],"key view count "+line);check(Integer.toString(values.get_Count()),p[11],"value view count "+line);check(contents(d),p[12],"contents "+line);check(h.calls+","+t.calls+","+third.calls+","+fresh.calls+","+q.calls,p[13],"callbacks "+line);check(h.fired?"1":"0",p[14],"callback marker "+line);groups+=6;cases++;}
 java.lang.System.out.println("PASS reentrant Data cases="+cases+" groups="+groups);}
}
