"""
防止电脑锁屏脚本
使用Windows API模拟按键，防止系统进入空闲状态
按 Ctrl+C 停止脚本
"""
import ctypes
import time
import sys

# Windows API 常量
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def keep_awake():
    print("=" * 50)
    print("防锁屏脚本已启动")
    print("使用Windows API保持系统活跃")
    print("按 Ctrl+C 停止脚本")
    print("=" * 50)
    
    try:
        count = 0
        while True:
            # 使用Windows API阻止系统进入睡眠和关闭显示器
            ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            )
            
            count += 1
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] 保持活跃中... (第 {count} 次)", end='\r')
            
            # 每30秒刷新一次
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\n正在恢复系统设置...")
        # 恢复系统默认电源设置
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        print("脚本已停止")
        sys.exit(0)

if __name__ == "__main__":
    keep_awake()
