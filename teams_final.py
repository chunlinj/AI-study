"""
Microsoft Teams 自动发送并删除消息脚本（最终版）
使用图像识别或坐标记录方式精确删除消息
"""

import time
import pyautogui
import pyperclip
from datetime import datetime

# ===== 配置区域 =====
MESSAGE = "你好"
INTERVAL = 60  # 发送间隔（秒）
DELETE_DELAY = 2  # 删除前等待（秒）

# 消息位置偏移量（需要根据你的屏幕调整）
MESSAGE_Y_OFFSET = 120  # 消息在输入框上方的像素距离

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


def delete_last_message_by_position(input_x, input_y):
    """通过位置删除消息"""
    time.sleep(DELETE_DELAY)
    
    # 移动到消息位置
    message_y = input_y - MESSAGE_Y_OFFSET
    pyautogui.moveTo(input_x, message_y, duration=0.3)
    time.sleep(0.5)
    
    # 右键点击
    pyautogui.rightClick()
    time.sleep(0.8)
    
    # 尝试多种方式触发删除
    # 方式1: 按 Delete 键
    pyautogui.press('delete')
    time.sleep(0.3)
    
    # 如果没反应，尝试方式2: 按 D 键
    if pyautogui.position() != (input_x, message_y):
        pyautogui.press('d')
        time.sleep(0.3)
    
    # 确认删除
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 移回输入框
    pyautogui.moveTo(input_x, input_y, duration=0.3)


def setup_message_position():
    """设置消息位置 - 只记录相对偏移"""
    print("\n=== 位置校准 ===")
    print("重要：整个过程请保持在 Teams 窗口中，不要切换到其他应用！")
    print("\n步骤:")
    print("1. 在 Teams 中手动发送一条测试消息")
    print("2. 将鼠标移到消息输入框中（点击一下）")
    print("3. 按回车记录输入框位置")
    
    input("\n准备好后按回车...")
    
    print("\n3秒后记录输入框位置，请保持鼠标在输入框中...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    input_x, input_y = pyautogui.position()
    print(f"✓ 输入框位置: ({input_x}, {input_y})")
    
    print("\n现在将鼠标向上移动，悬停在刚发送的消息上")
    print("（不要点击，只是悬停）")
    input("准备好后按回车...")
    
    print("\n3秒后记录消息位置，请保持鼠标在消息上...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    message_x, message_y = pyautogui.position()
    print(f"✓ 消息位置: ({message_x}, {message_y})")
    
    # 计算相对偏移
    offset_x = message_x - input_x
    offset_y = input_y - message_y  # 注意：消息在上方，所以是 input_y - message_y
    
    print(f"\n✓ 计算出的偏移量:")
    print(f"  X偏移: {offset_x} 像素")
    print(f"  Y偏移: {offset_y} 像素（消息在输入框上方）")
    
    return offset_x, offset_y


def delete_by_offset(offset_x, offset_y):
    """使用偏移量删除消息（相对于当前输入框位置）"""
    time.sleep(DELETE_DELAY)
    
    # 获取当前输入框位置（应该还在输入框）
    input_x, input_y = pyautogui.position()
    
    # 计算消息位置
    message_x = input_x + offset_x
    message_y = input_y - offset_y
    
    # 移动到消息位置
    pyautogui.moveTo(message_x, message_y, duration=0.3)
    time.sleep(0.5)
    
    # 右键点击
    pyautogui.rightClick()
    time.sleep(0.8)
    
    # 按 Delete 键
    pyautogui.press('delete')
    time.sleep(0.3)
    
    # 确认
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 移回输入框
    pyautogui.moveTo(input_x, input_y, duration=0.3)


def main():
    print("=" * 60)
    print("Teams 自动消息发送器 (发送后自动删除 - 最终版)")
    print("=" * 60)
    print(f"\n消息内容: {MESSAGE}")
    print(f"发送间隔: {INTERVAL} 秒")
    print(f"删除延迟: {DELETE_DELAY} 秒")
    
    print("\n选择模式:")
    print("1. 自动模式（使用默认偏移量 120 像素）")
    print("2. 校准模式（记录精确偏移量）")
    
    mode = input("\n请选择 (1/2，默认1): ").strip() or "1"
    
    if mode == "2":
        # 校准模式 - 记录偏移量
        offset_x, offset_y = setup_message_position()
        use_offset = True
    else:
        # 自动模式 - 使用默认值
        print("\n使用自动模式（默认偏移量）")
        offset_x = 0
        offset_y = MESSAGE_Y_OFFSET
        use_offset = True
    
    print("\n请将鼠标放在 Teams 消息输入框中")
    print("重要：运行过程中请不要切换窗口！")
    
    input("\n准备好后按回车开始...")
    
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
                
                # 删除消息（使用偏移量）
                delete_by_offset(offset_x, offset_y)
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
