@echo off
:: Abre a interface gráfica sem exibir janela de console.
:: Tenta usar o pythonw do PATH; se não achar, usa o da instalação local.
cd /d "%~dp0"
where pythonw >nul 2>&1
if %errorlevel%==0 (
    start "" pythonw "Reajuste_de_precos_gui.py"
) else if exist "..\pythonw.exe" (
    start "" "..\pythonw.exe" "Reajuste_de_precos_gui.py"
) else (
    echo Python nao encontrado. Instale o Python 3 em https://www.python.org/downloads/
    pause
)
