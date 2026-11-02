package org.dotj.internal.build.evaluation;

import java.io.IOException;
import java.io.ByteArrayInputStream;
import java.nio.ByteBuffer;
import java.nio.charset.*;
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
    enum ImportProfile { DEFAULT, RECORD_DUPLICATES, REJECT_CIRCULAR }
    enum DiagnosticKind { WARNING, ERROR }
    enum ContextKind { ROOT, PREVIOUS, CIRCULAR, MISSING, INVALID }
    enum FailureReason { MISSING_IMPORT, CIRCULAR_IMPORT, INVALID_IMPORT_EXPRESSION }
    public static final class EvaluationFailure extends IOException {
        public final FailureReason reason;
        public final String referenceCode;
        public final Path project;
        public final Path importedProject;
        public final Path missingImport;
        public final WarningPosition current;
        public final List<DuplicateImport> diagnostics;
        EvaluationFailure(Path project, Path missing) {
            this(FailureReason.MISSING_IMPORT, "MSB4019", project, missing,
                 new WarningPosition(0,0,0,0), List.of());
        }
        EvaluationFailure(FailureReason reason, String code, Path project, Path imported,
                          WarningPosition current, List<DuplicateImport> diagnostics) {
            super(switch(reason) {
                case MISSING_IMPORT -> "Declared local import does not exist: " + imported;
                case CIRCULAR_IMPORT -> "Circular local import: " + imported;
                case INVALID_IMPORT_EXPRESSION -> "Evaluated Import Project expression is empty";
            });
            this.reason = reason; referenceCode = code; this.project = project; importedProject = imported;
            missingImport = reason == FailureReason.MISSING_IMPORT ? imported : null;
            this.current = current; this.diagnostics = List.copyOf(diagnostics);
        }
    }
    private record WarningPosition(int line, int column, int endLine, int endColumn) { }
    private record ImportSite(Path owner, int line, int column) { }
    record ImportEdge(Path owner, Path target, int line, int column) { }
    // Historical private notice name. Circular contexts carry only owner/target/current;
    // rootContext is a root path, and neither context invents previous sites or chains.
    public record DuplicateImport(String referenceCode, Path owner, Path importedProject,
                                  WarningPosition current, ImportSite previous, Path rootContext,
                                  DiagnosticKind kind, ContextKind contextKind) { }
    public record ConditionWarning(String referenceCode, Path file, int line, int column, String condition) { }
    public record Result(Map<String, String> escapedProperties, List<Path> evaluatedFiles,
                         List<DuplicateImport> duplicateImports, List<ImportEdge> imports,
                         List<ImportEdge> importsIncludingDuplicates, List<ConditionWarning> conditionWarnings) {
        public Result {
            conditionWarnings = List.copyOf(conditionWarnings);
            escapedProperties = Map.copyOf(escapedProperties); evaluatedFiles = List.copyOf(evaluatedFiles);
            duplicateImports = List.copyOf(duplicateImports); imports = List.copyOf(imports);
            // Null explicitly means unavailable for this profile; an available empty list stays empty.
            if (importsIncludingDuplicates != null) importsIncludingDuplicates = List.copyOf(importsIncludingDuplicates);
        }
        public String property(String name) { return unescape(escapedProperties.getOrDefault(key(name), "")); }
    }
    private static final Pattern NAME = Pattern.compile("[A-Za-z_][A-Za-z0-9_]*");
    private static final Pattern EXISTS = Pattern.compile("Exists\\('([^']*)'\\)");
    private static final Pattern HAS_TRAILING_SLASH = Pattern.compile("HasTrailingSlash\\('([^']*)'\\)", Pattern.CASE_INSENSITIVE);
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
        return evaluate(project, sandbox, globals, ImportProfile.DEFAULT);
    }
    static Result evaluate(Path project, Path sandbox, Map<String,String> globals, ImportProfile profile) throws IOException {
        if (profile == null) throw reject("IMPORT_PROFILE", "An explicit supported import profile is required");
        State state = new State(sandbox, globals, profile);
        state.read(project.toAbsolutePath().normalize(), true);
        return new Result(state.properties, state.files, state.duplicates, state.imports,
                          profile == ImportProfile.RECORD_DUPLICATES ? state.recordedImports : null, state.conditionWarnings);
    }
    private static final class State {
        final Path sandbox;
        Path rootProject;
        final ImportProfile profile;
        final List<ImportEdge> imports = new ArrayList<>();
        final List<ImportEdge> recordedImports = new ArrayList<>();
        final LinkedHashMap<String,String> properties = new LinkedHashMap<>();
        final Set<String> globalNames = new HashSet<>();
        final Set<String> localOverrides = new HashSet<>();
        final LinkedHashSet<Path> seen = new LinkedHashSet<>();
        final List<Path> files = new ArrayList<>();
        final List<DuplicateImport> duplicates = new ArrayList<>();
        final List<ConditionWarning> conditionWarnings = new ArrayList<>();
        final Map<Element,ImportSite> conditionSites = new IdentityHashMap<>();
        final Map<Element,ImportSite> sourceSites = new IdentityHashMap<>();
        final Map<Path,ImportSite> firstImports = new HashMap<>();
        State(Path sandbox, Map<String,String> globals, ImportProfile profile) throws IOException {
            this.profile = profile;
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
            if (input.chars().anyMatch(c -> "*?;$%".indexOf(c) >= 0)) throw reject("IMPORT_PATH_PROFILE", "Lists/globs/escaped or residual-dollar import paths not supported");
            return inside(owner.getParent().resolve(input));
        }
        void read(Path input, boolean main) throws IOException {
            Path file = inside(input);
            if (!Files.exists(file)) throw new EvaluationFailure(file, file);
            if (main) rootProject = file;
            if (!seen.add(file)) return;
            if (seen.size() > 16 || Files.size(file) > 65536) throw reject("INPUT_BOUND", "Bounded profile import/file size exceeded");
            files.add(file);
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
                byte[] bytes = Files.readAllBytes(file);
                Document document = builder.parse(new ByteArrayInputStream(bytes),file.toUri().toString());
                SourceIndex.attach(document,bytes,file,sourceSites,conditionSites);
                return document;
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
            if (path.isEmpty() || path.indexOf(':') >= 0 || path.indexOf('\\') >= 0 || path.startsWith("/"))
                throw reject("IMPORT_PATH_PROFILE", "Only nonempty relative slash expressions supported");
            // Grammar only: no property reads, expansion or filesystem probes while parsing.
            for (int cursor=0;cursor<path.length();) {
                char c=path.charAt(cursor);
                if(c=='$' && path.startsWith("$(",cursor)) {
                    int end=path.indexOf(')',cursor+2);
                    if(end<0)throw reject("PROPERTY_REFERENCE", "Unclosed import property reference");
                    key(path.substring(cursor+2,end));cursor=end+1;
                } else {
                    if("*?;$%".indexOf(c)>=0)throw reject("IMPORT_PATH_PROFILE", "Import list/glob/escaped/dollar syntax outside profile");
                    cursor++;
                }
            }
        }
        void children(Element parent, Path owner) throws IOException {
            for (Element child : elements(parent)) {
                switch(child.getTagName()) {
                    case "PropertyGroup" -> propertyGroup(child, owner);
                    case "Import" -> importFile(child, owner);
                    case "ImportGroup" -> {
                        attrs(child, Set.of("Condition"));
                        if (condition(child,owner)) {
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
            if (!condition(group,owner)) return;
            for (Element property : elements(group)) {
                String name=key(property.getTagName()); attrs(property,Set.of("Condition"));
                if (globalNames.contains(name) && !localOverrides.contains(name)) continue;
                // Individual property conditions use the main project directory. Group/import
                // conditions and Import Project resolution retain their defining-file owner.
                if (!condition(property,rootProject)) continue;
                if (property.getElementsByTagName("*").getLength()!=0) throw reject("PROPERTY_XML", "Nested property XML not supported");
                String value=expand(property.getTextContent());unescape(value);properties.put(name,value);
            }
        }
        private static boolean importWhiteSpace(char c) {
            // Exact .NET 10.0.12 Char.IsWhiteSpace BMP set, captured for FR-18-01.
            // Java trim/strip/isBlank differ (notably NBSP, NEL and U+001C).
            return c >= 0x0009 && c <= 0x000d || c >= 0x2000 && c <= 0x200a || switch(c) {
                case 0x0020, 0x0085, 0x00a0, 0x1680, 0x2028, 0x2029, 0x202f, 0x205f, 0x3000 -> true;
                default -> false;
            };
        }
        private static String trimImportWhiteSpace(String value) {
            int start=0,end=value.length();
            while(start<end && importWhiteSpace(value.charAt(start)))start++;
            while(start<end && importWhiteSpace(value.charAt(end-1)))end--;
            return value.substring(start,end);
        }
        void importFile(Element element, Path owner) throws IOException {
            attrs(element,Set.of("Project","Condition"));
            if(!elements(element).isEmpty()) throw reject("IMPORT_CHILD", "Import children not supported");
            if(!condition(element,owner))return;
            ImportSite current = sourceSites.get(element);
            if (current == null) throw reject("XML_SOURCE_INDEX", "Missing import source identity");
            // All selected same-profile native end fields were observed as 0/0.
            WarningPosition position = new WarningPosition(current.line(),current.column(),0,0);
            String expanded = trimImportWhiteSpace(expand(element.getAttribute("Project")));
            if (expanded.isEmpty()) {
                // Undefined, empty and whitespace-only references were observed as MSB4020.
                // There is no imported target and no missing-file identity for this failure.
                duplicates.add(new DuplicateImport("MSB4020",owner,null,position,null,null,
                    DiagnosticKind.ERROR,ContextKind.INVALID));
                throw new EvaluationFailure(FailureReason.INVALID_IMPORT_EXPRESSION,"MSB4020",owner,null,position,duplicates);
            }
            Path path=relative(owner,expanded);
            if (!Files.exists(path)) {
                duplicates.add(new DuplicateImport("MSB4019",owner,path,position,null,null,
                    DiagnosticKind.ERROR,ContextKind.MISSING));
                throw new EvaluationFailure(FailureReason.MISSING_IMPORT,"MSB4019",owner,path,position,duplicates);
            }
            // Root self-import precedes both flagged policies in the pinned evaluator.
            if (path.equals(files.getFirst())) {
                duplicates.add(new DuplicateImport("MSB4210",owner,path,position,null,path,
                    DiagnosticKind.WARNING,ContextKind.ROOT));
                return;
            }
            if (profile != ImportProfile.DEFAULT && introducesCircularity(path,owner)) {
                duplicates.add(new DuplicateImport(null,owner,path,position,null,null,
                    DiagnosticKind.WARNING,ContextKind.CIRCULAR));
                if (profile == ImportProfile.REJECT_CIRCULAR) {
                    duplicates.add(new DuplicateImport(null,owner,path,position,null,null,
                        DiagnosticKind.ERROR,ContextKind.CIRCULAR));
                    throw new EvaluationFailure(FailureReason.CIRCULAR_IMPORT,null,owner,path,position,duplicates);
                }
                return;
            }
            ImportEdge edge = new ImportEdge(owner,path,current.line(),current.column());
            if (seen.contains(path)) {
                ImportSite previous = firstImports.get(path);
                if (previous == null) throw reject("XML_SOURCE_INDEX", "Missing previous import source identity");
                duplicates.add(new DuplicateImport("MSB4011",owner,path,position,previous,null,
                    DiagnosticKind.WARNING,ContextKind.PREVIOUS));
                if (profile == ImportProfile.RECORD_DUPLICATES) recordedImports.add(edge);
                return;
            }
            firstImports.put(path,current);
            imports.add(edge);
            if (profile == ImportProfile.RECORD_DUPLICATES) recordedImports.add(edge);
            read(path,false);
        }
        boolean introducesCircularity(Path target, Path owner) {
            // Walk first-import containing-project ancestry, as the pinned evaluator does.
            // A completed shared import is not an ancestor merely because it was seen.
            for (Path ancestor = owner; ancestor != null;) {
                if (target.equals(ancestor)) return true;
                ImportSite first = firstImports.get(ancestor);
                ancestor = first == null ? null : first.owner();
            }
            return false;
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
        private static final int CONDITION_GROUP_LIMIT = 64;
        private static final int CONDITION_NODE_LIMIT = 256;
        private interface ConditionExpression { }
        private record ConditionScalar(String raw, boolean numeric) implements ConditionExpression { }
        private record ExistsAtom(String rawArgument) implements ConditionExpression { }
        private record ConditionNot(ConditionExpression child) implements ConditionExpression { }
        private record ConditionRelation(ConditionExpression left, ConditionExpression right, boolean unequal) implements ConditionExpression { }
        private enum OrderingOperator { LESS, LESS_OR_EQUAL, GREATER, GREATER_OR_EQUAL }
        private record ConditionOrdering(ConditionExpression left, ConditionExpression right,
                                         OrderingOperator operator) implements ConditionExpression { }
        private record ConditionVersion(int major, int minor, int build, int revision) {
            int compareTo(ConditionVersion other) {
                int result=Integer.compare(major,other.major);
                if(result==0)result=Integer.compare(minor,other.minor);
                if(result==0)result=Integer.compare(build,other.build);
                if(result==0)result=Integer.compare(revision,other.revision);
                return result;
            }
        }
        private record HasTrailingSlashAtom(String rawArgument) implements ConditionExpression { }
        private record ConditionAnd(ConditionExpression left, ConditionExpression right) implements ConditionExpression { }
        private record ConditionOr(ConditionExpression left, ConditionExpression right) implements ConditionExpression { }
        private record ParsedCondition(ConditionExpression expression, boolean mixedAndOr) { }
        // All supported sites use AllowProperties. Exact raw spelling is the cache key.
        // Retain immutable syntax only: no State, owner, globals or expanded values.
        private static final Map<String,ParsedCondition> CONDITIONS = new HashMap<>();
        private static final int CONDITION_CACHE_THRESHOLD = 3000;
        private final class ConditionParser {
            final String raw;
            int cursor, depth, nodes;
            // MSBuild marks every And/Or node, and each Expr level consumes its own marks.
            boolean andMarked, orMarked, mixedAndOr;
            ConditionParser(String raw) {
                this.raw=raw;
                // Validate references without expanding values or decoding predicate data.
                conditionReferences(raw);
            }
            void space() { while(cursor<raw.length() && raw.charAt(cursor)<=0x20)cursor++; }
            boolean word(char c) { return c>='A'&&c<='Z'||c>='a'&&c<='z'||c>='0'&&c<='9'||c=='_'; }
            boolean keyword(String lower) {
                int end=cursor+lower.length();
                if(end>raw.length() || cursor>0&&word(raw.charAt(cursor-1)))return false;
                for(int i=0;i<lower.length();i++) {
                    char c=raw.charAt(cursor+i);
                    if(c!=lower.charAt(i)&&c!=Character.toUpperCase(lower.charAt(i)))return false;
                }
                return end==raw.length()||!word(raw.charAt(end));
            }
            void node() {
                if(nodes>=CONDITION_NODE_LIMIT)throw reject("CONDITION_BOUND","Private condition AST node limit exceeded");
                nodes++;
            }
            ConditionExpression parse() {
                ConditionExpression result=disjunction();space();
                if(cursor!=raw.length())throw reject("CONDITION_PROFILE","Trailing condition syntax outside selected profile");
                return result;
            }
            // And binds tighter than Or; both associate left and short-circuit.
            ConditionExpression disjunction() {
                boolean outerAnd=andMarked,outerOr=orMarked;
                andMarked=orMarked=false;
                ConditionExpression result=conjunction();space();
                while(keyword("or")) {
                    cursor+=2;
                    ConditionExpression right=conjunction();
                    node();result=new ConditionOr(result,right);orMarked=true;space();
                }
                mixedAndOr|=andMarked&&orMarked;
                andMarked=outerAnd;orMarked=outerOr;
                return result;
            }
            ConditionExpression conjunction() {
                ConditionExpression result=relation();space();
                while(keyword("and")) {
                    cursor+=3;
                    ConditionExpression right=relation();
                    node();result=new ConditionAnd(result,right);andMarked=true;space();
                }
                return result;
            }
            ConditionExpression relation() {
                ConditionExpression left=primary();space();
                if(raw.startsWith("==",cursor)||raw.startsWith("!=",cursor)) {
                    boolean unequal=raw.charAt(cursor)=='!';cursor+=2;node();
                    return new ConditionRelation(left,primary(),unequal);
                }
                if(cursor<raw.length()&&(raw.charAt(cursor)=='<'||raw.charAt(cursor)=='>')) {
                    boolean less=raw.charAt(cursor++)=='<';
                    boolean inclusive=cursor<raw.length()&&raw.charAt(cursor)=='=';
                    if(inclusive)cursor++;
                    OrderingOperator operator=less
                        ?(inclusive?OrderingOperator.LESS_OR_EQUAL:OrderingOperator.LESS)
                        :(inclusive?OrderingOperator.GREATER_OR_EQUAL:OrderingOperator.GREATER);
                    node();return new ConditionOrdering(left,primary(),operator);
                }
                return left;
            }
            ConditionExpression primary() {
                space();
                if(cursor>=raw.length())throw reject("CONDITION_PROFILE","Missing condition operand");
                if(raw.charAt(cursor)=='!' && !raw.startsWith("!=",cursor)) {
                    node();cursor++;return new ConditionNot(primary());
                }
                if(raw.charAt(cursor)=='(') {
                    if(depth>=CONDITION_GROUP_LIMIT)throw reject("CONDITION_BOUND","Private condition grouping depth exceeded");
                    depth++;cursor++;
                    ConditionExpression result=disjunction();space();
                    if(cursor>=raw.length()||raw.charAt(cursor)!=')')throw reject("CONDITION_PROFILE","Unbalanced condition group");
                    cursor++;depth--;return result;
                }
                Matcher slash=HAS_TRAILING_SLASH.matcher(raw).region(cursor,raw.length());
                if(slash.lookingAt()) { cursor=slash.end();node();return new HasTrailingSlashAtom(slash.group(1)); }
                Matcher exists=EXISTS.matcher(raw).region(cursor,raw.length());
                if(exists.lookingAt()) { cursor=exists.end();node();return new ExistsAtom(exists.group(1)); }
                int start=cursor;boolean numeric=false;String text;
                char first=raw.charAt(cursor);
                if(first=='\'') {
                    start=++cursor;
                    while(cursor<raw.length()&&raw.charAt(cursor)!='\'')cursor++;
                    if(cursor==raw.length())throw reject("CONDITION_PROFILE","Unclosed quoted operand");
                    text=raw.substring(start,cursor++);
                } else if(raw.startsWith("$(",cursor)) {
                    int end=raw.indexOf(')',cursor+2);
                    if(end<0)throw reject("PROPERTY_REFERENCE","Unclosed property reference");
                    key(raw.substring(cursor+2,end));cursor=end+1;text=raw.substring(start,cursor);
                } else if(first>='0'&&first<='9'||first=='+'||first=='-'||first=='.') {
                    numeric=true;
                    if(raw.startsWith("0x",cursor)||raw.startsWith("0X",cursor)) {
                        cursor+=2;while(cursor<raw.length()&&hexDigit(raw.charAt(cursor))>=0)cursor++;
                    } else {
                        if(first=='+'||first=='-')cursor++;
                        while(cursor<raw.length()&&(raw.charAt(cursor)>='0'&&raw.charAt(cursor)<='9'||raw.charAt(cursor)=='.'))cursor++;
                    }
                    text=raw.substring(start,cursor);
                } else if(first>='a'&&first<='z'||first>='A'&&first<='Z'||first=='_') {
                    while(cursor<raw.length()&&word(raw.charAt(cursor)))cursor++;
                    text=raw.substring(start,cursor);
                    if(text.equalsIgnoreCase("And")||text.equalsIgnoreCase("Or"))throw reject("CONDITION_PROFILE","Operator without operand");
                } else throw reject("CONDITION_PROFILE","Operand outside selected ASCII grammar");
                // The inherited comparison boundary is static, including skipped syntax.
                asciiFold(decodeConditionScalar(conditionReferences(text)));
                node();return new ConditionScalar(text,numeric);
            }
        }

        boolean condition(Element element, Path owner) throws IOException {
            String raw=element.getAttribute("Condition");
            if(raw.isEmpty())return true;
            ParsedCondition parsed;
            boolean warn=false;
            synchronized(CONDITIONS) {
                // Source-derived bounded retention; native eviction/concurrency remain unqualified.
                if(CONDITIONS.size()>CONDITION_CACHE_THRESHOLD)CONDITIONS.clear();
                parsed=CONDITIONS.get(raw);
                if(parsed==null) {
                    ConditionParser parser=new ConditionParser(raw);
                    parsed=new ParsedCondition(parser.parse(),parser.mixedAndOr);
                    CONDITIONS.put(raw,parsed);
                    warn=parsed.mixedAndOr();
                }
            }
            if(warn) {
                ImportSite site=conditionSites.get(element);
                if(site==null)throw reject("XML_SOURCE_INDEX","Missing condition source identity");
                conditionWarnings.add(new ConditionWarning("MSB4130",site.owner(),site.line(),site.column(),raw));
            }
            return requireBoolean(parsed.expression(),owner,true);
        }
        // Each conversion is evaluation-local. Cached records contain only raw syntax.
        // In particular, emptiness checks never execute Boolean operators.
        private boolean empty(ConditionExpression expression) {
            return expression instanceof ConditionScalar scalar && !scalar.numeric() && scalarText(scalar).isEmpty();
        }
        private String scalarText(ConditionScalar scalar) { return decodeConditionScalar(expand(scalar.raw())); }
        private String text(ConditionExpression expression) {
            if(expression instanceof ConditionScalar scalar)return scalarText(scalar);
            if(expression instanceof ConditionNot not) {
                String child=text(not.child());return "!"+(child==null?"":child);
            }
            return null;
        }
        private Double number(ConditionExpression expression) {
            return expression instanceof ConditionScalar scalar ? conditionNumber(scalarText(scalar)) : null;
        }
        private Boolean bool(ConditionExpression expression,Path owner) throws IOException {
            if(expression instanceof ConditionScalar scalar)
                return scalar.numeric()?null:conditionBoolean(scalarText(scalar));
            if(expression instanceof ConditionNot not)return !requireBoolean(not.child(),owner,false);
            if(expression instanceof ConditionAnd and)
                return requireBoolean(and.left(),owner,false)&&requireBoolean(and.right(),owner,false);
            if(expression instanceof ConditionOr or)
                return requireBoolean(or.left(),owner,false)||requireBoolean(or.right(),owner,false);
            if(expression instanceof HasTrailingSlashAtom slash)return hasTrailingSlash(slash.rawArgument());
            if(expression instanceof ExistsAtom exists) {
                // Retain the separately qualified Exists path conversion and source directory.
                String argument=unescape(expand(exists.rawArgument()));
                return Files.exists(relative(owner,argument));
            }
            if(expression instanceof ConditionOrdering ordering)return ordering(ordering);
            ConditionRelation relation=(ConditionRelation)expression;
            ConditionExpression left=relation.left(),right=relation.right();
            boolean leftEmpty=empty(left),rightEmpty=empty(right),equal;
            if(leftEmpty||rightEmpty)equal=leftEmpty==rightEmpty;
            else {
                Double ln=number(left),rn=ln==null?null:number(right);
                if(ln!=null&&rn!=null)equal=ln.doubleValue()==rn.doubleValue();
                else {
                    Boolean lb=bool(left,owner),rb=lb==null?null:bool(right,owner);
                    if(lb!=null&&rb!=null)equal=lb.booleanValue()==rb.booleanValue();
                    else {
                        String lt=text(left),rt=text(right);
                        if(lt==null||rt==null)throw reject("CONDITION_ILL_FORMED","Comparison operand has no string representation");
                        equal=asciiFold(lt).equals(asciiFold(rt));
                    }
                }
            }
            return relation.unequal()?!equal:equal;
        }
        private boolean ordering(ConditionOrdering expression) {
            // Match NumericComparisonExpressionNode's conversion and dispatch order.
            // Expand each reached scalar once; these locals never enter the raw AST cache.
            String left=expression.left() instanceof ConditionScalar scalar?scalarText(scalar):null;
            Double leftNumber=left==null?null:conditionNumber(left);
            ConditionVersion leftVersion=left==null?null:conditionVersion(left);
            String right=expression.right() instanceof ConditionScalar scalar?scalarText(scalar):null;
            Double rightNumber=right==null?null:conditionNumber(right);
            ConditionVersion rightVersion=right==null?null:conditionVersion(right);
            if(leftNumber==null&&leftVersion==null||rightNumber==null&&rightVersion==null) {
                // The native error selects by numeric-left success, even when left is a valid version.
                ConditionExpression offending=leftNumber!=null?expression.right():expression.left();
                String expanded=leftNumber!=null?right:left;
                if(offending instanceof ConditionScalar scalar)
                    throw reject("CONDITION_NON_NUMERIC","Ordering operand \""+scalar.raw()+"\" evaluates to \""+expanded+"\" instead of a number or version");
                throw reject("CONDITION_NON_NUMERIC","Ordering operand has no numeric or version representation");
            }
            OrderingOperator operator=expression.operator();
            if(leftNumber!=null&&rightNumber!=null)return compareNumbers(leftNumber,rightNumber,operator);
            if(leftVersion!=null&&rightVersion!=null)return compareNumbers(leftVersion.compareTo(rightVersion),0,operator);
            if(leftNumber!=null) {
                if(leftNumber.doubleValue()==rightVersion.major())
                    return operator==OrderingOperator.LESS||operator==OrderingOperator.LESS_OR_EQUAL;
                return compareNumbers(leftNumber,rightVersion.major(),operator);
            }
            if(leftVersion.major()==rightNumber.doubleValue())
                return operator==OrderingOperator.GREATER||operator==OrderingOperator.GREATER_OR_EQUAL;
            return compareNumbers(leftVersion.major(),rightNumber,operator);
        }
        private static boolean compareNumbers(double left,double right,OrderingOperator operator) {
            // Primitive comparisons preserve NaN=false in every homogeneous and mixed path.
            return switch(operator) {
                case LESS -> left<right;
                case LESS_OR_EQUAL -> left<=right;
                case GREATER -> left>right;
                case GREATER_OR_EQUAL -> left>=right;
            };
        }
        private static ConditionVersion conditionVersion(String text) {
            asciiFold(text);
            String[] components=text.split("\\.",-1);
            if(components.length<2||components.length>4)return null;
            int[] values={0,0,-1,-1};
            for(int i=0;i<components.length;i++) {
                Integer value=versionComponent(components[i]);
                if(value==null)return null;
                values[i]=value;
            }
            return new ConditionVersion(values[0],values[1],values[2],values[3]);
        }
        private static boolean integerSpace(char c) { return c==' '||c>='\t'&&c<='\r'; }
        private static Integer versionComponent(String text) {
            // Invariant NumberStyles.Integer: ASCII whitespace, one sign, decimal digits,
            // trailing whitespace then optional NUL compatibility characters (in that order).
            int cursor=0;
            while(cursor<text.length()&&integerSpace(text.charAt(cursor)))cursor++;
            boolean negative=false;
            if(cursor<text.length()&&(text.charAt(cursor)=='+'||text.charAt(cursor)=='-'))
                negative=text.charAt(cursor++)=='-';
            int start=cursor,value=0;
            while(cursor<text.length()&&text.charAt(cursor)>='0'&&text.charAt(cursor)<='9') {
                int digit=text.charAt(cursor++)-'0';
                if(value>(Integer.MAX_VALUE-digit)/10)return null;
                value=value*10+digit;
            }
            if(cursor==start||negative&&value!=0)return null;
            while(cursor<text.length()&&integerSpace(text.charAt(cursor)))cursor++;
            while(cursor<text.length()&&text.charAt(cursor)=='\0')cursor++;
            return cursor==text.length()?value:null;
        }
        private boolean requireBoolean(ConditionExpression expression,Path owner,boolean root) throws IOException {
            Boolean value=bool(expression,owner);
            if(value==null)throw reject(root?"CONDITION_NOT_BOOLEAN":"CONDITION_NOT_BOOLEAN_CHILD","Reached operand does not evaluate to Boolean");
            return value;
        }
        private static Boolean conditionBoolean(String text) {
            asciiFold(text);
            // ASCII aliases only, deliberately no whitespace trimming or expression reparse.
            for(String alias:List.of("true","on","yes","!false","!off","!no"))if(alias.equalsIgnoreCase(text))return true;
            for(String alias:List.of("false","off","no","!true","!on","!yes"))if(alias.equalsIgnoreCase(text))return false;
            return null;
        }
        private static final Pattern CONDITION_DECIMAL=Pattern.compile("[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)");
        private static Double conditionNumber(String text) {
            asciiFold(text);
            // AllowDecimalPoint|AllowLeadingSign with invariant culture; Java's broader
            // exponent, suffix, whitespace and hexadecimal-floating grammar is excluded.
            // Runtime numeric parsing accepts trailing NUL compatibility characters.
            // Special-symbol fallback instead trims whitespace from the ORIGINAL input.
            int end=text.length();while(end>0&&text.charAt(end-1)=='\0')end--;
            String ordinary=text.substring(0,end);
            if(CONDITION_DECIMAL.matcher(ordinary).matches()) {
                double value=Double.parseDouble(ordinary);
                if(!Double.isInfinite(value))return value;
            }
            String special=trimImportWhiteSpace(text);
            if(special.equalsIgnoreCase("NaN")||special.equalsIgnoreCase("+NaN")||special.equalsIgnoreCase("-NaN"))return Double.NaN;
            if(ordinary.length()>=3&&ordinary.charAt(0)=='0'&&(ordinary.charAt(1)=='x'||ordinary.charAt(1)=='X')) {
                String digits=ordinary.substring(2);int first=0;
                while(first<digits.length()&&digits.charAt(first)=='0')first++;
                if(digits.length()-first>8)return null;
                for(int i=0;i<digits.length();i++)if(hexDigit(digits.charAt(i))<0)return null;
                return (double)(int)(first==digits.length()?0:Long.parseLong(digits.substring(first),16));
            }
            return null;
        }
        private static String decodeConditionScalar(String raw) {
            StringBuilder result=new StringBuilder();
            for(int i=0;i<raw.length();i++) {
                char c=raw.charAt(i);
                if(c=='%'&&i+2<raw.length()) {
                    int h=hexDigit(raw.charAt(i+1)),l=hexDigit(raw.charAt(i+2));
                    if(h>=0&&l>=0){result.append((char)(h*16+l));i+=2;continue;}
                }
                result.append(c);
            }
            return result.toString();
        }
        private boolean hasTrailingSlash(String rawArgument) {
            // MSBuild's scalar conversion splits and trims before a single unescape.
            // Expanded syntax remains data; nothing here reparses or resolves a path.
            String scalar=null;
            for(String token:expand(rawArgument).split(";",-1)) {
                token=trimImportWhiteSpace(token);
                if(token.isEmpty())continue;
                if(scalar!=null)throw reject("CONDITION_PROFILE","HasTrailingSlash requires at most one nonempty scalar token");
                scalar=token;
            }
            if(scalar==null)return false;
            StringBuilder decoded=new StringBuilder();
            for(int i=0;i<scalar.length();i++) {
                char c=scalar.charAt(i);
                if(c=='%' && i+2<scalar.length()) {
                    int high=hexDigit(scalar.charAt(i+1)),low=hexDigit(scalar.charAt(i+2));
                    if(high>=0 && low>=0) { decoded.append((char)(high*16+low));i+=2;continue; }
                }
                decoded.append(c);
            }
            if(decoded.isEmpty())return false;
            char last=decoded.charAt(decoded.length()-1);
            return last=='/' || last=='\\';
        }
        private static int hexDigit(char c) {
            return c>='0'&&c<='9'?c-'0':c>='a'&&c<='f'?c-'a'+10:c>='A'&&c<='F'?c-'A'+10:-1;
        }
        void validateCondition(String raw) {
            if (!raw.isEmpty()) new ConditionParser(raw).parse();
        }
        String conditionReferences(String raw) {
            Matcher references = REFERENCE.matcher(raw);
            StringBuilder template = new StringBuilder();
            while (references.find()) {
                key(references.group(1));references.appendReplacement(template, "");
            }
            references.appendTail(template);
            if (template.indexOf("$(") >= 0) throw reject("PROPERTY_REFERENCE", "Unclosed property reference");
            return template.toString();
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

    /** Lexical positions only: the secured DOM remains the semantic/validity authority.
     * Align every real start tag to DOM preorder so repeated tags, scalar text,
     * comments, CDATA and quoted delimiters cannot silently select another import.
     * Positions count UTF-16 characters, with XML CR/CRLF line normalization.
     */
    private static final class SourceIndex {
        private record Start(String name, int offset, int conditionOffset) { }
        static void attach(Document document, byte[] bytes, Path file, Map<Element,ImportSite> sites,
                           Map<Element,ImportSite> conditionSites) {
            String source;
            try {
                source = Charset.forName(document.getInputEncoding()).newDecoder()
                    .onMalformedInput(CodingErrorAction.REPORT).onUnmappableCharacter(CodingErrorAction.REPORT)
                    .decode(ByteBuffer.wrap(bytes)).toString();
            } catch (CharacterCodingException | IllegalArgumentException error) {
                throw reject("XML_SOURCE_INDEX", "XML source encoding cannot be indexed");
            }
            if (source.startsWith("\uFEFF")) source = source.substring(1);
            source = source.replace("\r\n","\n").replace('\r','\n');
            List<Start> starts = new ArrayList<>();
            int cursor = 0;
            while (cursor < source.length()) {
                int open = source.indexOf('<',cursor);
                if (open < 0) break;
                if (source.startsWith("<!--",open)) { cursor = after(source,"-->",open+4); continue; }
                if (source.startsWith("<![CDATA[",open)) { cursor = after(source,"]]>",open+9); continue; }
                if (source.startsWith("<?",open)) { cursor = after(source,"?>",open+2); continue; }
                if (source.startsWith("<!",open)) throw reject("XML_SOURCE_INDEX", "Unexpected XML declaration");
                boolean closing = source.startsWith("</",open);
                int nameStart = open+(closing ? 2 : 1), nameEnd = nameStart;
                while (nameEnd < source.length() && !Character.isWhitespace(source.charAt(nameEnd))
                       && source.charAt(nameEnd) != '/' && source.charAt(nameEnd) != '>') nameEnd++;
                char quote = 0;int end = nameEnd,conditionOffset = -1;
                for (;end < source.length();end++) {
                    char c = source.charAt(end);
                    if (quote != 0) { if (c == quote) quote = 0; }
                    else if (c == '\'' || c == '"') quote = c;
                    else if (c == '>') break;
                    else if (Character.isWhitespace(source.charAt(end-1)) && source.startsWith("Condition",end)) conditionOffset = end;
                }
                if (end == source.length()) throw reject("XML_SOURCE_INDEX", "Unterminated XML start tag");
                if (!closing) starts.add(new Start(source.substring(nameStart,nameEnd),open,conditionOffset));
                cursor = end+1;
            }
            NodeList elements = document.getElementsByTagName("*");
            if (elements.getLength() != starts.size()) throw reject("XML_SOURCE_INDEX", "XML source/DOM count differs");
            int position = 0,line = 1,column = 1;
            for (int i=0;i<starts.size();i++) {
                Start start = starts.get(i);Element element = (Element)elements.item(i);
                if (!element.getTagName().equals(start.name())) throw reject("XML_SOURCE_INDEX", "XML source/DOM identity differs");
                while (position < start.offset()) {
                    if (source.charAt(position++) == '\n') { line++;column = 1; }
                    else column++;
                }
                sites.put(element,new ImportSite(file,line,column));
                if (start.conditionOffset() >= 0) {
                    int conditionLine = line,conditionColumn = column;
                    for (int i2 = position;i2 < start.conditionOffset();i2++) {
                        if (source.charAt(i2) == '\n') { conditionLine++;conditionColumn = 1; }
                        else conditionColumn++;
                    }
                    conditionSites.put(element,new ImportSite(file,conditionLine,conditionColumn));
                }
            }
        }
        private static int after(String source,String delimiter,int start) {
            int end = source.indexOf(delimiter,start);
            if (end < 0) throw reject("XML_SOURCE_INDEX", "Unterminated XML lexical section");
            return end+delimiter.length();
        }
    }
}
