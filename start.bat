@echo off
color 0A
title LipSync Video Generator Pro - Launcher

:: Banner
cls
echo.
echo ================================================================
echo.
echo      LipSync Video Generator Pro v2.0
echo.
echo      Sistema Profissional de Geracao de Videos com IA
echo.
echo ================================================================
echo.
echo.

:: Verifica se Python esta instalado
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.8+ de: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Python encontrado
echo.

:: Verifica se o .env existe
echo [2/4] Verificando configuracoes...
if not exist .env (
    color 0E
    echo.
    echo [AVISO] Arquivo .env nao encontrado!
    echo.
    echo Criando a partir do .env.example...
    copy .env.example .env >nul
    echo.
    echo [OK] Arquivo .env criado
    echo.
    echo [IMPORTANTE] Edite o arquivo .env e adicione suas API Keys!
    echo.
    echo Pressione qualquer tecla para abrir o .env no Notepad...
    pause >nul
    notepad .env
    echo.
)
echo [OK] Configuracoes OK
echo.

:: Verifica se os assets foram criados
echo [3/4] Verificando assets...
if not exist projects\\metadata.json (
    color 0E
    echo.
    echo [AVISO] Assets nao encontrados!
    echo.
    echo Executando setup inicial...
    python setup_assets.py
    echo.
    echo [OK] Assets criados
    echo.
) else (
    echo [OK] Assets OK
)
echo.

:: Menu de selecao
:menu
cls
echo.
echo ================================================================
echo.
echo      LipSync Video Generator Pro v2.0
echo.
echo ================================================================
echo.
echo.
echo [4/4] Selecione a interface:
echo.
echo     [1] Interface Profissional (app_pro.py) - RECOMENDADO
echo         -- Dashboard, Projetos, Logs em tempo real
echo.
echo     [2] Interface Original (app.py)
echo         -- Interface classica com tabs
echo.
echo     [3] Interface GUI Nativa (app_gui.py)
echo         -- Aplicacao desktop Windows
echo.
echo     [4] Executar Setup de Assets
echo         -- Recria avatares e templates
echo.
echo     [5] Sair
echo.
echo.
set /p choice="Digite sua escolha (1-5): "

if "%choice%"=="1" goto pro
if "%choice%"=="2" goto original
if "%choice%"=="3" goto gui
if "%choice%"=="4" goto setup
if "%choice%"=="5" goto exit
echo.
echo [ERRO] Opcao invalida! Tente novamente.
timeout /t 2 >nul
goto menu

:pro
cls
echo.
echo ================================================================
echo.
echo   Iniciando Interface Profissional...
echo.
echo   [OK] Dashboard
echo   [OK] Projetos
echo   [OK] Gerador
echo   [OK] Logs
echo.
echo   Acesse: http://localhost:7860
echo.
echo ================================================================
echo.
echo.
color 0B
python app_pro.py
goto end

:original
cls
echo.
echo ================================================================
echo.
echo   Iniciando Interface Original...
echo.
echo   [OK] Video Unico
echo   [OK] Processamento Lote
echo.
echo   Acesse: http://localhost:7860
echo.
echo ================================================================
echo.
echo.
color 0B
python app.py
goto end

:gui
cls
echo.
echo ================================================================
echo.
echo   Iniciando Interface GUI Nativa...
echo.
echo   Aplicacao desktop sera aberta em uma nova janela
echo.
echo ================================================================
echo.
echo.
color 0B
python app_gui.py
goto end

:setup
cls
echo.
echo ================================================================
echo.
echo   Executando Setup de Assets...
echo.
echo ================================================================
echo.
echo.
color 0E
python setup_assets.py
echo.
echo.
echo [OK] Setup concluido!
echo.
pause
goto menu

:exit
cls
echo.
echo Ate logo!
echo.
timeout /t 1 >nul
exit /b 0

:end
echo.
echo.
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRO] Erro ao executar a aplicacao!
    echo.
    echo Verifique:
    echo   - Se todas as API Keys estao configuradas no .env
    echo   - Se as dependencias foram instaladas corretamente
    echo   - Se ha erros no terminal acima
    echo.
) else (
    color 0A
    echo.
    echo [OK] Aplicacao encerrada com sucesso!
    echo.
)
pause
goto menu
