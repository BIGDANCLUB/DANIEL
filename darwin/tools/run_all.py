"""①〜③を順に実行する。  python tools/run_all.py 01-keiba [--mock]"""
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
args = sys.argv[1:]
if not args:
    sys.exit("usage: python tools/run_all.py <episode> [--mock]")
ep, mock = args[0], ["--mock"] if "--mock" in args else []
for step in (["tts_gemini.py", ep, *mock], ["comfy_h3.py", ep, *mock], ["assemble.py", ep]):
    print(f"\n=== {step[0]} ===")
    subprocess.run([sys.executable, str(here / step[0]), *step[1:]], check=True)
