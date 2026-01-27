"""
第3周 - 3.4 个性化 RAG 与记忆系统（进阶）
==========================================

学习目标：
1. 理解 LLM 无状态性的局限
2. 学习 LangChain Memory 类型
3. 实现用户专属记忆向量库
4. 构建"会记住用户"的 RAG 系统

核心概念：
- LLM 本身是无状态的，每次对话都是独立的
- Memory 让系统能记住对话历史和用户偏好
- 个性化记忆可以提升用户体验
"""

import os
import json
import httpx
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)

load_dotenv()


# ============================================
# Part 1: LLM 无状态性演示
# ============================================

print("="*60)
print("Part 1: LLM 无状态性的问题")
print("="*60)

def get_llm():
    """获取 DeepSeek LLM"""
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        http_client=httpx.Client(verify=False),
        temperature=0.7
    )

llm = get_llm()

print("\n演示：LLM 无法记住之前的对话\n")

# 第一轮对话
response1 = llm.invoke("我叫张三，我喜欢 Python 编程")
print(f"用户: 我叫张三，我喜欢 Python 编程")
print(f"AI: {response1.content}\n")

# 第二轮对话（LLM 不记得之前说的）
response2 = llm.invoke("我叫什么名字？")
print(f"用户: 我叫什么名字？")
print(f"AI: {response2.content}\n")

print("❌ 问题：LLM 不记得用户叫张三")
print("💡 解决方案：使用 Memory 系统\n")


# ============================================
# Part 2: LangChain Memory 类型
# ============================================

print("="*60)
print("Part 2: LangChain Memory 类型")
print("="*60)

print("""
LangChain 提供了多种 Memory 类型：

1. ConversationBufferMemory
   - 保存完整的对话历史
   - 优点：信息完整
   - 缺点：token 消耗大

2. ConversationBufferWindowMemory
   - 只保留最近 N 轮对话
   - 优点：控制 token 消耗
   - 缺点：会忘记早期对话

3. ConversationSummaryMemory
   - 对历史对话进行总结
   - 优点：节省 token，保留关键信息
   - 缺点：可能丢失细节

4. VectorStoreRetrieverMemory
   - 将对话存入向量库，按相似度检索
   - 优点：可以记住大量信息
   - 缺点：实现复杂
""")


# ============================================
# Part 3: ConversationBufferMemory 示例
# ============================================

print("\n" + "="*60)
print("Part 3: ConversationBufferMemory（完整历史）")
print("="*60)

from langchain.chains import ConversationChain

# 创建带记忆的对话链
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

print("\n演示：带记忆的对话\n")

# 第一轮
response1 = conversation.predict(input="我叫张三，我喜欢 Python 编程")
print(f"用户: 我叫张三，我喜欢 Python 编程")
print(f"AI: {response1}\n")

# 第二轮（现在能记住了）
response2 = conversation.predict(input="我叫什么名字？")
print(f"用户: 我叫什么名字？")
print(f"AI: {response2}\n")

# 第三轮
response3 = conversation.predict(input="我喜欢什么？")
print(f"用户: 我喜欢什么？")
print(f"AI: {response3}\n")

print("✅ 成功：LLM 现在能记住对话历史了")

# 查看记忆内容
print("\n记忆内容:")
print(memory.load_memory_variables({}))


# ============================================
# Part 4: ConversationBufferWindowMemory 示例
# ============================================

print("\n" + "="*60)
print("Part 4: ConversationBufferWindowMemory（滑动窗口）")
print("="*60)

# 只保留最近 2 轮对话
window_memory = ConversationBufferWindowMemory(k=2)
window_conversation = ConversationChain(
    llm=llm,
    memory=window_memory,
    verbose=False
)

print("\n演示：只记住最近 2 轮对话\n")

conversations = [
    "我叫张三",
    "我今年 25 岁",
    "我住在北京",
    "我叫什么名字？",  # 应该忘记了
    "我住在哪里？",    # 应该记得
]

for msg in conversations:
    response = window_conversation.predict(input=msg)
    print(f"用户: {msg}")
    print(f"AI: {response}\n")

print("💡 注意：系统忘记了早期的对话（名字），但记得最近的（住址）")


# ============================================
# Part 5: 用户专属记忆向量库
# ============================================

print("\n" + "="*60)
print("Part 5: 用户专属记忆向量库")
print("="*60)

