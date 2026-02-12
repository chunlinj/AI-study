"""
第4周 - 4.3 MCP (Model Context Protocol) 协议
目标：
- 理解 MCP 协议的意义和架构
- 安装和使用现有 MCP Server
- 开发自己的 MCP Server
- 集成 MCP 到 Agent

MCP 是 Anthropic 在 2024 年底推出的开放协议，用于标准化 AI 与工具的交互
"""

# ============ 安装依赖 ============
"""
运行前先安装：
pip install mcp                    # MCP Python SDK
pip install httpx                  # HTTP 客户端
pip install fastmcp               # 快速创建 MCP Server（可选）

MCP 官方文档：https://modelcontextprotocol.io/
"""

# ============================================================
# 第1部分：MCP 协议是什么？
# ============================================================
"""
🔌 MCP = Model Context Protocol（模型上下文协议）

一、为什么需要 MCP？

传统方式的问题：
┌─────────────────────────────────────────────────────────┐
│  每个 AI 应用都要自己实现工具调用                         │
│                                                          │
│  Claude App ──┬── 自己写代码调用文件系统                  │
│               ├── 自己写代码调用数据库                    │
│               └── 自己写代码调用 GitHub                   │
│                                                          │
│  ChatGPT App ──┬── 又自己写一遍文件系统                   │
│                ├── 又自己写一遍数据库                     │
│                └── 又自己写一遍 GitHub                    │
│                                                          │
│  问题：重复工作、接口不统一、难以复用                      │
└─────────────────────────────────────────────────────────┘

MCP 的解决方案：
┌─────────────────────────────────────────────────────────┐
│  统一的协议标准                                          │
│                                                          │
│  Claude/ChatGPT/Any AI  ←──MCP协议──→  MCP Server       │
│                                          ├── 文件系统    │
│                                          ├── 数据库      │
│                                          └── GitHub      │
│                                                          │
│  优点：一次开发，到处使用                                 │
└─────────────────────────────────────────────────────────┘

二、MCP 架构

┌──────────────┐         MCP 协议         ┌──────────────┐
│  MCP Client  │ ←───────────────────────→│  MCP Server  │
│  (AI 应用)   │    JSON-RPC over stdio   │  (工具提供方) │
└──────────────┘                          └──────────────┘
      │                                          │
      │                                          │
  Claude Desktop                          可以是任何服务：
  Cursor IDE                              - 文件系统访问
  自定义 Agent                            - 数据库查询
                                          - API 调用
                                          - 浏览器控制

三、MCP 的三大核心概念

1. Tools（工具）
   - 可执行的操作，如：读文件、发邮件、查天气
   - AI 可以调用这些工具
   
2. Resources（资源）
   - 只读的数据源，如：文档、数据库表
   - AI 可以读取这些资源作为上下文
   
3. Prompts（提示模板）
   - 预定义的 prompt 模板
   - 帮助 AI 更好地使用工具

四、MCP vs 传统 API vs LangChain Tool

┌─────────────────┬─────────────────┬─────────────────┐
│     传统 API     │  LangChain Tool │      MCP        │
├─────────────────┼─────────────────┼─────────────────┤
│ HTTP REST       │ Python 函数     │ 标准化协议       │
│ 每个都不一样     │ 框架特定        │ 跨框架通用       │
│ 需要自己封装     │ 需要写适配代码   │ 即插即用        │
│ 无发现机制       │ 手动注册        │ 自动发现工具     │
└─────────────────┴─────────────────┴─────────────────┘
"""


# ============================================================
# 第2部分：查看 Cursor 中已有的 MCP Server
# ============================================================
"""
Cursor IDE 已经内置了 MCP 支持，你可以在设置中配置 MCP Server。

你当前配置的 MCP Server（从项目信息中获取）：
1. cursor-ide-browser - 浏览器控制
2. cursor-browser-extension - 浏览器扩展
3. user-windows-mcp - Windows 桌面操作

这些 MCP Server 让 Cursor 中的 AI 可以：
- 打开网页、点击按钮、填写表单
- 控制 Windows 桌面应用
- 执行各种自动化操作
"""

import os
import json


