# 🎬 Subtitle Toolbox (字幕工具箱) v2.0
**Subtitle Toolbox** 是一款功能强大的本地字幕处理工具。它可以将 SRT/ASS/VTT 字幕文件批量转换为易于阅读的 PDF 剧本、Word 文档或纯文本文件，支持智能分卷、ASS 样式转换以及多格式合并。
> **v2.0 重大更新**：采用了全新的模块化架构，实现了界面与逻辑分离，新增递归搜索、智能页眉生成及万能编码解析。
---
## ✨ 核心功能
### 1. 多格式转换与生成
* **📄 字幕转 PDF**: 生成排版精美的 PDF 剧本，支持**居中页眉**（显示当前集数名称）和智能目录书签。
* **📝 字幕转 Word**: 生成 `.docx` 文档，支持分节符和独立页眉，方便二次编辑。
* **📃 字幕转 TXT**: 提取纯文本对白，自动过滤时间轴和特效标签。
* **🎨 ASS 样式转换**: 将普通字幕转换为带有双语样式（中文/外语）的高级 ASS 字幕。
### 2. 智能处理
* **🔍 递归扫描**: 自动扫描选定目录及其所有**子文件夹**中的字幕文件。
* **📦 智能分卷**: 支持按集数分组（如每 4 集生成一个文件），自动平衡卷容量。
* **📂 自动归档**: 生成的文件会自动分类存入 `pdf/`, `word/`, `txt/` 子文件夹，保持目录整洁。
* **🛠 万能解析**: 内置强健的解析器，自动识别 **UTF-8 / UTF-16 / GBK** 编码，彻底解决乱码和“方块字”问题。
### 3. 便捷工具
* **🗑️ 安全清理**: “清空输出目录”功能使用系统回收站（Recycle Bin），防止误删文件。
* **📑 文件合并**: 提供独立的 PDF、Word、TXT 合并工具，可将零散文件合并为“全剧本”。
---
## 🛠️ 项目结构 (v2.0 架构)
本项目采用 MVC 模式进行了重构，逻辑清晰，易于维护：
```text
subtitle_toolbox/
├── main.py              # 程序入口，负责调度和线程管理
├── gui.py               # 图形用户界面 (Tkinter) 代码
├── config.py            # 配置文件管理
├── logic/               # 核心逻辑模块
│   ├── utils.py         # 通用工具 (解析、分组、路径处理)
│   ├── cleaners.py      # 文本清洗正则 (去除特效、标签)
│   ├── naming.py        # 文件名识别与格式化
│   ├── pdf_logic.py     # PDF 生成与合并逻辑 (ReportLab)
│   ├── word_logic.py    # Word 生成与合并逻辑 (python-docx / win32com)
│   ├── txt_logic.py     # TXT 生成与合并逻辑
│   └── ass_logic.py     # ASS 样式处理逻辑
└── resources/           # 静态资源 (图标、字体)
```
---
## 📦 环境依赖
请确保已安装 Python 3.10+，并安装以下依赖库：
```bash
pip install reportlab python-docx pysrt pywin32 send2trash pypdf
```
* `reportlab`: 用于生成 PDF。
* `python-docx`: 用于生成 Word 文档。
* `pysrt`: 用于解析 SRT 字幕。
* `pywin32`: 用于调用 Word 进行完美合并。
* `send2trash`: 用于安全删除文件到回收站。
* `pypdf`: 用于合并 PDF 文件。
---
## 🚀 运行与打包
### 运行源码
在项目根目录下运行：
```bash
python main.py
```
### 打包为 EXE (Windows)
本项目配置了复杂的隐藏导入，请使用以下命令进行打包（确保已安装 `pyinstaller`）：
```bash
python -m PyInstaller --noconfirm --onefile --windowed --name="SubtitleToolbox" --icon="resources/subtitle-toolbox.ico" --add-data "logic;logic" --add-data "resources;resources" --add-data "resources/subtitle-toolbox.ico;." --hidden-import="reportlab" --hidden-import="reportlab.platypus" --hidden-import="reportlab.lib.styles" --hidden-import="reportlab.platypus.tableofcontents" --hidden-import="win32timezone" --hidden-import="pysrt" --hidden-import="docx" --hidden-import="win32com" --hidden-import="win32com.client" --hidden-import="pythoncom" --hidden-import="pypdf" --hidden-import="send2trash" --clean main.py
```
---
## 📝 使用指南
1. **选择源目录**：点击 `📂` 选择包含字幕文件（srt/ass/vtt）的文件夹。
2. **设置输出**：默认在源目录下生成 `script` 文件夹，也可以手动指定。
3. **选择模式**：
* **合并/转换字幕 (ASS)**：处理字幕样式。
* **生成台词剧本 (PDF/Word)**：勾选需要的格式。

4. **高级选项**：勾选“启用智能分卷”可将剧集自动分组。
5. **开始处理**：点击按钮，进度条将显示处理进度。
---
## 📄 License
此项目遵循 MIT 开源协议。
