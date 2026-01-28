"""
第4周 - 4.1 Agent 基础概念
目标：
- 理解 Agent = LLM + Tools + Memory
- 掌握 ReAct 模式（推理+行动）
- 学会工具调用（Function Calling）
"""

import os
import httpx
from langchain_openai import ChatOpenAI

# ============ 安装依赖 ============
"""
运行前先安装：
pip install langchain langchain-openai langchain-core langchain-community

确保已设置环境变量：
set DEEPSEEK_API_KEY=你的API密钥
"""

# ============ 创建 LLM 实例 ============
def get_llm():
    """获取 DeepSeek LLM 实例"""
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        http_client=httpx.Client(verify=False)
    )


# ============================================================
# 第1部分：Agent 是什么？
# ============================================================
"""
🤖 Agent = LLM + Tools + Memory

传统 LLM：
    用户提问 → LLM 回答 → 结束
    
Agent：
    用户提问 → LLM 思考 → 调用工具 → 获取结果 → 继续思考 → ... → 最终回答

核心区别：
1. LLM 只能根据训练数据回答
2. Agent 可以调用外部工具获取实时信息、执行操作

三大组成部分：
┌─────────────────────────────────────────┐
│                 Agent                    │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │   LLM   │ │  Tools  │ │ Memory  │   │
│  │ (大脑)  │ │ (工具)  │ │ (记忆)  │   │
│  └─────────┘ └─────────┘ └─────────┘   │
│       ↓          ↓           ↓          │
│    决策推理    执行动作    记住上下文     │
└─────────────────────────────────────────┘

类比：
- LLM = 一个聪明的大脑，但被关在房间里
- Tools = 给大脑配上手脚，可以上网、查数据库、发邮件
- Memory = 让大脑记住之前聊过什么
"""


# ============================================================
# 第2部分：ReAct 模式（Reasoning + Acting）
# ============================================================
"""
🔄 ReAct = Reasoning（推理） + Acting（行动）

这是 Agent 最核心的工作模式：
1. Thought（思考）：分析当前情况，决定下一步
2. Action（行动）：选择并调用工具
3. Observation（观察）：获取工具返回的结果
4. 重复上述过程，直到得出最终答案

示例流程：
用户问：北京今天的天气怎么样？

┌──────────────────────────────────────────────┐
│ Thought: 用户想知道北京天气，我需要查询天气API   │
│ Action: 调用天气查询工具，参数：城市=北京         │
│ Observation: 返回结果：晴天，25°C              │
│                                               │
│ Thought: 我已经获得了天气信息，可以回答用户了    │
│ Final Answer: 北京今天是晴天，气温25°C          │
└──────────────────────────────────────────────┘

ReAct 的优势：
1. 可解释性：每一步推理都有迹可循
2. 可控性：可以干预中间步骤
3. 准确性：通过工具获取真实数据，不是"幻觉"
"""

def demonstrate_react_thinking():
    """演示 ReAct 思维过程（模拟版）"""
    
    print("=" * 60)
    print("ReAct 模式演示：回答'北京到上海的距离是多少？'")
    print("=" * 60)
    
    # 模拟 ReAct 过程
    steps = [
        {
            "type": "Thought",
            "content": "用户想知道北京到上海的距离。这个信息我可以通过计算或查询获得。让我调用距离计算工具。"
        },
        {
            "type": "Action",
            "content": "calculate_distance(city1='北京', city2='上海')"
        },
        {
            "type": "Observation",
            "content": "距离：约 1068 公里（直线距离）"
        },
        {
            "type": "Thought",
            "content": "我已经获得了距离信息，可以回答用户了。"
        },
        {
            "type": "Final Answer",
            "content": "北京到上海的直线距离约为 1068 公里。如果是高铁，全程约 1318 公里，需要 4-5 小时。"
        }
    ]
    
    for step in steps:
        print(f"\n【{step['type']}】")
        print(f"  {step['content']}")
    
    print("\n" + "=" * 60)


