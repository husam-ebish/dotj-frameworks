#!/bin/sh
set -eu
ulimit -c 0
mkdir -p /work/directory-probe/Nested/Child
dir_case=false
if [ -d /work/Directory-Probe ]; then dir_case=true; fi
printf upper > /work/directory-probe/Nested/Child/CaseFile
nested_case=false
if [ -e /work/directory-probe/Nested/Child/casefile ]; then nested_case=true; fi
printf lower > /work/directory-probe/Nested/Child/casefile
printf '{"alternateDirectoryExists":%s,"alternateNestedFileExistsBefore":%s,"upperAfter":"%s","lowerAfter":"%s"}\n' "$dir_case" "$nested_case" "$(cat /work/directory-probe/Nested/Child/CaseFile)" "$(cat /work/directory-probe/Nested/Child/casefile)" > /work/directory-probe.json
/usr/share/dotnet/dotnet --list-runtimes > /work/runtimes.stdout 2> /work/runtimes.stderr
/jdk/bin/java -Xms32m -Xmx128m -XX:ActiveProcessorCount=2 -XX:+UseSerialGC -XX:ReservedCodeCacheSize=32m -XX:-UsePerfData -Djava.io.tmpdir=/work/tmp -Duser.home=/work/home -XX:ErrorFile=/work/tmp/hs_err_pid%p.log -XX:HeapDumpPath=/work/tmp -version > /work/java.stdout 2> /work/java.stderr
/usr/share/dotnet/dotnet /observer/CaptureItemsV1.dll preflight /work /observer > /work/observer.stdout 2> /work/observer.stderr
