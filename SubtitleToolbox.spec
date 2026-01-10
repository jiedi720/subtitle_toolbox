# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules, collect_all

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(SPEC))

# Full path to the icon file
ICON_PATH = os.path.join(current_dir, 'icons', 'SubtitleToolbox.ico')

# Collect all torch-related modules and files
torch_modules = collect_submodules('torch')
torch_datas = collect_data_files('torch', include_py_files=True)
torch_bins = collect_dynamic_libs('torch')

# Collect ctranslate2-related files
ctranslate2_datas = collect_data_files('ctranslate2')
ctranslate2_bins = collect_dynamic_libs('ctranslate2')

# Collect numpy-related files
numpy_datas = collect_data_files('numpy')
numpy_bins = collect_dynamic_libs('numpy')

# Add necessary DLLs using PyInstaller's automatic collection only
# This avoids duplicate DLLs and ensures they're placed in the correct locations

# Collect numpy's .libs directory DLLs
numpy_lib_datas = []
numpy_lib_dir = os.path.join('.venv', 'Lib', 'site-packages', 'numpy', '.libs')
if os.path.exists(numpy_lib_dir):
    numpy_lib_datas.append((numpy_lib_dir, 'numpy/.libs'))

# 使用 collect_all 自动收集 PIL 模块的所有依赖
# collect_all 返回 (binaries, datas, hiddenimports)
pil_binaries, pil_datas, pil_hiddenimports = collect_all('PIL')

# 去重处理：确保每个 DLL 只被打包一次
# 特别是处理不同包（如 torch、ctranslate2、PIL）可能带来的同名 DLL
seen_binaries = set()
unique_bins = []
# PyInstaller 的 binaries 格式为 (src_path, dest_path) 或 (src_path, dest_path, kind)
for binary in torch_bins + ctranslate2_bins + numpy_bins + pil_binaries:
    # 解析 binary 格式
    if len(binary) == 3:
        src_path, dest_path, kind = binary
    else:
        src_path, dest_path = binary
        kind = None
    
    # 提取文件名
    file_name = os.path.basename(src_path)
    
    # 只对通用的 .dll 文件执行严格的文件名去重
    if file_name.endswith('.dll'):
        if file_name not in seen_binaries:
            if kind is not None:
                unique_bins.append((src_path, dest_path, kind))
            else:
                unique_bins.append((src_path, dest_path))
            seen_binaries.add(file_name)
    else:
        # 对于 .pyd 文件和其他文件，不进行去重
        if kind is not None:
            unique_bins.append((src_path, dest_path, kind))
        else:
            unique_bins.append((src_path, dest_path))

