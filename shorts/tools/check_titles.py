"""参考元チャンネルのショート動画タイトルと再生数を一覧表示（被りチェック用）。
使い方: python3 tools/check_titles.py [@handle]   既定は @yoneapp-games
※ページ最初の約30本のみ（それより古い動画は出ない）。"""
import re
import subprocess
import sys

h = sys.argv[1] if len(sys.argv) > 1 else "@yoneapp-games"
s = subprocess.run(["curl", "-sS", "-m", "30", "-H", "Accept-Language: ja",
                    f"https://www.youtube.com/{h}/shorts"], capture_output=True, text=True).stdout
seen = []
for t in re.findall(r'"accessibilityText":"([^"]+?), ([^"]+?回視聴)', s):
    if t not in seen:
        seen.append(t)
for title, views in seen:
    print(f"{views}\t{title}")
print(f"-- {len(seen)} 本")
