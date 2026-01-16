"""
第3周 - 3.1 向量数据库
======================

学习目标：
1. 理解 Embedding 原理
2. 安装使用 Chroma / FAISS
3. 文档切分策略

前置知识：你已经学过向量和余弦相似度，这里会用到！
"""

# ============================================
# Part 1: Embedding 原理
# ============================================
"""
什么是 Embedding？
-----------------
Embedding 就是把文本转换成向量（一串数字）。

为什么需要？
- 计算机不懂文字，但懂数字
- 向量可以计算相似度（你学过的余弦相似度！）
- 语义相近的文本，向量也相近

举例：
"我喜欢吃苹果" -> [0.1, 0.3, 0.5, ...]  (1536维向量)
"我爱吃水果"   -> [0.12, 0.28, 0.48, ...] (相似！)
"今天天气好"   -> [0.8, 0.1, 0.2, ...]   (不相似)
"""

# 先安装必要的库
# pip install chromadb sentence-transformers

print("=" * 50)
print("Part 1: 使用 Embedding 模型")
print("=" * 50)

# 使用开源的 Embedding 模型（不需要 API）
from sentence_transformers import SentenceTransformer

# 加载模型（第一次会下载，约 100MB）
# 这个模型支持中文！
print("\n正在加载 Embedding 模型...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 测试文本
texts = [
    "我喜欢吃苹果",
    "我爱吃水果",
    "今天天气真好",
    "Python 是一门编程语言",
    "Java 也是编程语言"
]

# 生成 Embedding
print("\n生成文本的 Embedding 向量...")
embeddings = model.encode(texts)

print(f"文本数量: {len(texts)}")
print(f"向量维度: {embeddings.shape[1]}")
print(f"第一个文本的向量（前10维）: {embeddings[0][:10]}")


# ============================================
# Part 2: 计算相似度（复习你学过的余弦相似度）
# ============================================
print("\n" + "=" * 50)
print("Part 2: 计算文本相似度")
print("=" * 50)

import numpy as np

def cosine_similarity(v1, v2):
    """计算余弦相似度 - 你在 01_vector_basics.py 学过！"""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

# 计算所有文本与第一个文本的相似度
print(f"\n基准文本: '{texts[0]}'")
print("\n与其他文本的相似度:")
for i, text in enumerate(texts):
    similarity = cosine_similarity(embeddings[0], embeddings[i])
    print(f"  '{text}': {similarity:.4f}")

"""
预期结果：
- "我爱吃水果" 相似度最高（语义相近）
- "今天天气真好" 相似度较低（话题不同）
- 两个编程语言的句子相似度会比较高
"""

# ============================================
# Part 3: Chroma 向量数据库
# ============================================
print("\n" + "=" * 50)
print("Part 3: Chroma 向量数据库")
print("=" * 50)

"""
为什么需要向量数据库？
--------------------
- 当文档很多时（几万、几十万），不能每次都全部计算相似度
- 向量数据库使用特殊的索引结构，快速找到相似向量
- 还能持久化存储，重启后数据不丢失

常见向量数据库：
- Chroma: 轻量级，适合学习和小项目
- FAISS: Facebook 开源，性能强
- Pinecone: 云服务，企业级
- Milvus: 开源，支持大规模
"""

import chromadb

# 创建 Chroma 客户端（内存模式）
client = chromadb.Client()

# 创建一个集合（类似数据库的表）
collection = client.create_collection(
    name="my_documents",
    metadata={"description": "我的第一个向量数据库"}
)

# 准备一些文档
documents = [
    "LangChain 是一个用于开发 LLM 应用的框架",
    "RAG 是检索增强生成的缩写，可以让 LLM 回答基于文档的问题",
    "向量数据库用于存储和检索文本的向量表示",
    "Python 是 AI 开发最常用的编程语言",
    "Transformer 是现代大语言模型的基础架构",
    "Prompt Engineering 是设计有效提示词的技术",
]

# 添加文档到集合
# Chroma 会自动生成 Embedding！
collection.add(
    documents=documents,
    ids=[f"doc_{i}" for i in range(len(documents))]  # 每个文档需要唯一ID
)

print(f"已添加 {collection.count()} 个文档到向量数据库")


# 查询相似文档
print("\n--- 测试查询 ---")
query = "什么是 RAG？"
results = collection.query(
    query_texts=[query],
    n_results=3  # 返回最相似的3个
)

print(f"查询: '{query}'")
print("\n最相似的文档:")
for i, doc in enumerate(results['documents'][0]):
    print(f"  {i+1}. {doc}")

# 再试一个查询
print("\n" + "-" * 30)
query2 = "如何开发 AI 应用？"
results2 = collection.query(
    query_texts=[query2],
    n_results=3
)

print(f"查询: '{query2}'")
print("\n最相似的文档:")
for i, doc in enumerate(results2['documents'][0]):
    print(f"  {i+1}. {doc}")

# ============================================
# Part 4: 文档切分策略
# ============================================
print("\n" + "=" * 50)
print("Part 4: 文档切分策略")
print("=" * 50)

"""
为什么要切分文档？
----------------
1. LLM 有 token 限制（如 4096、8192）
2. 太长的文本 Embedding 效果差
3. 检索时需要精确定位相关段落

切分策略：
- chunk_size: 每个块的大小（字符数）
- chunk_overlap: 块之间的重叠（避免切断句子）

常见设置：
- chunk_size: 500-1000 字符
- chunk_overlap: 50-200 字符
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

# 模拟一个长文档
long_document = """
大语言模型（Large Language Model，LLM）是一种基于深度学习的自然语言处理模型。
这类模型通常包含数十亿甚至数千亿个参数，通过在海量文本数据上进行预训练，
学习语言的统计规律和语义知识。

LLM 的核心技术是 Transformer 架构，由 Google 在 2017 年提出。
Transformer 使用自注意力机制（Self-Attention），能够捕捉文本中的长距离依赖关系。
这使得模型能够理解上下文，生成连贯的文本。

目前主流的 LLM 包括：
1. GPT 系列（OpenAI）：GPT-3、GPT-4 等
2. Claude 系列（Anthropic）：Claude 2、Claude 3 等
3. LLaMA 系列（Meta）：开源模型
4. 国产模型：文心一言、通义千问、DeepSeek 等

LLM 的应用场景非常广泛：
- 智能问答和对话系统
- 文本生成和创作
- 代码生成和辅助编程
- 文档摘要和翻译
- 知识检索和 RAG 系统

RAG（Retrieval-Augmented Generation）是一种结合检索和生成的技术。
它首先从知识库中检索相关文档，然后将检索结果作为上下文提供给 LLM，
让模型基于这些信息生成回答。这样可以减少模型的"幻觉"问题，提高回答的准确性。
"""

# 创建文本切分器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,      # 每块约200字符
    chunk_overlap=50,    # 重叠50字符
    length_function=len,
    separators=["\n\n", "\n", "。", "，", " ", ""]  # 优先在这些位置切分
)

# 切分文档
chunks = text_splitter.split_text(long_document)

print(f"原文档长度: {len(long_document)} 字符")
print(f"切分后块数: {len(chunks)}")
print("\n各块内容预览:")
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ({len(chunk)} 字符) ---")
    print(chunk[:100] + "..." if len(chunk) > 100 else chunk)


# ============================================
# Part 5: FAISS 向量数据库（可选）
# ============================================
print("\n" + "=" * 50)
print("Part 5: FAISS 向量数据库")
print("=" * 50)

"""
FAISS (Facebook AI Similarity Search)
-------------------------------------
- Facebook 开源的向量检索库
- 性能比 Chroma 更强
- 适合大规模数据（百万级）
- 但 API 相对底层一些

安装: pip install faiss-cpu
"""

try:
    import faiss
    
    # 准备向量数据
    # 使用之前生成的 embeddings
    dimension = embeddings.shape[1]  # 向量维度
    
    # 创建 FAISS 索引
    index = faiss.IndexFlatL2(dimension)  # L2 距离（欧氏距离）
    
    # 添加向量
    index.add(embeddings.astype('float32'))
    
    print(f"FAISS 索引中的向量数量: {index.ntotal}")
    
    # 查询
    query_text = "我喜欢编程"
    query_embedding = model.encode([query_text])
    
    # 搜索最相似的 3 个
    k = 3
    distances, indices = index.search(query_embedding.astype('float32'), k)
    
    print(f"\n查询: '{query_text}'")
    print("最相似的文本:")
    for i, idx in enumerate(indices[0]):
        print(f"  {i+1}. {texts[idx]} (距离: {distances[0][i]:.4f})")
        
except ImportError:
    print("FAISS 未安装，跳过此部分")
    print("安装命令: pip install faiss-cpu")

# ============================================
# Part 6: 实战练习
# ============================================
print("\n" + "=" * 50)
print("Part 6: 实战练习")
print("=" * 50)

"""
练习任务：构建一个简单的知识库问答系统

步骤：
1. 准备一些知识文档
2. 切分文档
3. 存入向量数据库
4. 实现查询功能
"""

# 创建一个新的集合
qa_collection = client.create_collection(name="qa_knowledge_base")

# 知识库内容（模拟公司FAQ）
knowledge_base = [
    "公司的工作时间是周一到周五，早上9点到下午6点。",
    "年假政策：入职满一年可享受5天年假，满三年10天，满五年15天。",
    "报销流程：填写报销单，附上发票，提交给部门经理审批，然后交给财务。",
    "会议室预约：通过公司内部系统预约，最多提前一周预约。",
    "IT 支持：遇到电脑问题可以拨打内线 8888 或发邮件到 it@company.com。",
    "新员工入职需要准备：身份证复印件、学历证明、银行卡信息、一寸照片。",
    "公司提供免费午餐，餐厅在一楼，用餐时间是11:30-13:00。",
    "加班政策：加班需要提前申请，周末加班可以调休或按1.5倍计算工资。",
]

# 添加到向量数据库
qa_collection.add(
    documents=knowledge_base,
    ids=[f"faq_{i}" for i in range(len(knowledge_base))]
)

print("知识库已建立！")
print(f"包含 {qa_collection.count()} 条FAQ")

# 测试问答
test_questions = [
    "公司几点上班？",
    "我想请年假，能请几天？",
    "电脑坏了找谁？",
    "中午在哪吃饭？",
]

print("\n--- 测试问答 ---")
for question in test_questions:
    results = qa_collection.query(
        query_texts=[question],
        n_results=1
    )
    print(f"\nQ: {question}")
    print(f"A: {results['documents'][0][0]}")

# ============================================
# 总结
# ============================================
print("\n" + "=" * 50)
print("本节总结")
print("=" * 50)

print("""
✅ 学到的内容：

1. Embedding 原理
   - 文本 -> 向量
   - 语义相近的文本，向量也相近
   - 可以用余弦相似度计算相似性

2. Chroma 向量数据库
   - 轻量级，适合学习
   - 自动生成 Embedding
   - 支持相似度查询

3. 文档切分策略
   - chunk_size: 块大小
   - chunk_overlap: 重叠大小
   - RecursiveCharacterTextSplitter

4. FAISS（可选）
   - 性能更强
   - 适合大规模数据

下一步：3.2 RAG 完整流程
- 加载真实文档（PDF、Word）
- 构建完整的 RAG 系统
""")
