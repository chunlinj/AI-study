"""
第3周 - 3.2 RAG 完整流程
========================

学习目标：
1. 理解 RAG 架构
2. 加载真实文档（PDF、TXT）
3. 构建完整的 RAG 问答系统

前置知识：3.1 向量数据库
"""

# ============================================
# Part 1: RAG 架构概述
# ============================================
"""
RAG = Retrieval-Augmented Generation（检索增强生成）

为什么需要 RAG？
---------------
LLM 的问题：
1. 知识有截止日期（训练数据的时间）
2. 不知道你的私有数据（公司文档、个人笔记）
3. 可能产生"幻觉"（编造不存在的信息）

RAG 的解决方案：
1. 把你的文档存入向量数据库
2. 用户提问时，先检索相关文档
3. 把检索结果 + 问题一起发给 LLM
4. LLM 基于真实文档生成回答

RAG 流程图：
┌─────────┐    ┌─────────────┐    ┌─────────┐
│  文档   │ -> │ 切分+Embedding │ -> │ 向量库  │
└─────────┘    └─────────────┘    └─────────┘
                                       ↓
┌─────────┐    ┌─────────────┐    ┌─────────┐
│  问题   │ -> │   检索相关   │ <- │ 向量库  │
└─────────┘    └─────────────┘    └─────────┘
                    ↓
              ┌─────────────┐
              │ 问题+上下文  │
              └─────────────┘
                    ↓
              ┌─────────────┐
              │    LLM     │
              └─────────────┘
                    ↓
              ┌─────────────┐
              │    回答     │
              └─────────────┘
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# DeepSeek LLM 配置（兼容 OpenAI SDK）
def get_llm():
    """获取 DeepSeek LLM 实例"""
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        http_client=httpx.Client(verify=False),
        temperature=0
    )

print("=" * 50)
print("Part 1: RAG 基本概念")
print("=" * 50)
print(__doc__)

# ============================================
# Part 2: 准备示例文档
# ============================================
print("\n" + "=" * 50)
print("Part 2: 准备示例文档")
print("=" * 50)

# 创建示例文档目录
docs_dir = "rag_docs"
os.makedirs(docs_dir, exist_ok=True)

# 创建几个示例文档
sample_docs = {
    "python_intro.txt": """
Python 编程语言简介

Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。
Python 的设计哲学强调代码的可读性和简洁性。

Python 的主要特点：
1. 简单易学：语法清晰，适合初学者
2. 解释型语言：不需要编译，直接运行
3. 动态类型：变量不需要声明类型
4. 丰富的库：有大量第三方库支持各种应用

Python 的应用领域：
- Web 开发：Django、Flask 框架
- 数据科学：NumPy、Pandas、Matplotlib
- 机器学习：TensorFlow、PyTorch、Scikit-learn
- 自动化脚本：系统管理、文件处理
- AI 应用：LangChain、OpenAI API
""",
    
    "langchain_guide.txt": """
LangChain 框架指南

LangChain 是一个用于开发大语言模型（LLM）应用的开源框架。
它提供了一系列工具和抽象，简化了 LLM 应用的开发过程。

LangChain 的核心组件：
1. Models：支持各种 LLM（OpenAI、Anthropic、本地模型等）
2. Prompts：提示词模板和管理
3. Chains：将多个组件串联成工作流
4. Agents：让 LLM 自主决定使用哪些工具
5. Memory：对话历史管理
6. Retrievers：文档检索（RAG 的核心）

安装 LangChain：
pip install langchain langchain-openai langchain-community

基本使用示例：
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo")
response = llm.invoke("你好")
""",

    "rag_explanation.txt": """
RAG 技术详解

RAG（Retrieval-Augmented Generation）是一种结合检索和生成的技术。

RAG 的工作原理：
1. 索引阶段：将文档切分成小块，转换为向量，存入向量数据库
2. 检索阶段：用户提问时，将问题转换为向量，检索相似文档
3. 生成阶段：将检索到的文档作为上下文，与问题一起发送给 LLM

RAG 的优势：
- 减少幻觉：LLM 基于真实文档回答
- 知识更新：只需更新文档库，无需重新训练模型
- 可解释性：可以追溯答案来源
- 成本低：不需要微调模型

RAG 的最佳实践：
- 文档切分：chunk_size 通常设为 500-1000 字符
- 重叠设置：chunk_overlap 设为 10-20%
- 检索数量：通常检索 3-5 个相关文档
- 提示词设计：明确告诉 LLM 基于上下文回答

