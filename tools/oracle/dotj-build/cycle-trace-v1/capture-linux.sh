#!/bin/sh
set -eu
ulimit -c 0
slot=$1
case "$slot" in native-linux-default-[12]-v1|native-linux-record_duplicates-[12]-v1|native-linux-reject_circular-[12]-v1) ;; *) exit 64 ;; esac
test ! -e "/work/$slot"
mkdir "/work/$slot"
cd "/work/$slot"
mkdir tmp home evaluation
export HOME="/work/$slot/home" TMPDIR="/work/$slot/tmp" DOTNET_CLI_HOME="/work/$slot/home"
export DOTNET_DbgMiniDumpName="/work/$slot/tmp/dotnet.dmp" MSBUILDUSEREXTENSIONSPATH="/work/$slot/home/msbuild"
cp -R /corpus evaluation/fixtures
for main in "/work/$slot/evaluation/fixtures/"*/main.proj; do
  dir=${main%/main.proj}
  id=${dir##*/}
  lower=$(printf '%s' "$id" | tr A-Z a-z)
  file_alias=false
  dir_alias=false
  if [ -e "$dir/MAIN.PROJ" ]; then file_alias=true; fi
  if [ -d "/work/$slot/evaluation/fixtures/$lower" ]; then dir_alias=true; fi
  printf '%s\t%s\t%s\n' "$id" "$file_alias" "$dir_alias"
done > case-profile.tsv
/usr/share/dotnet/dotnet exec --runtimeconfig /observer/CaptureImports.runtimeconfig.json --depsfile /sdk/MSBuild.deps.json /observer/CaptureImports.dll "/work/$slot/evaluation/fixtures" "$2" > native.stdout 2> native.stderr
