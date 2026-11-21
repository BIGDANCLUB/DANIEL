@echo off
rem ScreenCap を黒い窓なしで起動する（エラー時は %APPDATA%\ScreenCap\error.log）
start "" pythonw "%~dp0screencap.py" %*
