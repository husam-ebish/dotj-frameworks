package org.dotj.internal.build.evaluation;

import java.io.IOException;
import java.nio.file.Path;
import java.util.*;
import java.util.function.Function;
import org.w3c.dom.*;
import static org.dotj.internal.build.evaluation.ItemExpressions.Site.*;

/** Deferred definition and item passes over source-owned DOM sites. */
final class ItemEvaluator {
    record Site(Element element,Path owner) { }
    record Output(List<ItemSnapshot> items,Map<String,ItemSnapshot.Definition> definitions) {
        Output { items=List.copyOf(items);definitions=ItemSnapshot.freeze(definitions); }
        static Output empty() { return new Output(List.of(),Map.of()); }
        List<ItemSnapshot> items(String type) {
            String key=ItemExpressions.key(type);
            return items.stream().filter(i->ItemExpressions.key(i.itemType()).equals(key)).toList();
        }
    }
    final ProjectEvaluationComponent.State state;
    final List<Site> definitions=new ArrayList<>(), groups=new ArrayList<>();
    final Map<String,ItemSnapshot.Definition> defaults=new LinkedHashMap<>();
    final List<ItemSnapshot> live=new ArrayList<>();
    ItemGlobs globs;
    int operations;
    ItemEvaluator(ProjectEvaluationComponent.State state) { this.state=state; }
    void record(Element element,Path owner) {
        (element.getTagName().equals("ItemDefinitionGroup")?definitions:groups).add(new Site(element,owner));
    }
    void validateGroup(Element group) {
        boolean definition=group.getTagName().equals("ItemDefinitionGroup");
        attributes(group,Set.of("Condition"),definition?DEFINITION_GROUP:GROUP,null);
        for(Element item:state.elements(group)) {
            if(++operations>512)throw ItemExpressions.fail("ITEM_OPERATION_BOUND", "More than 512 item or definition operations");
            String type=item.getTagName();ItemExpressions.key(type);
            attributes(item,definition?Set.of("Condition"):Set.of("Condition","Include","Exclude","Update","Remove"),definition?DEFINITION:ITEM,type);
            if(!definition) {
                int count=0;for(String operation:List.of("Include","Update","Remove"))if(item.hasAttribute(operation))count++;
                if(count!=1 || item.hasAttribute("Exclude")&&!item.hasAttribute("Include"))
                    throw ItemExpressions.fail("ITEM_OPERATION", "Exactly one Include, Update or Remove is required; Exclude belongs to Include");
                for(String attribute:List.of("Include","Exclude","Update","Remove"))if(item.hasAttribute(attribute))validateSpec(item.getAttribute(attribute));
            }
            List<Element> metadata=state.elements(item);
            if(!definition&&item.hasAttribute("Remove")&&!metadata.isEmpty())
                throw ItemExpressions.fail("ITEM_REMOVE_METADATA", "Remove metadata is not selected");
            for(Element value:metadata) {
                String name=value.getTagName();ItemExpressions.key(name);
                if(ItemSnapshot.builtIn(name)||ItemSnapshot.timestamp(name))
                    throw ItemExpressions.fail("METADATA_RESERVED", "Built-in metadata cannot be assigned");
                attributes(value,Set.of("Condition"),definition?DEFINITION:METADATA,type);
                if(value.getElementsByTagName("*").getLength()!=0)throw ItemExpressions.fail("METADATA_XML", "Nested metadata XML is not selected");
                ItemExpressions.validate(value.getTextContent(),definition?DEFINITION:METADATA,type);
            }
        }
    }
    private void attributes(Element element,Set<String> allowed,ItemExpressions.Site context,String type) {
        NamedNodeMap attributes=element.getAttributes();
        for(int i=0;i<attributes.getLength();i++) {
            Node attribute=attributes.item(i);
            if(!allowed.contains(attribute.getNodeName()))throw ItemExpressions.fail("UNSUPPORTED_ATTRIBUTE", element.getTagName()+" attribute "+attribute.getNodeName());
            ItemExpressions.validate(attribute.getNodeValue(),context,type);
            if(attribute.getNodeName().equals("Condition"))state.validateCondition(attribute.getNodeValue());
        }
    }
    private void validateSpec(String raw) {
        for(String fragment:ItemExpressions.fragments(raw)) {
            if(fragment.contains("@(") && !(fragment.startsWith("@(")&&fragment.endsWith(")")&&fragment.indexOf(')')==fragment.length()-1))
                throw ItemExpressions.fail("ITEM_MIXED_VECTOR", "Item spec vectors must occupy a whole fragment");
            if(ItemGlobs.wildcard(fragment))ItemGlobs.validate(fragment);
        }
    }
    Output evaluate() throws IOException {
        globs=new ItemGlobs(state.rootProject.getParent(),state.sandbox);
        for(Site site:definitions)evaluateDefinitions(site);
        for(Site site:groups)evaluateGroup(site);
        // ItemDictionary enumerates per-type lists created by final surviving materialization.
        // This selected ordering is not a general public inter-type ordering guarantee.
        Map<String,List<ItemSnapshot>> types=new LinkedHashMap<>();
        for(ItemSnapshot item:live)types.computeIfAbsent(ItemExpressions.key(item.itemType()),unused->new ArrayList<>()).add(item);
        List<ItemSnapshot> items=new ArrayList<>();types.values().forEach(items::addAll);
        return new Output(items,defaults);
    }
    private boolean condition(Element element,ItemExpressions.Site context,String type,
                              Function<String,String> metadata,List<ItemSnapshot> prior) throws IOException {
        String raw=element.getAttribute("Condition");ItemExpressions.validate(raw,context,type);
        return state.itemCondition(element,state.rootProject,(context.items?1:0)|(context.metadata?2:0),
            text->ItemExpressions.expand(text,context,type,state.properties,metadata,name->vector(prior,name)),
            ()->ItemExpressions.validate(raw,context,type));
    }
    private static String vector(List<ItemSnapshot> prior,String type) {
        String key=ItemExpressions.key(type);StringJoiner value=new StringJoiner(";");
        for(ItemSnapshot item:prior)if(ItemExpressions.key(item.itemType()).equals(key))value.add(item.escapedInclude);
        return value.toString();
    }
    private String expand(String value,ItemExpressions.Site context,String type,Function<String,String> metadata,List<ItemSnapshot> prior) {
        return ItemExpressions.expand(value,context,type,state.properties,metadata,name->vector(prior,name));
    }
    private static String defaultValue(Map<String,ItemSnapshot.Metadata> metadata,String qualified) {
        String name=qualified.substring(qualified.lastIndexOf('.')+1);
        ItemSnapshot.Metadata value=metadata.get(ItemExpressions.key(name));return value==null?"":value.escapedValue();
    }
    private void evaluateDefinitions(Site site) throws IOException {
        if(!condition(site.element(),DEFINITION_GROUP,null,name->"",List.of()))return;
        for(Element element:state.elements(site.element())) {
            String type=element.getTagName(),key=ItemExpressions.key(type);
            ItemSnapshot.Definition old=defaults.get(key);
            Map<String,ItemSnapshot.Metadata> metadata=new LinkedHashMap<>(old==null?Map.of():old.metadata());
            if(!condition(element,DEFINITION,type,name->defaultValue(metadata,name),List.of()))continue;
            for(Element child:state.elements(element)) {
                if(!condition(child,DEFINITION,type,name->defaultValue(metadata,name),List.of()))continue;
                String value=expand(child.getTextContent(),DEFINITION,type,name->defaultValue(metadata,name),List.of());
                ItemExpressions.decode(value);
                metadata.put(ItemExpressions.key(child.getTagName()),new ItemSnapshot.Metadata(child.getTagName(),value));
                if(metadata.size()>64)throw ItemExpressions.fail("ITEM_METADATA_BOUND", "More than 64 default metadata entries");
            }
            defaults.put(key,new ItemSnapshot.Definition(old==null?type:old.itemType(),metadata));
        }
    }
    private Map<String,ItemSnapshot.Metadata> defaults(String type) {
        ItemSnapshot.Definition value=defaults.get(ItemExpressions.key(type));return value==null?Map.of():value.metadata();
    }
    private void evaluateGroup(Site site) throws IOException {
        if(!condition(site.element(),GROUP,null,name->"",List.copyOf(live)))return;
        for(Element element:state.elements(site.element())) {
            String type=element.getTagName(),key=ItemExpressions.key(type);
            List<ItemSnapshot> prior=List.copyOf(live);
            if(!condition(element,ITEM,type,name->"",prior))continue;
            if(element.hasAttribute("Include")) {
                List<ItemSnapshot> candidates=include(element.getAttribute("Include"),type,site.owner(),prior);
                List<String> excludes=spec(element.getAttribute("Exclude"),prior);
                for(ItemSnapshot item:candidates)if(!selected(excludes,item)) {
                    live.add(metadata(element,item,prior));
                    if(live.size()>1024)throw ItemExpressions.fail("ITEM_LIVE_BOUND", "More than 1024 live item occurrences");
                }
            } else {
                boolean remove=element.hasAttribute("Remove");
                List<String> selectors=spec(element.getAttribute(remove?"Remove":"Update"),prior);
                List<ItemSnapshot> result=new ArrayList<>();
                for(ItemSnapshot item:prior) {
                    if(ItemExpressions.key(item.itemType()).equals(key)&&selected(selectors,item)) {
                        if(!remove)result.add(metadata(element,item,prior));
                    } else result.add(item);
                }
                live.clear();live.addAll(result);
            }
        }
    }
    private String propertySpec(String raw) {
        ItemExpressions.validate(raw,ITEM,null);
        String value=ItemExpressions.replace(raw,'$',name->state.properties.getOrDefault(ProjectEvaluationComponent.key(name),""));
        ItemExpressions.validate(value,ITEM,null);ItemExpressions.ascii(value);validateSpec(value);return value;
    }
    private List<String> spec(String raw,List<ItemSnapshot> prior) {
        List<String> result=new ArrayList<>();
        for(String fragment:ItemExpressions.fragments(propertySpec(raw))) {
            if(fragment.startsWith("@(")) {
                String type=ItemExpressions.key(fragment.substring(2,fragment.length()-1));
                for(ItemSnapshot item:prior)if(ItemExpressions.key(item.itemType()).equals(type))result.add(item.escapedInclude);
            } else result.add(fragment);
        }
        return result;
    }
    private List<ItemSnapshot> include(String raw,String type,Path owner,List<ItemSnapshot> prior) throws IOException {
        List<ItemSnapshot> result=new ArrayList<>();
        for(String fragment:ItemExpressions.fragments(propertySpec(raw))) {
            if(fragment.startsWith("@(")) {
                String source=ItemExpressions.key(fragment.substring(2,fragment.length()-1));
                for(ItemSnapshot item:prior)if(ItemExpressions.key(item.itemType()).equals(source))result.add(item.copy(type,owner,defaults(type)));
            } else if(ItemGlobs.wildcard(fragment)) {
                for(ItemGlobs.Match match:globs.enumerate(fragment))result.add(new ItemSnapshot(type,match.escapedIdentity(),match.recursiveDir(),state.rootProject.getParent(),owner,defaults(type),List.of(),Map.of()));
            } else {
                ItemExpressions.decode(fragment);
                result.add(new ItemSnapshot(type,fragment,"",state.rootProject.getParent(),owner,defaults(type),List.of(),Map.of()));
            }
            if(result.size()>1024)throw ItemExpressions.fail("ITEM_LIVE_BOUND", "More than 1024 Include candidates");
        }
        return result;
    }
    private boolean selected(List<String> selectors,ItemSnapshot item) {
        for(String pattern:selectors) {
            if(ItemGlobs.wildcard(pattern)) { if(ItemGlobs.matches(pattern,item.evaluatedInclude()))return true; }
            else if(ItemExpressions.decode(pattern).replace('\\','/').equalsIgnoreCase(item.evaluatedInclude().replace('\\','/')))return true;
        }
        return false;
    }
    private ItemSnapshot metadata(Element element,ItemSnapshot item,List<ItemSnapshot> prior) throws IOException {
        for(Element child:state.elements(element)) {
            ItemSnapshot current=item;
            if(!condition(child,METADATA,item.itemType(),current::escapedMetadata,prior))continue;
            String value=expand(child.getTextContent(),METADATA,item.itemType(),current::escapedMetadata,prior);
            ItemExpressions.decode(value);item=item.withMetadata(child.getTagName(),value);
        }
        return item;
    }
}
