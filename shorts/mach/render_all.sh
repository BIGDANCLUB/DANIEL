#!/bin/bash
# 全場面の3Dを順番に書き出す。usage: bash render_all.sh 出力フォルダ
cd "$(dirname "$0")"
R=$1
for spec in "s02_wheel 1" "s03a_cab 1" "s03b_shinagawa 1" "s03c_tama 1" "s03d_town 1" "s03e_arrive 1" "s06_boom 1" "s07_heat 1" \
            "s08_streak 1" "s09_sound 1" "s10_after 1" "s11_bench 1" "s12_osaka 1" "s13_fisher 1" "s14_river 1" "s15_end 2"; do
  set -- $spec
  t0=$(date +%s)
  python3 film.py $1 $R/$1 $2 2>&1 | grep -E "Error|Traceback|rendered"
  echo "$1 $(( $(date +%s) - t0 ))s"
done
