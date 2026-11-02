"""Pure baseline JAR/module and consumer-source isolation checks."""
import hashlib
import struct
import zipfile
from pathlib import Path

def require(ok,message):
    if not ok:raise ValueError(message)
def module_descriptor(raw):
    offset=0
    def take(count):
        nonlocal offset
        require(offset+count<=len(raw),'truncated classfile');data=raw[offset:offset+count];offset+=count;return data
    def u2():return struct.unpack('>H',take(2))[0]
    def u4():return struct.unpack('>I',take(4))[0]
    require(u4()==0xCAFEBABE,'classfile magic');u2();u2();count=u2();pool=[None]*count;i=1
    while i<count:
        tag=take(1)[0]
        if tag==1:pool[i]=take(u2()).decode('utf-8')
        elif tag in [7,8,16,19,20]:pool[i]=(tag,u2())
        elif tag in [3,4,9,10,11,12,17,18]:take(4)
        elif tag in [5,6]:take(8);i+=1
        elif tag==15:take(3)
        else:raise ValueError('unknown constant-pool tag')
        i+=1
    def text(index,tag):
        entry=pool[index];require(type(entry) is tuple and entry[0]==tag,'typed constant pool');return pool[entry[1]]
    u2();u2();u2()
    for _ in range(u2()):u2()
    for section in range(2):
        for _ in range(u2()):
            u2();u2();u2()
            for _ in range(u2()):u2();take(u4())
    found=None
    for _ in range(u2()):
        name=pool[u2()];size=u4();end=offset+size
        if name=='Module':
            module=text(u2(),19);u2();u2();requires=[]
            for _ in range(u2()):requires.append(text(u2(),19));u2();u2()
            exports=[]
            for _ in range(u2()):
                exports.append(text(u2(),20));u2()
                for _ in range(u2()):u2()
            opens=[]
            for _ in range(u2()):
                opens.append(text(u2(),20));u2()
                for _ in range(u2()):u2()
            for _ in range(u2()):u2()
            for _ in range(u2()):
                u2()
                for _ in range(u2()):u2()
            found=dict(name=module,requires=requires,exports=exports,opens=opens)
        else:take(size)
        require(offset==end,'class attribute byte boundary')
    require(offset==len(raw) and found is not None,'complete Module attribute');return found

def verify_jar(path,expected_sha,consumer_root):
    path=Path(path);require(hashlib.sha256(path.read_bytes()).hexdigest()==expected_sha,'baseline JAR digest')
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist();require(len(names)==len(set(names)),'duplicate JAR entries')
        descriptor=module_descriptor(archive.read('module-info.class'))
        require(descriptor==dict(name='org.dotj.build.evaluation.candidate',requires=['java.base','java.xml'],exports=[],opens=[]),'baseline module/dependency/no-export boundary')
        classes=[n for n in names if n.endswith('.class') and n!='module-info.class']
        require(classes and all(n.startswith('org/dotj/internal/build/evaluation/ProjectEvaluationComponent') for n in classes),'baseline product class inventory')
        require(not any(n.endswith('.java') for n in names),'JAR contains no source fallback')
    sources=[x for x in Path(consumer_root).rglob('*') if x.is_file()]
    require(sources and all(x.suffix=='.java' and not x.name.startswith('ProjectEvaluationComponent') and x.name!='module-info.java' for x in sources),'fixture-only consumer sources; no product/module leak')
    return dict(module=descriptor,productClasses=classes,sourceFiles=[str(x) for x in sources],status='PURE_JAR_BYTES_VERIFIED_NOT_EXECUTED')
