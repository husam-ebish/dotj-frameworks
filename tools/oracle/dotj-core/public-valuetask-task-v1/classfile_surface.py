"""Pure ZIP/classfile surface reader. No javap/JDK execution."""
import struct,zipfile
def parse(data):
    p=0
    def take(n):
        nonlocal p
        if p+n>len(data):raise ValueError('truncated class')
        r=data[p:p+n];p+=n;return r
    def u1():return take(1)[0]
    def u2():return struct.unpack('>H',take(2))[0]
    def u4():return struct.unpack('>I',take(4))[0]
    if u4()!=0xcafebabe:raise ValueError('class magic')
    minor,major=u2(),u2();cp=[None]*u2();i=1
    while i<len(cp):
        tag=u1()
        if tag==1:cp[i]=take(u2()).replace(b'\xc0\x80',b'\x00').decode('utf-8',errors='surrogatepass')
        elif tag in (3,4):take(4)
        elif tag in (5,6):take(8);i+=1
        elif tag in (7,8,16,19,20):cp[i]=u2()
        elif tag in (9,10,11,12,17,18):take(4)
        elif tag==15:take(3)
        else:raise ValueError('constant pool tag')
        i+=1
    flags=u2();name=cp[cp[u2()]];u2()
    for _ in range(u2()):u2()
    def attrs():
        result=[]
        for _ in range(u2()):result.append((cp[u2()],take(u4())))
        return result
    members=[]
    for kind in ('F','M'):
        for _ in range(u2()):
            f,n,d=u2(),cp[u2()],cp[u2()];attrs()
            if f&1:members.append({'kind':kind,'name':n,'descriptor':d,'modifiers':f})
    classattrs=attrs()
    for attr,raw in classattrs:
        if attr=='InnerClasses':
            count=struct.unpack_from('>H',raw,0)[0]
            for i in range(count):
                inner,outer,innername,access=struct.unpack_from('>HHHH',raw,2+8*i)
                if inner and cp[cp[inner]]==name:flags=access
    if p!=len(data):raise ValueError('trailing class bytes')
    return {'name':name,'major':major,'modifiers':flags,'publicMembers':sorted(members,key=lambda x:(x['kind'],x['name'],x['descriptor']))}
def surface(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise ValueError('duplicate ZIP members')
        classes=[parse(z.read(n)) for n in names if n.endswith('.class')]
        if any(n.startswith('/') or '..' in n.split('/') for n in names):raise ValueError('unsafe ZIP path')
    return {'entries':names,'classes':sorted(classes,key=lambda x:x['name'])}
