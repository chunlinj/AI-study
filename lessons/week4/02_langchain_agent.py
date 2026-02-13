"""
第4周 - 4.2 LangChain Agent
目标：
- 创建自定义 Tool
- 使用 LangGraph 的 create_react_agent（新版 API）
- 实现一个能搜索网页的 Agent

注意：LangChain 1.2+ 版本已将 Agent 功能迁移到 LangGraph
旧版的 AgentExecutor 和 create_tool_calling_agent 已被弃用
"""

import os
import httpx
from langchain_openai import ChatOpenAI

# ============ 安装依赖 ============
"""
运行前先安装：
pip install langchain langchain-openai langchain-core langgraph
pip install duckduckgo-search  # 用于网页搜索（免费，无需API Key）
pip install wikipedia          # 用于维基百科搜索

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
        http_client=httpx.Client(verify=False),
        temperature=0  # Agent 场景建议用 0，保证稳定性
    )


# ============================================================
# 第1部分：创建自定义 Tool（三种方式）
# ============================================================
"""
🔧 LangChain 提供了三种创建 Tool 的方式：

1. @tool 装饰器 - 最简单，适合简单函数
2. StructuredTool - 更灵活，适合复杂参数
3. BaseTool 子类 - 最灵活，适合复杂逻辑

核心要素：
- name: 工具名称（LLM 用这个名字来调用）
- description: 工具描述（LLM 根据这个决定何时使用）
- args_schema: 参数定义（告诉 LLM 需要什么参数）
"""

from langchain_core.tools import tool, StructuredTool, BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type


# ============ 方式1：@tool 装饰器 ============

@tool
def calculate(expression: str) -> str:
    """
    计算数学表达式。支持加减乘除、括号、幂运算。
    
    Args:
        expression: 数学表达式，如 "(2 + 3) * 4" 或 "2 ** 10"
    
    Returns:
        计算结果
    """
    try:
        # 安全检查：只允许数字和基本运算符
        allowed_chars = set("0123456789+-*/().** ")
        if not all(c in allowed_chars for c in expression):
            return "错误：表达式包含不允许的字符"
        
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"


@tool
def get_word_length(word: str) -> int:
    """
    获取单词或文本的字符长度。
    
    Args:
        word: 要计算长度的文本
    
    Returns:
        字符数量
    """
    return len(word)


# ============ 方式2：StructuredTool ============

def search_product(name: str, max_price: Optional[float] = None) -> str:
    """搜索商品（模拟）"""
    products = {
        "iphone": {"name": "iPhone 15", "price": 5999, "stock": 100},
        "macbook": {"name": "MacBook Pro", "price": 12999, "stock": 50},
        "airpods": {"name": "AirPods Pro", "price": 1899, "stock": 200},
    }
    
    name_lower = name.lower()
    for key, product in products.items():
        if key in name_lower or name_lower in key:
            if max_price and product["price"] > max_price:
                return f"找到 {product['name']}，但价格 {product['price']} 元超出预算 {max_price} 元"
            return f"商品：{product['name']}，价格：{product['price']} 元，库存：{product['stock']} 件"
    
    return f"未找到商品：{name}"


# 定义参数 Schema
class SearchProductInput(BaseModel):
    name: str = Field(description="商品名称或关键词")
    max_price: Optional[float] = Field(default=None, description="最高价格限制（可选）")


# 创建 StructuredTool
search_product_tool = StructuredTool.from_function(
    func=search_product,
    name="search_product",
    description="搜索商品信息，包括名称、价格、库存。可以设置最高价格限制。",
    args_schema=SearchProductInput
)


# ============ 方式3：继承 BaseTool ============

class WeatherTool(BaseTool):
    """天气查询工具"""
    
    name: str = "get_weather"
    description: str = "查询指定城市的天气信息。返回温度、天气状况等。"
    
    # 参数 Schema
    class ArgsSchema(BaseModel):
        city: str = Field(description="城市名称，如：北京、上海")
    
    args_schema: Type[BaseModel] = ArgsSchema
    
    def _run(self, city: str) -> str:
        """同步执行"""
        # 模拟天气数据
        weather_data = {
            "北京": {"temp": -2, "condition": "晴", "humidity": 30, "wind": "北风3级"},
            "上海": {"temp": 8, "condition": "多云", "humidity": 65, "wind": "东风2级"},
            "深圳": {"temp": 18, "condition": "晴", "humidity": 70, "wind": "南风2级"},
            "广州": {"temp": 15, "condition": "阴", "humidity": 75, "wind": "东南风1级"},
        }
        
        if city in weather_data:
            w = weather_data[city]
            return f"{city}天气：{w['condition']}，温度 {w['temp']}°C，湿度 {w['humidity']}%，{w['wind']}"
        else:
            return f"暂无 {city} 的天气数据"
    
    async def _arun(self, city: str) -> str:
        """异步执行（可选实现）"""
        return self._run(city)


# 实例化
weather_tool = WeatherTool()


def demo_custom_tools():
    """演示自定义工具"""
    print("=" * 60)
    print("自定义 Tool 演示")
    print("=" * 60)
    
    # 方式1：@tool 装饰器
    print("\n【方式1】@tool 装饰器")
    print(f"  工具名称：{calculate.name}")
    print(f"  描述：{calculate.description}")
    result = calculate.invoke({"expression": "(2 + 3) * 4"})
    print(f"  调用结果：{result}")
    
    # 方式2：StructuredTool
    print("\n【方式2】StructuredTool")
    print(f"  工具名称：{search_product_tool.name}")
    print(f"  描述：{search_product_tool.description}")
    result = search_product_tool.invoke({"name": "iPhone", "max_price": 6000})
    print(f"  调用结果：{result}")
    
    # 方式3：BaseTool
    print("\n【方式3】BaseTool 子类")
    print(f"  工具名称：{weather_tool.name}")
    print(f"  描述：{weather_tool.description}")
    result = weather_tool.invoke({"city": "北京"})
    print(f"  调用结果：{result}")


# ============================================================
# 第2部分：使用 LangGraph 的 create_react_agent
# ============================================================
"""
🤖 LangGraph create_react_agent（新版 API）

