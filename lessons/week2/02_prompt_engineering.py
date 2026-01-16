"""
第2周 - 2.2 Prompt Engineering
目标：掌握 prompt 模板设计、Few-shot、Chain-of-Thought
"""

import os
import httpx
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# 创建 LLM 实例（复用）
def get_llm():
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        http_client=httpx.Client(verify=False),
        temperature=0.7
    )


# ============ 1. 基础 Prompt 模板 ============

def basic_prompt_template():
    """
    Prompt 模板的基本结构：
    角色设定 + 任务说明 + 上下文 + 输出格式
    """
    llm = get_llm()
    
    # 简单模板：用 {变量名} 作为占位符
    prompt = ChatPromptTemplate.from_template(
        """你是一个资深的Python开发者。

请帮我review以下代码，指出问题并给出改进建议。

代码：
{code}

请按以下格式输出：
- 问题：（列出发现的问题）
- 改进建议：（给出具体建议）
- 改进后代码：（给出修改后的代码）
"""
    )
    
    chain = prompt | llm
    
    # 测试
    test_code = """
def get_user(id):
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    for u in users:
        if u["id"] == id:
            return u
    return None
"""
    
    result = chain.invoke({"code": test_code})
    
    print("=== 基础 Prompt 模板 ===")
    print(result.content)
    return result


# ============ 2. Few-shot Learning ============

def few_shot_example():
    """
    Few-shot：给几个例子，让 LLM 学会你想要的格式/风格
    
    适用场景：
    - 特定格式输出
    - 翻译风格统一
    - 分类任务
    """
    llm = get_llm()
    
    # 定义示例
    examples = [
        {"input": "Machine Learning", "output": "机器学习"},
        {"input": "Neural Network", "output": "神经网络"},
        {"input": "Deep Learning", "output": "深度学习"},
    ]
    
    # 示例的格式模板
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}")
    ])
    
    # 创建 Few-shot prompt
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples
    )
    
    # 完整 prompt
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的AI术语翻译专家。将英文术语翻译成中文，保持专业性。"),
        few_shot_prompt,
        ("human", "{input}")
    ])
    
    chain = final_prompt | llm
    
    # 测试
    test_terms = ["Transformer", "Attention Mechanism", "Gradient Descent"]
    
    print("=== Few-shot Learning ===")
    for term in test_terms:
        result = chain.invoke({"input": term})
        print(f"{term} → {result.content}")
    
    return result



# ============ 3. Chain-of-Thought (思维链) ============

def chain_of_thought_example():
    """
    Chain-of-Thought：让 LLM 一步步思考，展示推理过程
    
    为什么有效？
    - LLM 是逐 token 生成的
    - 先输出中间步骤，后面的 token 能"看到"前面的推理
    - 减少直接跳到错误答案的概率
    """
    llm = get_llm()
    
    # 对比：不用 CoT vs 用 CoT
    
    # 问题
    question = "一个商店有15个苹果，卖掉了7个，又进货了12个，然后坏掉了3个扔掉了。现在有多少个苹果？"
    
    # 方式1：直接问（容易出错）
    prompt_direct = ChatPromptTemplate.from_template(
        "{question}\n\n直接给出答案："
    )
    
    # 方式2：Chain-of-Thought（一步步思考）
    prompt_cot = ChatPromptTemplate.from_template(
        """{question}

让我们一步步思考这个问题：
1. 首先，
"""
    )
    
    print("=== Chain-of-Thought 对比 ===\n")
    
    # 直接回答
    chain_direct = prompt_direct | llm
    result_direct = chain_direct.invoke({"question": question})
    print("【直接回答】")
    print(result_direct.content)
    
    print("\n" + "="*50 + "\n")
    
    # CoT 回答
    chain_cot = prompt_cot | llm
    result_cot = chain_cot.invoke({"question": question})
    print("【Chain-of-Thought】")
    print(result_cot.content)
    
    return result_cot


# ============ 4. 综合练习：优化问答 Prompt ============

def optimize_qa_prompt():
    """
    练习：优化一个问答 prompt
    
    场景：技术问答助手
    目标：回答准确、格式清晰、有代码示例
    """
    llm = get_llm()
    
    # 优化后的 prompt
    prompt = ChatPromptTemplate.from_template(
        """你是一个经验丰富的Python技术专家。

用户问题：{question}

请按以下结构回答：
1. **简短回答**：一句话概括答案
2. **详细解释**：解释原理（2-3句话）
3. **代码示例**：给出可运行的代码
4. **注意事项**：常见坑或最佳实践（如果有）

保持回答简洁专业。
"""
    )
    
    chain = prompt | llm
    
    # 测试问题
    questions = [
        "Python中 list 和 tuple 有什么区别？",
        "什么是装饰器？怎么用？"
    ]
    
    print("=== 优化后的问答 Prompt ===\n")
    
    for q in questions:
        print(f"问题：{q}")
        print("-" * 40)
        result = chain.invoke({"question": q})
        print(result.content)
        print("\n" + "=" * 50 + "\n")
    
    return result


# ============ 运行测试 ============

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    
    print("选择要运行的示例：")
    print("1. 基础 Prompt 模板")
    print("2. Few-shot Learning")
    print("3. Chain-of-Thought")
    print("4. 优化问答 Prompt")
    print("5. 运行全部")
    
    choice = input("\n请输入数字 (1-5): ").strip()
    
    if choice == "1":
        basic_prompt_template()
    elif choice == "2":
        few_shot_example()
    elif choice == "3":
        chain_of_thought_example()
    elif choice == "4":
        optimize_qa_prompt()
    elif choice == "5":
        basic_prompt_template()
        print("\n" + "=" * 60 + "\n")
        few_shot_example()
        print("\n" + "=" * 60 + "\n")
        chain_of_thought_example()
        print("\n" + "=" * 60 + "\n")
        optimize_qa_prompt()
    else:
        print("无效选择")