class UserMemoryStore:
    """
    用户专属记忆存储
    
    功能：
    - 存储用户的个人信息、偏好、对话历史
    - 基于向量检索相关记忆
    - 持久化存储
    """
    
    def __init__(self, user_id, memory_dir="./user_memories"):
        self.user_id = user_id
        self.memory_dir = os.path.join(memory_dir, user_id)
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # 初始化 Embedding 模型
        self.embeddings = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # 加载或创建向量库
        self.vectorstore = Chroma(
            persist_directory=self.memory_dir,
            embedding_function=self.embeddings,
            collection_name=f"memory_{user_id}"
        )
        
        # 用户信息文件
        self.user_info_file = os.path.join(self.memory_dir, "user_info.json")
        self.user_info = self._load_user_info()
        
        print(f"✅ 用户记忆库初始化完成: {user_id}")
        print(f"   记忆数量: {self.vectorstore._collection.count()}")
    
    def _load_user_info(self):
        """加载用户信息"""
        if os.path.exists(self.user_info_file):
            with open(self.user_info_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "user_id": self.user_id,
            "name": None,
            "preferences": {},
            "created_at": datetime.now().isoformat()
        }
    
    def _save_user_info(self):
        """保存用户信息"""
        with open(self.user_info_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_info, f, ensure_ascii=False, indent=2)
    
    def add_memory(self, content, memory_type="conversation"):
        """
        添加记忆
        
        参数：
            content: 记忆内容
            memory_type: 记忆类型（conversation, preference, fact）
        """
        timestamp = datetime.now().isoformat()
        
        # 添加到向量库
        self.vectorstore.add_texts(
            texts=[content],
            metadatas=[{
                "type": memory_type,
                "timestamp": timestamp
            }]
        )
        
        print(f"  💾 已保存记忆: {content[:50]}...")
    
    def extract_and_save_info(self, user_message, ai_response):
        """
        从对话中提取并保存用户信息
        """
        # 简单的信息提取（实际项目中可以用 LLM 做更智能的提取）
        message_lower = user_message.lower()
        
        # 提取姓名
        if "我叫" in user_message or "我是" in user_message:
            # 这里简化处理，实际可以用 NER 或 LLM 提取
            self.add_memory(f"用户说: {user_message}", "fact")
        
        # 提取偏好
        if "喜欢" in user_message or "爱好" in user_message:
            self.add_memory(f"用户偏好: {user_message}", "preference")
        
        # 保存对话
        conversation = f"用户: {user_message}\nAI: {ai_response}"
        self.add_memory(conversation, "conversation")
    
    def retrieve_relevant_memories(self, query, k=3):
        """检索相关记忆"""
        if self.vectorstore._collection.count() == 0:
            return []
        
        results = self.vectorstore.similarity_search(query, k=k)
        return results
    
    def get_memory_summary(self):
        """获取记忆摘要"""
        total = self.vectorstore._collection.count()
        return f"用户 {self.user_id} 的记忆库包含 {total} 条记忆"


# ============================================
# Part 6: 个性化 RAG 系统
# ============================================

print("\n" + "="*60)
print("Part 6: 个性化 RAG 系统")
print("="*60)

