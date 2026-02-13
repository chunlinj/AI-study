"""
Microsoft Teams 简化版自动发送消息脚本
手动方式：运行前请先手动打开 Teams 并点击要发送消息的联系人聊天窗口
"""

import time
import pyautogui
import pyperclip
from datetime import datetime

# ===== 配置区域 =====
# 发送的消息内容
MESSAGE = "哈哈"

# 发送间隔（秒）
INTERVAL = 60  # 1分钟

# 安全设置
pyautogui.FAILSAFE = True


def send_message(message):
    """发送消息"""
    # 使用剪贴板输入消息（支持中文）
    pyperclip.copy(message)
    
    # 点击输入框（假设已经在聊天窗口）
    pyautogui.click()
    time.sleep(0.3)
    
    # 粘贴消息
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # 发送消息
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(0.5)


def delete_last_message():
    """删除最后发送的消息"""
    # 等待2秒
    time.sleep(2)
    
    # 获取当前鼠标位置（应该在输入框）
    input_x, input_y = pyautogui.position()
    
    # 向上移动鼠标到刚发送的消息位置
    # 通常消息在输入框上方约100-150像素
    message_x = input_x
    message_y = input_y - 120
    
    # 移动到消息位置
    pyautogui.moveTo(message_x, message_y, duration=0.3)
    time.sleep(0.3)
    
    # 右键点击消息
    pyautogui.rightClick()
    time.sleep(0.8)
    
    # 在右键菜单中查找并点击"删除"
    # 通常"删除"选项在菜单中，我们可以按 D 键或者向下找
    pyautogui.press('delete')  # 尝试 Delete 键
    time.sleep(0.5)
    
    # 如果有确认对话框，按回车确认
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 移回输入框位置
    pyautogui.moveTo(input_x, input_y, duration=0.3)


def main():
    print("=" * 60)
    print("Teams 自动消息发送器 (简化版)")
    print("=" * 60)
    print(f"\n消息内容: {MESSAGE}")
    print(f"发送间隔: {INTERVAL} 秒")
    print("\n⚠️  使用步骤:")
    print("1. 打开 Teams 桌面应用")
    print("2. 手动搜索并打开要发送消息的联系人聊天窗口")
    print("3. 将鼠标移到消息输入框位置")
    print("4. 回到这个终端窗口")
    print("\n⚠️  注意:")
    print("- 脚本会在鼠标当前位置点击并发送消息")
    print("- 运行时不要移动鼠标或操作键盘")
    print("- 将鼠标移到屏幕左上角可紧急停止")
    print("- 按 Ctrl+C 也可以停止程序")
    
    input("\n准备好后按回车开始...")
    
    print("\n程序将在 5 秒后开始，请不要移动鼠标...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\n开始发送消息...\n")
    
    count = 0
    try:
        while True:
            count += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            try:
                send_message(MESSAGE)
                print(f"[{current_time}] 第 {count} 次 - ✓ 消息已发送: {MESSAGE}")
                
                # 删除消息
                delete_last_message()
                print(f"[{current_time}] 第 {count} 次 - ✓ 消息已删除")
                
            except Exception as e:
                print(f"[{current_time}] 第 {count} 次 - ✗ 操作失败: {str(e)}")
            
            # 等待下一次发送
            time.sleep(INTERVAL)
                
    except KeyboardInterrupt:
        print(f"\n\n程序已停止，共发送 {count} 条消息")
    except pyautogui.FailSafeException:
        print(f"\n\n检测到紧急停止（鼠标移到角落），共发送 {count} 条消息")


if __name__ == "__main__":
    main()