# ============================================================
# 第3部分：Function Calling（工具调用）
# ============================================================
"""
🔧 Function Calling = 让 LLM 调用外部函数/工具

工作流程：
1. 定义工具的 schema（名称、参数、描述）
2. 把工具信息告诉 LLM
3. LLM 根据用户问题，决定是否调用工具
4. 如果调用，LLM 返回工具名称和参数
5. 我们执行工具，把结果返回给 LLM
6. LLM 根据结果生成最终回答

关键点：
- LLM 不会真的执行工具，它只是"决定"调用哪个工具
- 实际执行是我们的代码完成的
- LLM 需要知道工具的 schema 才能正确调用
"""

# 3.1 定义一个简单的工具
def get_current_weather(city: str) -> str:
    """
    模拟天气查询工具
    实际项目中这里会调用真正的天气 API
    """
    # 模拟返回（实际应该调用天气 API）
    weather_data = {
        "北京": "晴天，气温 -2°C，有轻度雾霾",
        "上海": "多云，气温 8°C，湿度较高",
        "深圳": "晴天，气温 18°C，适合户外活动",
        "成都": "阴天，气温 6°C，有小雨"
    }
    return weather_data.get(city, f"抱歉，暂无 {city} 的天气数据")


def calculate_expression(expression: str) -> str:
    """
    计算数学表达式
    注意：实际项目中要做安全检查，防止代码注入
    """
    try:
        # 只允许数字和基本运算符
        allowed_chars = set("0123456789+-*/().% ")
        if not all(c in allowed_chars for c in expression):
            return "表达式包含不允许的字符"
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算出错：{str(e)}"


# 3.2 为工具定义 Schema（让 LLM 知道工具怎么用）
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "查询指定城市的当前天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_expression",
            "description": "计算数学表达式，支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如：(1+2)*3"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 工具映射（用于执行）
available_tools = {
    "get_current_weather": get_current_weather,
    "calculate_expression": calculate_expression
}


# 3.3 使用 Function Calling 的完整流程
def function_calling_demo():
    """
    演示 Function Calling 完整流程
    """
    import json
    from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
    
    llm = get_llm()
    
    # 绑定工具到 LLM
    llm_with_tools = llm.bind_tools(tools_schema)
    
    print("=" * 60)
    print("Function Calling 演示")
    print("=" * 60)
    
    # 测试问题列表
    test_questions = [
        "北京今天天气怎么样？",
        "帮我计算一下 (15 + 27) * 3 等于多少？",
        "你好，请介绍一下你自己"  # 这个不需要工具
    ]
    
    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"用户问题：{question}")
        print("-" * 60)
        
        # 第一步：发送问题给 LLM
        messages = [HumanMessage(content=question)]
        response = llm_with_tools.invoke(messages)
        
        # 检查 LLM 是否要调用工具
        if response.tool_calls:
            print(f"LLM 决定调用工具：")
            
            # 处理所有工具调用
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                
                print(f"  工具名称：{tool_name}")
                print(f"  参数：{tool_args}")
                
                # 执行工具
                if tool_name in available_tools:
                    tool_result = available_tools[tool_name](**tool_args)
                    print(f"  执行结果：{tool_result}")
                    
                    # 第二步：把工具结果返回给 LLM
                    messages.append(response)  # AI 的工具调用消息
                    messages.append(ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_id
                    ))
            
            # 第三步：让 LLM 根据工具结果生成最终回答
            final_response = llm_with_tools.invoke(messages)
            print(f"\n最终回答：{final_response.content}")
        else:
            # LLM 直接回答，不需要工具
            print(f"LLM 直接回答（无需工具）：")
            print(f"  {response.content}")


# ============================================================
# 第4部分：使用 LangChain 的 @tool 装饰器
# ============================================================
"""
LangChain 提供了更优雅的方式定义工具
"""

from langchain_core.tools import tool

