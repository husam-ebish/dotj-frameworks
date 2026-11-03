package org.dotj.internal.build.evaluation;

import java.util.*;
import java.util.function.Function;
import java.util.regex.Pattern;

/** Escaped, single-pass expressions. Admission is a site rule, never a cached AST property. */
final class ItemExpressions {
    enum Site {
        PROPERTY_DATA(false, false), GROUP(true, false), ITEM(true, false),
        DEFINITION_GROUP(false, false), DEFINITION(false, true), METADATA(true, true);
        final boolean items, metadata;
        Site(boolean items, boolean metadata) { this.items=items; this.metadata=metadata; }
    }
    private static final Pattern NAME=Pattern.compile("[A-Za-z_][A-Za-z0-9_]*");
    private static final Set<String> ESCAPES=Set.of("25","2A","3F","40","24","28","29","3B","27");
    static String key(String name) {
        if(!NAME.matcher(name).matches())throw fail("ITEM_NAME", "Only ASCII item and metadata identifiers are selected");
        return name.toUpperCase(Locale.ROOT);
    }
    static ProjectEvaluationComponent.ProfileRejected fail(String code,String message) {
        return new ProjectEvaluationComponent.ProfileRejected(code,message);
    }
    static void ascii(String value) {
        for(int i=0;i<value.length();i++)if(value.charAt(i)>126 || value.charAt(i)<32)
            throw fail("ITEM_ASCII", "Reached item data must be printable ASCII");
    }
    static void validate(String raw, Site site, String type) {
        if(raw.contains("$(["))throw fail("PROPERTY_FUNCTION", "Property functions are not selected");
        for(int i=0;i<raw.length();i++) {
            char c=raw.charAt(i);
            if(c=='%' && i+1<raw.length() && raw.charAt(i+1)!='(') {
                if(i+2>=raw.length() || !ESCAPES.contains(raw.substring(i+1,i+3).toUpperCase(Locale.ROOT)))
                    throw fail("ITEM_ESCAPE", "Unselected item escape");
                i+=2; continue;
            }
            if((c=='$'||c=='@'||c=='%') && i+1<raw.length() && raw.charAt(i+1)=='(') {
                int end=raw.indexOf(')',i+2);
                if(end<0)throw fail("ITEM_REFERENCE", "Unclosed reference");
                String name=raw.substring(i+2,end);
                if(c=='$')ProjectEvaluationComponent.key(name);
                else if(c=='@') {
                    key(name);
                    if(!site.items && site!=Site.PROPERTY_DATA)throw fail("ITEM_REFERENCE_CONTEXT", "Item references are forbidden at this site");
                } else {
                    if(!site.metadata)throw fail("METADATA_REFERENCE_CONTEXT", "Metadata references are forbidden at this site");
                    String[] parts=name.split("\\.",-1);
                    if(parts.length>2)throw fail("ITEM_REFERENCE", "Malformed qualified metadata");
                    if(parts.length==2 && (type==null || !key(parts[0]).equals(key(type))))
                        throw fail("METADATA_QUALIFIER", "Cross-item metadata is not selected");
                    String metadata=parts[parts.length-1];key(metadata);
                    if(ItemSnapshot.timestamp(metadata))throw fail("METADATA_TIMESTAMP", "Timestamp metadata is not selected");
                    if(site==Site.DEFINITION && ItemSnapshot.builtIn(metadata))
                        throw fail("DEFINITION_BUILTIN", "Built-ins are not selected in definitions");
                }
                i=end;
            } else if(c=='%')throw fail("ITEM_ESCAPE", "Incomplete percent escape");
        }
    }
    static String replace(String raw,char sigil,Function<String,String> values) {
        StringBuilder result=new StringBuilder();int cursor=0;
        while(cursor<raw.length()) {
            int start=raw.indexOf(""+sigil+'(',cursor);
            if(start<0){result.append(raw,cursor,raw.length());break;}
            int end=raw.indexOf(')',start+2);
            if(end<0)throw fail("ITEM_REFERENCE", "Unclosed reference");
            result.append(raw,cursor,start).append(values.apply(raw.substring(start+2,end)));cursor=end+1;
        }
        return result.toString();
    }
    static String expand(String raw,Site site,String type,Map<String,String> properties,
                         Function<String,String> metadata,Function<String,String> items) {
        validate(raw,site,type);
        String value=site.metadata?replace(raw,'%',metadata):raw;
        value=replace(value,'$',name->properties.getOrDefault(ProjectEvaluationComponent.key(name),""));
        // Only the next stage sees inserted syntax. No recursive property or metadata expansion.
        if(site.items) {
            validate(value,site,type);
            value=replace(value,'@',items);
        }
        ascii(value);return value;
    }
    static List<String> fragments(String value) {
        List<String> result=new ArrayList<>();
        for(String part:value.split(";",-1)) { part=part.trim();if(!part.isEmpty())result.add(part); }
        return result;
    }
    static String decode(String escaped) {
        StringBuilder result=new StringBuilder();
        for(int i=0;i<escaped.length();i++) {
            char c=escaped.charAt(i);
            if(c=='%') {
                if(i+2>=escaped.length())throw fail("ITEM_ESCAPE", "Incomplete percent escape");
                String hex=escaped.substring(i+1,i+3).toUpperCase(Locale.ROOT);
                if(!ESCAPES.contains(hex))throw fail("ITEM_ESCAPE", "Unselected item escape");
                c=(char)Integer.parseInt(hex,16);i+=2;
            }
            result.append(c);
        }
        ascii(result.toString());return result.toString();
    }
    static String escape(String value) {
        StringBuilder out=new StringBuilder();
        for(char c:value.toCharArray()) {
            if("%*?@$();'".indexOf(c)>=0)out.append('%').append(String.format(Locale.ROOT,"%02X",(int)c));
            else out.append(c);
        }
        return out.toString();
    }
    private ItemExpressions() { }
}