常见问题：
Q: 检索结果不相关怎么办？
A: 优化切分策略，或使用更好的 Embedding 模型

Q: 回答不够准确怎么办？
A: 增加检索数量，或优化提示词
"""
}

# 写入文件
for filename, content in sample_docs.items():
    filepath = os.path.join(docs_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✓ 创建文档: {filepath}")

print(f"\n已创建 {len(sample_docs)} 个示例文档")


# ============================================
# Part 3: 加载和切分文档
# ============================================
print("\n" + "=" * 50)
print("Part 3: 加载和切分文档")
print("=" * 50)

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载目录下所有 txt 文件
loader = DirectoryLoader(
    docs_dir,
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

documents = loader.load()
print(f"加载了 {len(documents)} 个文档")

# 查看文档结构
print("\n文档示例:")
print(f"  内容预览: {documents[0].page_content[:100]}...")
print(f"  元数据: {documents[0].metadata}")

# 切分文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,      # 每块约300字符
    chunk_overlap=50,    # 重叠50字符
    length_function=len,
    separators=["\n\n", "\n", "。", "，", " ", ""]
)

chunks = text_splitter.split_documents(documents)
print(f"\n切分后共 {len(chunks)} 个文本块")

# 查看切分结果
print("\n切分结果预览:")
for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i+1} ---")
    print(f"来源: {chunk.metadata.get('source', 'unknown')}")
    print(f"内容: {chunk.page_content[:100]}...")


# ============================================
# Part 4: 构建向量数据库
# ============================================
print("\n" + "=" * 50)
print("Part 4: 构建向量数据库")
print("=" * 50)

import chromadb
from sentence_transformers import SentenceTransformer

# 加载 Embedding 模型
print("加载 Embedding 模型...")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 创建 Chroma 客户端
client = chromadb.Client()

# 创建集合
collection = client.create_collection(
    name="rag_documents",
    metadata={"description": "RAG 示例文档库"}
)

# 为每个文本块生成 Embedding 并存入数据库
print("正在构建向量索引...")
for i, chunk in enumerate(chunks):
    # 生成 Embedding
    embedding = embedding_model.encode(chunk.page_content).tolist()
    
    # 添加到集合
    collection.add(
        ids=[f"chunk_{i}"],
        embeddings=[embedding],
        documents=[chunk.page_content],
        metadatas=[{"source": chunk.metadata.get("source", "unknown")}]
    )

print(f"✓ 已索引 {collection.count()} 个文本块")


# ============================================
# Part 5: 实现检索功能
# ============================================
print("\n" + "=" * 50)
print("Part 5: 实现检索功能")
print("=" * 50)

def retrieve_documents(query: str, n_results: int = 3):
    """检索与查询相关的文档"""
    # 将查询转换为向量
    query_embedding = embedding_model.encode(query).tolist()
    
    # 在向量数据库中搜索
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results

# 测试检索
test_queries = [
    "Python 有什么特点？",
    "LangChain 的核心组件有哪些？",
    "RAG 是什么？有什么优势？",
]

print("测试检索功能:")
for query in test_queries:
    print(f"\n查询: {query}")
    results = retrieve_documents(query, n_results=2)
    print("检索结果:")
    for i, doc in enumerate(results['documents'][0]):
        source = results['metadatas'][0][i]['source']
        print(f"  {i+1}. [{source}] {doc[:80]}...")


# ============================================
# Part 6: 完整的 RAG 问答系统
# ============================================
print("\n" + "=" * 50)
print("Part 6: 完整的 RAG 问答系统")
print("=" * 50)

# 初始化 LLM（使用 DeepSeek）
llm = get_llm()

from langchain_core.prompts import ChatPromptTemplate

# RAG 提示词模板
rag_prompt = ChatPromptTemplate.from_template("""
你是一个知识助手。请根据以下参考资料回答用户的问题。

参考资料：
{context}

用户问题：{question}

要求：
1. 只根据参考资料回答，不要编造信息
2. 如果参考资料中没有相关信息，请说"根据现有资料无法回答"
3. 回答要简洁明了
4. 可以适当组织语言，但不要改变原意

