嗯i"""
Discord to Kiro Bridge
通过 Discord 消息远程与 Kiro 对话

使用方法:
1. 在 Discord Developer Portal 创建 bot 并获取 token
2. 设置环境变量 DISCORD_BOT_TOKEN
3. 运行此脚本: python discord_to_kiro_bridge.py
4. 在 Discord 中 @bot 或发送 DM 来与 Kiro 对话
"""

import discord
import asyncio
import os
import json
from datetime import datetime
from pathlib import Path

# 配置
KIRO_INPUT_FILE = "kiro_input.txt"
KIRO_OUTPUT_FILE = "kiro_output.txt"
COMMAND_PREFIX = "!kiro"

class KiroBridge(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        super().__init__(intents=intents)
        
        # 确保文件存在
        Path(KIRO_INPUT_FILE).touch(exist_ok=True)
        Path(KIRO_OUTPUT_FILE).touch(exist_ok=True)
        
    async def on_ready(self):
        print(f'✅ Bot 已登录: {self.user}')
        print(f'📝 使用 {COMMAND_PREFIX} <消息> 或直接 DM bot 来与 Kiro 对话')
        print(f'📂 输入文件: {KIRO_INPUT_FILE}')
        print(f'📂 输出文件: {KIRO_OUTPUT_FILE}')
        
    async def on_message(self, message):
        # 忽略自己的消息
        if message.author == self.user:
            return
            
        # 检查是否是命令或 DM
        is_dm = isinstance(message.channel, discord.DMChannel)
        is_command = message.content.startswith(COMMAND_PREFIX)
        is_mention = self.user in message.mentions
        
        if not (is_dm or is_command or is_mention):
            return
            
        # 提取消息内容
        content = message.content
        if is_command:
            content = content[len(COMMAND_PREFIX):].strip()
        elif is_mention:
            content = content.replace(f'<@{self.user.id}>', '').strip()
            
        if not content:
            await message.reply("请提供要发送给 Kiro 的消息")
            return
            
        # 发送确认
        await message.add_reaction('⏳')
        
        try:
            # 写入 Kiro 输入文件
            with open(KIRO_INPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(content)
            
            await message.remove_reaction('⏳', self.user)
            await message.add_reaction('✅')
            
            # 发送确认消息
            embed = discord.Embed(
                title="📨 消息已发送到 Kiro",
                description=f"```{content[:500]}```",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            embed.set_footer(text="请在 Kiro 中查看并回复")
            await message.reply(embed=embed)
            
            # 提示用户如何获取回复
            await message.channel.send(
                "💡 提示: 在 Kiro 中处理完成后，使用 `!kiro-response` 获取回复"
            )
            
        except Exception as e:
            await message.remove_reaction('⏳', self.user)
            await message.add_reaction('❌')
            await message.reply(f"❌ 错误: {str(e)}")

def main():
    # 从环境变量获取 token
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        print("❌ 错误: 请设置环境变量 DISCORD_BOT_TOKEN")
        print("\n设置方法:")
        print("Windows CMD: set DISCORD_BOT_TOKEN=your_token_here")
        print("Windows PowerShell: $env:DISCORD_BOT_TOKEN='your_token_here'")
        print("\n或创建 .env 文件:")
        print("DISCORD_BOT_TOKEN=your_token_here")
        return
        
    client = KiroBridge()
    
    try:
        client.run(token)
    except discord.LoginFailure:
        print("❌ 登录失败: Token 无效")
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()
