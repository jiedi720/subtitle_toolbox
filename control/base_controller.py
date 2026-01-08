import os
from PySide6.QtCore import Signal, QObject
from function.settings import ConfigManager, DEFAULT_KOR_STYLE, DEFAULT_CHN_STYLE


class BaseController(QObject):
    """
    基础控制器类，提供应用程序的核心功能和状态管理
    继承自QObject以支持信号和槽机制
    """
    # 信号定义：用于线程安全地更新GUI
    update_log = Signal(str)  # 更新日志信号
    update_progress = Signal(int)  # 更新进度条信号
    enable_start_button = Signal(bool)  # 启用/禁用开始按钮信号
    
    def __init__(self, root, startup_path=None, startup_out=None):
        """
        初始化基础控制器
        
        Args:
            root: 根窗口对象
            startup_path: 启动时的源目录路径
            startup_out: 启动时的输出目录路径
        """
        super().__init__()
        self.root = root
        
        # 初始化配置管理器
        self.config = ConfigManager()
        
        # 加载设置
        self.config.load_settings()
        
        # 将配置属性同步到控制器实例
        self.config.sync_to_controller(self)

    def load_settings(self):
        """从配置文件加载设置"""
        self.config.load_settings()
        self.config.sync_to_controller(self)

    def save_settings(self):
        """保存设置到配置文件"""
        self.config.sync_from_controller(self)
        self.config.save_settings()

    def refresh_parsed_styles(self):
        """刷新解析后的样式"""
        self.config.refresh_parsed_styles()
        self.config.sync_to_controller(self)

    def log(self, message, tag=None):
        """
        记录日志信息
        
        Args:
            message: 日志消息
            tag: 日志标签（可选）
        """
        # 使用信号线程安全地更新日志
        self.update_log.emit(message)
    
    def delete_generated_files(self):
        """删除生成的文件"""
        from function.trash import clear_output_to_trash
        import re
        
        # 获取目标目录
        target_dir = self.output_path_var.strip() or self.path_var.strip()
        if not target_dir:
            self.log("❌ 请先选择源目录或输出目录")
            return
        
        # 检查当前模式
        current_mode = getattr(self, 'task_mode', None)
        
        if current_mode == "AutoSub":
            # AutoSub 模式：只删除 .whisper.[].srt 文件
            self._delete_autosub_files(target_dir)
        else:
            # 其他模式：使用现有的清理功能
            clear_output_to_trash(target_dir, self.log)
    
    def _delete_autosub_files(self, target_dir):
        """删除 AutoSub 生成的 .whisper.[].srt 文件
        
        Args:
            target_dir: 目标目录
        """
        from send2trash import send2trash
        from PySide6.QtWidgets import QMessageBox
        
        if not os.path.exists(target_dir):
            self.log("[清理] ℹ️ 目录不存在。")
            return
        
        # 查找所有 .whisper.[].srt 文件
        whisper_files = []
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                # 匹配 .whisper.[xxx].srt 格式
                if re.search(r'\.whisper\.\[[^\]]+\]\.srt$', file, re.IGNORECASE):
                    file_path = os.path.join(root, file)
                    whisper_files.append(file_path)
        
        if not whisper_files:
            self.log("[清理] ℹ️ 未找到 .whisper.[].srt 文件。")
            return
        
        # 确认删除
        if not QMessageBox.question(
            None, 
            "确认清空", 
            f"即将删除 {len(whisper_files)} 个 AutoSub 生成的字幕文件\n确定吗？", 
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            return
        
        # 删除文件
        deleted_count = 0
        error_count = 0
        
        for file_path in whisper_files:
            try:
                send2trash(file_path)
                deleted_count += 1
                relative_path = os.path.relpath(file_path, target_dir)
                self.log(f"✓ 已删除: {relative_path}")
            except Exception as e:
                error_count += 1
                relative_path = os.path.relpath(file_path, target_dir)
                self.log(f"❌ 删除失败: {relative_path} ({e})", "error")
        
        # 汇总
        if deleted_count > 0:
            self.log(f"✅ 已清理完成，共删除 {deleted_count} 个文件", "success")
        if error_count > 0:
            self.log(f"⚠️ 有 {error_count} 个文件删除失败", "error")
    
    def get_whisper_model_config(self):
        """
        获取 Whisper 模型配置
        
        Returns:
            dict: 包含模型大小和模型路径的字典
        """
        return self.config.get_whisper_model_config()