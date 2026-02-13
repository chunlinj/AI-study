# Discord to Kiro Bridge 设置指南

## 功能说明

通过 Discord 聊天远程与 Windows 上的 Kiro 对话。

## 工作流程

```
Discord 消息 → Discord Bot → 写入文件 → 文件监听器 → 复制到剪贴板 → 粘贴到 Kiro
```

## 安装步骤

### 1. 安装依赖

```bash
pip install discord.py watchdog pyperclip
```

### 2. 创建 Discord Bot

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. 点击 "New Application"
3. 给应用命名（如 "Kiro Bridge"）
4. 进入 "Bot" 标签页
5. 点击 "Add Bot"
6. 在 "Privileged Gateway Intents" 中启用:
   - MESSAGE CONTENT INTENT
   - DIRECT MESSAGES
7. 复制 Bot Token（保密！）

### 3. 邀请 Bot 到服务器

1. 进入 "OAuth2" → "URL Generator"
2. 选择 Scopes: `bot`
3. 选择 Bot Permissions: 
   - Send Messages
   - Read Messages/View Channels
   - Add Reactions
4. 复制生成的 URL 并在浏览器中打开
5. 选择要添加 Bot 的服务器

### 4. 配置 Token

**方法 1: 环境变量（推荐）**

Windows CMD:
```cmd
set DISCORD_BOT_TOKEN=your_token_here
```

Windows PowerShell:
```powershell
$env:DISCORD_BOT_TOKEN="your_token_here"
```

**方法 2: .env 文件**

创建 `.env` 文件:
```
DISCORD_BOT_TOKEN=your_token_here
```

然后安装 python-dotenv:
```bash
pip install python-dotenv
```

## 使用方法

### 启动服务

**终端 1 - Discord Bot:**
```bash
python discord_to_kiro_bridge.py
```

**终端 2 - 文件监听器:**
```bash
python kiro_file_watcher.py
```

### 发送消息到 Kiro

在 Discord 中有三种方式:

1. **使用命令:**
   ```
   !kiro 你好，帮我写一个 Python 函数
   ```

2. **@提及 Bot:**
   ```
   @KiroBridge 帮我解释这段代码
   ```

3. **直接 DM Bot:**
   ```
   直接发送消息即可
   ```

### 工作流程

1. 在 Discord 发送消息
2. Bot 确认收到（✅ 反应）
3. 文件监听器自动复制到剪贴板
4. 在 Kiro 中按 `Ctrl+V` 粘贴
5. Kiro 处理并回复

## 高级功能（可选）

### 自动启动

创建 `start_bridge.bat`:
```batch
@echo off
start "Discord Bot" cmd /k python discord_to_kiro_bridge.py
start "File Watcher" cmd /k python kiro_file_watcher.py
echo Bridge started!
```

### 后台运行

使用 `pythonw.exe` 替代 `python.exe`:
```batch
start /B pythonw discord_to_kiro_bridge.py
start /B pythonw kiro_file_watcher.py
```

## 故障排除

### Bot 无法登录
- 检查 Token 是否正确
- 确认已启用 MESSAGE CONTENT INTENT

### 文件监听器不工作
- 确认安装了 watchdog 和 pyperclip
- 检查文件权限

### 剪贴板不更新
- 重启文件监听器
- 检查是否有其他程序占用剪贴板

## 安全提示

⚠️ **重要:**
- 不要分享你的 Bot Token
- 不要将 Token 提交到 Git
- 将 `.env` 添加到 `.gitignore`

## 下一步改进

- [ ] 添加 Kiro 回复自动发送回 Discord
- [ ] 支持文件上传
- [ ] 添加命令历史记录
- [ ] 支持多用户队列
- [ ] 添加 Web 界面
