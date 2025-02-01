@echo off
cd C:\ProgramData\windos

:: Verifica se Python è installato
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [⚠] Python non trovato! Installalo prima di avviare il bot. >> C:\ProgramData\windos\windos.log
    exit
)

:: Controlla se il bot è già in esecuzione
tasklist | findstr /I /C:"python.exe" | findstr /I /C:"windos.py" >nul
if %errorlevel% equ 0 (
    echo [⚠] Il bot è già in esecuzione! >> C:\ProgramData\windos\windos.log
    exit
)

:: Avvia il bot senza mostrare la finestra
echo [✔] Avvio del bot... >> C:\ProgramData\windos\windos.log
wscript C:\ProgramData\windos\windos.vbs
exit
