"""
Microsoft Teams 自动发送并删除消息脚本
发送消息后等待2秒自动删除，不留痕迹
"""

import time
import pyautogui
import pyperclip
from datetime import datetime

# ===== 配置区域 =====
# 发送的消息内容
MESSAGE = "你好"

# 发送间隔（秒）
INTERVAL = 60  # 1分钟

# 删除前等待时间（秒）
DELETE_DELAY = 2  # 2秒

# 安全设置
pyautogui.FAILSAFE = True


def send_message(message):
    """发送消息"""
    # 使用剪贴板输入消息（支持中文）
    pyperclip.copy(message)
    
    # 点击输入框
    pyautogui.click()
    time.sleep(0.3)
    
    # 粘贴消息
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # 发送消息
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(0.5)


def delete_last_message_method1():
    """删除最后发送的消息 - 方法1：使用向上箭头"""
    # 等待消息发送完成
    time.sleep(DELETE_DELAY)
    
    # 按向上箭头键编辑最后一条消息
    pyautogui.press('up')
    time.sleep(0.5)
    
    # 全选并删除内容
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.3)
    
    # 按 ESC 取消编辑，这会提示删除空消息
    pyautogui.press('esc')
    time.sleep(0.3)


def delete_last_message_method2():
    """删除最后发送的消息 - 方法2：右键菜单"""
    # 等待消息发送完成
    time.sleep(DELETE_DELAY)
    
    # 向上移动一点鼠标，点击刚发送的消息
    x, y = pyautogui.position()
    pyautogui.moveTo(x, y - 50)  # 向上移动50像素
    time.sleep(0.3)
    
    # 右键点击消息
    pyautogui.rightClick()
    time.sleep(0.5)
    
    # 按 D 键选择删除（Delete 的快捷键）
    pyautogui.press('d')
    time.sleep(0.5)
    
    # 确认删除
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 鼠标移回原位
    pyautogui.moveTo(x, y)


def delete_last_message_method3():
    """删除最后发送的消息 - 方法3：鼠标悬停"""
    # 等待消息发送完成
    time.sleep(DELETE_DELAY)
    
    # 获取当前鼠标位置
    x, y = pyautogui.position()
    
    # 向上移动鼠标到消息位置
    pyautogui.moveTo(x, y - 80)
    time.sleep(0.5)
    
    # 再向右移动到消息右侧（更多选项按钮位置）
    pyautogui.moveTo(x + 300, y - 80)
    time.sleep(0.3)
    
    # 点击更多选项按钮（三个点）
    pyautogui.click()
    time.sleep(0.5)
    
    # 点击删除选项（通常是第一个或第二个）
    pyautogui.press('down')
    time.sleep(0.2)
    pyautogui.press('down')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 确认删除
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 鼠标移回原位
    pyautogui.moveTo(x, y)


def main():
    print("=" * 60)
    print("Teams 自动消息发送器 (发送后自动删除)")
    print("=" * 60)
    print(f"\n消息内容: {MESSAGE}")
    print(f"发送间隔: {INTERVAL} 秒")
    print(f"删除延迟: {DELETE_DELAY} 秒")
    print("\n⚠️  使用步骤:")
    print("1. 打开 Teams 桌面应用")
    print("2. 手动搜索并打开要发送消息的联系人聊天窗口")
    print("3. 将鼠标移到消息输入框位置")
    print("4. 回到这个终端窗口")
    print("\n⚠️  注意:")
    print("- 消息发送后会等待 2 秒自动删除")
    print("- 运行时不要移动鼠标或操作键盘")
    print("- 将鼠标移到屏幕左上角可紧急停止")
    print("- 按 Ctrl+C 也可以停止程序")
    print("\n选择删除方法:")
    print("1. 方法1：使用向上箭头（推荐，最简单）")
    print("2. 方法2：右键菜单")
    print("3. 方法3：鼠标悬停点击")
    
    method = input("\n请选择方法 (1/2/3，默认1): ").strip() or "1"
    
    if method == "1":
        delete_func = delete_last_message_method1
        print("\n使用方法1：向上箭头")
    elif method == "2":
        delete_func = delete_last_message_method2
        print("\n使用方法2：右键菜单")
    else:
        delete_func = delete_last_message_method3
        print("\n使用方法3：鼠标悬停")
    
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
                # 发送消息
                send_message(MESSAGE)
                print(f"[{current_time}] 第 {count} 次 - ✓ 消息已发送: {MESSAGE}")
                
                # 删除消息
                delete_func()
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
