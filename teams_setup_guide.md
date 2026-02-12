# Teams 自动消息发送器 - 使用指南（UI自动化版本）

## 前置要求

1. 安装依赖包：
```bash
pip install pyautogui
```

2. 确保 Microsoft Teams 桌面应用已安装并登录

## 配置步骤

### 1. 编辑脚本配置
打开 `teams_auto_message.py`，修改以下配置：

```python
# 接收消息的联系人名称（在Teams中显示的名字）
RECIPIENT_NAME = "张三"  # 改为你要发送消息的联系人名称

# 发送的消息内容
MESSAGE = "你好"  # 可以修改为任何消息

# 发送间隔（秒）
INTERVAL = 60  # 1分钟，可以调整
```

### 2. 准备 Teams 应用
1. 打开 Microsoft Teams 桌面应用
2. 确保已登录你的账号
3. 确认能在搜索中找到目标联系人

## 使用方法

### 运行脚本
```bash
python teams_auto_message.py
```

### 脚本运行流程
1. 显示配置信息和注意事项
2. 5秒倒计时准备
3. 自动执行以下操作：
   - 使用 Ctrl+E 打开搜索框
   - 输入联系人名称
   - 按回车打开聊天
   - 输入消息内容
   - 使用 Ctrl+Enter 发送消息
   - 等待指定时间后重复

### 停止脚本
有三种方式停止：
1. 按 `Ctrl+C`
2. 将鼠标快速移到屏幕左上角（紧急停止）
3. 等待达到最大发送次数（999次）

## Teams 快捷键说明

脚本使用的 Teams 快捷键：
- `Ctrl+E` - 打开搜索框
- `Ctrl+Shift+X` - 聚焦到消息撰写框
- `Ctrl+Enter` - 发送消息

## 注意事项

⚠️ **重要提醒**：

1. **运行环境**
   - 脚本运行时会控制鼠标和键盘
   - 请不要在脚本运行时操作电脑
   - 建议在独立的虚拟机或测试环境中运行

2. **Teams 窗口**
   - Teams 必须保持打开状态
   - 不要最小化 Teams 窗口
   - 确保 Teams 窗口没有被其他窗口遮挡

3. **联系人名称**
   - 必须使用 Teams 中显示的准确名称
   - 区分大小写
   - 如果有多个同名联系人，会选择第一个

4. **使用限制**
   - 仅用于学习和测试目的
   - 频繁发送消息可能违反公司政策
   - 可能被视为骚扰行为
   - 使用前请获得接收者同意

5. **安全性**
   - 脚本会模拟真实用户操作
   - 所有操作都通过你已登录的 Teams 账号执行
   - 不需要提供密码或 API 密钥

## 故障排除

### 问题：找不到联系人
- 检查 `RECIPIENT_NAME` 是否与 Teams 中显示的名称完全一致
- 尝试手动在 Teams 中搜索该名称，确认能找到
- 如果是中文名，确保编码正确

### 问题：消息没有发送
- 确认 Teams 窗口处于活动状态
- 检查是否有弹窗或通知遮挡
- 尝试增加 `time.sleep()` 的等待时间

### 问题：脚本运行太快或太慢
- 调整脚本中的 `time.sleep()` 参数
- 根据你的电脑性能适当增减等待时间

### 问题：中文输入失败
- pyautogui 可能不支持直接输入中文
- 需要使用剪贴板方式（见下方改进版本）

## 改进建议

如果需要发送中文消息，可以使用剪贴板方式：

```python
import pyperclip

def send_message(message):
    # 复制消息到剪贴板
    pyperclip.copy(message)
    
    # 聚焦到撰写框
    pyautogui.hotkey('ctrl', 'shift', 'x')
    time.sleep(0.3)
    
    # 粘贴消息
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # 发送
    pyautogui.hotkey('ctrl', 'enter')
```

需要安装：`pip install pyperclip`
