# -*- mode: python ; coding: utf-8 -*-

import os

# Define base path for the build directory
base_path = os.getcwd()

a = Analysis(
    ['wordguessr.py'],
    pathex=[base_path],
    binaries=[],
    datas=[
        ('wordLists/*', 'wordLists'),
        ('languages/*', 'languages'),
        ('categories.txt', '.'),
        ('version.txt', '.'),
        ('wordguessr.ico', '.'),
        ('language.ini', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WordGuessr',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='wordguessr.ico',
)