LangChain 1.2+ 版本将 Agent 功能迁移到了 LangGraph
新的 create_react_agent 更简洁、更强大

工作流程（与旧版相同）：
1. 接收用户输入
2. LLM 决定是否需要调用工具
3. 如果需要 → 执行工具 → 把结果返回给 LLM
4. 重复步骤 2-3，直到 LLM 输出最终答案

主要变化：
- 不再需要 AgentExecutor
- 不再需要定义复杂的 prompt 模板
- 返回的是一个 graph，使用 .invoke() 调用
"""

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


def create_simple_agent():
    """创建一个简单的 Agent（使用 LangGraph）"""
    
    llm = get_llm()
    
    # 定义可用工具
    tools = [calculate, get_word_length, weather_tool, search_product_tool]
    
    # 系统提示词
    system_prompt = """你是一个智能助手，可以使用以下工具来帮助用户：
- calculate: 计算数学表达式
- get_word_length: 获取文本长度
- get_weather: 查询天气
- search_product: 搜索商品

请根据用户问题选择合适的工具。如果不需要工具，直接回答即可。
回答时请使用中文。"""
    
    # 创建 React Agent（LangGraph 新 API）
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )
    
    return agent


def demo_agent_executor():
    """演示 LangGraph Agent"""
    print("\n" + "=" * 60)
    print("LangGraph Agent 演示")
    print("=" * 60)
    
    agent = create_simple_agent()
    
    # 测试问题
    test_questions = [
        "北京今天天气怎么样？",
        "计算一下 (100 + 200) * 3 等于多少",
        "帮我查一下 iPhone 的价格",
        "'人工智能' 这个词有多少个字？",
        "你好，请介绍一下你自己",  # 不需要工具
    ]
    
    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"问题：{question}")
        print("-" * 60)
        
        try:
            # LangGraph 使用 messages 格式
            result = agent.invoke({
                "messages": [HumanMessage(content=question)]
            })
            
            # 获取最后一条消息作为答案
            final_message = result["messages"][-1]
            print(f"\n最终答案：{final_message.content}")
            
        except Exception as e:
            print(f"错误：{str(e)}")


# ============================================================
# 第3部分：带对话历史的 Agent
# ============================================================

def create_agent_with_memory():
    """创建带记忆的 Agent"""
    
    llm = get_llm()
    tools = [calculate, weather_tool, search_product_tool]
    
    system_prompt = """你是一个友好的AI助手，可以使用工具来帮助用户。
