#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 UI 文件脚本
只更新图标路径为绝对路径（主题样式更新会破坏文件结构）
"""

import os
import sys
import io

# 设置标准输出为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 获取项目根目录（脚本所在目录的父目录）
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ui_file = os.path.join(base_dir, "gui", "ui_SubtitleToolbox.py")
resources_dir = os.path.join(base_dir, "resources")

print(f"项目根目录: {base_dir}")
print(f"UI 文件路径: {ui_file}")
print(f"资源目录: {resources_dir}")

# 检查文件是否存在
if not os.path.exists(ui_file):
    print(f"[错误] UI 文件不存在: {ui_file}")
    sys.exit(1)

# 读取文件内容
with open(ui_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("\n" + "="*60)
print("步骤 1: 更新图标路径")
print("="*60)

# 更新图标路径为绝对路径
old_pattern = 'Icons/'
# 构建正确的路径格式
abs_resources_path = resources_dir.replace('\\', '/')
new_pattern = abs_resources_path + '/'

count_before = content.count(old_pattern)
content = content.replace(old_pattern, new_pattern)
count_after = content.count(old_pattern)

print(f"  替换: {old_pattern} -> {new_pattern}")
print(f"  替换前: {count_before} 处")
print(f"  替换后: {count_after} 处")
print(f"  实际替换: {count_before - count_after} 处")

# 写回文件
print("\n" + "="*60)
print("步骤 2: 保存文件")
print("="*60)

with open(ui_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[OK] 已更新 {ui_file}")

# 验证语法
print("\n" + "="*60)
print("步骤 3: 验证语法")
print("="*60)

try:
    with open(ui_file, 'r', encoding='utf-8') as f:
        compile(f.read(), ui_file, 'exec')
    print("[OK] 语法验证通过")
except SyntaxError as e:
    print(f"[错误] 语法错误: {e}")
    print(f"  行号: {e.lineno}")
    print(f"  错误: {e.msg}")
    sys.exit(1)

print("\n" + "="*60)
print("更新完成！")
print("="*60)
print("\n注意: 主题样式更新未包含，因为正则表达式替换会破坏文件结构。")
print("如果需要更新主题样式，建议在 Qt Designer 中手动修改。")