def show_mcp_config_location():
    """展示 MCP 配置文件位置"""
    print("=" * 60)
    print("MCP 配置文件位置")
    print("=" * 60)
    
    # Cursor 的 MCP 配置通常在这些位置
    possible_locations = [
        os.path.expanduser("~/.cursor/mcp.json"),
        os.path.expanduser("~/AppData/Roaming/Cursor/mcp.json"),
        os.path.join(os.getcwd(), ".cursor", "mcp.json"),
    ]
    
    print("\nMCP 配置文件可能的位置：")
    for loc in possible_locations:
        exists = "✓ 存在" if os.path.exists(loc) else "✗ 不存在"
        print(f"  {loc} - {exists}")
    
    print("\n提示：你也可以在 Cursor 设置中搜索 'MCP' 来配置")


# ============================================================
# 第3部分：使用 Python 创建简单的 MCP Server
# ============================================================
"""
我们将创建一个简单的 MCP Server，提供以下工具：
1. 获取当前时间
2. 计算数学表达式
3. 查询天气（模拟）
"""

# MCP Server 代码需要单独运行，这里展示代码结构
MCP_SERVER_CODE = '''
"""
简单的 MCP Server 示例
运行方式：python mcp_server_example.py
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Any

# MCP 协议使用 JSON-RPC over stdio
# 这是一个简化的实现，用于理解原理

class SimpleMCPServer:
    """简单的 MCP Server 实现"""
    
    def __init__(self):
        self.tools = {
            "get_current_time": {
                "description": "获取当前日期和时间",
                "parameters": {}
            },
            "calculate": {
                "description": "计算数学表达式",
                "parameters": {
                    "expression": {"type": "string", "description": "数学表达式"}
                }
            },
            "get_weather": {
                "description": "查询城市天气",
                "parameters": {
                    "city": {"type": "string", "description": "城市名称"}
                }
            }
        }
    
    def handle_request(self, request: dict) -> dict:
        """处理 MCP 请求"""
        method = request.get("method", "")
        params = request.get("params", {})
        request_id = request.get("id")
        
        if method == "initialize":
            # 初始化连接
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "simple-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            # 列出所有可用工具
            tools_list = []
            for name, info in self.tools.items():
                tools_list.append({
                    "name": name,
                    "description": info["description"],
                    "inputSchema": {
                        "type": "object",
                        "properties": info["parameters"]
                    }
                })
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"tools": tools_list}
            }
        
        elif method == "tools/call":
            # 调用工具
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            result = self.execute_tool(tool_name, tool_args)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": result}]
                }
            }
        
        return {"jsonrpc": "2.0", "id": request_id, "error": {"message": "Unknown method"}}
    
    def execute_tool(self, name: str, args: dict) -> str:
        """执行具体工具"""
        if name == "get_current_time":
            return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        elif name == "calculate":
            try:
                expression = args.get("expression", "")
                # 安全检查
                allowed = set("0123456789+-*/().** ")
                if all(c in allowed for c in expression):
                    result = eval(expression)
                    return f"{expression} = {result}"
                return "表达式包含不允许的字符"
            except Exception as e:
                return f"计算错误: {e}"
        
        elif name == "get_weather":
            city = args.get("city", "未知")
            # 模拟天气数据
            weather_data = {
                "北京": "晴天, -2°C, 北风3级",
                "上海": "多云, 8°C, 东风2级",
                "深圳": "晴天, 18°C, 南风2级",
            }
            return weather_data.get(city, f"暂无 {city} 的天气数据")
        
        return f"未知工具: {name}"
    
    async def run(self):
        """运行 MCP Server（通过 stdio 通信）"""
        print("MCP Server 启动...", file=sys.stderr)
        
        while True:
            try:
                # 从 stdin 读取请求
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                if not line:
                    break
                
                request = json.loads(line)
                response = self.handle_request(request)
                
                # 输出响应到 stdout
                print(json.dumps(response), flush=True)
                
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    server = SimpleMCPServer()
    asyncio.run(server.run())
'''


def show_mcp_server_code():
    """展示 MCP Server 代码"""
    print("=" * 60)
    print("简单 MCP Server 代码示例")
    print("=" * 60)
    print(MCP_SERVER_CODE)


# ============================================================
# 第4部分：使用 fastmcp 快速创建 MCP Server（推荐）
# ============================================================

