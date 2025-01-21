@echo off
for /f "tokens=*" %%i in ('where python') do set ruta_python=%%i
%ruta_python% ".\Main.py"
pause