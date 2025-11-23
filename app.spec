# -*- mode: python ; coding: utf-8 -*-
"""
Arquivo de especificação do PyInstaller para gerar executável Windows
Sistema de Geração de Vídeos com Lip-Sync
"""

block_cipher = None

# Análise dos imports e dependências
a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Adiciona arquivos de configuração e templates
        ('.env.example', '.'),
        ('README.md', '.'),
        ('QUICKSTART.md', '.'),
        ('TROUBLESHOOTING.md', '.'),
    ],
    hiddenimports=[
        # Imports explícitos que PyInstaller pode não detectar
        'gradio',
        'gradio.routes',
        'gradio.blocks',
        'gradio.components',
        'elevenlabs',
        'google.generativeai',
        'google.ai.generativelanguage',
        'requests',
        'PIL',
        'PIL.Image',
        'pathlib',
        'concurrent.futures',
        'dotenv',
        'json',
        'uuid',
        'datetime',
        'enum',
        'typing',
        'time',
        'subprocess',
        'shutil',
        'tempfile',
        'webbrowser',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Remove módulos desnecessários para reduzir tamanho
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'pytest',
        'sphinx',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Coletor de arquivos Python
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executável
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LipSync_Video_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compressão UPX para reduzir tamanho
    console=True,  # Mantém console para ver logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Adicione caminho para ícone .ico se tiver
)

# Coletor de binários e dependências
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LipSync_Video_Generator',
)
