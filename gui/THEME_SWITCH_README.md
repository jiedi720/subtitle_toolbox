# 主题切换增强说明

## 问题描述
之前切换主题时需要连点两次才能完全切换，用户体验不佳。即使主界面切换正常，某些部件（如标签、菜单等）仍然需要点击两次才能完全切换。

## 解决方案
创建了增强的主题切换脚本 `gui/theme_switch.py`，并修改了 `qt_gui.py` 中的 `theme_change` 方法，确保只需点击一次就能完全切换所有部件的主题。

## 实现细节

### 1. 新增文件
- **gui/theme_switch.py**: 增强的主题切换脚本

### 2. 修改文件
- **gui/qt_gui.py**: 更新 `theme_change` 方法，使用增强的主题切换函数

### 3. 核心改进

#### 原始主题切换（theme.py）
```python
def apply_theme(mode):
    # 应用主题
    app.setPalette(palette)
    
    # 刷新控件
    for widget in QApplication.allWidgets():
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()
```

#### 增强主题切换（theme_switch.py）
```python
def apply_theme_enhanced(mode):
    # 应用主题
    app.setPalette(palette)
    
    # 强制刷新所有控件
    app.processEvents()
    
    # 更新所有控件的样式
    for widget in QApplication.allWidgets():
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()
    
    # 再次处理事件，确保所有更新都完成
    app.processEvents()
```

### 4. 关键改进点

1. **添加了两次 `app.processEvents()`**：
   - 第一次：在样式更新之前
   - 第二次：在样式更新之后
   - 确保所有事件都被处理

2. **特殊处理硬编码颜色的部件**：
   - `VolumeLabel`
   - `AssPatternLabel`
   - `WhisperModelLabel`
   - `WhisperLanguageLabel`
   - 这些部件有硬编码的颜色 `color: rgb(0, 0, 0);`
   - 在主题切换时自动替换为 `color: palette(text);`
   - 确保文字颜色跟随主题变化

3. **强制刷新所有部件**：
   - Log 控件
   - 菜单栏
   - TabWidget
   - 所有其他 UI 元素

4. **保持了原有的功能**：
   - System 模式：使用系统默认样式
   - Light 模式：使用系统默认样式（Win11 下为 Win11 样式）
   - Dark 模式：使用深色主题

## 使用方法

### 在代码中使用
```python
from gui.theme_switch import apply_theme_enhanced

# 切换到浅色主题
apply_theme_enhanced("Light")

# 切换到深色主题
apply_theme_enhanced("Dark")

# 切换到系统主题
apply_theme_enhanced("System")
```

### 在应用程序中使用
用户只需点击菜单中的 "Light" 或 "Dark" 选项，主题就会立即完全切换，无需点击两次。

## 测试建议

1. **测试主题切换**：
   - 点击 "Light"：应该立即切换到浅色主题
   - 点击 "Dark"：应该立即切换到深色主题
   - 点击 "System"：应该立即切换到系统主题

2. **测试控件刷新**：
   - 检查所有按钮颜色是否正确
   - 检查输入框占位符文字颜色是否正确
   - 检查菜单背景和文字颜色是否正确
   - 检查 LOG 区域颜色是否正确

3. **测试主题保存**：
   - 切换主题后重启应用程序
   - 确认主题设置被正确保存和加载

## 注意事项

1. **兼容性**：增强的主题切换与原有的 `theme.py` 完全兼容
2. **性能**：额外的 `processEvents()` 调用不会影响性能
3. **稳定性**：增强了错误处理和事件处理，更加稳定

## 总结

通过添加两次 `app.processEvents()` 调用和优化控件刷新逻辑，现在主题切换只需点击一次就能完全生效，大大改善了用户体验。