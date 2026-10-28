import System.Type;
import System.Reflection.MemberInfo;
import System.Reflection.ParameterInfo;
import System.Reflection.MethodInfo;
import System.Reflection.BindingFlags;
import java.nio.file.*;
import java.util.*;
class MethodParameterInfoIdentityProbe {
 static String units(String text){if(text==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:text.toCharArray())j.add(Integer.toString(c));return j.toString();}
 public static void main(String[] args)throws java.lang.Exception {List<MethodInfo> methods=new ArrayList<>();BindingFlags flags=BindingFlags.Public.or(BindingFlags.Instance);int calls=0,groups=0;Object foreign=new Object();
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);if(p[0].equals("L")){Type owner=Type.GetType(p[1]);String name=p[2];Type[] types=p[4].isEmpty()?new Type[0]:Arrays.stream(p[4].split(";")).map(Type::GetType).toArray(Type[]::new);MethodInfo m=switch(p[3]){case "name"->owner.GetMethod(name);case "flags"->owner.GetMethod(name,flags);case "types"->owner.GetMethod(name,types);case "flags-types"->owner.GetMethod(name,flags,types);case "methods"->owner.GetMethods(flags)[0];case "ignore-case"->owner.GetMethod(name.toUpperCase(Locale.ROOT),flags.or(BindingFlags.IgnoreCase));default->throw new AssertionError(p[3]);};if(m==null||!m.get_Name().equals(name))throw new AssertionError(line);methods.add(m);calls++;
 }else{MethodInfo method=methods.get(Integer.parseInt(p[1]));ParameterInfo[] first=method.GetParameters(),second=method.GetParameters();boolean stable=true,membersSame=true;StringJoiner metadata=new StringJoiner(";");for(int i=0;i<first.length;i++){stable &= first[i]==second[i];membersSame &= first[i].get_Member()==method;metadata.add(first[i].get_Position()+"|"+first[i].get_ParameterType().get_FullName()+"|"+units(first[i].get_Name()));}ParameterInfo saved=first.length==0?null:first[0];if(first.length>0)first[0]=null;ParameterInfo[] third=method.GetParameters();boolean defensive=first.length==0||saved==third[0];ParameterInfo return1=method.get_ReturnParameter(),return2=method.get_ReturnParameter();Object[] actual={second.length,first==second,stable,defensive,membersSame,return1==return2,return1.get_Member()==method,return1.get_Position(),units(return1.get_Name()),metadata.toString()};for(int i=0;i<actual.length;i++){if(!actual[i].toString().equals(p[2+i]))throw new AssertionError(line+" field="+i+" actual="+actual[i]);groups++;}calls+=5;}}
 java.lang.System.out.println("PASS method equality calls="+calls+" groups="+groups);}
}