FASTMCP_SERVER_CODE = '''
"""
使用 fastmcp 创建 MCP Server（更简洁）
安装：pip install fastmcp
运行：python mcp_server_fastmcp.py
"""

from fastmcp import FastMCP
from datetime import datetime

# 创建 MCP Server 实例
mcp = FastMCP("我的工具箱")


# 使用装饰器定义工具
@mcp.tool()
def get_current_time() -> str:
    """获取当前日期和时间"""
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


@mcp.tool()
def calculate(expression: str) -> str:
    """
    计算数学表达式
    
    Args:
        expression: 数学表达式，如 "(2+3)*4"
    """
    try:
        allowed = set("0123456789+-*/().** ")
        if all(c in allowed for c in expression):
            result = eval(expression)
            return f"{expression} = {result}"
        return "表达式包含不允许的字符"
    except Exception as e:
        return f"计算错误: {e}"


@mcp.tool()
def get_weather(city: str) -> str:
    """
    查询城市天气
    
    Args:
        city: 城市名称，如 "北京"
    """
    weather_data = {
        "北京": "晴天, -2°C, 北风3级",
        "上海": "多云, 8°C, 东风2级", 
        "深圳": "晴天, 18°C, 南风2级",
    }
    return weather_data.get(city, f"暂无 {city} 的天气数据")


@mcp.tool()
def search_music(keyword: str) -> str:
    """
    搜索音乐（模拟网易云音乐API）
    
    Args:
        keyword: 搜索关键词，如歌名或歌手名
    """
    # 模拟搜索结果
    mock_results = {
        "周杰伦": ["晴天 - 周杰伦", "七里香 - 周杰伦", "稻香 - 周杰伦"],
        "林俊杰": ["江南 - 林俊杰", "她说 - 林俊杰", "修炼爱情 - 林俊杰"],
    }
    
    for artist, songs in mock_results.items():
        if artist in keyword or keyword in artist:
            return f"搜索结果:\\n" + "\\n".join(f"  {i+1}. {s}" for i, s in enumerate(songs))
    
    return f"未找到与 '{keyword}' 相关的音乐"


# 定义资源（只读数据）
@mcp.resource("config://app-settings")
def get_app_settings() -> str:
    """应用配置信息"""
    return """
    {
        "app_name": "我的AI助手",
        "version": "1.0.0",
        "features": ["天气查询", "音乐搜索", "计算器"]
    }
    """


if __name__ == "__main__":
    # 运行 MCP Server
    mcp.run()
'''


def show_fastmcp_code():
    """展示 fastmcp 代码"""
    print("=" * 60)
    print("fastmcp 快速创建 MCP Server")
    print("=" * 60)
    print(FASTMCP_SERVER_CODE)


# ============================================================
# 第5部分：实战 - 创建中国服务的 MCP Server
# ============================================================

