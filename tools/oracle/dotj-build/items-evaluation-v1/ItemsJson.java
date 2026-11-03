package org.dotj.internal.build.evaluation;

import java.util.*;

/** Test wire format only; no dependency enters the product module. */
final class ItemsJson {
    static Map<String,Object> object(Object... entries) {
        Map<String,Object> result=new LinkedHashMap<>();
        for(int i=0;i<entries.length;i+=2)result.put((String)entries[i],entries[i+1]);return result;
    }
    @SuppressWarnings("unchecked") static Map<String,Object> map(Object value) { return (Map<String,Object>)value; }
    @SuppressWarnings("unchecked") static List<Object> list(Object value) { return (List<Object>)value; }
    static String write(Object value) {
        if(value==null)return "null";
        if(value instanceof Boolean||value instanceof Number)return value.toString();
        if(value instanceof String text) {
            StringBuilder out=new StringBuilder("\"");
            for(char c:text.toCharArray()) {
                if(c=='"'||c=='\\')out.append('\\').append(c);
                else if(c<32)out.append(String.format(Locale.ROOT,"\\u%04x",(int)c));
                else out.append(c);
            }
            return out.append('"').toString();
        }
        if(value instanceof Map<?,?> map) {
            StringJoiner out=new StringJoiner(",","{","}");
            for(var entry:map.entrySet())out.add(write(entry.getKey())+":"+write(entry.getValue()));return out.toString();
        }
        if(value instanceof Collection<?> list) { StringJoiner out=new StringJoiner(",","[","]");for(Object entry:list)out.add(write(entry));return out.toString(); }
        throw new IllegalArgumentException("Unsupported wire value "+value.getClass());
    }
    static Object read(String text) {
        Parser parser=new Parser(text);Object value=parser.value();parser.space();
        if(parser.cursor!=text.length())throw new IllegalArgumentException("Trailing JSON");return value;
    }
    private static final class Parser {
        final String text;int cursor;
        Parser(String text) { this.text=text; }
        void space() { while(cursor<text.length()&&Character.isWhitespace(text.charAt(cursor)))cursor++; }
        boolean take(char c) { space();if(cursor<text.length()&&text.charAt(cursor)==c){cursor++;return true;}return false; }
        void require(char c) { if(!take(c))throw new IllegalArgumentException("Expected "+c+" at "+cursor); }
        Object value() {
            space();char c=text.charAt(cursor);
            if(c=='"')return string();
            if(take('{')) {
                Map<String,Object> map=new LinkedHashMap<>();if(take('}'))return map;
                do { String key=string();require(':');if(map.put(key,value())!=null)throw new IllegalArgumentException("Duplicate key"); }while(take(','));
                require('}');return map;
            }
            if(take('[')) { List<Object> list=new ArrayList<>();if(take(']'))return list;do{list.add(value());}while(take(','));require(']');return list; }
            for(String token:List.of("true","false","null"))if(text.startsWith(token,cursor)) {
                cursor+=token.length();return token.equals("null")?null:Boolean.valueOf(token);
            }
            int start=cursor;while(cursor<text.length()&&"-0123456789.eE+".indexOf(text.charAt(cursor))>=0)cursor++;
            if(start==cursor)throw new IllegalArgumentException("JSON value at "+cursor);
            return Long.valueOf(text.substring(start,cursor));
        }
        String string() {
            require('"');StringBuilder out=new StringBuilder();
            while(cursor<text.length()) {
                char c=text.charAt(cursor++);if(c=='"')return out.toString();
                if(c=='\\') {
                    c=text.charAt(cursor++);
                    c=switch(c) {
                        case '"','\\','/' -> c;case 'b' -> '\b';case 'f' -> '\f';case 'n' -> '\n';case 'r' -> '\r';case 't' -> '\t';
                        case 'u' -> { char decoded=(char)Integer.parseInt(text.substring(cursor,cursor+4),16);cursor+=4;yield decoded; }
                        default -> throw new IllegalArgumentException("JSON escape");
                    };
                }
                out.append(c);
            }
            throw new IllegalArgumentException("Unclosed JSON string");
        }
    }
}
