import System.Int32;import System.ICloneable;import System.Exception;import System.ArgumentException;import System.ArgumentOutOfRangeException;import System.Globalization.NumberFormatInfo;import System.Type;import java.nio.file.*;import java.util.*;
class NumberFormatInfoInvariantProviderProbe {
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
 public static void main(String[] args)throws java.lang.Exception{NumberFormatInfo invariant=NumberFormatInfo.get_InvariantInfo();int identities=0,clones=0,formats=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);switch(p[0]){case "I"->{check(snapshot(invariant),p[1],"invariant defaults");check(snapshot(new NumberFormatInfo()),p[2],"fresh defaults");check(flag(NumberFormatInfo.ReadOnly(invariant)==invariant),p[3],"readonly identity");check(flag(invariant.GetFormat(Type.GetType("System.Globalization.NumberFormatInfo"))==invariant),p[4],"provider self");for(String expected:p[5].split(",")){check(flag(NumberFormatInfo.get_InvariantInfo()==invariant),expected,"cache identity");identities++;groups++;}groups+=4;}case "C"->{int property=Integer.parseInt(p[1]);check(outcome(()->set(invariant,property,p[2])),p[3],"readonly mutation "+line);NumberFormatInfo copy=(NumberFormatInfo)((ICloneable)invariant).Clone();check(snapshot(copy),p[4],"clone defaults "+line);set(copy,property,p[2]);check(snapshot(copy),p[5],"clone mutation "+line);check(snapshot(invariant),p[6],"invariant isolation "+line);check(flag(copy!=invariant),p[7],"clone distinct");check(flag(copy.GetFormat(Type.GetType("System.Globalization.NumberFormatInfo"))==copy),p[8],"clone provider self");clones++;groups+=6;}case "F"->{String actual=new Int32(Integer.parseInt(p[1])).ToString(text(p[2]),invariant);check(units(actual),p[3],"invariant format "+line);formats++;groups++;}case "S"->{check(snapshot(invariant),p[1],"final invariant state");groups++;}default->throw new AssertionError();}}java.lang.System.out.println("PASS InvariantInfo identities="+identities+" clones="+clones+" formats="+formats+" groups="+groups);}
}