请记住用户告诉你的信息，并在后续对话中使用。
回答时请使用中文。"""
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )
    
    return agent


def demo_agent_with_memory():
    """演示带记忆的 Agent"""
    print("\n" + "=" * 60)
    print("带记忆的 Agent 演示")
    print("=" * 60)
    
    agent = create_agent_with_memory()
    
    # 对话历史
    messages = []
    
    # 多轮对话
    conversations = [
        "你好，我叫张三，我住在北京",
        "我想买一个手机，预算 6000 元",
        "请问我住的城市天气怎么样？",  # 需要记住用户住在北京
        "刚才你帮我查的手机多少钱？",  # 需要记住之前的查询
    ]
    
    for user_input in conversations:
        print(f"\n{'='*60}")
        print(f"用户：{user_input}")
        print("-" * 60)
        
        # 添加用户消息
        messages.append(HumanMessage(content=user_input))
        
        # 调用 Agent
        result = agent.invoke({"messages": messages})
        
        # 更新消息历史（使用 Agent 返回的完整消息列表）
        messages = result["messages"]
        
        # 获取最后一条消息作为答案
        final_message = messages[-1]
        print(f"\n助手：{final_message.content}")
    
    print(f"\n对话历史长度：{len(messages)} 条消息")


# ============================================================
# 第4部分：实现网页搜索 Agent
# ============================================================
"""
🌐 网页搜索 Agent

使用 DuckDuckGo 搜索（免费，无需 API Key）
也可以用：
- Google Search API（需要 API Key）
- Bing Search API（需要 API Key）
- SerpAPI（第三方聚合，需要 API Key）
"""

@tool
def search_web(query: str) -> str:
    """
    搜索网页获取实时信息。用于查询新闻、事实、最新动态等。
    
    Args:
        query: 搜索关键词
    
    Returns:
        搜索结果摘要
    """
    try:
        from duckduckgo_search import DDGS
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        
        if not results:
            return f"未找到关于 '{query}' 的搜索结果"
        
        # 格式化结果
        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(f"{i}. {r['title']}\n   {r['body']}\n   来源：{r['href']}")
        
        return "\n\n".join(formatted)
    
    except ImportError:
        return "错误：请先安装 duckduckgo-search 库：pip install duckduckgo-search"
    except Exception as e:
        return f"搜索出错：{str(e)}"


@tool
def search_wikipedia(query: str) -> str:
    """
    搜索维基百科获取百科知识。适合查询概念、人物、历史事件等。
    
    Args:
        query: 搜索关键词
    
    Returns:
        维基百科摘要
    """
    try:
        import wikipedia
        wikipedia.set_lang("zh")  # 设置为中文
        
        # 搜索并获取摘要
        try:
            summary = wikipedia.summary(query, sentences=3)
            return f"【{query}】\n{summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            # 如果有多个匹配，取第一个
            first_option = e.options[0]
            summary = wikipedia.summary(first_option, sentences=3)
            return f"【{first_option}】\n{summary}"
        except wikipedia.exceptions.PageError:
            return f"维基百科中未找到关于 '{query}' 的内容"
    
    except ImportError:
        return "错误：请先安装 wikipedia 库：pip install wikipedia"
    except Exception as e:
        return f"查询出错：{str(e)}"


def create_search_agent():
    """创建能搜索网页的 Agent"""
    
    llm = get_llm()
    
    # 搜索相关工具
    tools = [search_web, search_wikipedia, calculate]
    
    system_prompt = """你是一个智能搜索助手，可以使用以下工具获取信息：

1. search_web: 搜索网页，获取最新新闻、实时信息
2. search_wikipedia: 搜索维基百科，获取百科知识、概念解释
3. calculate: 计算数学表达式

使用策略：
- 查询最新新闻、实时信息 → 使用 search_web
- 查询概念、人物、历史 → 使用 search_wikipedia
- 需要计算 → 使用 calculate
- 简单问候或闲聊 → 直接回答

