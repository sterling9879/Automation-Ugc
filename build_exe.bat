@echo off
REM ========================================================
REM Script de Build - Gera executável Windows do sistema
REM ========================================================

echo.
echo ========================================================
echo   BUILD: Gerador de Videos com Lip-Sync
echo ========================================================
echo.

REM Verifica se está no ambiente virtual
if not exist "venv\" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute primeiro: install.bat
    echo.
    pause
    exit /b 1
)

echo [1/6] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [2/6] Instalando PyInstaller...
pip install pyinstaller --quiet

echo.
echo [3/6] Limpando builds anteriores...
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist

echo.
echo [4/6] Gerando executavel com PyInstaller...
echo (Isso pode levar alguns minutos...)
echo.
pyinstaller app.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao gerar executavel!
    echo.
    pause
    exit /b 1
)

echo.
echo [5/6] Criando estrutura de distribuicao...

REM Cria pasta de distribuição
if not exist "dist\LipSync_Video_Generator\config\" mkdir "dist\LipSync_Video_Generator\config"

REM Copia arquivo .env.example
copy ".env.example" "dist\LipSync_Video_Generator\.env.example" >nul

REM Cria arquivo de instruções
echo Criando README_EXE.txt...
(
echo ========================================================
echo  GERADOR DE VIDEOS COM LIP-SYNC - Versao Executavel
echo ========================================================
echo.
echo INSTRUCOES DE USO:
echo.
echo 1. CONFIGURACAO INICIAL:
echo    - Renomeie o arquivo ".env.example" para ".env"
echo    - Abra o arquivo .env com Bloco de Notas
echo    - Adicione suas API keys:
echo      * GEMINI_API_KEY=sua_chave_aqui
echo      * ELEVENLABS_API_KEY=sua_chave_aqui
echo      * WAVESPEED_API_KEY=sua_chave_aqui
echo.
echo 2. INSTALACAO DO FFMPEG:
echo    - Baixe FFmpeg de: https://ffmpeg.org/download.html
echo    - Extraia em C:\ffmpeg
echo    - Adicione C:\ffmpeg\bin ao PATH do Windows
echo.
echo 3. EXECUTAR O PROGRAMA:
echo    - Duplo clique em "LipSync_Video_Generator.exe"
echo    - Aguarde a interface abrir no navegador
echo    - Se nao abrir automaticamente, acesse:
echo      http://localhost:7860
echo.
echo 4. USAR A INTERFACE:
echo    - Cole seu roteiro no campo de texto
echo    - Selecione a voz e modelo do ElevenLabs
echo    - Faca upload das imagens do apresentador
echo    - Clique em "Gerar Video"
echo.
echo NOTAS IMPORTANTES:
echo - Mantenha o console aberto enquanto usa o programa
echo - Os arquivos temporarios ficam na pasta "temp"
echo - Verifique os logs no console em caso de erros
echo.
echo SUPORTE:
echo - README.md: Documentacao completa
echo - QUICKSTART.md: Guia rapido de inicio
echo - TROUBLESHOOTING.md: Solucao de problemas
echo.
echo ========================================================
) > "dist\LipSync_Video_Generator\README_EXE.txt"

REM Cria script de inicialização amigável
echo Criando INICIAR.bat...
(
echo @echo off
echo cls
echo.
echo ========================================================
echo   GERADOR DE VIDEOS COM LIP-SYNC
echo ========================================================
echo.
echo Iniciando aplicacao...
echo.
echo A interface web sera aberta automaticamente em:
echo http://localhost:7860
echo.
echo Mantenha esta janela aberta enquanto usa o programa.
echo Pressione Ctrl+C para fechar.
echo.
echo ========================================================
echo.
echo.
echo LipSync_Video_Generator.exe
) > "dist\LipSync_Video_Generator\INICIAR.bat"

echo.
echo [6/6] Verificando arquivos gerados...

if exist "dist\LipSync_Video_Generator\LipSync_Video_Generator.exe" (
    echo.
    echo ========================================================
    echo  BUILD CONCLUIDO COM SUCESSO!
    echo ========================================================
    echo.
    echo Executavel criado em:
    echo   dist\LipSync_Video_Generator\
    echo.
    echo Arquivos gerados:
    echo   - LipSync_Video_Generator.exe  (executavel principal^)
    echo   - INICIAR.bat                  (atalho de inicio^)
    echo   - README_EXE.txt               (instrucoes de uso^)
    echo   - .env.example                 (template de configuracao^)
    echo   - Bibliotecas e dependencias
    echo.
    echo PROXIMOS PASSOS:
    echo   1. Abra a pasta: dist\LipSync_Video_Generator\
    echo   2. Configure o arquivo .env com suas API keys
    echo   3. Execute INICIAR.bat ou LipSync_Video_Generator.exe
    echo.
    echo Para distribuir:
    echo   - Compacte a pasta "LipSync_Video_Generator" em ZIP
    echo   - Distribua o arquivo ZIP
    echo   - Usuario deve extrair e configurar .env
    echo.
    echo ========================================================
    echo.
) else (
    echo.
    echo [ERRO] Executavel nao foi gerado!
    echo Verifique os logs acima para detalhes.
    echo.
)

pause
