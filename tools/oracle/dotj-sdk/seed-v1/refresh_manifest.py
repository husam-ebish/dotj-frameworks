"""Developer-only input lock refresh. Checked-in seed builds never run this tool."""
import argparse,hashlib,re
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);a=p.parse_args();root=a.source_root
    sources=sorted([f.relative_to(root).as_posix() for sub in ['dotj-build/evaluation-candidate/src','dotj-sdk/src'] for f in (root/sub).rglob('*.java')])
    inputs=sources+['dotj-sdk/seed/Bootstrap.java','dotj-sdk/seed/jdk.properties','dotj-sdk/launcher/dotj','dotj-sdk/launcher/dotj.ps1']
    lines=['sources='+','.join(sources)]
    for relative in sorted(inputs):
        raw=(root/relative).read_bytes()
        if relative.endswith('.java'):raw=raw.replace(b'\r\n',b'\n')
        lines.append('sha256.'+relative+'='+hashlib.sha256(raw).hexdigest())
    lock=root/'dotj-sdk/seed/sources.properties';lock.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n');digest=hashlib.sha256(lock.read_bytes()).hexdigest()
    for name in ['build.sh','build.ps1']:
        path=root/'dotj-sdk/seed'/name
        path.write_text(re.sub('SOURCE_LOCK_SHA256|[a-f0-9]{64}',digest,path.read_text(encoding='utf-8')),encoding='utf-8',newline='\n')
    print(digest)
if __name__=='__main__':main()
