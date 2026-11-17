#!/bin/bash
# 電車の動画を全場面書き出す（書き出し済みのコマは飛ばす）。usage: bash render_queue.sh 出力フォルダ
cd "$(dirname "$0")"
bash render_all.sh $1 e01_open:1 e02_one:1 e03a_car:1 e03b_platform:1 e03c_city:1 e03d_wide:1 e06_five:2 e07_ten:2 \
  e08_full:2 e09_dome:2 e10_tokyo:2 e11_japan:2 e12_loop:2 e13_world:2 e14_area:2 e15_end:2
echo TRAIN_DONE
