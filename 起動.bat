@echo off
chcp 65001 > nul
title Gemini Voice Studio Lite
cd /d "%~dp0"
echo ====================================================
echo  Gemini Voice Studio Lite を起動しています...
echo ====================================================
echo ブラウザが自動的に開きます。終了するときはこの黒い画面を閉じてください。
streamlit run app.py
pause
