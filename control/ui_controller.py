import os
from tkinter import messagebox, filedialog

class UIController:
    # --- 目录打开逻辑 ---
    def open_current_folder(self):
        p = self.path_var.get().strip()
        if p and os.path.isdir(p): 
            os.startfile(p)
        else: 
            messagebox.showwarning("错误", f"目录不存在:\n{p}")

    def get_output_dir(self):
        custom = self.output_path_var.get().strip()
        if custom: return custom
        source = self.path_var.get().strip()
        return os.path.join(source, "script") if source else ""

    def open_output_folder(self):
        target = self.get_output_dir()
        if not os.path.exists(target):
            try: os.makedirs(target)
            except: pass
        if os.path.isdir(target): 
            os.startfile(target)

    # --- 目录浏览逻辑 (GUI 强依赖) ---
    def browse_folder(self):
        """选择源目录"""
        d = filedialog.askdirectory(initialdir=self.path_var.get().strip() or None)
        if d: self.path_var.set(d)

    def browse_output_folder(self):
        """选择自定义输出目录"""
        initial = self.output_path_var.get().strip() or self.path_var.get().strip() or None
        d = filedialog.askdirectory(initialdir=initial)
        if d: self.output_path_var.set(d)

# --- 输入框验证逻辑 ---
    def update_path_from_entry(self, var, entry_widget):
        """验证路径并提供彩色日志反馈"""
        p = entry_widget.get().strip()
        path_type = "源文件目录" if var == self.path_var else "输出位置"

        if os.path.isdir(p):
            var.set(p)
            # 视觉反馈
            entry_widget.configure(border_color="#2ecc71") 
            self.root.after(1000, lambda: entry_widget.configure(border_color=["#979797", "#565b5e"]))
            
            # --- 关键修改：成功用绿色标签 ---
            self.log(f"✅ {path_type}设置成功: {p}", tag="success")
            self.save_settings()
        else:
            if p == "" and var == self.output_path_var:
                self.log(f"ℹ️ {path_type}已重置为默认")
                self.save_settings()
                return
            
            # 视觉反馈
            entry_widget.configure(border_color="#e74c3c") 
            self.root.after(1000, lambda: entry_widget.configure(border_color=["#979797", "#565b5e"]))
            
            # --- 关键修改：失败用红色标签 ---
            if not p:
                self.log(f"⚠️ {path_type}设置失败：路径不能为空", tag="error")
            else:
                self.log(f"❌ {path_type}设置失败：目录不存在 -> {p}", tag="error")

    # --- 预设切换逻辑 ---
    def on_preset_change(self, event):
        name = self.current_preset_name.get()
        if name in self.presets:
            self.refresh_parsed_styles()
            if hasattr(self, 'kor_panel_ui'):
                for p, parsed in [('kor', self.kor_parsed), ('chn', self.chn_parsed)]:
                    ui = getattr(self, f"{p}_panel_ui")
                    for key, val in parsed.items():
                        var_key = f"{key}_var"
                        if var_key in ui: ui[var_key].set(val)