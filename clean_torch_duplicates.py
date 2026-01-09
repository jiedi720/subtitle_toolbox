#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理打包后的重复 torch DLL 文件
删除 torch/lib 中的 DLL，因为它们已经被复制到 _internal 根目录
"""

import os
import shutil

def clean_torch_duplicates(dist_dir):
    """
    清理打包后的重复 torch DLL 文件
    
    Args:
        dist_dir: 打包后的目录路径
    """
    internal_dir = os.path.join(dist_dir, '_internal')
    torch_lib_dir = os.path.join(internal_dir, 'torch', 'lib')
    
    if not os.path.exists(torch_lib_dir):
        return
    
    # 获取 _internal 根目录中的所有 DLL 文件
    internal_dlls = set()
    if os.path.exists(internal_dir):
        for filename in os.listdir(internal_dir):
            if filename.endswith('.dll'):
                internal_dlls.add(filename)
    
    # 遍历 torch/lib 目录中的所有 DLL 文件
    for filename in os.listdir(torch_lib_dir):
        if filename.endswith('.dll'):
            # 如果 _internal 根目录中也有这个 DLL，则删除 torch/lib 中的
            if filename in internal_dlls:
                dll_path = os.path.join(torch_lib_dir, filename)
                os.remove(dll_path)
    
    # 检查 torch/lib 目录是否为空，如果为空则删除
    if os.path.exists(torch_lib_dir) and not os.listdir(torch_lib_dir):
        os.rmdir(torch_lib_dir)

if __name__ == "__main__":
    dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SubtitleToolbox')
    clean_torch_duplicates(dist_dir)
    print("清理完成！")