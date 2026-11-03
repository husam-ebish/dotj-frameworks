#!/bin/sh
set -eu
ulimit -c 0
slot=$1
expected=$2
case "$slot" in product-v[0-9]*) ;; *) exit 64 ;; esac
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
cat /proc/self/mountinfo > mountinfo.txt
sha256sum /product.jar /consumer.jar /jdk/bin/java > executed-files.sha256
/jdk/bin/java -Xms16m -Xmx128m -XX:ActiveProcessorCount=2 -XX:+UseSerialGC -XX:ReservedCodeCacheSize=32m -XX:-UsePerfData \
    "-Djava.io.tmpdir=/work/$slot/tmp" "-Duser.home=/work/$slot/home" -Duser.language=en -Duser.country=US -Dfile.encoding=UTF-8 \
    "-XX:ErrorFile=/work/$slot/tmp/hs_err_pid%p.log" "-XX:HeapDumpPath=/work/$slot/tmp" \
    --limit-modules java.base,java.xml,org.dotj.build.evaluation.candidate --module-path /product.jar \
    --patch-module org.dotj.build.evaluation.candidate=/consumer.jar \
    -m org.dotj.build.evaluation.candidate/org.dotj.internal.build.evaluation.ItemsProductCapture \
    "/work/$slot/fixtures" "/work/$slot/fixtures/manifest.json" /product.jar "$expected" > capture.stdout 2> capture.stderr
