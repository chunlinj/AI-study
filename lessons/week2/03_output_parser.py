"""
第2周 - 2.3 输出解析
目标：使用 OutputParser 让 LLM 输出结构化数据
"""

import os
import httpx
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field
from typing import List


def get_llm():
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        http_client=httpx.Client(verify=False),
        temperature=0
    )


# ============ 1. StrOutputParser（最简单） ============

def str_output_example():
    """
    StrOutputParser：提取纯文本内容
    
    LLM 返回的是 AIMessage 对象，用 StrOutputParser 提取 .content
    """
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_template("用一句话介绍{topic}")
    
    # 不用 parser：返回 AIMessage 对象
    chain_no_parser = prompt | llm
    result1 = chain_no_parser.invoke({"topic": "Python"})
    print(f"不用 Parser: {type(result1)} → {result1}")
    
    # 用 StrOutputParser：返回纯字符串
    chain_with_parser = prompt | llm | StrOutputParser()
    result2 = chain_with_parser.invoke({"topic": "Python"})
    print(f"用 Parser:   {type(result2)} → {result2}")
    
    return result2


# ============ 2. JsonOutputParser ============

def json_output_example():
    """
    JsonOutputParser：让 LLM 输出 JSON，自动解析成 dict
    """
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_template(
        """分析以下编程语言，输出 JSON 格式。

语言：{language}

请严格按以下 JSON 格式输出（不要有其他内容）：
{{
    "name": "语言名称",
    "type": "静态类型/动态类型",
    "main_use": "主要用途",
    "difficulty": "入门难度(1-5)"
}}
"""
    )
    
    # 加上 JsonOutputParser
    chain = prompt | llm | JsonOutputParser()
    
    result = chain.invoke({"language": "Python"})
    
    print("=== JSON 输出解析 ===")
    print(f"类型: {type(result)}")
    print(f"结果: {result}")
    print(f"访问字段: name={result['name']}, type={result['type']}")
    
    return result



# ============ 3. PydanticOutputParser（推荐） ============

# 定义数据结构
class BookInfo(BaseModel):
    """书籍信息"""
    title: str = Field(description="书名")
    author: str = Field(description="作者")
    year: int = Field(description="出版年份")
    summary: str = Field(description="一句话简介")
    tags: List[str] = Field(description="标签列表")


def pydantic_output_example():
    """
    PydanticOutputParser：输出带类型验证的结构化对象
    
    优点：
    - 自动生成格式说明给 LLM
    - 类型验证（year 必须是 int）
    - IDE 自动补全
    """
    from langchain_core.output_parsers import PydanticOutputParser
    
    llm = get_llm()
    
    # 创建 parser
    parser = PydanticOutputParser(pydantic_object=BookInfo)
    
    prompt = ChatPromptTemplate.from_template(
        """请介绍一本关于{topic}的经典书籍。

{format_instructions}
"""
    )
    
    # 把格式说明注入 prompt
    chain = prompt | llm | parser
    
    result = chain.invoke({
        "topic": "机器学习",
        "format_instructions": parser.get_format_instructions()
    })
    
    print("=== Pydantic 输出解析 ===")
    print(f"类型: {type(result)}")
    print(f"书名: {result.title}")
    print(f"作者: {result.author}")
    print(f"年份: {result.year}")
    print(f"简介: {result.summary}")
    print(f"标签: {result.tags}")
    
    return result


# ============ 4. 练习：提取结构化数据 ============

class PersonInfo(BaseModel):
    """人物信息"""
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    occupation: str = Field(description="职业")
    skills: List[str] = Field(description="技能列表")


def extract_person_info():
    """
    练习：从自然语言中提取结构化人物信息
    """
    from langchain_core.output_parsers import PydanticOutputParser
    
    llm = get_llm()
    parser = PydanticOutputParser(pydantic_object=PersonInfo)
    
    prompt = ChatPromptTemplate.from_template(
        """从以下文本中提取人物信息：

文本：{text}

{format_instructions}
"""
    )
    
    chain = prompt | llm | parser
    
    # 测试文本
    test_texts = [
        "张三今年28岁，是一名软件工程师，擅长Python、Java和数据库设计。",
        "李四，35岁的产品经理，精通用户研究、原型设计和项目管理。"
    ]
    
    print("=== 提取结构化数据练习 ===\n")
    
    for text in test_texts:
        print(f"原文: {text}")
        result = chain.invoke({
            "text": text,
            "format_instructions": parser.get_format_instructions()
        })
        print(f"提取: {result.model_dump()}")
        print("-" * 50)
    
    return result


# ============ 运行测试 ============

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    
    print("选择要运行的示例：")
    print("1. StrOutputParser")
    print("2. JsonOutputParser")
    print("3. PydanticOutputParser")
    print("4. 练习：提取结构化数据")
    print("5. 运行全部")
    
    choice = input("\n请输入数字 (1-5): ").strip()
    
    if choice == "1":
        str_output_example()
    elif choice == "2":
        json_output_example()
    elif choice == "3":
        pydantic_output_example()
    elif choice == "4":
        extract_person_info()
    elif choice == "5":
        str_output_example()
        print("\n" + "=" * 60 + "\n")
        json_output_example()
        print("\n" + "=" * 60 + "\n")
        pydantic_output_example()
        print("\n" + "=" * 60 + "\n")
        extract_person_info()
    else:
        print("无效选择")
