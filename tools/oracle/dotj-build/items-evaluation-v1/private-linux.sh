#!/bin/sh
set -eu
ulimit -c 0
slot=$1
expected=$2
case "$slot" in product-v[0-9]*) ;; *) exit 64 ;; esac
test ! -e "/work/$slot"
mkdir "/work/$slot"
mkdir "/work/$slot/tmp" "/work/$slot/home"
cd "/work/$slot"
cat /proc/self/mountinfo > mountinfo.txt
sha256sum /product.jar /consumer.jar /jdk/bin/java > executed-files.sha256
/jdk/bin/java -Xms16m -Xmx128m -XX:ActiveProcessorCount=2 -XX:+UseSerialGC -XX:ReservedCodeCacheSize=32m -XX:-UsePerfData \
    "-Djava.io.tmpdir=/work/$slot/tmp" "-Duser.home=/work/$slot/home" -Duser.language=en -Duser.country=US -Dfile.encoding=UTF-8 \
    "-XX:ErrorFile=/work/$slot/tmp/hs_err_pid%p.log" "-XX:HeapDumpPath=/work/$slot/tmp" \
    --limit-modules java.base,java.xml,org.dotj.build.evaluation.candidate --module-path /product.jar \
    --patch-module org.dotj.build.evaluation.candidate=/consumer.jar \
    -m org.dotj.build.evaluation.candidate/org.dotj.internal.build.evaluation.ItemsPrivateTest \
    "/work/$slot/controls" linux /product.jar "$expected" > private.stdout 2> private.stderr
cp controls/results.tsv results.tsv