a = Analysis(
    ['SubtitleToolbox.py'],
    pathex=[os.path.join('.venv', 'Lib', 'site-packages')],  # Add virtual env site-packages to path
    binaries=unique_bins,
    datas=[
        # Include project directories
        ('function', 'function'),
        ('gui', 'gui'),
        ('font', 'font'),
        ('logic', 'logic'),
        ('icons', 'icons'),
        # Include faster_whisper assets
        ('.venv/Lib/site-packages/faster_whisper/assets', 'faster_whisper/assets'),
        # Include other necessary packages
        ('.venv/Lib/site-packages/tokenizers', 'tokenizers'),
        ('.venv/Lib/site-packages/huggingface_hub', 'huggingface_hub'),
    ] + torch_datas + ctranslate2_datas + numpy_datas + numpy_lib_datas + pil_datas,
    hiddenimports=[
        # PySide6 related
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        # Windows related
        'win32com.client',
        'winreg',
        # Python standard library
        'timeit',
        'typing_extensions',
        'dataclasses',
        'importlib.metadata',
    ] + pil_hiddenimports + [
        # Project modules
        'function.controllers',
        'function.settings',
        'function.tasks',
        'function.AutoSubtitles',
        'function.file_utils',
        'function.merge',
        'function.naming',
        'function.parsers',
        'function.trash',
        'function.volumes',
        'gui.qt_gui',
        'gui.theme',
        'gui.ui_SubtitleToolbox',
        'gui.log_gui',
        'logic.pdf_logic',
        'logic.txt_logic',
        'logic.word_logic',
        'font.srt2ass',
        # Document generation libraries
        'reportlab',
        'reportlab.platypus',
        'reportlab.lib.styles',
        'reportlab.pdfgen.canvas',
        'reportlab.lib.pagesizes',
        'reportlab.lib.units',
        'pysrt',
        'pysubs2',
        'docx',
        'docx.opc',
        'docx.oxml',
        'pypdf',
        'send2trash',
        # Speech recognition libraries
        'faster_whisper',
        'faster_whisper.transcribe',
        'faster_whisper.utils',
        'ctranslate2',
        'ctranslate2.models',
        'ctranslate2.Translator',
        'numpy',
        'numpy.core._multiarray_umath',
        'numpy.fft',
        'numpy.linalg',
        'numpy.random',
        'tokenizers',
        'huggingface_hub',
        # Torch related - all necessary submodules
        'torch',
        'torch.cuda',
        'torch.backends',
        'torch.backends.cudnn',
        'torch.backends.cuda',
        'torch.version',
        'torch.distributed',
        'torch.nn',
        'torch.nn.functional',
        'torch.serialization',
        'torch.utils',
        'torch.utils.data',
        'torch.optim',
        'torch.multiprocessing',
        'torch.autograd',
        'torch.quantization',
        'torch.jit',
        'torch.onnx',
        'torch.profiler',
        'torch.testing',
        'torch.utils.tensorboard',
        'torch.utils.mobile_optimizer',
        'torch.utils.checkpoint',
        'torch.utils.dlpack',
        'torch.utils.hipify',
        'torch.utils.hooks',
        'torch.utils.cpp_extension',
    ] + torch_modules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'matplotlib',
        'pandas',
        'scipy',
        'IPython',
        'tensorboard',
        'torch.utils.tensorboard',
        'PySide6.Qt3DAnimation',
        'PySide6.Qt3DCore',
        'PySide6.Qt3DExtras',
        'PySide6.Qt3DInput',
        'PySide6.Qt3DLogic',
        'PySide6.Qt3DRender',
        'PySide6.QtCharts',
        'PySide6.QtConcurrent',
        'PySide6.QtDataVisualization',
        'PySide6.QtDesigner',
        'PySide6.QtHelp',
        'PySide6.QtLocation',
        'PySide6.QtMultimedia',
        'PySide6.QtMultimediaWidgets',
        'PySide6.QtNetwork',
        'PySide6.QtNetworkAuth',
        'PySide6.QtNfc',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtPdf',
        'PySide6.QtPdfWidgets',
        'PySide6.QtPositioning',
        'PySide6.QtPrintSupport',
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuick3D',
        'PySide6.QtQuickControls2',
        'PySide6.QtQuickWidgets',
        'PySide6.QtRemoteObjects',
        'PySide6.QtScxml',
        'PySide6.QtSensors',
        'PySide6.QtSerialPort',
        'PySide6.QtSql',
        'PySide6.QtStateMachine',
        'PySide6.QtSvg',
        'PySide6.QtSvgWidgets',
        'PySide6.QtTest',
        'PySide6.QtTextToSpeech',
        'PySide6.QtUiTools',
        'PySide6.QtWebChannel',
        'PySide6.QtWebEngine',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineQuick',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebSockets',
        'PySide6.QtXml',
        'PySide6.QtXmlPatterns',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SubtitleToolbox',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_PATH,
)

coll = COLLECT(
    exe,                # Include the EXE object defined above (main program)
    a.binaries,         # Collect all dependent DLLs/dynamic libraries
    a.datas,            # Collect all resource files (images, configs, etc.)
    strip=False,        # Whether to remove symbol table (usually False to avoid errors)
    upx=True,           # Whether to use UPX compression/obfuscation
    upx_exclude=[],     # Files to exclude from compression
    name='SubtitleToolbox',  # Final folder name that will be generated
)