回答：
""")

def rag_answer(question: str) -> str:
    """RAG 问答函数"""
    # 1. 检索相关文档
    results = retrieve_documents(question, n_results=3)
    
    # 2. 组合上下文
    context = "\n\n".join(results['documents'][0])
    
    # 3. 构建提示词
    prompt = rag_prompt.format(context=context, question=question)
    
    # 4. 调用 LLM
    response = llm.invoke(prompt)
    
    return response.content

# 测试 RAG 问答
print("\n--- RAG 问答测试 ---")
questions = [
    "Python 适合做什么？",
    "如何安装 LangChain？",
    "RAG 有什么优势？",
    "什么是 chunk_size？",
]

for q in questions:
    print(f"\n问: {q}")
    answer = rag_answer(q)
    print(f"答: {answer}")


# ============================================
# Part 7: 带来源引用的 RAG
# ============================================
print("\n" + "=" * 50)
print("Part 7: 带来源引用的 RAG")
print("=" * 50)

def rag_answer_with_sources(question: str) -> dict:
    """带来源引用的 RAG 问答"""
    # 1. 检索
    results = retrieve_documents(question, n_results=3)
    
    # 2. 准备上下文（带编号）
    context_parts = []
    sources = []
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        context_parts.append(f"[{i+1}] {doc}")
        sources.append(meta['source'])
    
    context = "\n\n".join(context_parts)
    
    # 3. 修改提示词，要求引用来源
    prompt_with_sources = f"""
你是一个知识助手。请根据以下参考资料回答用户的问题。

参考资料：
{context}

用户问题：{question}

要求：
1. 只根据参考资料回答
2. 在回答中用 [1]、[2] 等标注信息来源
3. 回答要简洁明了

回答：
"""
    
    # 4. 调用 LLM
    response = llm.invoke(prompt_with_sources)
    
    return {
        "answer": response.content,
        "sources": list(set(sources))  # 去重
    }

# 测试带来源的问答
print("\n--- 带来源引用的问答 ---")
result = rag_answer_with_sources("LangChain 有哪些核心组件？")
print(f"\n问: LangChain 有哪些核心组件？")
print(f"答: {result['answer']}")
print(f"来源: {result['sources']}")


# ============================================
# Part 8: 对话式 RAG（带历史记录）
# ============================================
print("\n" + "=" * 50)
print("Part 8: 对话式 RAG")
print("=" * 50)

class ConversationalRAG:
    """支持多轮对话的 RAG 系统"""
    
    def __init__(self):
        self.history = []
        self.llm = get_llm()
    
    def chat(self, question: str) -> str:
        # 1. 检索相关文档
        results = retrieve_documents(question, n_results=3)
        context = "\n\n".join(results['documents'][0])
        
        # 2. 构建包含历史的提示词
        history_text = ""
        if self.history:
            history_text = "对话历史：\n"
            for h in self.history[-3:]:  # 只保留最近3轮
                history_text += f"用户: {h['question']}\n助手: {h['answer']}\n"
            history_text += "\n"
        
        prompt = f"""
你是一个知识助手。

{history_text}参考资料：
{context}

当前问题：{question}

请根据参考资料和对话历史回答问题。如果是追问，要结合上下文理解。
"""
        
        # 3. 调用 LLM
        response = self.llm.invoke(prompt)
        answer = response.content
        
        # 4. 保存历史
        self.history.append({"question": question, "answer": answer})
        
        return answer
    
    def clear_history(self):
        self.history = []

# 测试对话式 RAG
print("\n--- 对话式 RAG 测试 ---")
rag_chat = ConversationalRAG()

conversation = [
    "Python 是什么？",
    "它有什么特点？",  # 追问，需要理解"它"指 Python
    "可以用来做 AI 开发吗？",
]

for q in conversation:
    print(f"\n用户: {q}")
    answer = rag_chat.chat(q)
    print(f"助手: {answer}")


# ============================================
# Part 9: 使用 LangChain 简化 RAG
# ============================================
print("\n" + "=" * 50)
print("Part 9: 使用 LangChain 简化 RAG")
print("=" * 50)

"""
LangChain 提供了更简洁的 RAG 实现方式。
下面展示如何用 LangChain 的高级 API 构建 RAG。

