#!/bin/sh
set -eu
ulimit -c 0
slot=$1
mode=$2
expected=$3
test ! -e "/work/$slot"
mkdir "/work/$slot"
cd "/work/$slot"
mkdir tmp home
cp -R /corpus fixtures
cat /proc/self/mountinfo > mountinfo.txt
sha256sum /product.jar /consumer.jar /jdk/bin/java > executed-files.sha256
for main in fixtures/*/main.proj; do
  dir=${main%/main.proj}
  id=${dir##*/}
  lower=$(printf '%s' "$id" | tr A-Z a-z)
  file_alias=false
  dir_alias=false
  if [ -e "$dir/MAIN.PROJ" ]; then file_alias=true; fi
  if [ -d "fixtures/$lower" ]; then dir_alias=true; fi
  printf '%s\t%s\t%s\n' "$id" "$file_alias" "$dir_alias"
done > case-profile.tsv
if [ "$mode" = private ]; then
  mkdir -p controls/links/inside/target controls/links/outside outside-link-target
  printf '<Project/>' > controls/links/inside/target/one.props
  printf '<Project/>' > outside-link-target/one.props
  ln -s target controls/links/inside/alias
  ln -s "/work/$slot/outside-link-target" controls/links/outside/alias
  set -- private "/work/$slot/controls" "/work/$slot/fixtures" linux
else
  test "$mode" = selected
  set -- selected "/work/$slot/fixtures"
fi
/jdk/bin/java -Xms16m -Xmx128m -XX:ActiveProcessorCount=2 -XX:+UseSerialGC -XX:ReservedCodeCacheSize=32m -XX:-UsePerfData \
  "-Djava.io.tmpdir=/work/$slot/tmp" "-Duser.home=/work/$slot/home" -Duser.language=en -Duser.country=US -Dfile.encoding=UTF-8 \
  "-XX:ErrorFile=/work/$slot/tmp/hs_err_pid%p.log" "-XX:HeapDumpPath=/work/$slot/tmp" \
  --limit-modules java.base,java.xml,org.dotj.build.evaluation.candidate --module-path /product.jar \
  --patch-module org.dotj.build.evaluation.candidate=/consumer.jar \
  -m org.dotj.build.evaluation.candidate/org.dotj.internal.build.evaluation.CycleTraceProductTest \
  "$@" /product.jar "$expected" > consumer.stdout 2> consumer.stderr
