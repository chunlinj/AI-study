"""
Teams 删除消息测试脚本
用于测试和调整删除消息的鼠标位置
"""

import time
import pyautogui
import pyperclip

# 安全设置
pyautogui.FAILSAFE = True

print("=" * 60)
print("Teams 删除消息位置测试")
print("=" * 60)
print("\n步骤:")
print("1. 打开 Teams 聊天窗口")
print("2. 手动发送一条测试消息")
print("3. 将鼠标放在消息输入框中")
print("4. 回到这里按回车")
print("\n脚本会尝试删除最后一条消息")
print("如果位置不对，可以调整代码中的偏移量\n")

input("准备好后按回车...")

print("\n5秒后开始...")
for i in range(5, 0, -1):
    print(f"{i}...")
    time.sleep(1)

# 记录输入框位置
input_x, input_y = pyautogui.position()
print(f"\n输入框位置: ({input_x}, {input_y})")

# 测试不同的偏移量
offsets = [80, 100, 120, 150, 180]

for offset in offsets:
    print(f"\n测试偏移量: {offset} 像素")
    
    # 移动到消息位置
    message_y = input_y - offset
    pyautogui.moveTo(input_x, message_y, duration=0.5)
    print(f"鼠标移动到: ({input_x}, {message_y})")
    
    time.sleep(1)
    
    # 显示当前位置
    print("检查鼠标是否在消息上...")
    time.sleep(2)
    
    choice = input("是否在消息上? (y/n，按 q 退出): ").strip().lower()
    
    if choice == 'y':
        print("\n找到正确位置！尝试右键点击...")
        pyautogui.rightClick()
        time.sleep(1)
        
        print("右键菜单已打开")
        print("请手动查看菜单选项，记下删除选项的位置")
        
        input("\n按回车继续...")
        
        # 按 ESC 关闭菜单
        pyautogui.press('esc')
        break
    elif choice == 'q':
        break
    else:
        print("继续测试下一个偏移量...")
        # 移回输入框
        pyautogui.moveTo(input_x, input_y, duration=0.3)

# 移回输入框
pyautogui.moveTo(input_x, input_y, duration=0.3)
print("\n测试完成！")
print(f"如果找到了正确位置，请在脚本中使用该偏移量")
