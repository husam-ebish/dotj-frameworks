#!/bin/sh
set -eu
ulimit -c 0
slot=$1
case "$slot" in pass1|pass2|v3-pass1|v3-pass2) ;; *) exit 64 ;; esac
test ! -e "/work/$slot"
mkdir "/work/$slot"
mkdir "/work/$slot/tmp" "/work/$slot/home"
cp -R /corpus "/work/$slot/fixtures"
cd "/work/$slot"
for main in fixtures/*/main.proj; do
    dir=${main%/main.proj}
    id=${dir##*/}
    lower=$(printf '%s' "$id" | tr A-Z a-z)
    file_alias=false
    dir_alias=false
    if [ -e "$dir/MAIN.PROJ" ]; then file_alias=true; fi
    if [ -d "fixtures/$lower" ]; then dir_alias=true; fi
    printf '%s\t%s\t%s\n' "$id" "$file_alias" "$dir_alias"
done > materialized-case-profile.tsv
export HOME="/work/$slot/home" TMPDIR="/work/$slot/tmp" DOTNET_CLI_HOME="/work/$slot/home"
export DOTNET_DbgMiniDumpName="/work/$slot/tmp/dotnet.dmp"
/usr/share/dotnet/dotnet /observer/CaptureItemsV1.dll corpus "/work/$slot/fixtures" "/work/$slot/fixtures/manifest.json" /observer > native.stdout 2> native.stderr