CHINA_MCP_SERVER_CODE = '''
"""
中国服务 MCP Server
封装常用的中国互联网服务 API

功能：
1. 和风天气 API - 天气查询
2. 翻译服务 - 中英互译
3. IP 查询 - 获取 IP 位置信息
"""

from fastmcp import FastMCP
import httpx
import os

mcp = FastMCP("中国服务工具箱")

# ============ 1. 和风天气 ============

@mcp.tool()
async def get_hefeng_weather(city: str) -> str:
    """
    查询城市天气（和风天气API）
    
    Args:
        city: 城市名称，如 "北京" 或 "上海"
    """
    # 注意：需要申请免费 API Key: https://dev.qweather.com/
    api_key = os.getenv("HEFENG_API_KEY", "")
    
    if not api_key:
        # 没有 API Key 时返回模拟数据
        mock_data = {
            "北京": {"temp": "-2", "text": "晴", "windDir": "北风", "windScale": "3"},
            "上海": {"temp": "8", "text": "多云", "windDir": "东风", "windScale": "2"},
            "深圳": {"temp": "18", "text": "晴", "windDir": "南风", "windScale": "2"},
            "广州": {"temp": "15", "text": "阴", "windDir": "东南风", "windScale": "1"},
        }
        if city in mock_data:
            w = mock_data[city]
            return f"{city}天气：{w['text']}，温度 {w['temp']}°C，{w['windDir']}{w['windScale']}级"
        return f"暂无 {city} 的天气数据"
    
    try:
        async with httpx.AsyncClient() as client:
            # 先查询城市 ID
            geo_url = f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={api_key}"
            geo_resp = await client.get(geo_url)
            geo_data = geo_resp.json()
            
            if geo_data.get("code") != "200" or not geo_data.get("location"):
                return f"未找到城市: {city}"
            
            location_id = geo_data["location"][0]["id"]
            
            # 查询天气
            weather_url = f"https://devapi.qweather.com/v7/weather/now?location={location_id}&key={api_key}"
            weather_resp = await client.get(weather_url)
            weather_data = weather_resp.json()
            
            if weather_data.get("code") == "200":
                now = weather_data["now"]
                return f"{city}天气：{now['text']}，温度 {now['temp']}°C，{now['windDir']}{now['windScale']}级"
            
            return f"查询失败: {weather_data.get('code')}"
    except Exception as e:
        return f"查询出错: {e}"


# ============ 2. IP 位置查询 ============

@mcp.tool()
async def get_ip_location(ip: str = "") -> str:
    """
    查询 IP 地址的位置信息
    
    Args:
        ip: IP 地址，留空则查询当前 IP
    """
    try:
        async with httpx.AsyncClient() as client:
            # 使用免费的 IP 查询服务
            url = f"http://ip-api.com/json/{ip}?lang=zh-CN"
            resp = await client.get(url)
            data = resp.json()
            
            if data.get("status") == "success":
                return f"""
IP: {data.get('query', ip or '当前IP')}
国家: {data.get('country', '未知')}
地区: {data.get('regionName', '未知')}
城市: {data.get('city', '未知')}
ISP: {data.get('isp', '未知')}
"""
            return f"查询失败: {data.get('message', '未知错误')}"
    except Exception as e:
        return f"查询出错: {e}"


# ============ 3. 简单翻译 ============

@mcp.tool()
def translate_simple(text: str, to_lang: str = "en") -> str:
    """
    简单翻译（基于规则的模拟）
    
    Args:
        text: 要翻译的文本
        to_lang: 目标语言，"en" 或 "zh"
    """
    # 这里只是模拟，实际应该调用翻译 API
    # 可以接入：百度翻译、有道翻译、Google 翻译等
    
    simple_dict = {
        "你好": "Hello",
        "谢谢": "Thank you",
        "再见": "Goodbye",
        "人工智能": "Artificial Intelligence",
        "机器学习": "Machine Learning",
        "Hello": "你好",
        "Thank you": "谢谢",
        "Goodbye": "再见",
    }
    
    if text in simple_dict:
        return f"{text} → {simple_dict[text]}"
    
    return f"暂不支持翻译: '{text}'（这是模拟版本，实际使用需接入翻译API）"


# ============ 4. 日期时间工具 ============

@mcp.tool()
def get_chinese_date() -> str:
    """获取当前中国日期时间（北京时间）"""
    from datetime import datetime, timezone, timedelta
    
    beijing_tz = timezone(timedelta(hours=8))
    now = datetime.now(beijing_tz)
    
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[now.weekday()]
    
    return f"{now.year}年{now.month}月{now.day}日 {weekday} {now.strftime('%H:%M:%S')} (北京时间)"


if __name__ == "__main__":
    mcp.run()
'''


def show_china_mcp_code():
    """展示中国服务 MCP Server 代码"""
    print("=" * 60)
    print("中国服务 MCP Server 代码")
    print("=" * 60)
    print(CHINA_MCP_SERVER_CODE)


# ============================================================
# 第6部分：将 MCP Server 集成到 Cursor
# ============================================================

MCP_CONFIG_EXAMPLE = '''
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["C:/path/to/mcp_server.py"],
      "env": {
        "HEFENG_API_KEY": "your-api-key-here"
      }
    },
    "china-services": {
      "command": "python",
      "args": ["C:/path/to/china_mcp_server.py"]
    }
  }
}
'''


def show_mcp_integration():
    """展示如何集成 MCP Server"""
    print("=" * 60)
    print("将 MCP Server 集成到 Cursor")
    print("=" * 60)
    
    print("""
步骤 1：创建 MCP Server 文件
   保存上面的代码到 .py 文件

步骤 2：配置 Cursor
   方式A：通过 Cursor 设置界面
   - 打开 Cursor 设置
   - 搜索 "MCP"
   - 添加新的 MCP Server

   方式B：编辑配置文件
   创建/编辑 ~/.cursor/mcp.json：
""")
    print(MCP_CONFIG_EXAMPLE)
    
    print("""
步骤 3：重启 Cursor
   配置后需要重启 Cursor 才能生效

步骤 4：测试
   在 Cursor 中向 AI 提问，如：
   - "现在几点了？"
   - "北京天气怎么样？"
   - "帮我搜索周杰伦的歌"
""")


