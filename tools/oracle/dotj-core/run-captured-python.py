"""Preserve child stdout and stderr together on D while forwarding output to PowerShell."""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--log',type=Path,required=True)
    parser.add_argument('command',nargs=argparse.REMAINDER);args=parser.parse_args()
    command=args.command[1:] if args.command[:1]==['--'] else args.command
    if not command:parser.error('A Python script is required')
    path=args.log.resolve()
    if path.drive.upper()!='D:':parser.error('Validation logs must remain on D:')
    # A fresh run must never silently replace an earlier failure log.
    with path.open('xb') as log:
        with subprocess.Popen([sys.executable,*command],stdout=subprocess.PIPE,stderr=subprocess.STDOUT) as child:
            for line in child.stdout:
                log.write(line);log.flush()
                sys.stdout.buffer.write(line);sys.stdout.buffer.flush()
            return child.wait()


if __name__=='__main__':raise SystemExit(main())
