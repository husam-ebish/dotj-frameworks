#!/bin/sh
set -eu
if [ -z "${JAVA_HOME:-}" ]; then echo 'dotj seed: JAVA_HOME_REQUIRED' >&2; exit 1; fi
if [ "$#" -ne 1 ]; then echo 'Usage: sh build.sh /absolute/output-root' >&2; exit 1; fi
case "$1" in /*) scratch=${1%/*}; [ -n "$scratch" ] || scratch=/ ;; *) echo 'dotj seed: absolute output root required' >&2; exit 1;; esac
case "$0" in /*) script=$0 ;; *) script=$PWD/$0 ;; esac
seed=${script%/*}
root=$seed/../..
exec "$JAVA_HOME/bin/java" -Xms16m -Xmx128m -XX:ActiveProcessorCount=2 -XX:+UseSerialGC -XX:ReservedCodeCacheSize=32m -XX:-UsePerfData "-Djava.io.tmpdir=$scratch" "-Duser.home=$scratch" "-XX:ErrorFile=$scratch/hs_err_pid%p.log" "-XX:HeapDumpPath=$scratch" "-Ddotj.seed.script=$script" --class-path "$seed/sources.properties" --add-modules jdk.compiler,jdk.jartool --source 21 "$seed/Bootstrap.java" "$root" "$1" 414e04c987d4c6a928a71d8bb78e61448ef0f453146fa4ade3ef67f9aaa4ab0e
