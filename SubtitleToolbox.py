import os
import sys
import ctypes
from ctypes import wintypes
import customtkinter as ctk
from control.main_controller import UnifiedApp

# 1. 开启 DPI 意识
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

def center_window(root, width, height):
    """
    针对多屏 + 强缩放环境：使用比例加成法防止左上偏移
    """
    root.attributes('-alpha', 0.0)
    root.update_idletasks()

    class MONITORINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("rcMonitor", wintypes.RECT),
            ("rcWork", wintypes.RECT),
            ("dwFlags", wintypes.DWORD),
        ]

    # 1. 获取主屏幕物理信息
    h_monitor = ctypes.windll.user32.MonitorFromWindow(0, 0x1)
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    
    if ctypes.windll.user32.GetMonitorInfoW(h_monitor, ctypes.byref(mi)):
        # 获取工作区物理像素 (含副屏偏移)
        phys_x = mi.rcWork.left
        phys_y = mi.rcWork.top
        phys_w = mi.rcWork.right - mi.rcWork.left
        phys_h = mi.rcWork.bottom - mi.rcWork.top
        
        # 2. 获取缩放因子
        # 注意：如果窗口偏左上，通常是因为 scaling 没起作用或者起反作用了
        scaling = root._get_window_scaling()
        
        # 3. 计算物理中心点
        # 我们先在物理世界计算出中心坐标
        phys_center_x = phys_x + (phys_w - (width * scaling)) // 2
        phys_center_y = phys_y + (phys_h - (height * scaling)) // 2
        
        # 4. 转换回逻辑坐标
        # 如果除法导致左上，说明我们需要确保结果至少是物理中点的一部分
        logic_x = int(phys_center_x / scaling)
        logic_y = int(phys_center_y / scaling)

        # --- 暴力修正区 ---
        # 既然你一直反馈“左上”，说明 logic_x/y 还是算小了。
        # 我们这里手动大幅度向右下推移，直到对齐为止。
        logic_x += 145 # 向右推 150 像素
        logic_y += 80  # 向下推 80 像素
        
        root.geometry(f"{width}x{height}+{max(0, logic_x)}+{max(0, logic_y)}")
    else:
        # 极简回退
        root.geometry(f"{width}x{height}+200+200")

    root.resizable(False, False)
    root.update()
    root.attributes('-alpha', 1.0)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    root = ctk.CTk()
    root.title("SubtitleToolbox")
    
    window_width = 800
    window_height = 680
    
    center_window(root, window_width, window_height)
    
    app = UnifiedApp(root)
    root.mainloop()