class PersonalizedRAG:
    """
    个性化 RAG 系统
    
    功能：
    - 结合知识库和用户记忆
    - 根据用户偏好定制回答
    - 记住用户的对话历史
    """
    
    def __init__(self, user_id, knowledge_base_dir="../../rag_docs"):
        print(f"\n初始化个性化 RAG 系统 (用户: {user_id})")
        
        self.user_id = user_id
        self.llm = get_llm()
        
        # 初始化用户记忆
        self.user_memory = UserMemoryStore(user_id)
        
        # 初始化知识库
        self.embeddings = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # 加载知识库（如果存在）
        self.knowledge_base = None
        if os.path.exists(knowledge_base_dir):
            self._load_knowledge_base(knowledge_base_dir)
        
        print("✅ 系统初始化完成\n")
    
    def _load_knowledge_base(self, docs_dir):
        """加载知识库"""
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        try:
            # 加载文档
            loader = DirectoryLoader(
                docs_dir,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"}
            )
            documents = loader.load()
            
            if not documents:
                return
            
            # 切分
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            chunks = splitter.split_documents(documents)
            
            # 创建向量库
            self.knowledge_base = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                collection_name="kb"
            )
            
            print(f"  📚 知识库加载完成: {len(chunks)} 个文档块")
        
        except Exception as e:
            print(f"  ⚠️  知识库加载失败: {e}")
    
    def chat(self, user_message):
        """
        个性化对话
        
        流程：
        1. 检索用户相关记忆
        2. 检索知识库相关内容
        3. 结合记忆和知识生成个性化回答
        4. 保存对话到记忆库
        """
        print(f"\n用户: {user_message}")
        
        # 1. 检索用户记忆
        user_memories = self.user_memory.retrieve_relevant_memories(user_message, k=2)
        memory_context = "\n".join([m.page_content for m in user_memories]) if user_memories else "无相关记忆"
        
        # 2. 检索知识库
        kb_context = ""
        if self.knowledge_base:
            kb_docs = self.knowledge_base.similarity_search(user_message, k=2)
            kb_context = "\n".join([d.page_content for d in kb_docs]) if kb_docs else "无相关知识"
        
        # 3. 构建个性化 Prompt
        prompt = f"""你是一个个性化的 AI 助手。请根据用户的历史记忆和知识库内容回答问题。

用户历史记忆：
{memory_context}

知识库内容：
{kb_context}

当前问题：{user_message}

要求：
1. 如果记忆中有用户的个人信息，要体现出你记得用户
2. 优先使用知识库内容回答专业问题
3. 结合用户偏好给出个性化建议
4. 回答要自然、友好

回答："""
        
        # 4. 生成回答
        response = self.llm.invoke(prompt)
        ai_response = response.content
        
        print(f"AI: {ai_response}")
        
        # 5. 保存到记忆
        self.user_memory.extract_and_save_info(user_message, ai_response)
        
        return ai_response
    
    def show_memory_stats(self):
        """显示记忆统计"""
        print(f"\n📊 {self.user_memory.get_memory_summary()}")


# ============================================
# Part 7: 实战演示
# ============================================

print("\n" + "="*60)
print("Part 7: 个性化 RAG 实战演示")
print("="*60)

# 创建个性化 RAG 系统
rag = PersonalizedRAG(user_id="user_001")

# 模拟对话
print("\n--- 第一次对话 ---")
rag.chat("你好，我叫李明，我是一名 Python 开发者")
rag.chat("我对机器学习很感兴趣")

print("\n--- 第二次对话（测试记忆） ---")
rag.chat("我叫什么名字？")
rag.chat("我对什么感兴趣？")

print("\n--- 结合知识库的对话 ---")
rag.chat("Python 有什么特点？")

# 显示记忆统计
rag.show_memory_stats()


# ============================================
# Part 8: 高级功能 - 记忆管理
# ============================================

print("\n" + "="*60)
print("Part 8: 高级功能 - 记忆管理")
print("="*60)

class AdvancedMemoryManager:
    """
    高级记忆管理器
    
    功能：
    - 记忆重要性评分
    - 自动遗忘不重要的记忆
    - 记忆冲突检测
    - 隐私保护
    """
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory_store = UserMemoryStore(user_id)
        self.llm = get_llm()
    
    def evaluate_importance(self, memory_content):
        """
        评估记忆重要性（1-10分）
        
        使用 LLM 判断记忆的重要性
        """
        prompt = f"""请评估以下记忆的重要性，给出 1-10 的分数。

记忆内容：{memory_content}

评分标准：
- 10分：关键个人信息（姓名、联系方式）
- 7-9分：重要偏好和习惯
- 4-6分：一般对话内容
- 1-3分：无关紧要的闲聊

只需要返回数字分数，不要解释。
分数："""
        
        try:
            response = self.llm.invoke(prompt)
            score = int(response.content.strip())
            return min(max(score, 1), 10)  # 限制在 1-10
        except:
            return 5  # 默认中等重要性
    
    def detect_conflict(self, new_info, existing_memories):
        """
        检测记忆冲突
        
        例如：用户说"我叫张三"，但之前说过"我叫李四"
        """
        # 简化实现：检查是否有矛盾的信息
        # 实际项目中可以用 LLM 做更智能的判断
        
        conflicts = []
        for memory in existing_memories:
            # 这里可以用 LLM 判断是否冲突
            pass
        
        return conflicts
    
    def forget_unimportant_memories(self, threshold=3, max_age_days=30):
        """
        遗忘不重要的旧记忆
        
        参数：
            threshold: 重要性阈值，低于此值的记忆会被遗忘
            max_age_days: 超过此天数的低重要性记忆会被删除
        """
        print(f"\n🧹 清理不重要的记忆...")
        print(f"   阈值: 重要性 < {threshold}, 年龄 > {max_age_days} 天")
        
        # 实际实现需要：
        # 1. 遍历所有记忆
        # 2. 评估重要性和年龄
        # 3. 删除符合条件的记忆
        
        print("   (演示功能，实际实现略)")
    
    def anonymize_sensitive_info(self, content):
        """
        匿名化敏感信息
        
        保护用户隐私：电话、地址、身份证等
        """
        # 简化实现
        import re
        
        # 隐藏电话号码
        content = re.sub(r'1[3-9]\d{9}', '***********', content)
        
        # 隐藏邮箱
        content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                        '***@***.com', content)
        
        return content


