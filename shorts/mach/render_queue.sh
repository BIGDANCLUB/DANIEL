#!/bin/bash
# 3本ぶんの3Dをまとめて順番に書き出す（書き出し済みのコマは飛ばすので、止まっても続きから再開できる）。
# usage: bash render_queue.sh 出力の親フォルダ
P=$1
S=/home/user/daniel/shorts
bash $S/mach/render_all.sh $P/mach s01_open:1 s02_wheel:1 s03a_cab:1 s03b_shinagawa:1 s03c_tama:1 s03d_town:1 s03e_arrive:1 \
  s06_boom:1 s07_heat:1 s08_streak:1 s09_sound:1 s10_after:1 s11_bench:1 s12_osaka:1 s13_fisher:1 s14_river:1 s15_end:2
bash $S/momo/render_all.sh $P/momo m01_open:1 m02_foot:1 m03a_vanish:1 m03b_island:2 m03c_animals:1 m06_run:1 m07_fire:1 m08_safe:1 \
  m09_light:1 m10_sound:1 m11_sea:1 m12_clock:1 m13_oni:1 m14_club:1 m15_end:2
bash $S/ohtani/render_all.sh $P/ohtani o01_open:1 o02_swing:1 o03a_fly:1 o03b_stands:1 o03c_board:1 o03d_last:1 o06_pergame:1 \
  o07_bonds:2 o08_rain:1 o09_lap:1 o10_distance:2 o11_walk:1 o12_fans:1 o15_end:2
echo ALL_DONE