请根据搜索结果，用中文给出准确、有条理的回答。
如果搜索结果不足以回答问题，请诚实说明。"""
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )
    
    return agent


def demo_search_agent():
    """演示网页搜索 Agent"""
    print("\n" + "=" * 60)
    print("网页搜索 Agent 演示")
    print("=" * 60)
    
    agent = create_search_agent()
    
    # 测试问题
    test_questions = [
        "什么是人工智能？",
        "Python 编程语言是谁发明的？",
    ]
    
    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"问题：{question}")
        print("-" * 60)
        
        try:
            result = agent.invoke({
                "messages": [HumanMessage(content=question)]
            })
            final_message = result["messages"][-1]
            print(f"\n最终答案：{final_message.content}")
        except Exception as e:
            print(f"错误：{str(e)}")


# ============================================================
# 第5部分：交互式 Agent（命令行聊天）
# ============================================================

def interactive_agent():
    """交互式 Agent - 命令行聊天"""
    print("\n" + "=" * 60)
    print("交互式搜索 Agent")
    print("输入 'quit' 或 'exit' 退出")
    print("=" * 60)
    
    agent = create_search_agent()
    messages = []
    
    while True:
        try:
            user_input = input("\n你：").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
            
            if not user_input:
                continue
            
            # 添加用户消息
            messages.append(HumanMessage(content=user_input))
            
            # 调用 Agent
            result = agent.invoke({"messages": messages})
            
            # 更新消息历史
            messages = result["messages"]
            
            # 获取最后一条消息
            final_message = messages[-1]
            print(f"\n助手：{final_message.content}")
            
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误：{str(e)}")


# ============================================================
# 第6部分：查看 Agent 执行过程（调试）
# ============================================================

def demo_agent_with_debug():
    """演示如何查看 Agent 的执行过程"""
    print("\n" + "=" * 60)
    print("Agent 执行过程调试演示")
    print("=" * 60)
    
    agent = create_simple_agent()
    
    question = "北京天气怎么样？然后帮我算一下 100 * 3"
    print(f"\n问题：{question}")
    print("-" * 60)
    
    # 使用 stream 方法可以看到每一步
    print("\n【执行过程】")
    for step in agent.stream({"messages": [HumanMessage(content=question)]}):
        # step 是一个字典，包含当前节点的输出
        for node_name, node_output in step.items():
            print(f"\n节点: {node_name}")
            if "messages" in node_output:
                for msg in node_output["messages"]:
                    msg_type = type(msg).__name__
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        print(f"  [{msg_type}] 调用工具: {msg.tool_calls}")
                    elif hasattr(msg, 'content') and msg.content:
                        content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                        print(f"  [{msg_type}] {content}")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("第4周 - 4.2 LangChain Agent（LangGraph 版）")
    print("=" * 60)
    
    # 检查 API Key
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("\n⚠️ 警告：未设置 DEEPSEEK_API_KEY 环境变量")
        print("请运行：set DEEPSEEK_API_KEY=你的API密钥")
        print("\n仅运行不需要 API 的演示：")
        demo_custom_tools()
    else:
        print("\n选择要运行的演示：")
        print("1. 自定义 Tool 演示（不需要 API）")
        print("2. LangGraph Agent 演示")
        print("3. 带记忆的 Agent 演示")
        print("4. 网页搜索 Agent 演示")
        print("5. 交互式聊天（命令行）")
        print("6. Agent 执行过程调试")
        print("7. 运行所有演示（除交互式）")
        
        choice = input("\n请输入选项（1-7）：").strip()
        
        if choice == "1":
            demo_custom_tools()
        elif choice == "2":
            demo_agent_executor()
        elif choice == "3":
            demo_agent_with_memory()
        elif choice == "4":
            demo_search_agent()
        elif choice == "5":
            interactive_agent()
        elif choice == "6":
            demo_agent_with_debug()
        elif choice == "7":
            demo_custom_tools()
            demo_agent_executor()
            demo_agent_with_memory()
            demo_search_agent()
            demo_agent_with_debug()
        else:
            print("无效选项，运行默认演示...")
            demo_custom_tools()


# ============================================================
# 学习总结
# ============================================================
"""
📝 本节重点：

1. 创建自定义 Tool 的三种方式：
   - @tool 装饰器：最简单，适合简单函数
   - StructuredTool：更灵活，支持复杂参数
   - BaseTool 子类：最灵活，适合复杂逻辑

2. Tool 的关键要素：
   - name：工具名称
   - description：描述（影响 LLM 何时调用）
   - args_schema：参数定义

3. LangGraph create_react_agent（新版 API）：
   - 替代了旧版的 AgentExecutor
   - 更简洁：只需要 model、tools、prompt
   - 输入输出使用 messages 格式

4. 新旧 API 对比：
   旧版（已弃用）：
     agent = create_tool_calling_agent(llm, tools, prompt)
     executor = AgentExecutor(agent=agent, tools=tools)
     result = executor.invoke({"input": question})
   
   新版（LangGraph）：
     agent = create_react_agent(model=llm, tools=tools, prompt=prompt)
     result = agent.invoke({"messages": [HumanMessage(content=question)]})

5. 对话历史：
   - 直接使用 messages 列表
   - Agent 返回完整的消息历史

下一步：4.3 多 Agent 协作
- 了解 AutoGen / CrewAI 框架
- 理解多 Agent 协作模式
"""