@tool
def search_knowledge_base(query: str) -> str:
    """
    搜索知识库，返回相关信息。
    
    Args:
        query: 搜索关键词
    
    Returns:
        搜索结果
    """
    # 模拟知识库搜索
    knowledge = {
        "python": "Python 是一种广泛使用的高级编程语言，以其简洁的语法著称。",
        "langchain": "LangChain 是一个用于开发 LLM 应用的框架，提供了 Chain、Agent 等组件。",
        "agent": "Agent 是能够自主决策和执行任务的 AI 系统，结合了 LLM、工具和记忆。",
        "rag": "RAG（检索增强生成）是一种结合检索和生成的技术，用于提高 LLM 回答的准确性。"
    }
    
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    
    return f"知识库中没有找到关于 '{query}' 的信息"


@tool
def get_current_time() -> str:
    """
    获取当前时间。
    
    Returns:
        当前日期时间字符串
    """
    from datetime import datetime
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


def langchain_tool_demo():
    """
    演示 LangChain @tool 装饰器的使用
    """
    print("=" * 60)
    print("LangChain @tool 装饰器演示")
    print("=" * 60)
    
    # 查看工具信息
    print(f"\n工具名称：{search_knowledge_base.name}")
    print(f"工具描述：{search_knowledge_base.description}")
    print(f"参数 Schema：{search_knowledge_base.args}")
    
    # 直接调用工具
    print(f"\n测试调用 search_knowledge_base('LangChain')：")
    result = search_knowledge_base.invoke({"query": "LangChain"})
    print(f"结果：{result}")
    
    print(f"\n测试调用 get_current_time()：")
    result = get_current_time.invoke({})
    print(f"结果：{result}")


# ============================================================
# 第5部分：手动实现一个简单的 Agent 循环
# ============================================================

def simple_agent_loop():
    """
    手动实现一个简单的 Agent 循环
    展示 Agent 的核心工作原理
    """
    import json
    from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
    
    print("=" * 60)
    print("简单 Agent 循环演示")
    print("=" * 60)
    
    llm = get_llm()
    
    # 定义可用工具
    my_tools = [search_knowledge_base, get_current_time]
    
    # 绑定工具
    llm_with_tools = llm.bind_tools(my_tools)
    
    # 系统提示词
    system_prompt = """你是一个智能助手，可以使用工具来回答问题。
    
可用工具：
1. search_knowledge_base - 搜索知识库
2. get_current_time - 获取当前时间

请根据用户问题决定是否需要使用工具。如果需要，请调用相应工具。"""

    # 用户问题
    user_question = "现在几点了？另外，请帮我查一下什么是 RAG？"
    
    print(f"\n用户问题：{user_question}")
    print("-" * 60)
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_question)
    ]
    
    # Agent 循环
    max_iterations = 5  # 防止无限循环
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n--- 迭代 {iteration} ---")
        
        # 调用 LLM
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        # 检查是否有工具调用
        if not response.tool_calls:
            print("Agent 决定直接回答，循环结束")
            print(f"\n最终回答：{response.content}")
            break
        
        # 执行所有工具调用
        print(f"Agent 调用了 {len(response.tool_calls)} 个工具：")
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]
            
            print(f"  - {tool_name}({tool_args})")
            
            # 找到对应工具并执行
            tool_func = None
            for t in my_tools:
                if t.name == tool_name:
                    tool_func = t
                    break
            
            if tool_func:
                result = tool_func.invoke(tool_args)
                print(f"    结果：{result}")
                
                # 添加工具结果到消息
                messages.append(ToolMessage(
                    content=result,
                    tool_call_id=tool_id
                ))
            else:
                messages.append(ToolMessage(
                    content=f"工具 {tool_name} 不存在",
                    tool_call_id=tool_id
                ))
    
    if iteration >= max_iterations:
        print("达到最大迭代次数，强制结束")