print("""
高级记忆管理功能：

1. 记忆重要性评分
   - 使用 LLM 评估每条记忆的重要性
   - 重要记忆永久保存，不重要的可以遗忘

2. 自动遗忘机制
   - 定期清理低重要性的旧记忆
   - 避免记忆库无限增长

3. 记忆冲突检测
   - 检测矛盾的信息（如用户改名）
   - 提示用户确认或更新

4. 隐私保护
   - 自动识别和匿名化敏感信息
   - 符合数据保护法规

5. 记忆检索优化
   - 结合时间衰减（越久越不重要）
   - 结合访问频率（常用的更重要）
""")


# ============================================
# Part 9: 了解 MemGPT / Zep
# ============================================

print("\n" + "="*60)
print("Part 9: 了解 MemGPT / Zep 等记忆管理方案")
print("="*60)

print("""
专业的记忆管理方案：

1. MemGPT
   - 模拟操作系统的内存管理
   - 分层记忆：工作记忆 + 长期记忆
   - 自动在层级间移动记忆
   - 适合需要大量上下文的应用

2. Zep
   - 专门的记忆存储服务
   - 支持多种记忆类型
   - 提供 API 和 SDK
   - 易于集成到现有系统

3. LangChain Memory
   - 我们今天学的
   - 轻量级，易于使用
   - 适合中小型项目

选择建议：
- 小项目：LangChain Memory
- 中型项目：自建向量库记忆（我们的方案）
- 大型项目：MemGPT 或 Zep

参考资源：
- MemGPT: https://github.com/cpacker/MemGPT
- Zep: https://www.getzep.com/
- LangChain Memory: https://python.langchain.com/docs/modules/memory/
""")


# ============================================
# Part 10: 实战练习
# ============================================

print("\n" + "="*60)
print("Part 10: 实战练习")
print("="*60)

print("""
练习任务：为 3.3 的个人知识库系统添加记忆功能

要求：
1. 为每个用户创建独立的记忆库
2. 记住用户的提问历史
3. 记住用户的偏好（如喜欢简短回答还是详细回答）
4. 在回答时体现出"记得"用户

提示：
- 可以复用 UserMemoryStore 类
- 在 PersonalKnowledgeBase 类中集成记忆功能
- 在生成回答时，同时检索知识库和记忆库

扩展挑战：
- 实现多用户支持
- 添加用户登录功能
- 实现记忆导出/导入
- 添加记忆可视化界面
""")


# ============================================
# 总结
# ============================================

print("\n" + "="*60)
print("本节总结")
print("="*60)

print("""
✅ 学到的内容：

1. LLM 无状态性
   - LLM 本身不记得之前的对话
   - 需要显式传入历史记录

2. LangChain Memory 类型
   - ConversationBufferMemory: 完整历史
   - ConversationBufferWindowMemory: 滑动窗口
   - ConversationSummaryMemory: 总结历史
   - VectorStoreRetrieverMemory: 向量检索

3. 用户专属记忆库
   - 使用向量数据库存储用户信息
   - 基于相似度检索相关记忆
   - 持久化存储

4. 个性化 RAG
   - 结合知识库和用户记忆
   - 生成个性化回答
   - 提升用户体验

5. 高级记忆管理
   - 重要性评分
   - 自动遗忘
   - 冲突检测
   - 隐私保护

💡 关键思考：

1. 记忆冲突
   - 用户信息变化怎么办？
   - 如何更新旧记忆？

2. 遗忘机制
   - 什么记忆应该遗忘？
   - 如何平衡记忆量和性能？

3. 隐私问题
   - 如何保护用户隐私？
   - 敏感信息如何处理？

4. 多用户场景
   - 如何隔离不同用户的记忆？
   - 如何处理共享知识？

下一步：第4周 - Agent 开发
- Agent = LLM + Tools + Memory
- ReAct 模式
- 工具调用
""")
