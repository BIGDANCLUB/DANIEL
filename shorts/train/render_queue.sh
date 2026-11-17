#!/bin/bash
# 電車の動画（v2：だんだん増える版）を全場面書き出す（書き出し済みのコマは飛ばす）。usage: bash render_queue.sh 出力フォルダ [場面...]
cd "$(dirname "$0")"
R=$1; shift
if [ $# -eq 0 ]; then set -- f02_car:2 f03_full:2 f04_deck:2 f05_wide:2 f06_tokyo:2 f07_japan:2 f08_loop:2 f09_world:2 f10_area:2 f11_end:2; fi
bash render_all.sh $R "$@"
echo TRAIN_DONE
