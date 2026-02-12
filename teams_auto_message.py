"""
Microsoft Teams 自动发送消息脚本（UI自动化版本）
每隔1分钟向指定账号发送"你好"消息
使用 pyautogui 模拟真实用户操作
"""

import time
import pyautogui
from datetime import datetime

# ===== 配置区域 =====
# 接收消息的联系人名称（在Teams中显示的名字）
RECIPIENT_NAME = "chunlin.jiang@consultant.volvo.com"  # 修改为实际联系人名称

# 发送的消息内容
MESSAGE = "你好"

# 发送间隔（秒）
INTERVAL = 60  # 1分钟

# 安全设置：移动鼠标到屏幕角落可以中断程序
pyautogui.FAILSAFE = True


def find_and_click_teams():
    """查找并激活Teams窗口"""
    print("正在查找 Teams 窗口...")
    # 这里可以添加窗口查找逻辑
    # 简单方式：假设Teams已经打开
    time.sleep(1)
    return True


def search_contact(name):
    """搜索联系人"""
    # 点击搜索框 (Ctrl+E 是Teams的搜索快捷键)
    pyautogui.hotkey('ctrl', 'e')
    time.sleep(0.5)
    
    # 清空搜索框
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    
    # 输入联系人名称
    pyautogui.write(name, interval=0.1)
    time.sleep(1)
    
    # 按下回车选择第一个结果
    pyautogui.press('enter')
    time.sleep(0.5)


def send_message(message):
    """发送消息"""
    # 点击消息输入框
    pyautogui.hotkey('ctrl', 'shift', 'x')  # Teams 聚焦到撰写框的快捷键
    time.sleep(0.3)
    
    # 输入消息
    pyautogui.write(message, interval=0.05)
    time.sleep(0.3)
    
    # 发送消息 (Ctrl+Enter)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(0.5)


def main():
    print("=" * 50)
    print("Teams 自动消息发送器 (UI自动化)")
    print("=" * 50)
    print(f"\n接收者: {RECIPIENT_NAME}")
    print(f"消息内容: {MESSAGE}")
    print(f"发送间隔: {INTERVAL} 秒")
    print("\n⚠️  重要提示:")
    print("1. 请确保 Teams 桌面应用已打开并登录")
    print("2. 脚本运行时请不要操作鼠标和键盘")
    print("3. 将鼠标移到屏幕左上角可紧急停止")
    print("4. 按 Ctrl+C 也可以停止程序")
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
                # 搜索联系人
                search_contact(RECIPIENT_NAME)
                
                # 发送消息
                send_message(MESSAGE)
                
                print(f"[{current_time}] 第 {count} 次 - ✓ 消息已发送: {MESSAGE}")
                
            except Exception as e:
                print(f"[{current_time}] 第 {count} 次 - ✗ 发送失败: {str(e)}")
            
            # 等待下一次发送
            if count < 999:  # 避免无限循环
                time.sleep(INTERVAL)
            else:
                print("\n已达到最大发送次数限制")
                break
                
    except KeyboardInterrupt:
        print(f"\n\n程序已停止，共发送 {count} 条消息")
    except pyautogui.FailSafeException:
        print(f"\n\n检测到紧急停止（鼠标移到角落），共发送 {count} 条消息")


if __name__ == "__main__":
    main()
