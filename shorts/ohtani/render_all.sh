#!/bin/bash
# usage: bash render_all.sh 出力フォルダ 場面名...（場面名は "名前:step"）
cd "$(dirname "$0")"
R=$1; shift
for spec in "$@"; do
  n=${spec%%:*}; st=${spec##*:}
  t0=$(date +%s)
  python3 film.py $n $R/$n $st 2>&1 | grep -E "Error|Traceback|rendered"
  echo "$n $(( $(date +%s) - t0 ))s"
done
