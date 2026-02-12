"""
Microsoft Teams 自动发送消息脚本（支持中文）
每隔1分钟向指定账号发送"你好"消息
使用剪贴板方式支持中文输入
"""

import time
import pyautogui
import pyperclip
import pygetwindow as gw
from datetime import datetime

# ===== 配置区域 =====
# 接收消息的联系人名称（在Teams中显示的名字）
RECIPIENT_NAME = "张三"  # 修改为实际联系人名称

# 发送的消息内容
MESSAGE = "你好"

# 发送间隔（秒）
INTERVAL = 60  # 1分钟

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5  # 每个操作后暂停0.5秒


def activate_teams_window():
    """激活 Teams 窗口"""
    try:
        # 查找 Teams 窗口（可能的窗口标题）
        teams_windows = []
        for window in gw.getAllWindows():
            title = window.title.lower()
            if 'teams' in title or 'microsoft teams' in title:
                teams_windows.append(window)
        
        if teams_windows:
            # 激活第一个找到的 Teams 窗口
            teams_windows[0].activate()
            time.sleep(0.5)
            return True
        else:
            print("⚠️  未找到 Teams 窗口，请确保 Teams 已打开")
            return False
    except Exception as e:
        print(f"⚠️  激活窗口时出错: {str(e)}")
        print("提示：请手动点击 Teams 窗口使其处于前台")
        time.sleep(3)
        return True  # 继续执行，假设用户已手动激活


def search_contact(name):
    """搜索联系人"""
    # 确保在 Teams 窗口中
    activate_teams_window()
    
    # 打开搜索框
    pyautogui.hotkey('ctrl', 'e')
    time.sleep(0.8)
    
    # 清空并输入联系人名称（使用剪贴板支持中文）
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    
    # 选择第一个结果
    pyautogui.press('enter')
    time.sleep(0.8)


def send_message(message):
    """发送消息（使用剪贴板支持中文）"""
    # 点击消息输入区域（使用 Tab 键导航更可靠）
    pyautogui.press('tab')
    time.sleep(0.3)
    
    # 使用剪贴板输入消息
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # 发送消息
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(0.5)


def main():
    print("=" * 60)
    print("Teams 自动消息发送器 (支持中文)")
    print("=" * 60)
    print(f"\n接收者: {RECIPIENT_NAME}")
    print(f"消息内容: {MESSAGE}")
    print(f"发送间隔: {INTERVAL} 秒")
    print("\n⚠️  重要提示:")
    print("1. 请确保 Teams 桌面应用已打开并登录")
    print("2. 脚本会自动激活 Teams 窗口")
    print("3. 脚本运行时请不要操作鼠标和键盘")
    print("4. 将鼠标移到屏幕左上角可紧急停止")
    print("5. 按 Ctrl+C 也可以停止程序")
    
    # 检查 Teams 是否运行
    print("\n正在检查 Teams 窗口...")
    if activate_teams_window():
        print("✓ 找到 Teams 窗口")
    else:
        print("⚠️  请手动打开 Teams 并点击窗口")
        input("准备好后按回车继续...")
    
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
            time.sleep(INTERVAL)
                
    except KeyboardInterrupt:
        print(f"\n\n程序已停止，共发送 {count} 条消息")
    except pyautogui.FailSafeException:
        print(f"\n\n检测到紧急停止（鼠标移到角落），共发送 {count} 条消息")


if __name__ == "__main__":
    main()
