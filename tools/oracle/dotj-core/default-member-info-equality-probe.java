import System.Type;
import System.Reflection.MemberInfo;
import java.nio.file.*;
import java.util.*;
class DefaultMemberInfoEqualityProbe {
 static Type owner(String name){Type list=Type.GetType("System.Collections.Generic.List`1");return switch(name){case "ListD"->list;case "ListS"->list.MakeGenericType(new Type[]{Type.GetType("System.String")});case "ListI"->list.MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType(name);};}
 public static void main(String[] args)throws java.lang.Exception{List<MemberInfo> members=new ArrayList<>();Object foreign=new Object();int calls=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);switch(p[0]){case "A"->{Type owner=owner(p[1]);MemberInfo[] first=owner.GetDefaultMembers(),second=owner.GetDefaultMembers();int count=first.length;MemberInfo saved=null;if(count>0){saved=first[0];members.add(first[0]);members.add(second[0]);first[0]=null;}MemberInfo[] third=owner.GetDefaultMembers();Object[] actual={count,first==second,count==0||saved==third[0]};for(int i=0;i<3;i++){if(!actual[i].toString().equals(p[2+i]))throw new AssertionError(line+" field="+i+" actual="+actual[i]);groups++;}calls+=3;}
 case "M"->{MemberInfo m=members.get(Integer.parseInt(p[1]));String[] actual={m.get_Name(),Integer.toString(m.get_MemberType().get_Value()),m.get_DeclaringType().get_FullName(),m.get_ReflectedType().get_FullName()};for(int i=0;i<4;i++){if(!actual[i].equals(p[2+i]))throw new AssertionError(line);groups++;}}
 case "E"->{MemberInfo m=members.get(Integer.parseInt(p[1]));int right=Integer.parseInt(p[2]);Object other=right<members.size()?members.get(right):right==members.size()?foreign:right==members.size()+1?Type.GetType("System.Int32"):null;boolean equal=m.Equals(other),hash=true;calls++;if(equal){hash=m.GetHashCode()==((MemberInfo)other).GetHashCode();calls+=2;}boolean[] actual={equal,m==other,hash};for(int i=0;i<3;i++){if(actual[i]!=Boolean.parseBoolean(p[3+i]))throw new AssertionError(line+" field="+i);groups++;}}
 case "H"->{MemberInfo m=members.get(Integer.parseInt(p[1]));if((m.GetHashCode()==m.GetHashCode())!=Boolean.parseBoolean(p[2]))throw new AssertionError(line);calls+=2;groups++;}default->throw new AssertionError(line);}}
 java.lang.System.out.println("PASS default members calls="+calls+" groups="+groups);}
}
