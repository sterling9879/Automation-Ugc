; ========================================================
; Instalador NSIS para LipSync Video Generator
; ========================================================
; COMO USAR:
; 1. Instale NSIS: https://nsis.sourceforge.io/Download
; 2. Gere o executável primeiro com: build_exe.bat
; 3. Clique direito neste arquivo → "Compile NSIS Script"
; ========================================================

!define APP_NAME "LipSync Video Generator"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "Seu Nome"
!define APP_EXE "LipSync_Video_Generator.exe"
!define SOURCE_DIR "dist\LipSync_Video_Generator"

; Configurações gerais
Name "${APP_NAME}"
OutFile "LipSync_Video_Generator_Setup.exe"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "Install_Dir"
RequestExecutionLevel admin

; Interface moderna
!include "MUI2.nsh"

; Configuração da interface
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Páginas do instalador
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Páginas do desinstalador
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Idioma
!insertmacro MUI_LANGUAGE "Portuguese"

; Seção de instalação
Section "Instalação Principal" SecMain
    SetOutPath "$INSTDIR"

    ; Copia todos os arquivos
    File /r "${SOURCE_DIR}\*.*"

    ; Cria atalhos
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\Iniciar.lnk" "$INSTDIR\INICIAR.bat"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\Desinstalar.lnk" "$INSTDIR\Uninstall.exe"
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\INICIAR.bat"

    ; Registra desinstalador
    WriteRegStr HKLM "Software\${APP_NAME}" "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Mensagem final
    MessageBox MB_OK "Instalação concluída!$\n$\n\
    PRÓXIMOS PASSOS:$\n\
    1. Configure o arquivo .env com suas API keys$\n\
    2. Instale FFmpeg (se ainda não tiver)$\n\
    3. Execute o programa pelo atalho criado$\n$\n\
    Consulte README_EXE.txt para mais informações."
SectionEnd

; Seção de desinstalação
Section "Uninstall"
    ; Remove arquivos
    Delete "$INSTDIR\*.*"
    RMDir /r "$INSTDIR\_internal"
    RMDir /r "$INSTDIR\temp"
    RMDir "$INSTDIR"

    ; Remove atalhos
    Delete "$SMPROGRAMS\${APP_NAME}\*.*"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    Delete "$DESKTOP\${APP_NAME}.lnk"

    ; Remove entradas do registro
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey HKLM "Software\${APP_NAME}"
SectionEnd
