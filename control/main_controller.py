import os
from tkinter import simpledialog
import customtkinter as ctk

# 导入同级目录下的子控制器
from .base_controller import BaseController
from .ui_controller import UIController
from .task_controller import TaskController
from .tool_controller import ToolController
from gui.main_gui import ToolboxGUI

class UnifiedApp(BaseController, UIController, TaskController, ToolController):
    def __init__(self, root, startup_path=None, startup_out=None):
        # 1. 初始化基础属性 (变量、设置、主题)
        # 注意：这里不再处理 DPI 适配和 center_window，因为入口文件已经做好了
        BaseController.__init__(self, root, startup_path, startup_out)
        
        # 2. 实例化 GUI 
        # root 此时已经是由入口文件设定的 800x680 并居中的窗口
        self.gui = ToolboxGUI(self.root, self)
        
        # 3. 设置窗口关闭协议
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """退出前保存所有当前设置"""
        self.save_settings()
        self.root.destroy()
        
    def save_preset_dialog(self):
        """保存预设的弹窗逻辑"""
        name = simpledialog.askstring("保存方案", "请输入新方案名称:", initialvalue=self.current_preset_name.get())
        if name and hasattr(self, 'kor_panel_ui'):
            name = name.strip()
            l_k = self.construct_style_line(self.kor_parsed["raw"], self.kor_panel_ui, "KOR")
            l_c = self.construct_style_line(self.chn_parsed["raw"], self.chn_panel_ui, "CHN")
            self.presets[name] = {"kor": l_k, "chn": l_c}
            self.save_settings()
            if hasattr(self.gui.ass_manager, 'preset_combo'):
                self.gui.ass_manager.preset_combo.configure(values=list(self.presets.keys()))
                self.current_preset_name.set(name)

    def construct_style_line(self, original_raw, ui_vars, style_name):
        """ASS 样式行构建工具"""
        parts = original_raw.replace("Style:", "").strip().split(',')
        parts[0] = style_name
        parts[1] = ui_vars["font_var"].get()
        parts[2] = ui_vars["size_var"].get()
        parts[3] = ui_vars["color_var"].get()
        parts[7] = "-1" if ui_vars["bold_var"].get() else "0"
        parts[19] = ui_vars["ml_var"].get()
        parts[20] = ui_vars["mr_var"].get()
        parts[21] = ui_vars["mv_var"].get()
        return "Style: " + ",".join(parts)

    def save_theme_setting(self, new_theme):
        """更新主题并保存"""
        self.theme_mode = new_theme
        self.save_settings()

    def open_config_file(self):
        """打开外部配置文件"""
        if not os.path.exists(self.config_file): 
            self.save_settings()
        os.startfile(self.config_file)