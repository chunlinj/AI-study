"""
第3周 - 3.3 RAG 项目实战
========================
项目：个人知识库问答系统（可以写进简历！）

功能：
1. 支持上传文档（TXT、PDF、Word）
2. 动态添加到知识库
3. 智能问答
4. 显示答案来源
5. 持久化存储（重启后数据不丢失）

这是一个完整的应用，不只是演示代码！
"""

import os
import shutil
import httpx
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader,
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


# ============================================
# 配置
# ============================================

class Config:
    """系统配置"""
    # 知识库存储目录
    KNOWLEDGE_BASE_DIR = "./my_knowledge_base"
    UPLOADED_DOCS_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "documents")
    VECTOR_DB_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "vector_db")
    
    # 文档处理参数
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    
    # 检索参数
    TOP_K = 3
    
    # 支持的文件类型
    SUPPORTED_EXTENSIONS = ['.txt', '.pdf', '.docx', '.doc']


# ============================================
# 核心类：个人知识库系统
# ============================================

class PersonalKnowledgeBase:
    """
    个人知识库问答系统
    
    功能：
    - 上传文档
    - 构建/更新向量索引
    - 智能问答
    - 查看知识库状态
    """
    
    def __init__(self):
        print("="*60)
        print("🚀 个人知识库问答系统")
        print("="*60)
        
        # 创建必要的目录
        os.makedirs(Config.UPLOADED_DOCS_DIR, exist_ok=True)
        os.makedirs(Config.VECTOR_DB_DIR, exist_ok=True)
        
        # 初始化组件
        self.embeddings = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        self.llm = self._get_llm()
        self.vectorstore = None
        self.rag_chain = None
        
        # 加载或创建向量数据库
        self._load_or_create_vectorstore()
        
        print(f"\n✅ 系统初始化完成")
        self._show_status()
    
    def _get_llm(self):
        """获取 DeepSeek LLM"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            print("⚠️  警告: 未设置 DEEPSEEK_API_KEY，问答功能将不可用")
            return None
        
        return ChatOpenAI(
            model="deepseek-chat",
            api_key=api_key,
            base_url="https://api.deepseek.com",
            http_client=httpx.Client(verify=False),
            temperature=0.7
        )
    
    def _load_or_create_vectorstore(self):
        """加载已有的向量数据库，或创建新的"""
        try:
            # 尝试加载已有的数据库
            if os.path.exists(Config.VECTOR_DB_DIR) and os.listdir(Config.VECTOR_DB_DIR):
                print("\n📂 加载已有的知识库...")
                self.vectorstore = Chroma(
                    persist_directory=Config.VECTOR_DB_DIR,
                    embedding_function=self.embeddings,
                    collection_name="personal_kb"
                )
                print(f"  ✅ 已加载 {self.vectorstore._collection.count()} 个文档块")
            else:
                print("\n📂 创建新的知识库...")
                self.vectorstore = Chroma(
                    persist_directory=Config.VECTOR_DB_DIR,
                    embedding_function=self.embeddings,
                    collection_name="personal_kb"
                )
                print("  ✅ 新知识库创建完成")
            
            # 创建 RAG 链
            if self.llm:
                self._create_rag_chain()
        
        except Exception as e:
            print(f"❌ 加载向量数据库失败: {e}")
            self.vectorstore = None
    
    def _create_rag_chain(self):
        """创建 RAG 问答链"""
        if not self.vectorstore or not self.llm:
            return
        
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": Config.TOP_K}
        )
        
        prompt = ChatPromptTemplate.from_template("""
你是一个专业的知识库助手。请根据以下参考资料回答用户的问题。

参考资料：
{context}

用户问题：{question}

要求：
1. 只根据参考资料回答，不要编造信息
2. 如果资料中没有相关信息，请明确说明
3. 回答要简洁、准确、有条理
4. 可以适当组织语言，但不要改变原意

