"""
第2周 - 2.1 LangChain 基础
目标：理解 Chain 概念，实现简单的 LLMChain
"""

import os

# ============ 安装依赖 ============
"""
运行前先安装：
pip install langchain langchain-openai langchain-core

如果用 DeepSeek，它兼容 OpenAI SDK，所以用 langchain-openai 即可
"""

# ============ 1. 最简单的 Chain ============

def simple_chain_example():
    """
    最简单的 Chain：Prompt | LLM
    
    Chain 就是把多个组件用 | 串起来：
    - 前一个的输出 → 后一个的输入
    - 像流水线一样处理数据
    """
    import httpx
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    
    # 1. 创建 Prompt 模板
    prompt = ChatPromptTemplate.from_template(
        "用一句话解释什么是{topic}"
    )
    
    # 2. 创建 LLM（使用 DeepSeek，禁用 SSL 验证）
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        http_client=httpx.Client(verify=False)
    )
    
    # 3. 用 | 连接成 Chain
    chain = prompt | llm
    
    # 4. 调用 Chain
    result = chain.invoke({"topic": "机器学习"})
    
    print("=== 简单 Chain 示例 ===")
    print(f"输入: topic='机器学习'")
    print(f"输出: {result.content}")
    
    return result

simple_chain_example()