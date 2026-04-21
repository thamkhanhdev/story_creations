@echo off
if "%~1"=="" (
    python load_story.py
) else (
    python load_story.py "%~1"
)