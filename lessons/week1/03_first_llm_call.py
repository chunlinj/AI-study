"""
第1周 - 1.3 第一个 LLM 调用
目标：用 Python 调用大模型 API，理解核心参数
"""

import json
import os

# ============ 准备工作 ============
"""
在运行这个脚本之前，你需要：

1. 注册 DeepSeek API（推荐，国产便宜）
   - 官网：https://platform.deepseek.com/
   - 注册后获取 API Key
   - 新用户有免费额度

2. 或者注册智谱 AI
   - 官网：https://open.bigmodel.cn/
   - 同样有免费额度

3. 设置环境变量（推荐）或直接在代码中填写 API Key
   Windows: set DEEPSEEK_API_KEY=your-key-here
   Mac/Linux: export DEEPSEEK_API_KEY=your-key-here
"""

# ============ 1. 使用 requests 调用 DeepSeek API ============

def call_deepseek_api(prompt, api_key=None):
    """
    调用 DeepSeek API
    
    DeepSeek 兼容 OpenAI 格式，学会这个，其他 API 都类似
    """
    import requests
    
    # 获取 API Key
    api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "错误：请设置 DEEPSEEK_API_KEY 环境变量"
    
    # API 端点
    url = "https://api.deepseek.com/chat/completions"
    
    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 请求体
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "扮演一个诗人"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 1.5,
        "max_tokens": 1000
    }
    
    try:
        # verify=False 禁用 SSL 证书验证（解决代理/VPN 证书问题）
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.post(url, headers=headers, json=data, timeout=30, verify=False)
        response.raise_for_status()  # 检查 HTTP 错误
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        return f"请求错误: {e}"
    except KeyError as e:
        return f"解析响应错误: {e}"


# ============ 2. 核心参数详解 ============

"""
LLM API 的核心参数：

1. model（模型）
   - deepseek-chat: DeepSeek 的对话模型
   - gpt-4: OpenAI 的最强模型
   - glm-4: 智谱的模型
   
2. messages（消息列表）
   - role: "system" | "user" | "assistant"
   - system: 设定 AI 的角色和行为
   - user: 用户的输入
   - assistant: AI 的回复（用于多轮对话）

3. temperature（温度）0-2
   - 0: 确定性输出，每次回答相同
   - 0.7: 平衡创造性和一致性（推荐）
   - 1.5+: 更随机、更有创意

4. max_tokens（最大输出长度）
   - 限制回复的 token 数量
   - 1 个中文字 ≈ 1-2 个 token
   - 1 个英文单词 ≈ 1 个 token
"""


# ============ 3. 使用 OpenAI SDK（更简洁） ============

def call_with_openai_sdk(prompt, api_key=None):
    """
    使用 OpenAI SDK 调用（DeepSeek 兼容 OpenAI SDK）
    
    安装：pip install openai
    """
    try:
        from openai import OpenAI
    except ImportError:
        return "请先安装: pip install openai"
    
    api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "错误：请设置 DEEPSEEK_API_KEY 环境变量"
    
    # 创建客户端（指定 DeepSeek 的 base_url）
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
        http_client=httpx.Client(verify=False)
    )
    
    # 调用 API
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个有帮助的AI助手"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content


# ============ 4. 多轮对话示例 ============

def chat_conversation():
    """
    演示多轮对话的消息结构
    """
    messages = [
        {"role": "system", "content": "你是一个Python编程助手"},
    ]
    
    # 第一轮
    messages.append({"role": "user", "content": "什么是列表推导式？"})
    # 假设 AI 回复了
    messages.append({"role": "assistant", "content": "列表推导式是Python中创建列表的简洁方式..."})
    
    # 第二轮（AI 能看到之前的对话）
    messages.append({"role": "user", "content": "给我一个例子"})
    
    print("多轮对话的消息结构：")
    print(json.dumps(messages, ensure_ascii=False, indent=2))
    
    return messages


# ============ 5. 测试运行 ============

if __name__ == "__main__":
    print("=== LLM API 调用测试 ===\n")
    
    # 检查 API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("⚠️  未检测到 DEEPSEEK_API_KEY 环境变量")
        print("\n请按以下步骤操作：")
        print("1. 访问 https://platform.deepseek.com/ 注册账号")
        print("2. 获取 API Key")
        print("3. 设置环境变量：")
        print("   Windows CMD: set DEEPSEEK_API_KEY=your-key-here")
        print("   Windows PowerShell: $env:DEEPSEEK_API_KEY='your-key-here'")
        print("   Mac/Linux: export DEEPSEEK_API_KEY=your-key-here")
        print("\n或者直接在代码中填写 api_key 参数")
    else:
        print(f"✓ 检测到 API Key: {api_key[:8]}...")
        
        # 测试调用
        print("\n正在调用 DeepSeek API...")
        prompt = "描述春天"
        
        result = call_deepseek_api(prompt)
        print(f"\n问题: {prompt}")
        print(f"回答: {result}")
    
    # 演示多轮对话结构
    print("\n" + "="*50)
    chat_conversation()


# ============ 练习题 ============
"""
练习1：修改 temperature 参数为 0 和 1.5，观察输出的差异

练习2：修改 system prompt，让 AI 扮演一个诗人，然后问它"描述春天"

练习3：实现一个简单的命令行聊天程序：
       - 循环接收用户输入
       - 调用 API 获取回复
       - 保持对话历史（多轮对话）
       - 输入 "quit" 退出

把你的代码写在下面：
---
"""

# 练习3 参考框架：
def simple_chat():
    """简单的命令行聊天程序"""
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：请设置 DEEPSEEK_API_KEY 环境变量")
        return
    
    messages = [
        {"role": "system", "content": "你是一个友好的AI助手"}
    ]
    
    print("开始聊天（输入 quit 退出）")
    
    while True:
        user_input = input("\n你: ")
        if user_input.lower() == "quit":
            print("再见！")
            break
        
        # 1. 将用户输入添加到 messages
        messages.append({"role": "user", "content": user_input})
        
        # 2. 调用 API
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30, verify=False)
            response.raise_for_status()
            result = response.json()
            ai_reply = result["choices"][0]["message"]["content"]
            
            # 3. 将 AI 回复添加到 messages
            messages.append({"role": "assistant", "content": ai_reply})
            
            # 4. 打印回复
            print(f"\nAI: {ai_reply}")
            
        except Exception as e:
            print(f"请求错误: {e}")

# 取消注释运行：
simple_chat()
