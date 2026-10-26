import System.ICloneable;import System.Exception;import System.ArgumentException;import System.ArgumentOutOfRangeException;import System.Globalization.NumberFormatInfo;import System.Type;import java.nio.file.*;import java.util.*;
class NumberFormatInfoCloneInterfaceProbe {
 interface Action{void run();}
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String text(String s){if(s.equals("~"))return null;StringBuilder b=new StringBuilder();if(!s.isEmpty())for(String u:s.split(","))b.append((char)Integer.parseInt(u));return b.toString();}
 static int[] sizes(String s){if(s.equals("~"))return null;if(s.isEmpty())return new int[0];String[] p=s.split(",");int[] a=new int[p.length];for(int i=0;i<a.length;i++)a[i]=Integer.parseInt(p[i]);return a;}
 static String csv(int[] a){StringJoiner j=new StringJoiner(",");for(int v:a)j.add(Integer.toString(v));return j.toString();}
 static String outcome(Action a){try{a.run();return "OK";}catch(Exception e){return String.join("|","ERR",e.getClass().getName(),units(e.get_Message()),Integer.toString(e.get_HResult()),units(e instanceof ArgumentException x?x.get_ParamName():null),e instanceof ArgumentOutOfRangeException x&&x.get_ActualValue()!=null?x.get_ActualValue().toString():"~");}}
 static void check(String a,String e,String c){if(!a.equals(e))throw new AssertionError(c+" actual="+a+" expected="+e);}
 static String flag(boolean b){return b?"1":"0";}
 static void set(NumberFormatInfo n,int property,String value){switch(property){
  case 0->n.set_NumberGroupSeparator(text(value));
  case 1->n.set_NumberGroupSizes(sizes(value));
  case 2->n.set_NumberDecimalSeparator(text(value));
  case 3->n.set_NumberDecimalDigits(Integer.parseInt(value));
  case 4->n.set_NumberNegativePattern(Integer.parseInt(value));
  case 5->n.set_NegativeSign(text(value));
  case 6->n.set_PositiveSign(text(value));
  case 7->n.set_CurrencySymbol(text(value));
  case 8->n.set_CurrencyGroupSeparator(text(value));
  case 9->n.set_CurrencyGroupSizes(sizes(value));
  case 10->n.set_CurrencyDecimalSeparator(text(value));
  case 11->n.set_CurrencyDecimalDigits(Integer.parseInt(value));
  case 12->n.set_CurrencyPositivePattern(Integer.parseInt(value));
  case 13->n.set_CurrencyNegativePattern(Integer.parseInt(value));
  case 14->n.set_PercentSymbol(text(value));
  case 15->n.set_PerMilleSymbol(text(value));
  case 16->n.set_PercentGroupSeparator(text(value));
  case 17->n.set_PercentGroupSizes(sizes(value));
  case 18->n.set_PercentDecimalSeparator(text(value));
  case 19->n.set_PercentDecimalDigits(Integer.parseInt(value));
  case 20->n.set_PercentPositivePattern(Integer.parseInt(value));
  case 21->n.set_PercentNegativePattern(Integer.parseInt(value));
  default->throw new AssertionError(property);
 }}
 static NumberFormatInfo seed(){NumberFormatInfo n=new NumberFormatInfo();
  n.set_NumberGroupSeparator(text("95"));
  n.set_NumberGroupSizes(sizes("1,2,0"));
  n.set_NumberDecimalSeparator(text("58"));
  n.set_NumberDecimalDigits(Integer.parseInt("7"));
  n.set_NumberNegativePattern(Integer.parseInt("4"));
  n.set_NegativeSign(text("126"));
  n.set_PositiveSign(text("112"));
  n.set_CurrencySymbol(text("99,117,114,0,55296"));
  n.set_CurrencyGroupSeparator(text("39"));
  n.set_CurrencyGroupSizes(sizes("4,3"));
  n.set_CurrencyDecimalSeparator(text("59"));
  n.set_CurrencyDecimalDigits(Integer.parseInt("8"));
  n.set_CurrencyPositivePattern(Integer.parseInt("3"));
  n.set_CurrencyNegativePattern(Integer.parseInt("16"));
  n.set_PercentSymbol(text("37,120"));
  n.set_PerMilleSymbol(text("112,101,114,109"));
  n.set_PercentGroupSeparator(text("124"));
  n.set_PercentGroupSizes(sizes("0"));
  n.set_PercentDecimalSeparator(text("44"));
  n.set_PercentDecimalDigits(Integer.parseInt("9"));
  n.set_PercentPositivePattern(Integer.parseInt("3"));
  n.set_PercentNegativePattern(Integer.parseInt("11"));
  return n;
 }
 static String snapshot(NumberFormatInfo n){StringJoiner j=new StringJoiner("|");j.add(flag(n.get_IsReadOnly()));
  j.add(units(n.get_NumberGroupSeparator()));
  j.add(csv(n.get_NumberGroupSizes()));
  j.add(units(n.get_NumberDecimalSeparator()));
  j.add(Integer.toString(n.get_NumberDecimalDigits()));
  j.add(Integer.toString(n.get_NumberNegativePattern()));
  j.add(units(n.get_NegativeSign()));
  j.add(units(n.get_PositiveSign()));
  j.add(units(n.get_CurrencySymbol()));
  j.add(units(n.get_CurrencyGroupSeparator()));
  j.add(csv(n.get_CurrencyGroupSizes()));
  j.add(units(n.get_CurrencyDecimalSeparator()));
  j.add(Integer.toString(n.get_CurrencyDecimalDigits()));
  j.add(Integer.toString(n.get_CurrencyPositivePattern()));
  j.add(Integer.toString(n.get_CurrencyNegativePattern()));
  j.add(units(n.get_PercentSymbol()));
  j.add(units(n.get_PerMilleSymbol()));
  j.add(units(n.get_PercentGroupSeparator()));
  j.add(csv(n.get_PercentGroupSizes()));
  j.add(units(n.get_PercentDecimalSeparator()));
  j.add(Integer.toString(n.get_PercentDecimalDigits()));
  j.add(Integer.toString(n.get_PercentPositivePattern()));
  j.add(Integer.toString(n.get_PercentNegativePattern()));
  return j.toString();
 }
 static String interfaces(Type[] types){StringJoiner j=new StringJoiner(",");for(Type t:types)j.add(t.get_FullName());return j.toString();}
 static String lookup(Type t,String name,boolean ignore){try{Type value=t.GetInterface(name,ignore);return "OK|"+(value==null?"~":value.get_FullName());}catch(Exception e){return String.join("|","ERR",e.getClass().getName(),units(e.get_Message()),Integer.toString(e.get_HResult()),units(e instanceof ArgumentException x?x.get_ParamName():null),"~");}}
 public static void main(String[] args)throws java.lang.Exception{int groups=0,lookups=0,assignments=0,clones=0;Type nfi=Type.GetType("System.Globalization.NumberFormatInfo"),contract=Type.GetType("System.ICloneable");for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);switch(p[0]){case "I"->{Type[] first=nfi.GetInterfaces(),second=nfi.GetInterfaces();check(interfaces(first),p[1],"NFI interfaces");check(flag(first!=second),p[2],"interface array identity");first[0]=null;check(interfaces(nfi.GetInterfaces()),p[3],"interface array mutation");groups+=3;}case "L"->{check(lookup(nfi,text(p[1]),p[2].equals("1")),p[3],"lookup "+line);lookups++;groups++;}case "A"->{check(flag(Type.GetType(p[1]).IsAssignableFrom(Type.GetType(p[2]))),p[3],"assignability "+line);assignments++;groups++;}case "C"->{NumberFormatInfo original=seed(),ro=NumberFormatInfo.ReadOnly(original),target=switch(p[1]){case "mutable"->original;case "readonly"->ro;case "clone"->(NumberFormatInfo)ro.Clone();default->throw new AssertionError();};NumberFormatInfo copy=(NumberFormatInfo)((ICloneable)(Object)target).Clone();check(snapshot(target),p[2],"interface original "+line);check(snapshot(copy),p[3],"interface clone "+line);check(flag(target!=copy),p[4],"clone distinct");check(flag(contract.IsInstanceOfType(target)),p[5],"original interface instance");check(flag(contract.IsInstanceOfType(copy)),p[6],"clone interface instance");check(copy.getClass().getName(),p[7],"clone type");clones++;groups+=6;}default->throw new AssertionError();}}java.lang.System.out.println("PASS NumberFormatInfo clone interface lookups="+lookups+" assignments="+assignments+" clones="+clones+" groups="+groups);}
}