注意：新版 LangChain 推荐使用 LCEL (LangChain Expression Language)
而不是旧的 RetrievalQA Chain。
"""

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 使用 HuggingFace Embeddings（与 LangChain 集成）
print("初始化 LangChain RAG 组件...")

embeddings = HuggingFaceEmbeddings(
    model_name='paraphrase-multilingual-MiniLM-L12-v2'
)

# 创建 LangChain 的 Chroma 向量存储
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="langchain_rag"
)

# 创建检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 使用 LCEL 构建 RAG Chain（新版推荐方式）
rag_prompt_template = ChatPromptTemplate.from_template("""
根据以下参考资料回答问题：

参考资料：
{context}

问题：{question}

回答：
""")

def format_docs(docs):
    """格式化检索到的文档"""
    return "\n\n".join(doc.page_content for doc in docs)

# 构建 RAG Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt_template
    | get_llm()
    | StrOutputParser()
)

# 测试 LangChain RAG
print("\n--- LangChain RAG 测试 ---")
question = "RAG 的工作原理是什么？"
result = rag_chain.invoke(question)
print(f"\n问: {question}")
print(f"答: {result}")


# ============================================
# Part 10: 实战练习
# ============================================
print("\n" + "=" * 50)
print("Part 10: 实战练习")
print("=" * 50)

"""
练习：构建你自己的知识库问答系统

任务：
1. 准备你自己的文档（可以是笔记、文章等）
2. 加载并切分文档
3. 构建向量索引
4. 实现问答功能

提示：
- 可以尝试不同的 chunk_size 和 chunk_overlap
- 可以调整检索数量 n_results
- 可以优化提示词模板
"""

# 示例：创建一个简单的 RAG 类
class SimpleRAG:
    """简单的 RAG 系统封装"""
    
    def __init__(self, documents: list, chunk_size: int = 300):
        # 初始化组件
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.llm = get_llm()
        self.client = chromadb.Client()
        
        # 切分文档
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=50
        )
        
        # 如果是字符串列表，转换为 Document 格式
        if documents and isinstance(documents[0], str):
            from langchain_core.documents import Document
            documents = [Document(page_content=doc) for doc in documents]
        
        self.chunks = splitter.split_documents(documents)
        
        # 构建索引
        self.collection = self.client.create_collection(name="simple_rag")
        for i, chunk in enumerate(self.chunks):
            embedding = self.embedding_model.encode(chunk.page_content).tolist()
            self.collection.add(
                ids=[f"doc_{i}"],
                embeddings=[embedding],
                documents=[chunk.page_content]
            )
        
        print(f"RAG 系统初始化完成，索引了 {len(self.chunks)} 个文本块")
    
    def ask(self, question: str) -> str:
        # 检索
        query_embedding = self.embedding_model.encode(question).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        context = "\n\n".join(results['documents'][0])
        
        # 生成回答
        prompt = f"""根据以下资料回答问题：

资料：
{context}

问题：{question}

回答："""
        
        response = self.llm.invoke(prompt)
        return response.content

# 使用示例
print("\n--- SimpleRAG 使用示例 ---")
my_docs = [
    "机器学习是人工智能的一个分支，它使计算机能够从数据中学习。",
    "深度学习是机器学习的子集，使用神经网络处理复杂问题。",
    "自然语言处理（NLP）让计算机能够理解和生成人类语言。",
    "大语言模型（LLM）是在海量文本上训练的深度学习模型。",
]

from langchain_core.documents import Document
docs = [Document(page_content=d) for d in my_docs]
simple_rag = SimpleRAG(docs)

answer = simple_rag.ask("什么是深度学习？")
print(f"\n问: 什么是深度学习？")
print(f"答: {answer}")


# ============================================
# 总结
# ============================================
print("\n" + "=" * 50)
print("本节总结")
print("=" * 50)

print("""
✅ 学到的内容：

1. RAG 架构
   - 索引阶段：文档 -> 切分 -> Embedding -> 向量库
   - 检索阶段：问题 -> Embedding -> 相似度搜索
   - 生成阶段：上下文 + 问题 -> LLM -> 回答

2. 文档加载
   - DirectoryLoader: 加载目录下的文件
   - TextLoader: 加载文本文件
   - 还支持 PDF、Word、HTML 等格式

3. 完整 RAG 实现
   - 基础问答
   - 带来源引用
   - 对话式 RAG（带历史）

4. LangChain 简化
   - Chroma 向量存储
   - RetrievalQA Chain
   - 一行代码实现 RAG

下一步：3.3 高级 RAG 技术
- 混合检索（关键词 + 语义）
- 重排序（Reranking）
- 查询改写
""")
