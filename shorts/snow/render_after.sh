#!/bin/bash
# 他の書き出しが終わるのを待ってから、雪の動画を書き出す。usage: bash render_after.sh 出力の親フォルダ
P=$1
while pgrep -f render_queue.sh >/dev/null; do sleep 30; done
bash /home/user/daniel/shorts/snow/render_all.sh $P/snow n01_open:1 n02_flake:1 n03a_village:1 n03b_town:1 n03c_tokyo:1 n03d_fuji:1 \
  n03e_space:1 n06_winter:1 n07_house:1 n08_record:1 n09_town:1 n10_tokyo:1 n11_fuji:1 n12_space100:2 n13_space30:1 n14_moon:1 n15_end:2
echo SNOW_DONE