# ============================================================
# 第6部分：Agent 中的 Memory（记忆）
# ============================================================
"""
🧠 Memory = 让 Agent 记住之前的对话

为什么需要 Memory？
- LLM 本身是无状态的，每次调用都是独立的
- 用户期望多轮对话能记住上下文
- Agent 需要记住已经完成的步骤

Memory 类型：
1. 短期记忆：当前对话的上下文
2. 长期记忆：跨对话的用户偏好、知识等

简单实现：把历史消息都传给 LLM（但有 token 限制）
"""

def agent_with_memory_demo():
    """
    演示带 Memory 的 Agent
    """
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    
    print("=" * 60)
    print("带 Memory 的 Agent 演示")
    print("=" * 60)
    
    llm = get_llm()
    
    # 对话历史（这就是最简单的 Memory）
    conversation_history = [
        SystemMessage(content="你是一个友好的AI助手，请记住用户告诉你的信息。")
    ]
    
    # 模拟多轮对话
    conversations = [
        "你好，我叫张三，我是一名程序员",
        "我最喜欢的编程语言是 Python",
        "请问我叫什么名字？我喜欢什么语言？"
    ]
    
    for user_input in conversations:
        print(f"\n用户：{user_input}")
        
        # 添加用户消息
        conversation_history.append(HumanMessage(content=user_input))
        
        # 调用 LLM（传入完整历史）
        response = llm.invoke(conversation_history)
        
        # 添加 AI 回复到历史
        conversation_history.append(AIMessage(content=response.content))
        
        print(f"AI：{response.content}")
    
    print(f"\n当前 Memory 中的消息数：{len(conversation_history)}")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("第4周 - 4.1 Agent 基础概念")
    print("=" * 60)
    
    # 检查 API Key
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("\n⚠️ 警告：未设置 DEEPSEEK_API_KEY 环境变量")
        print("请运行：set DEEPSEEK_API_KEY=你的API密钥")
        print("\n以下仅运行模拟演示：")
        print("-" * 60)
        
        # 运行不需要 API 的演示
        demonstrate_react_thinking()
    else:
        print("\n选择要运行的演示：")
        print("1. ReAct 思维过程演示（不需要 API）")
        print("2. Function Calling 演示")
        print("3. LangChain @tool 装饰器演示")
        print("4. 简单 Agent 循环演示")
        print("5. 带 Memory 的 Agent 演示")
        print("6. 运行所有演示")
        
        choice = input("\n请输入选项（1-6）：").strip()
        
        if choice == "1":
            demonstrate_react_thinking()
        elif choice == "2":
            function_calling_demo()
        elif choice == "3":
            langchain_tool_demo()
        elif choice == "4":
            simple_agent_loop()
        elif choice == "5":
            agent_with_memory_demo()
        elif choice == "6":
            demonstrate_react_thinking()
            print("\n\n")
            function_calling_demo()
            print("\n\n")
            langchain_tool_demo()
            print("\n\n")
            simple_agent_loop()
            print("\n\n")
            agent_with_memory_demo()
        else:
            print("无效选项，运行默认演示...")
            demonstrate_react_thinking()


# ============================================================
# 学习总结
# ============================================================
"""
📝 本节重点：

1. Agent 三要素：
   - LLM：大脑，负责思考和决策
   - Tools：工具，执行具体操作
   - Memory：记忆，保持上下文

2. ReAct 模式：
   - Thought → Action → Observation → 循环
   - 让 AI 的决策过程可解释、可控

3. Function Calling：
   - 定义工具 Schema（告诉 LLM 工具怎么用）
   - LLM 决定调用哪个工具
   - 我们执行工具，返回结果
   - LLM 根据结果生成答案

4. @tool 装饰器：
   - LangChain 提供的便捷方式
   - 自动从函数签名生成 Schema

下一步：4.2 LangChain Agent
- 使用 AgentExecutor 简化 Agent 开发
- 创建自定义 Tool
- 实现一个能搜索网页的 Agent
"""
