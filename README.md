# SubtitleToolbox v3.1

**SubtitleToolbox** 是一款专为字幕组、翻译者及办公自动化设计的全能型工具箱。v3.1 版本通过重构核心架构，实现了极佳的 Windows 高 DPI 适配与多屏工作流支持。

## ✨ v3.1 新特性

* **📺 多屏自适应居中**：重构了窗口初始化算法，通过 Windows API 实时获取主屏幕工作区，彻底解决在副屏环境下窗口偏移至左上角的 Bug。
* **🎨 紧凑型 UI 布局**：
* **顶部集成栏**：将“配置文件”与“ASS样式配置”整合至标题行，释放纵向空间。
* **智能布局**：将“智能分卷”开关移至合并工具栏，操作路径更短。


* **🧩 组件化架构**：UI 逻辑已完全拆分为 `LogComponent`、`ASSConfigWindow` 等独立模块，提升了代码的可维护性与扩展性。
* **🔍 视觉优化**：
* 关键功能开关（如智能分卷、格式选框）全面支持**微软雅黑加粗**显示。
* 进度条支持**动态显色逻辑**：任务进行时显绿，静默状态自动归位。



---

## 🛠️ 核心功能

### 1. 字幕转换 (SRT2ASS)

* 支持批量将 SRT 字幕转换为 ASS 格式。
* 内置强大的样式配置面板，支持自定义字体、颜色、边框及阴影。

### 2. 文档合并工具

* **PDF 合并**：基于 `pypdf` 实现的高性能 PDF 页面拼接。
* **Word 合并**：调用 `win32com` 原生引擎，完美保留文档格式与排版。
* **TXT 合并**：支持多种编码检测，一键合并零散文本。

### 3. 自动化处理

* **智能分卷**：自动识别文件序列，按逻辑分组处理。
* **一键日志管理**：实时反馈处理进度，支持一键清空历史记录。

---

## 🚀 快速开始

### 开发环境配置

1. 克隆仓库：
```bash
git clone https://github.com/your-repo/SubtitleToolbox.git

```


2. 安装依赖：
```bash
pip install customtkinter pysrt pysubs2 reportlab pypdf pywin32 docxcompose send2trash

```



### 运行程序

执行主入口文件：

```bash
python SubtitleToolbox.py

```

---

## 📦 打包说明

项目根目录提供了 `build.bat` 自动化打包脚本。

* **环境要求**：已安装 `PyInstaller`。
* **打包特性**：
* 开启 `--windowed` 模式，无黑窗口运行。
* 自动封装所有子模块（logic, gui, control 等）及资源文件。
* 包含 DPI 意识补丁，确保生成的 `.exe` 在不同缩放倍率下不模糊。



---

## 📂 项目结构

```text
SubtitleToolbox/
├── SubtitleToolbox.py   # 程序主入口 (含DPI及多屏修正)
├── gui/                 # UI 组件库 (Log, ASS, PathRow等)
├── logic/               # 字幕转换与文件处理核心逻辑
├── control/             # 业务逻辑控制器
├── resources/           # 图标及 UI 图片资源
└── config/              # 默认配置文件

```

---

## 📝 许可证

本项目采用 MIT 许可证。欢迎提交 Issue 或 Pull Request 参与贡献。

---

### 💡 开发者注

> 在 v3.1 中，如果您在使用 4K 屏幕或双显示器时发现窗口位置异常，程序会自动调用 `ctypes` 尝试校准。如果仍有偏差，请检查系统“显示设置”中的主屏幕标记。
