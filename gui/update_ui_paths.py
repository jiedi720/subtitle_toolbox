#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 ui_SubtitleToolbox.py 中的图标路径为绝对路径
"""

import os
import sys
import io

# 设置标准输出为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 文件路径
ui_file = "gui/ui_SubtitleToolbox.py"
resources_dir = "resources"

# 获取绝对路径
abs_resources_dir = os.path.abspath(resources_dir)

print(f"资源目录绝对路径: {abs_resources_dir}")

# 读取文件
with open(ui_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有 Icons/ 为绝对路径
old_pattern = 'Icons/'
new_pattern = abs_resources_dir + '/'

content = content.replace(old_pattern, new_pattern)

# 写回文件
with open(ui_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[OK] 已更新 {ui_file}")
print(f"  替换: {old_pattern} -> {new_pattern}")

# 统计替换次数
count = content.count(new_pattern)
print(f"  共替换 {count} 处")