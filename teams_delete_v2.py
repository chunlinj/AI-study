"""
Microsoft Teams 自动发送并删除消息脚本（精确版）
记录消息位置和删除按钮位置
"""

import time
import pyautogui
import pyperclip
from datetime import datetime

# ===== 配置区域 =====
MESSAGE = "你好"
INTERVAL = 60  # 发送间隔（秒）
DELETE_DELAY = 2  # 删除前等待（秒）

# 安全设置
pyautogui.FAILSAFE = True


def send_message(message):
    """发送消息"""
    pyperclip.copy(message)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(0.5)


def calibrate_positions():
    """校准消息和删除按钮位置"""
    print("\n" + "=" * 60)
    print("位置校准向导")
    print("=" * 60)
    
    # 步骤1：记录输入框位置
    print("\n【步骤 1/3】记录输入框位置")
    print("请在 Teams 中手动发送一条测试消息（比如'测试'）")
    print("然后将鼠标放在消息输入框中")
    input("准备好后按回车...")
    
    print("\n3秒后记录输入框位置...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    input_x, input_y = pyautogui.position()
    print(f"✓ 输入框位置: ({input_x}, {input_y})")
    
    # 步骤2：记录消息位置
    print("\n【步骤 2/3】记录消息位置")
    print("将鼠标移到刚发送的测试消息上")
    print("注意：要移到消息文字上，不是表情图标上")
    input("准备好后按回车...")
    
    print("\n3秒后记录消息位置...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    message_x, message_y = pyautogui.position()
    print(f"✓ 消息位置: ({message_x}, {message_y})")
    
    # 计算偏移
    offset_x = message_x - input_x
    offset_y = input_y - message_y
    print(f"✓ 偏移量: X={offset_x}, Y={offset_y}")
    
    # 步骤3：记录删除按钮位置
    print("\n【步骤 3/3】记录删除按钮位置")
    print("现在我会在消息位置右键点击，打开菜单")
    print("请不要移动鼠标")
    input("准备好后按回车...")
    
    print("\n3秒后右键点击...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # 移动到消息位置并右键点击
    pyautogui.moveTo(message_x, message_y, duration=0.3)
    time.sleep(0.5)
    pyautogui.rightClick()
    time.sleep(1)
    
    print("\n✓ 右键菜单已打开")
    print("现在将鼠标移到'删除'按钮上（就是那个垃圾桶图标）")
    print("不要点击，只是悬停在上面")
    input("准备好后按回车...")
    
    print("\n3秒后记录删除按钮位置...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    delete_x, delete_y = pyautogui.position()
    print(f"✓ 删除按钮位置: ({delete_x}, {delete_y})")
    
    # 计算删除按钮相对于消息的偏移
    delete_offset_x = delete_x - message_x
    delete_offset_y = delete_y - message_y
    print(f"✓ 删除按钮偏移: X={delete_offset_x}, Y={delete_offset_y}")
    
    # 关闭菜单
    pyautogui.press('esc')
    time.sleep(0.5)
    
    # 移回输入框
    pyautogui.moveTo(input_x, input_y, duration=0.3)
    
    print("\n" + "=" * 60)
    print("校准完成！")
    print("=" * 60)
    print(f"消息偏移: X={offset_x}, Y={offset_y}")
    print(f"删除按钮偏移: X={delete_offset_x}, Y={delete_offset_y}")
    
    return offset_x, offset_y, delete_offset_x, delete_offset_y


def delete_message_precise(msg_offset_x, msg_offset_y, del_offset_x, del_offset_y):
    """精确删除消息"""
    time.sleep(DELETE_DELAY)
    
    # 获取当前输入框位置
    input_x, input_y = pyautogui.position()
    
    # 计算消息位置
    message_x = input_x + msg_offset_x
    message_y = input_y - msg_offset_y
    
    # 移动到消息并右键点击
    pyautogui.moveTo(message_x, message_y, duration=0.3)
    time.sleep(0.5)
    pyautogui.rightClick()
    time.sleep(0.8)
    
    # 计算删除按钮位置
    delete_x = message_x + del_offset_x
    delete_y = message_y + del_offset_y
    
    # 移动到删除按钮并点击
    pyautogui.moveTo(delete_x, delete_y, duration=0.3)
    time.sleep(0.3)
    pyautogui.click()
    time.sleep(0.5)
    
    # 如果有确认对话框，按回车
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 移回输入框
    pyautogui.moveTo(input_x, input_y, duration=0.3)


def main():
    print("=" * 60)
    print("Teams 自动消息发送器 (精确删除版)")
    print("=" * 60)
    print(f"\n消息内容: {MESSAGE}")
    print(f"发送间隔: {INTERVAL} 秒")
    print(f"删除延迟: {DELETE_DELAY} 秒")
    
    print("\n⚠️  重要提示:")
    print("1. 整个过程请保持在 Teams 窗口中")
    print("2. 不要切换到其他应用")
    print("3. 按照提示逐步操作")
    
    # 校准位置
    msg_offset_x, msg_offset_y, del_offset_x, del_offset_y = calibrate_positions()
    
    print("\n请将鼠标放回消息输入框中")
    input("准备好后按回车开始自动发送...")
    
    print("\n程序将在 5 秒后开始...")
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
                # 发送消息
                send_message(MESSAGE)
                print(f"[{current_time}] 第 {count} 次 - ✓ 消息已发送: {MESSAGE}")
                
                # 删除消息
                delete_message_precise(msg_offset_x, msg_offset_y, del_offset_x, del_offset_y)
                print(f"[{current_time}] 第 {count} 次 - ✓ 消息已删除")
                
            except Exception as e:
                print(f"[{current_time}] 第 {count} 次 - ✗ 操作失败: {str(e)}")
            
            # 等待下一次发送
            time.sleep(INTERVAL)
                
    except KeyboardInterrupt:
        print(f"\n\n程序已停止，共发送 {count} 条消息")
    except pyautogui.FailSafeException:
        print(f"\n\n检测到紧急停止，共发送 {count} 条消息")


if __name__ == "__main__":
    main()
