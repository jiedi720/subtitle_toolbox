#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 UI 主题样式脚本
修改 Dark 模式下的颜色，使其跟随主题变色
"""

import os
import re

# 获取项目根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ui_file = os.path.join(base_dir, "gui", "ui_SubtitleToolbox.py")

print(f"UI 文件路径: {ui_file}")

# 读取文件内容
with open(ui_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改 QTabWidget[theme="dark"]::pane 的背景色
content = re.sub(
    r'QTabWidget\[theme="dark"\]::pane \{[^}]*background-color: #cecece;[^}]*\}',
    '''QTabWidget[theme="dark"]::pane {
    background-color: palette(base);    
    border-radius: 9px;            
    border-top-left-radius: 0px;   
    border-top-right-radius: 0px;  
    top: 0px;                     
}''',
    content,
    flags=re.DOTALL
)

# 2. 修改 QTabBar::tab 的颜色
content = re.sub(
    r'QTabBar::tab \{[^}]*color: rgb\(0, 0, 0\);[^}]*\}',
    '''QTabBar::tab { 
    color: palette(text);
    background-color: #FFC209;
    padding: 2px 1px;/*设置标签文字与标签边框之间的留白区域 */
    min-width: 84px; /*设置标签的最小宽度 */
    margin-right: 1px; /* 默认保留边距用于重叠 */
    /* 核心修改：分别设置四个角的圆弧 顺序为：左上, 右上, 右下, 左下 */
    border-top-left-radius: 9px;  
    border-top-right-radius: 9px; 
    border-bottom-left-radius: 1px;
    border-bottom-right-radius: 1px;
}''',
    content,
    flags=re.DOTALL
)

# 3. 修改 QMenu 的样式（LOG 右键菜单）
content = re.sub(
    r'QMenu \{[^}]*background-color: #333333;[^}]*color: #ffffff;[^}]*border: 1px solid #555555;[^}]*\}',
    '''QMenu {
    background-color: palette(window);
    color: palette(text);
    border: 1px solid palette(mid);
}''',
    content,
    flags=re.DOTALL
)

# 4. 修改 QMenu::item:selected 的样式
content = re.sub(
    r'QMenu::item:selected \{[^}]*background-color: #555555;[^}]*\}',
    '''QMenu::item:selected {
    background-color: palette(highlight);
    color: palette(highlighted-text);
}''',
    content,
    flags=re.DOTALL
)

# 5. 修改 QMenuBar[theme="dark"]::item:pressed 的样式
content = re.sub(
    r'QMenuBar\[theme="dark"\]::item:pressed \{[^}]*background: #989898;[^}]*\}',
    '''QMenuBar[theme="dark"]::item:pressed {
	color: palette(text);
    background: palette(mid);
    border: 1px solid transparent;
    border-radius: 5px;
}''',
    content,
    flags=re.DOTALL
)

# 6. 修改 QMenuBar[theme="light"]::item:pressed 的样式
content = re.sub(
    r'QMenuBar\[theme="light"\]::item:pressed \{[^}]*background: #e0e0e0;[^}]*\}',
    '''QMenuBar[theme="light"]::item:pressed {
    background: palette(mid);
    border: 1px solid transparent;
    border-radius: 5px;
}''',
    content,
    flags=re.DOTALL
)

# 写回文件
with open(ui_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] 已更新 gui/ui_SubtitleToolbox.py")
print("  修改内容:")
print("  1. QTabWidget[theme='dark']::pane 背景色改为 palette(base)")
print("  2. QTabBar::tab 颜色改为 palette(text)")
print("  3. QMenu 背景色改为 palette(window)，文字颜色改为 palette(text)")
print("  4. QMenu::item:selected 背景色改为 palette(highlight)")
print("  5. QMenuBar[theme='dark']::item:pressed 背景色改为 palette(mid)")
print("  6. QMenuBar[theme='light']::item:pressed 背景色改为 palette(mid)")