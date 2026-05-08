# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec для сборки PyTrainer в один .exe."""
import sys
from pathlib import Path

block_cipher = None

ROOT = Path(SPECPATH).resolve()
SRC = ROOT / "src"

hiddenimports = [
    "pytrainer",
    "pytrainer.app",
    "pytrainer.runner",
    "pytrainer.progress",
    "pytrainer.theme",
    "pytrainer.content",
    "pytrainer.content.lessons",
    "pytrainer.content.tasks",
    "pytrainer.content.glossary",
    "pytrainer.content.flashcards",
    "pytrainer.content.achievements",
    "pytrainer.views.home",
    "pytrainer.views.lessons",
    "pytrainer.views.sandbox",
    "pytrainer.views.flashcards",
    "pytrainer.views.notes",
    "pytrainer.views.glossary",
    "pytrainer.views.achievements",
    "pytrainer.views.settings",
    "pytrainer.widgets.code_editor",
    "pytrainer.widgets.markdown_view",
    "pygments.lexers.python",
    "pygments.formatters.html",
    "pygments.styles.default",
    "pygments.styles.monokai",
    "markdown.extensions.extra",
    "markdown.extensions.sane_lists",
    "markdown.extensions.toc",
]


a = Analysis(
    [str(SRC / "pytrainer" / "__main__.py")],
    pathex=[str(SRC)],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "test",
        "unittest",
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="PyTrainer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
