@echo off
REM Script para iniciar a aplicacao do SaaS de Lip-Sync

echo ========================================================
echo 🎬 Iniciando SaaS de Geracao de Videos com Lip-Sync
echo ========================================================
echo.

REM Verifica se ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual nao encontrado!
    echo.
    echo Execute primeiro: install.bat
    echo.
    pause
    exit /b 1
)

REM Ativa ambiente virtual
echo ⚡ Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Verifica se .env existe
if not exist ".env" (
    echo ❌ Arquivo .env nao encontrado!
    echo.
    echo Execute primeiro: install.bat
    echo.
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando aplicacao...
echo.
echo ========================================================
echo 📱 A interface web sera aberta em:
echo    http://localhost:7860
echo ========================================================
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

REM Inicia aplicação
python app.py

pause
