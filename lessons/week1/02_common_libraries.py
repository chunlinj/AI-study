"""
第1周 - 1.1 常用库：requests, json, os
目标：掌握 AI 开发中最常用的 Python 库
"""

import json
import os

# ============ 1. JSON 处理 ============

print("=== JSON 处理 ===")

# Python 字典 → JSON 字符串
data = {
    "name": "张三",
    "age": 25,
    "skills": ["Python", "Java", "AI"]
}

json_str = json.dumps(data, ensure_ascii=False, indent=2)
print("字典转 JSON:")
print(json_str)

# JSON 字符串 → Python 字典
json_text = '{"model": "gpt-4", "temperature": 0.7}'
parsed = json.loads(json_text)
print(f"\nJSON 转字典: {parsed}")
print(f"模型: {parsed['model']}")


# ============ 2. OS 模块 ============

print("\n=== OS 模块 ===")

# 获取当前目录
current_dir = os.getcwd()
print(f"当前目录: {current_dir}")

# 路径拼接（跨平台安全）
file_path = os.path.join(current_dir, "lessons", "week1", "test.txt")
print(f"拼接路径: {file_path}")

# 检查文件/目录是否存在
print(f"当前目录存在: {os.path.exists(current_dir)}")

# 获取环境变量（API Key 通常这样获取）
api_key = os.getenv("OPENAI_API_KEY", "未设置")
print(f"API Key: {api_key[:10]}..." if api_key != "未设置" else "API Key: 未设置")

# 列出目录内容
print(f"\n当前目录文件:")
for item in os.listdir(".")[:5]:  # 只显示前5个
    print(f"  - {item}")


# ============ 3. Requests 库（需要安装：pip install requests） ============

print("\n=== Requests 库 ===")

# 注意：运行前需要安装 requests
# pip install requests

try:
    import requests
    
    # GET 请求示例
    print("发送 GET 请求到 httpbin.org...")
    response = requests.get("https://httpbin.org/get", timeout=10)
    
    print(f"状态码: {response.status_code}")
    print(f"响应类型: {type(response.json())}")
    
    # POST 请求示例（这是调用 LLM API 的基础）
    print("\n发送 POST 请求...")
    post_data = {
        "name": "test",
        "value": 123
    }
    response = requests.post(
        "https://httpbin.org/post",
        json=post_data,  # 自动转 JSON
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    print(f"POST 状态码: {response.status_code}")
    
except ImportError:
    print("requests 库未安装，请运行: pip install requests")
except Exception as e:
    print(f"请求失败: {e}")


# ============ 4. 文件读写 ============

print("\n=== 文件读写 ===")

# 写文件
test_file = "lessons/week1/test_output.txt"
with open(test_file, "w", encoding="utf-8") as f:
    f.write("这是测试内容\n")
    f.write("第二行\n")
print(f"已写入: {test_file}")

# 读文件
with open(test_file, "r", encoding="utf-8") as f:
    content = f.read()
print(f"读取内容:\n{content}")

# 读取 JSON 文件
json_file = "lessons/week1/config.json"
config_data = {"api_key": "your-key-here", "model": "deepseek-chat"}
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=2)
print(f"已创建配置文件: {json_file}")


# ============ 5. 实战：模拟 LLM API 调用结构 ============

print("\n=== 模拟 LLM API 调用 ===")

def mock_llm_call(prompt, model="deepseek-chat", temperature=0.7):
    """
    模拟 LLM API 调用的结构
    实际调用时只需要把 URL 和 headers 换成真实的
    """
    # 构造请求体（这是标准的 OpenAI 格式）
    request_body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个有帮助的助手"},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": 1000
    }
    
    print("请求体结构:")
    print(json.dumps(request_body, ensure_ascii=False, indent=2))
    
    # 模拟响应
    mock_response = {
        "id": "chatcmpl-123",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "这是模拟的回复内容"
                }
            }
        ],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 10,
            "total_tokens": 30
        }
    }
    
    return mock_response

# 测试
response = mock_llm_call("你好，请介绍一下自己")
print(f"\n模拟响应:")
print(f"回复: {response['choices'][0]['message']['content']}")
print(f"Token 使用: {response['usage']}")


# ============ 练习题 ============
"""
练习1：读取 config.json 文件，打印出 model 的值

练习2：写一个函数，接收 URL，发送 GET 请求并返回 JSON 响应

练习3：创建一个字典，包含你的个人信息，保存为 JSON 文件

把你的代码写在下面：
---
"""

# 练习1：
json_config_file = "lessons/week1/config.json"
with open(json_config_file, "r", encoding="utf-8") as f:
    config = json.load(f)  # 用 json.load() 解析文件内容为字典
    print(f"model 的值: {config['model']}")


# 练习2：
def getResponseBody(URL):
    return requests.get(URL, timeout=10).json()

# 练习3：
data1 = {
    "name": "张三",
    "age": 25
}
json_file1 = "lessons/week1/config1.json"
with open(json_file1, "w", encoding="utf-8") as f:
    json.dump(data1, f, indent=2, ensure_ascii=False)