from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QTextCharFormat, QColor, QTextCursor
from PySide6.QtCore import Qt

class LogComponent:
    def __init__(self, parent):
        self.parent = parent

        # 颜色常量定义
        self.colors = {
            "dark_bg": "#1d1e1e",
            "light_bg": "#f9f9f9",
            "dark_fg": "#ffffff",
            "light_fg": "#000000",
            "pdf_red": "#FC0273",
            "word_blue": "#2189CF",
            "success_green": "#2ecc71",  # 路径成功绿色
            "error_red": "#e74c3c"      # 路径失败红色
        }

        self.setup_ui()

    def setup_ui(self):
        # 创建 QTextEdit 组件
        self.widget = QTextEdit(self.parent)
        self.widget.setFixedHeight(150)
        self.widget.setReadOnly(True)

        # 设置字体
        font = self.widget.font()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.widget.setFont(font)

        # 初始检测主题（从父窗口获取）
        is_dark = hasattr(self.parent, 'is_dark_theme') and self.parent.is_dark_theme
        self.apply_theme(is_dark)

        # 创建颜色格式
        self.formats = {
            "pdf_red": self.create_format(self.colors["pdf_red"]),
            "word_blue": self.create_format(self.colors["word_blue"]),
            "success": self.create_format(self.colors["success_green"]),
            "error": self.create_format(self.colors["error_red"]),
        }

    def create_format(self, color):
        """创建文本格式"""
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        return fmt

    def apply_theme(self, is_dark):
        """应用主题"""
        bg = self.colors["dark_bg"] if is_dark else self.colors["light_bg"]
        fg = self.colors["dark_fg"] if is_dark else self.colors["light_fg"]
        border = "#3d3d3d" if is_dark else "#dbdbdb"

        self.widget.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {border};
                padding: 12px;
            }}
        """)

    def update_theme(self, mode):
        """当系统切换主题时，手动调整组件颜色"""
        is_dark = (mode == "Dark")
        self.apply_theme(is_dark)

    def clear(self):
        """清空日志区域"""
        self.widget.clear()

    def write_log(self, message, tag=None):
        """写入日志内容"""
        cursor = self.widget.textCursor()
        cursor.movePosition(QTextCursor.End)

        if tag and tag in self.formats:
            cursor.insertText(str(message) + "\n", self.formats[tag])
        else:
            cursor.insertText(str(message) + "\n")

        # 滚动到底部
        self.widget.setTextCursor(cursor)
        self.widget.ensureCursorVisible()

    def append(self, message):
        """为了兼容性增加的别名方法"""
        self.write_log(message)