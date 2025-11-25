@echo off
chcp 65001 >nul
color 0A
title LipSync Video Generator Pro - Launcher

:: Banner
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █     🎬 LipSync Video Generator Pro v2.0                     █
echo █                                                              █
echo █     Sistema Profissional de Geração de Vídeos com IA        █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo.

:: Verifica se Python está instalado
echo [1/5] 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Por favor, instale Python 3.8+ de: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✅ Python encontrado
echo.

:: Verifica se o .env existe
echo [2/5] 🔍 Verificando configurações...
if not exist .env (
    color 0E
    echo.
    echo ⚠️  AVISO: Arquivo .env não encontrado!
    echo.
    echo Criando a partir do .env.example...
    copy .env.example .env >nul
    echo.
    echo ✅ Arquivo .env criado
    echo.
    echo 📝 IMPORTANTE: Edite o arquivo .env e adicione suas API Keys!
    echo.
    echo Pressione qualquer tecla para abrir o .env no Notepad...
    pause >nul
    notepad .env
    echo.
)
echo ✅ Configurações OK
echo.

:: Verifica dependências
echo [3/5] 📦 Verificando dependências...
pip list | findstr "gradio" >nul 2>&1
if errorlevel 1 (
    color 0E
    echo.
    echo ⚠️  Dependências não instaladas!
    echo.
    echo Deseja instalar agora? (S/N)
    set /p install_deps=
    if /i "%install_deps%"=="S" (
        echo.
        echo 📥 Instalando dependências...
        pip install -r requirements.txt
        echo.
        echo ✅ Dependências instaladas
    ) else (
        echo.
        echo ❌ Não é possível continuar sem as dependências
        pause
        exit /b 1
    )
)
echo ✅ Dependências OK
echo.

:: Verifica se os assets foram criados
echo [4/5] 🎭 Verificando assets...
if not exist projects\metadata.json (
    color 0E
    echo.
    echo ⚠️  Assets não encontrados!
    echo.
    echo Executando setup inicial...
    python setup_assets.py
    echo.
    echo ✅ Assets criados
    echo.
) else (
    echo ✅ Assets OK
)
echo.

:: Menu de seleção
:menu
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █     🎬 LipSync Video Generator Pro v2.0                     █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo.
echo [5/5] 🚀 Selecione a interface:
echo.
echo     [1] 🌟 Interface Profissional (app_pro.py) - RECOMENDADO
echo         └─ Dashboard, Projetos, Logs em tempo real
echo.
echo     [2] 📋 Interface Original (app.py)
echo         └─ Interface clássica com tabs
echo.
echo     [3] 🖥️  Interface GUI Nativa (app_gui.py)
echo         └─ Aplicação desktop Windows
echo.
echo     [4] ⚙️  Executar Setup de Assets
echo         └─ Recria avatares e templates
echo.
echo     [5] ❌ Sair
echo.
echo.
set /p choice="Digite sua escolha (1-5): "

if "%choice%"=="1" goto pro
if "%choice%"=="2" goto original
if "%choice%"=="3" goto gui
if "%choice%"=="4" goto setup
if "%choice%"=="5" goto exit
echo.
echo ❌ Opção inválida! Tente novamente.
timeout /t 2 >nul
goto menu

:pro
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo.
echo   🌟 Iniciando Interface Profissional...
echo.
echo   📊 Dashboard    ✓
echo   📁 Projetos     ✓
echo   🎬 Gerador      ✓
echo   💻 Logs         ✓
echo.
echo   Acesse: http://localhost:7860
echo.
echo ████████████████████████████████████████████████████████████████
echo.
echo.
color 0B
python app_pro.py
goto end

:original
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo.
echo   📋 Iniciando Interface Original...
echo.
echo   🎬 Vídeo Único           ✓
echo   📚 Processamento Lote    ✓
echo.
echo   Acesse: http://localhost:7860
echo.
echo ████████████████████████████████████████████████████████████████
echo.
echo.
color 0B
python app.py
goto end

:gui
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo.
echo   🖥️  Iniciando Interface GUI Nativa...
echo.
echo   Aplicação desktop será aberta em uma nova janela
echo.
echo ████████████████████████████████████████████████████████████████
echo.
echo.
color 0B
python app_gui.py
goto end

:setup
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo.
echo   ⚙️  Executando Setup de Assets...
echo.
echo ████████████████████████████████████████████████████████████████
echo.
echo.
color 0E
python setup_assets.py
echo.
echo.
echo ✅ Setup concluído!
echo.
pause
goto menu

:exit
cls
echo.
echo 👋 Até logo!
echo.
timeout /t 1 >nul
exit /b 0

:end
echo.
echo.
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ Erro ao executar a aplicação!
    echo.
    echo Verifique:
    echo   - Se todas as API Keys estão configuradas no .env
    echo   - Se as dependências foram instaladas corretamente
    echo   - Se há erros no terminal acima
    echo.
) else (
    color 0A
    echo.
    echo ✅ Aplicação encerrada com sucesso!
    echo.
)
pause
goto menu