回答：
""")
        
        def format_docs(docs):
            return "\n\n".join(f"[资料 {i+1}]\n{doc.page_content}" 
                              for i, doc in enumerate(docs))
        
        self.rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        self.retriever = retriever
    
    def upload_document(self, file_path):
        """
        上传文档到知识库
        
        参数：
            file_path: 文档路径
        """
        print(f"\n📤 上传文档: {file_path}")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return False
        
        # 检查文件类型
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in Config.SUPPORTED_EXTENSIONS:
            print(f"❌ 不支持的文件类型: {file_ext}")
            print(f"   支持的类型: {', '.join(Config.SUPPORTED_EXTENSIONS)}")
            return False
        
        try:
            # 复制文件到知识库目录
            filename = Path(file_path).name
            dest_path = os.path.join(Config.UPLOADED_DOCS_DIR, filename)
            
            # 如果文件已存在，添加时间戳
            if os.path.exists(dest_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                dest_path = os.path.join(Config.UPLOADED_DOCS_DIR, filename)
            
            shutil.copy2(file_path, dest_path)
            print(f"  ✅ 文件已保存: {filename}")
            
            # 处理文档并添加到向量库
            self._process_and_index_document(dest_path)
            
            return True
        
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            return False
    
    def _process_and_index_document(self, file_path):
        """处理文档并添加到向量索引"""
        print(f"  🔄 处理文档...")
        
        # 1. 加载文档
        documents = self._load_document(file_path)
        if not documents:
            return
        
        # 2. 切分文档
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"  ✅ 切分成 {len(chunks)} 个文本块")
        
        # 3. 添加到向量库
        if self.vectorstore:
            self.vectorstore.add_documents(chunks)
            print(f"  ✅ 已添加到知识库")
            print(f"  📊 当前知识库共有 {self.vectorstore._collection.count()} 个文档块")
    
    def _load_document(self, file_path):
        """根据文件类型加载文档"""
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
            elif file_ext == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_ext in ['.docx', '.doc']:
                loader = UnstructuredWordDocumentLoader(file_path)
            else:
                print(f"❌ 不支持的文件类型: {file_ext}")
                return None
            
            return loader.load()
        
        except Exception as e:
            print(f"❌ 加载文档失败: {e}")
            return None
    
    def rebuild_index(self):
        """重建整个知识库索引"""
        print("\n🔄 重建知识库索引...")
        
        # 清空现有索引
        if os.path.exists(Config.VECTOR_DB_DIR):
            shutil.rmtree(Config.VECTOR_DB_DIR)
        
        # 重新创建向量库
        self.vectorstore = Chroma(
            persist_directory=Config.VECTOR_DB_DIR,
            embedding_function=self.embeddings,
            collection_name="personal_kb"
        )
        
        # 处理所有文档
        doc_files = list(Path(Config.UPLOADED_DOCS_DIR).glob("*"))
        doc_files = [f for f in doc_files if f.suffix.lower() in Config.SUPPORTED_EXTENSIONS]
        
        if not doc_files:
            print("  ⚠️  没有找到文档")
            return
        
        print(f"  找到 {len(doc_files)} 个文档")
        
        for doc_file in doc_files:
            print(f"\n  处理: {doc_file.name}")
            self._process_and_index_document(str(doc_file))
        
        print(f"\n✅ 索引重建完成")
        
        # 重新创建 RAG 链
        if self.llm:
            self._create_rag_chain()
    
    def ask(self, question):
        """提问"""
        if not self.rag_chain:
            print("❌ 问答系统未初始化（可能缺少 API Key）")
            return
        
        if not self.vectorstore or self.vectorstore._collection.count() == 0:
            print("❌ 知识库为空，请先上传文档")
            return
        
        print(f"\n💬 提问: {question}")
        print("="*60)
        
        try:
            # 检索相关文档
            relevant_docs = self.retriever.get_relevant_documents(question)
            
            # 生成回答
            answer = self.rag_chain.invoke(question)
            
            print(f"\n🤖 回答:")
            print(f"{answer}")
            
            print(f"\n📚 参考来源:")
            for i, doc in enumerate(relevant_docs, 1):
                source = doc.metadata.get('source', 'Unknown')
                source_name = Path(source).name
                print(f"  [{i}] {source_name}")
                print(f"      {doc.page_content[:80]}...")
        
        except Exception as e:
            print(f"❌ 问答失败: {e}")
    
    def _show_status(self):
        """显示知识库状态"""
        print(f"\n📊 知识库状态:")
        
        # 统计文档数量
        doc_files = list(Path(Config.UPLOADED_DOCS_DIR).glob("*"))
        doc_files = [f for f in doc_files if f.suffix.lower() in Config.SUPPORTED_EXTENSIONS]
        
        print(f"  📄 文档数量: {len(doc_files)}")
        
        if self.vectorstore:
            print(f"  🔢 文档块数: {self.vectorstore._collection.count()}")
        
        print(f"  📁 存储位置: {Config.KNOWLEDGE_BASE_DIR}")
    
    def list_documents(self):
        """列出所有文档"""
        print("\n📚 知识库文档列表:")
        
        doc_files = list(Path(Config.UPLOADED_DOCS_DIR).glob("*"))
        doc_files = [f for f in doc_files if f.suffix.lower() in Config.SUPPORTED_EXTENSIONS]
        
        if not doc_files:
            print("  (空)")
            return
        
        for i, doc_file in enumerate(doc_files, 1):
            size = doc_file.stat().st_size / 1024  # KB
            print(f"  [{i}] {doc_file.name} ({size:.1f} KB)")
    
    def interactive_mode(self):
        """交互式问答模式"""
        print("\n" + "="*60)
        print("💬 交互式问答模式")
        print("="*60)
        print("命令:")
        print("  - 直接输入问题进行提问")
        print("  - 'upload <文件路径>' 上传文档")
        print("  - 'list' 查看文档列表")
        print("  - 'status' 查看系统状态")
        print("  - 'rebuild' 重建索引")
        print("  - 'quit' 或 'exit' 退出")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("👤 你: ").strip()
                
                if not user_input:
                    continue
                
                # 退出命令
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 再见！")
                    break
                
                # 上传文档
                elif user_input.lower().startswith('upload '):
                    file_path = user_input[7:].strip()
                    self.upload_document(file_path)
                
                # 列出文档
                elif user_input.lower() == 'list':
                    self.list_documents()
                
                # 查看状态
                elif user_input.lower() == 'status':
                    self._show_status()
                
                # 重建索引
                elif user_input.lower() == 'rebuild':
                    self.rebuild_index()
                
                # 提问
                else:
                    self.ask(user_input)
                
                print()  # 空行分隔
            
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}\n")


# ============================================
# 主程序
# ============================================

def main():
    """主程序入口"""
    print("\n" + "="*60)
    print("🎯 第3周 - 3.3 RAG 项目实战")
    print("📚 个人知识库问答系统")
    print("="*60)
    
    # 创建知识库系统
    kb = PersonalKnowledgeBase()
    
    # 示例：上传一些初始文档（如果知识库为空）
    if kb.vectorstore._collection.count() == 0:
        print("\n💡 提示: 知识库为空，可以上传一些文档")
        print("   示例文档位置: ../../rag_docs/")
        
        # 自动加载示例文档
        sample_docs_dir = "../../rag_docs"
        if os.path.exists(sample_docs_dir):
            print(f"\n🔄 自动加载示例文档...")
            for file in Path(sample_docs_dir).glob("*.txt"):
                kb.upload_document(str(file))
    
    # 进入交互模式
    kb.interactive_mode()


if __name__ == "__main__":
    main()


# ============================================
# 💡 项目亮点（写简历用）
# ============================================
"""
项目名称：个人知识库问答系统

技术栈：
- Python, LangChain, Chroma, HuggingFace Embeddings
- DeepSeek API (LLM)
- RAG (Retrieval-Augmented Generation)

核心功能：
1. 文档管理：支持 TXT/PDF/Word 文档上传
2. 智能索引：自动文档切分、向量化、持久化存储
3. 语义检索：基于向量相似度的智能检索
4. 问答生成：结合检索结果和 LLM 生成准确答案
5. 来源追溯：显示答案来源文档，提高可信度

技术亮点：
- 使用 Chroma 向量数据库实现高效检索
- 采用 LCEL (LangChain Expression Language) 构建 RAG 链
- 支持动态添加文档，无需重启系统
- 持久化存储，数据不丢失
- 模块化设计，易于扩展

应用场景：
- 个人笔记管理与检索
- 企业知识库问答
- 技术文档助手
- 学习资料整理

可扩展方向：
- 添加 Web 界面（Streamlit/Gradio）
- 支持更多文档格式
- 实现对话历史记忆
- 添加文档管理功能（删除、更新）
- 多用户支持
"""
