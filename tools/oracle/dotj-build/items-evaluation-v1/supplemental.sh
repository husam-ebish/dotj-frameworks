#!/bin/sh
set -eu
ulimit -c 0
slot=$1
case "$slot" in supplemental-pass1|supplemental-pass2) ;; *) exit 64 ;; esac
test ! -e "/work/$slot"
mkdir "/work/$slot"
mkdir "/work/$slot/tmp" "/work/$slot/home"
cp -R /corpus "/work/$slot/fixtures"
cd "/work/$slot"
export HOME="/work/$slot/home" TMPDIR="/work/$slot/tmp" DOTNET_CLI_HOME="/work/$slot/home"
export DOTNET_DbgMiniDumpName="/work/$slot/tmp/dotnet.dmp"
/usr/share/dotnet/dotnet /observer/CaptureItemsV1.dll supplemental "/work/$slot/fixtures" "/work/$slot/fixtures/manifest.json" /observer > supplemental.stdout 2> supplemental.stderr
