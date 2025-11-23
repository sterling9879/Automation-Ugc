# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para aplicação GUI nativa do Windows
SEM CONSOLE - Interface gráfica pura
"""

block_cipher = None

a = Analysis(
    ['app_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
    ],
    hiddenimports=[
        # PyQt5
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        # APIs
        'elevenlabs',
        'google.generativeai',
        'google.ai.generativelanguage',
        'requests',
        'PIL',
        'PIL.Image',
        # Internos
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
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Remove interfaces não usadas
        'gradio',
        'gradio.routes',
        'gradio.blocks',
        'fastapi',
        'uvicorn',
        # Remove módulos pesados não necessários
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'pytest',
        'sphinx',
        'tk',
        'tkinter',
        '_tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LipSyncVideoGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # ⭐ SEM CONSOLE - Interface gráfica pura
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # TODO: Adicionar ícone .ico
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LipSyncVideoGenerator',
)
