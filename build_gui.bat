@echo off
REM ========================================================
REM Build - Aplicação GUI Nativa do Windows
REM Interface PyQt5 - SEM CONSOLE
REM ========================================================

echo.
echo ========================================================
echo   BUILD: GUI Nativa - LipSync Video Generator
echo ========================================================
echo.

REM Verifica ambiente virtual
if not exist "venv\" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute primeiro: install.bat
    pause
    exit /b 1
)

echo [1/7] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [2/7] Instalando PyQt5...
pip install PyQt5 --quiet

echo.
echo [3/7] Instalando PyInstaller...
pip install pyinstaller --quiet

echo.
echo [4/7] Limpando builds anteriores...
if exist "build\" rmdir /s /q build
if exist "dist\LipSyncVideoGenerator\" rmdir /s /q "dist\LipSyncVideoGenerator"

echo.
echo [5/7] Gerando executavel GUI nativo...
echo (Interface grafica pura, sem console)
echo (Isso pode levar alguns minutos...)
echo.

pyinstaller app_gui.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao gerar executavel!
    pause
    exit /b 1
)

echo.
echo [6/7] Criando estrutura de distribuicao...

REM Copia .env.example
copy ".env.example" "dist\LipSyncVideoGenerator\.env.example" >nul

REM Cria README para usuário final
echo Criando README_GUI.txt...
(
echo ========================================================
echo  LIPSYNC VIDEO GENERATOR - Aplicacao Nativa Windows
echo ========================================================
echo.
echo PROGRAMA DE GERACAO DE VIDEOS COM LIP-SYNC
echo Interface grafica profissional para Windows
echo.
echo ========================================================
echo  CONFIGURACAO INICIAL
echo ========================================================
echo.
echo 1. RENOMEIE O ARQUIVO:
echo    .env.example --^> .env
echo.
echo 2. ABRA O ARQUIVO .env E ADICIONE SUAS API KEYS:
echo.
echo    GEMINI_API_KEY=sua_chave_do_gemini_aqui
echo    ELEVENLABS_API_KEY=sua_chave_do_elevenlabs_aqui
echo    WAVESPEED_API_KEY=sua_chave_do_wavespeed_aqui
echo.
echo    Onde obter as chaves:
echo    - Gemini: https://ai.google.dev/
echo    - ElevenLabs: https://elevenlabs.io/
echo    - WaveSpeed: https://wavespeed.ai/
echo.
echo 3. INSTALE FFMPEG:
echo    - Baixe: https://ffmpeg.org/download.html
echo    - Extraia em C:\ffmpeg
echo    - Adicione C:\ffmpeg\bin ao PATH do Windows
echo.
echo    Verificar instalacao:
echo    - Abra CMD e digite: ffmpeg -version
echo.
echo ========================================================
echo  COMO USAR
echo ========================================================
echo.
echo 1. Duplo clique em: LipSyncVideoGenerator.exe
echo.
echo 2. Na interface:
echo    - Cole seu roteiro no campo de texto
echo    - Selecione a voz do ElevenLabs
echo    - Escolha o modelo de voz
echo    - Adicione imagens do apresentador ^(1-20 imagens^)
echo    - Clique em "GERAR VIDEO"
echo.
echo 3. Aguarde o processamento:
echo    - Progresso mostrado em tempo real
echo    - Logs visiveis no painel direito
echo    - Pode levar varios minutos
echo.
echo 4. Video pronto:
echo    - Botao "Abrir Video" para assistir
echo    - Botao "Abrir Pasta" para ver arquivos
echo.
echo ========================================================
echo  RECURSOS
echo ========================================================
echo.
echo - Interface grafica nativa do Windows
echo - Processamento em background ^(nao trava^)
echo - Barra de progresso em tempo real
echo - Logs detalhados de cada etapa
echo - Suporte a multiplas imagens
echo - Processamento paralelo de videos
echo - Selecao de modelos do ElevenLabs
echo.
echo ========================================================
echo  SOLUCAO DE PROBLEMAS
echo ========================================================
echo.
echo Erro: "FFmpeg nao encontrado"
echo   ^> Instale FFmpeg e adicione ao PATH
echo.
echo Erro: "API key invalida"
echo   ^> Verifique o arquivo .env
echo   ^> Certifique-se de nao ter espacos extras
echo.
echo Erro: "Nenhuma voz disponivel"
echo   ^> Verifique ELEVENLABS_API_KEY no .env
echo   ^> Teste em: https://elevenlabs.io/
echo.
echo Programa nao abre:
echo   ^> Execute como Administrador
echo   ^> Verifique antivirus/firewall
echo.
echo ========================================================
echo  SUPORTE
echo ========================================================
echo.
echo Para mais informacoes:
echo - README.md ^(documentacao completa^)
echo - TROUBLESHOOTING.md ^(solucao de problemas^)
echo - GitHub: [URL do projeto]
echo.
echo ========================================================
) > "dist\LipSyncVideoGenerator\README_GUI.txt"

echo.
echo [7/7] Verificando arquivos gerados...

if exist "dist\LipSyncVideoGenerator\LipSyncVideoGenerator.exe" (
    echo.
    echo ========================================================
    echo  BUILD CONCLUIDO COM SUCESSO!
    echo ========================================================
    echo.
    echo Aplicacao GUI nativa criada em:
    echo   dist\LipSyncVideoGenerator\
    echo.
    echo Arquivos gerados:
    echo   - LipSyncVideoGenerator.exe   ^(programa Windows nativo^)
    echo   - README_GUI.txt               ^(instrucoes de uso^)
    echo   - .env.example                 ^(configuracao^)
    echo   - _internal\                   ^(bibliotecas^)
    echo.
    echo CARACTERISTICAS:
    echo   ✓ Interface grafica nativa ^(PyQt5^)
    echo   ✓ SEM console ^(janela preta^)
    echo   ✓ Design moderno e profissional
    echo   ✓ Logs e progresso em tempo real
    echo   ✓ Threads para nao travar interface
    echo   ✓ Tamanho: ~200-300 MB
    echo.
    echo PROXIMOS PASSOS:
    echo   1. Entre em: dist\LipSyncVideoGenerator\
    echo   2. Configure .env com suas API keys
    echo   3. Execute: LipSyncVideoGenerator.exe
    echo.
    echo DISTRIBUIR:
    echo   - Compacte a pasta completa em ZIP
    echo   - Usuario extrai e executa o .exe
    echo   - Nao precisa de Python instalado!
    echo.
    echo ========================================================
    echo.
) else (
    echo.
    echo [ERRO] Executavel nao foi gerado!
    echo.
)

pause
