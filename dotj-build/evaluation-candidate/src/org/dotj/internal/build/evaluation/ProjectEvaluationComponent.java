package org.dotj.internal.build.evaluation;

import java.io.IOException;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import javax.xml.XMLConstants;
import javax.xml.parsers.*;
import org.w3c.dom.*;
import org.xml.sax.*;

/** Internal bounded evaluation component; not a public Microsoft.Build facade or product license choice. */
final class ProjectEvaluationComponent {
    private ProjectEvaluationComponent() { }
    public static final class ProfileRejected extends IllegalArgumentException {
        public final String code;
        ProfileRejected(String code, String message) { super(message); this.code = code; }
    }
    public static final class EvaluationFailure extends IOException {
        public final String referenceCode;
        public final Path project;
        public final Path missingImport;
        EvaluationFailure(Path project, Path missing) {
            super("Declared local import does not exist: " + missing);
            referenceCode = "MSB4019"; this.project = project; missingImport = missing;
        }
    }
    public record Result(Map<String, String> escapedProperties, List<Path> evaluatedFiles) {
        public Result { escapedProperties = Map.copyOf(escapedProperties); evaluatedFiles = List.copyOf(evaluatedFiles); }
        public String property(String name) { return unescape(escapedProperties.getOrDefault(key(name), "")); }
    }
    private static final Pattern NAME = Pattern.compile("[A-Za-z_][A-Za-z0-9_]*");
    private static final Pattern EQUALITY = Pattern.compile("'([^']*)'\\s*==\\s*'([^']*)'");
    private static final Pattern EXISTS = Pattern.compile("Exists\\('([^']*)'\\)");
    private static final Pattern REFERENCE = Pattern.compile("\\$\\(([^)]*)\\)");
    private static ProfileRejected reject(String code, String why) { return new ProfileRejected(code, why); }
    private static String key(String input) {
        if (!NAME.matcher(input).matches()) throw reject("ASCII_PROPERTY_NAME", "Only explicit ASCII property identifiers are supported");
        String folded = asciiFold(input);
        if (folded.startsWith("MSBUILD")) throw reject("RESERVED_PROPERTY_UNQUALIFIED", "MSBuild reserved-property prelude is not implemented");
        return folded;
    }
    private static String asciiFold(String input) {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < input.length(); i++) {
            char c = input.charAt(i);
            if (c > 127) throw reject("UNICODE_COMPARISON", "Unicode OrdinalIgnoreCase research not qualified");
            result.append(c >= 'a' && c <= 'z' ? (char)(c - ('a' - 'A')) : c);
        }
        return result.toString();
    }
    private static String unescape(String value) {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            if (c != '%') { result.append(c); continue; }
            if (i + 2 >= value.length()) throw reject("ESCAPE_PROFILE", "Incomplete percent escape outside selected profile");
            String escape = asciiFold(value.substring(i + 1, i + 3));
            result.append(switch (escape) { case "25" -> '%'; case "3B" -> ';'; case "24" -> '$'; default -> throw reject("ESCAPE_PROFILE", "Only selected percent, semicolon and dollar escapes are qualified"); });
            i += 2;
        }
        return result.toString();
    }
    public static Result evaluate(Path project, Path sandbox, Map<String,String> globals) throws IOException {
        State state = new State(sandbox, globals);
        state.read(project.toAbsolutePath().normalize(), true);
        return new Result(state.properties, state.files);
    }
    private static final class State {
        final Path sandbox;
        final LinkedHashMap<String,String> properties = new LinkedHashMap<>();
        final Set<String> globalNames = new HashSet<>();
        final Set<String> localOverrides = new HashSet<>();
        final LinkedHashSet<Path> seen = new LinkedHashSet<>();
        final Set<Path> active = new HashSet<>();
        final List<Path> files = new ArrayList<>();
        State(Path sandbox, Map<String,String> globals) throws IOException {
            this.sandbox = sandbox.toRealPath();
            for (var entry : globals.entrySet()) {
                String name = key(entry.getKey());
                if (!globalNames.add(name)) throw reject("GLOBAL_COLLISION", "Case-colliding global properties");
                verifyScalar(entry.getValue()); properties.put(name, entry.getValue());
            }
        }
        void verifyScalar(String value) {
            if (value.contains("$([") || value.contains("@(") || value.contains("%(")) throw reject("PROPERTY_FUNCTION", "Property function evaluation is not implemented");
        }
        Path inside(Path value) throws IOException {
            Path normalized = value.toAbsolutePath().normalize();
            if (!normalized.startsWith(sandbox)) throw reject("IMPORT_BOUNDARY", "Path outside explicit fixture sandbox");
            Path existing = normalized;
            while (existing != null && !Files.exists(existing)) existing = existing.getParent();
            if (existing == null || !existing.toRealPath().startsWith(sandbox)) throw reject("IMPORT_BOUNDARY", "Resolved path leaves sandbox");
            return Files.exists(normalized) ? normalized.toRealPath() : normalized;
        }
        Path relative(Path owner, String input) throws IOException {
            if (input.isEmpty() || input.indexOf(':') >= 0 || input.indexOf('\\') >= 0 || input.startsWith("/"))
                throw reject("IMPORT_PATH_PROFILE", "Only nonempty relative slash paths supported");
            if (input.chars().anyMatch(c -> "*?;$%".indexOf(c) >= 0)) throw reject("IMPORT_PATH_PROFILE", "Lists/globs/escaped/dynamic imports not supported");
            return inside(owner.getParent().resolve(input));
        }
        void read(Path input, boolean main) throws IOException {
            Path file = inside(input);
            if (!Files.exists(file)) throw new EvaluationFailure(file, file);
            if (active.contains(file)) throw reject("IMPORT_CYCLE_UNQUALIFIED", "Cycle semantics remain outside selected profile");
            if (!seen.add(file)) throw reject("DUPLICATE_IMPORT_UNQUALIFIED", "Repeated-import policy remains outside selected profile");
            if (seen.size() > 16 || Files.size(file) > 65536) throw reject("INPUT_BOUND", "Bounded profile import/file size exceeded");
            active.add(file); files.add(file);
            try {
                Document document = parse(file); Element root = document.getDocumentElement();
                if (!root.getTagName().equals("Project") || root.getNamespaceURI() != null)
                    throw reject("PROJECT_ROOT", "Only plain namespace-free Project supported");
                attrs(root, Set.of("DefaultTargets","InitialTargets","TreatAsLocalProperty"));
                validateStructure(root);
                if (root.hasAttribute("TreatAsLocalProperty")) {
                    if (!main) throw reject("IMPORTED_LOCAL_OVERRIDE", "Imported TreatAsLocalProperty scope not qualified");
                    localOverrides.add(key(root.getAttribute("TreatAsLocalProperty")));
                }
                children(root, file);
            } finally { active.remove(file); }
        }
        Document parse(Path file) throws IOException {
            try {
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                factory.setNamespaceAware(true); factory.setXIncludeAware(false); factory.setExpandEntityReferences(false);
                factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
                factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
                factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
                factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, ""); factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
                DocumentBuilder builder = factory.newDocumentBuilder();
                builder.setEntityResolver((publicId,systemId) -> { throw new SAXException("External entities denied"); });
                builder.setErrorHandler(new org.xml.sax.helpers.DefaultHandler() {
                    @Override public void error(SAXParseException e) throws SAXException { throw e; }
                    @Override public void fatalError(SAXParseException e) throws SAXException { throw e; }
                });
                return builder.parse(file.toFile());
            } catch (ParserConfigurationException | SAXException exception) {
                throw reject("XML_PROFILE", "XML syntax/DTD/entities outside controlled profile: " + exception.getMessage());
            }
        }
        void attrs(Element element, Set<String> permitted) {
            NamedNodeMap attributes = element.getAttributes();
            for (int i=0;i<attributes.getLength();i++) {
                Node attribute = attributes.item(i); verifyScalar(attribute.getNodeValue());
                if (!permitted.contains(attribute.getNodeName())) throw reject("UNSUPPORTED_ATTRIBUTE", element.getTagName()+" attribute "+attribute.getNodeName());
                if (attribute.getNodeName().equals("Condition")) validateCondition(attribute.getNodeValue());
            }
        }
        List<Element> elements(Element parent) {
            List<Element> result = new ArrayList<>();
            for (Node n=parent.getFirstChild();n!=null;n=n.getNextSibling()) {
                if (n instanceof Element element) result.add(element);
                else if ((n.getNodeType()==Node.TEXT_NODE || n.getNodeType()==Node.CDATA_SECTION_NODE) && !n.getNodeValue().isBlank())
                    throw reject("STRUCTURAL_TEXT", "Unexpected structural text");
                else if (n.getNodeType()!=Node.TEXT_NODE && n.getNodeType()!=Node.COMMENT_NODE && n.getNodeType()!=Node.CDATA_SECTION_NODE)
                    throw reject("XML_NODE", "Unsupported XML node");
            }
            return result;
        }
        void validateStructure(Element root) {
            for (Element child : elements(root)) {
                switch (child.getTagName()) {
                    case "PropertyGroup" -> {
                        attrs(child, Set.of("Condition"));
                        for (Element property : elements(child)) {
                            key(property.getTagName()); attrs(property, Set.of("Condition"));
                            verifyScalar(property.getTextContent());
                            if (property.getElementsByTagName("*").getLength()!=0)
                                throw reject("PROPERTY_XML", "Nested property XML unsupported even in skipped groups");
                        }
                    }
                    case "Import" -> validateImport(child);
                    case "ImportGroup" -> {
                        attrs(child, Set.of("Condition"));
                        for (Element element : elements(child)) {
                            if (!element.getTagName().equals("Import")) throw reject("IMPORT_GROUP_CHILD", "Only Import child supported");
                            validateImport(element);
                        }
                    }
                    case "Target" -> inertTarget(child);
                    default -> throw reject("UNSUPPORTED_ELEMENT", "Feature outside selected profile: " + child.getTagName());
                }
            }
        }
        void validateImport(Element element) {
            attrs(element, Set.of("Project", "Condition"));
            if (!elements(element).isEmpty()) throw reject("IMPORT_CHILD", "Import children unsupported");
            String path = element.getAttribute("Project");
            if (path.isEmpty() || path.chars().anyMatch(c -> "*?;$%".indexOf(c)>=0))
                throw reject("IMPORT_PATH_PROFILE", "Missing/dynamic/list/glob import outside profile");
        }
        void children(Element parent, Path owner) throws IOException {
            for (Element child : elements(parent)) {
                switch(child.getTagName()) {
                    case "PropertyGroup" -> propertyGroup(child, owner);
                    case "Import" -> importFile(child, owner);
                    case "ImportGroup" -> {
                        attrs(child, Set.of("Condition"));
                        if (condition(child.getAttribute("Condition"),owner)) {
                            for(Element element:elements(child)) {
                                if(!element.getTagName().equals("Import")) throw reject("IMPORT_GROUP_CHILD", "Only Import child supported");
                                importFile(element,owner);
                            }
                        }
                    }
                    case "Target" -> inertTarget(child);
                    default -> throw reject("UNSUPPORTED_ELEMENT", "Evaluation feature outside selected profile: "+child.getTagName());
                }
            }
        }
        void propertyGroup(Element group, Path owner) throws IOException {
            attrs(group, Set.of("Condition"));
            if (!condition(group.getAttribute("Condition"),owner)) return;
            for (Element property : elements(group)) {
                String name=key(property.getTagName()); attrs(property,Set.of("Condition"));
                if (globalNames.contains(name) && !localOverrides.contains(name)) continue;
                if (!condition(property.getAttribute("Condition"),owner)) continue;
                if (property.getElementsByTagName("*").getLength()!=0) throw reject("PROPERTY_XML", "Nested property XML not supported");
                String value=expand(property.getTextContent());unescape(value);properties.put(name,value);
            }
        }
        void importFile(Element element, Path owner) throws IOException {
            attrs(element,Set.of("Project","Condition"));
            if(!elements(element).isEmpty()) throw reject("IMPORT_CHILD", "Import children not supported");
            if(!condition(element.getAttribute("Condition"),owner))return;
            Path path=relative(owner,element.getAttribute("Project"));
            if(!Files.exists(path))throw new EvaluationFailure(owner,path);
            read(path,false);
        }
        String expand(String value) {
            verifyScalar(value);StringBuilder result=new StringBuilder();int cursor=0;
            while(cursor<value.length()) {
                int start=value.indexOf("$(",cursor);
                if(start<0){result.append(value,cursor,value.length());break;}
                result.append(value,cursor,start);int end=value.indexOf(')',start+2);
                if(end<0)throw reject("PROPERTY_REFERENCE", "Unclosed property reference");
                String name=key(value.substring(start+2,end));result.append(properties.getOrDefault(name,""));cursor=end+1;
            }
            return result.toString();
        }
        boolean condition(String raw, Path owner) throws IOException {
            if(raw.isEmpty())return true;
            String value=unescape(expand(raw)).trim();
            if(value.equals("true"))return true;if(value.equals("false"))return false;
            Matcher exists=EXISTS.matcher(value);
            if(exists.matches())return Files.exists(relative(owner,exists.group(1)));
            Matcher eq=EQUALITY.matcher(value);
            if(!eq.matches())throw reject("CONDITION_PROFILE", "Only literal true/false, selected Exists and quoted string equality supported");
            return equality(eq);
        }
        void validateCondition(String raw) {
            if (raw.isEmpty()) return;
            // Validate syntax without reading properties or probing files. Expansion still occurs
            // at the original evaluation point; skipped groups cannot conceal unknown syntax.
            Matcher references = REFERENCE.matcher(raw);
            StringBuilder template = new StringBuilder();
            while (references.find()) {
                key(references.group(1));
                references.appendReplacement(template, "");
            }
            references.appendTail(template);
            if (template.indexOf("$(") >= 0) throw reject("PROPERTY_REFERENCE", "Unclosed property reference");
            String value = unescape(template.toString()).trim();
            if (value.equals("true") || value.equals("false") || EXISTS.matcher(value).matches()) return;
            Matcher equality = EQUALITY.matcher(value);
            if (!equality.matches()) throw reject("CONDITION_PROFILE", "Condition syntax outside selected profile");
            equality(equality);
        }
        boolean equality(Matcher eq) {
            String left=asciiFold(eq.group(1)),right=asciiFold(eq.group(2));
            Set<String> boolAliases=Set.of("TRUE","FALSE","ON","OFF","YES","NO");
            for(String operand:List.of(left,right))
                if(!operand.matches("[A-Z]*") || boolAliases.contains(operand))
                    throw reject("CONDITION_COERCION", "Numeric/version/bool/other comparison coercion not qualified");
            return left.equals(right);
        }
        void inertTarget(Element target) {
            attrs(target,Set.of("Name"));key(target.getAttribute("Name"));
            for(Element task:elements(target)) {
                switch(task.getTagName()) {
                    case "WriteLinesToFile" -> attrs(task,Set.of("File","Lines","Overwrite"));
                    case "Error" -> attrs(task,Set.of("Text"));
                    default -> throw reject("TARGET_DECLARATION_PROFILE", "Unsupported inert target declaration");
                }
                if(!elements(task).isEmpty())throw reject("TARGET_DECLARATION_PROFILE", "Nested task content unsupported");
            }
            // Intentionally no task registry, invocation, network, restore or process API.
        }
    }
}
