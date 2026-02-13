"""
Kiro 文件监听器
监听文件变化并自动将内容复制到剪贴板，方便粘贴到 Kiro

使用方法:
1. 运行此脚本: python kiro_file_watcher.py
2. 当 Discord bot 写入新消息时，会自动复制到剪贴板
3. 在 Kiro 中按 Ctrl+V 粘贴
"""

import time
import pyperclip
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FILE = "kiro_input.txt"

class KiroFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_content = ""
        
    def on_modified(self, event):
        if event.src_path.endswith(WATCH_FILE):
            try:
                with open(WATCH_FILE, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                if content and content != self.last_content:
                    self.last_content = content
                    pyperclip.copy(content)
                    print(f"\n✅ 新消息已复制到剪贴板:")
                    print(f"{'='*50}")
                    print(content[:200] + ('...' if len(content) > 200 else ''))
                    print(f"{'='*50}")
                    print("📋 在 Kiro 中按 Ctrl+V 粘贴\n")
                    
            except Exception as e:
                print(f"❌ 错误: {e}")

def main():
    # 确保文件存在
    Path(WATCH_FILE).touch(exist_ok=True)
    
    print("🔍 Kiro 文件监听器已启动")
    print(f"📂 监听文件: {WATCH_FILE}")
    print("⏳ 等待 Discord 消息...\n")
    
    event_handler = KiroFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 监听器已停止")
        
    observer.join()

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print("❌ 缺少依赖库，请安装:")
        print("pip install watchdog pyperclip")
