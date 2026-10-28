import System.Type;
import System.Reflection.MemberInfo;
import System.Reflection.MethodInfo;
import System.Reflection.BindingFlags;
import java.nio.file.*;
import java.util.*;
class MethodInfoEqualityProbe {
 public static void main(String[] args)throws java.lang.Exception {List<MethodInfo> methods=new ArrayList<>();BindingFlags flags=BindingFlags.Public.or(BindingFlags.Instance);int calls=0,groups=0;Object foreign=new Object();
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);if(p[0].equals("L")){Type owner=Type.GetType(p[1]);String name=p[2];Type[] types=p[4].isEmpty()?new Type[0]:Arrays.stream(p[4].split(";")).map(Type::GetType).toArray(Type[]::new);MethodInfo m=switch(p[3]){case "name"->owner.GetMethod(name);case "flags"->owner.GetMethod(name,flags);case "types"->owner.GetMethod(name,types);case "flags-types"->owner.GetMethod(name,flags,types);case "methods"->owner.GetMethods(flags)[0];case "ignore-case"->owner.GetMethod(name.toUpperCase(Locale.ROOT),flags.or(BindingFlags.IgnoreCase));default->throw new AssertionError(p[3]);};if(m==null||!m.get_Name().equals(name))throw new AssertionError(line);methods.add(m);calls++;
 }else if(p[0].equals("E")){int left=Integer.parseInt(p[1]),right=Integer.parseInt(p[2]);MethodInfo m=methods.get(left);Object other=right<methods.size()?methods.get(right):right==methods.size()?foreign:right==methods.size()+1?Type.GetType("System.Int32"):null;boolean equal=m.Equals(other);calls++;boolean hash=true;if(equal){hash=m.GetHashCode()==((MemberInfo)other).GetHashCode();calls+=2;}boolean[] actual={equal,m==other,hash};for(int i=0;i<3;i++){if(actual[i]!=Boolean.parseBoolean(p[3+i]))throw new AssertionError(line+" field="+i+" actual="+actual[i]);groups++;}
 }else{MethodInfo m=methods.get(Integer.parseInt(p[1]));int first=m.GetHashCode(),second=m.GetHashCode();calls+=2;if((first==second)!=Boolean.parseBoolean(p[2]))throw new AssertionError(line);groups++;}}
 java.lang.System.out.println("PASS method equality calls="+calls+" groups="+groups);}
}
