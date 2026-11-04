@echo off
REM Executa os jobs de relatorios (main.py) direto do codigo-fonte.
REM A saida de cada execucao vai para logs\jobs_aaaammdd_hhmmss.log

REM Vai para a pasta onde este .bat esta
cd /d "%~dp0"

REM Evita erro de codificacao com acentos/simbolos
set PYTHONIOENCODING=utf-8

REM Nome do log com data/hora (independente do idioma do Windows)
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%i"
if not exist logs mkdir logs

REM Apaga logs com mais de 3 dias (mantem o de hoje e os dos 3 dias anteriores)
forfiles /p logs /m jobs_*.log /d -4 /c "cmd /c del @path" >nul 2>&1

py main.py > "logs\jobs_%STAMP%.log" 2>&1
exit /b %ERRORLEVEL%