# ============================================================
# 第7部分：MCP 协议详解
# ============================================================

def explain_mcp_protocol():
    """详细解释 MCP 协议"""
    print("=" * 60)
    print("MCP 协议详解")
    print("=" * 60)
    
    print("""
一、通信方式

MCP 使用 JSON-RPC 2.0 协议，通过 stdio（标准输入输出）通信：

Client (AI)                    Server (工具)
    │                              │
    │── initialize ──────────────>│  建立连接
    │<─────────── capabilities ───│  返回能力
    │                              │
    │── tools/list ──────────────>│  获取工具列表
    │<─────────── tools[] ────────│  返回工具列表
    │                              │
    │── tools/call ──────────────>│  调用工具
    │   {name, arguments}          │
    │<─────────── result ─────────│  返回结果
    │                              │

二、核心消息类型

1. initialize - 初始化连接
   请求: {"method": "initialize", "params": {...}}
   响应: {"result": {"capabilities": {...}}}

2. tools/list - 列出工具
   请求: {"method": "tools/list"}
   响应: {"result": {"tools": [...]}}

3. tools/call - 调用工具
   请求: {"method": "tools/call", "params": {"name": "xxx", "arguments": {...}}}
   响应: {"result": {"content": [...]}}

4. resources/list - 列出资源
5. resources/read - 读取资源
6. prompts/list - 列出提示模板
7. prompts/get - 获取提示模板

三、工具定义格式

{
  "name": "get_weather",
  "description": "查询城市天气",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "城市名称"
      }
    },
    "required": ["city"]
  }
}

四、为什么用 stdio？

- 简单：不需要网络配置
- 安全：进程隔离
- 跨平台：Windows/Mac/Linux 通用
- 易调试：可以用命令行测试
""")


# ============================================================
# 主程序
# ============================================================

def main():
    print("\n" + "=" * 60)
    print("第4周 - 4.3 MCP (Model Context Protocol) 协议")
    print("=" * 60)
    
    print("\n选择要查看的内容：")
    print("1. MCP 配置文件位置")
    print("2. 简单 MCP Server 代码（原理版）")
    print("3. fastmcp 快速创建 MCP Server（推荐）")
    print("4. 中国服务 MCP Server 示例")
    print("5. 如何集成到 Cursor")
    print("6. MCP 协议详解")
    print("7. 查看全部")
    
    choice = input("\n请输入选项（1-7）：").strip()
    
    if choice == "1":
        show_mcp_config_location()
    elif choice == "2":
        show_mcp_server_code()
    elif choice == "3":
        show_fastmcp_code()
    elif choice == "4":
        show_china_mcp_code()
    elif choice == "5":
        show_mcp_integration()
    elif choice == "6":
        explain_mcp_protocol()
    elif choice == "7":
        show_mcp_config_location()
        print("\n\n")
        show_mcp_server_code()
        print("\n\n")
        show_fastmcp_code()
        print("\n\n")
        show_china_mcp_code()
        print("\n\n")
        show_mcp_integration()
        print("\n\n")
        explain_mcp_protocol()
    else:
        print("无效选项")


if __name__ == "__main__":
    main()


# ============================================================
# 学习总结
# ============================================================
"""
📝 本节重点：

1. MCP 是什么？
   - Model Context Protocol，模型上下文协议
   - 标准化 AI 与工具的交互
   - 一次开发，到处使用

2. MCP 架构：
   - MCP Client（AI 应用）
   - MCP Server（工具提供方）
   - 通过 JSON-RPC over stdio 通信

3. MCP 三大核心：
   - Tools（工具）- 可执行操作
   - Resources（资源）- 只读数据
   - Prompts（提示模板）- 预定义模板

4. 创建 MCP Server：
   - 原生方式：手写 JSON-RPC 处理
   - 推荐方式：使用 fastmcp 库

5. 集成到 Cursor：
   - 编辑 ~/.cursor/mcp.json
   - 或通过设置界面添加

实战建议：
1. 先用 fastmcp 创建简单的工具
2. 测试通过后再添加更多功能
3. 可以封装常用的中国互联网服务

下一步：
- 为自己的项目创建 MCP Server
- 探索更多官方 MCP Server
- 了解 MCP 生态系统
"""
