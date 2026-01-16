# LLM 8周冲刺学习计划

> 目标：Java 背景转 AI 应用开发，2个月内具备面试能力
> 重点方向：LLM 应用开发、RAG、Agent

---

## 第1周：Python 基础 + AI 开发环境

- [x] 1.1 Python 快速入门（你有 Java 基础，3天够了）✅
  - [x] 语法差异：缩进、动态类型、列表推导式
  - [x] 常用库：requests, json, os
  - [x] 练习：写一个调用 API 的小脚本

- [x] 1.2 开发环境搭建 ✅
  - [x] 安装 Anaconda / venv 虚拟环境
  - [x] VS Code + Python 插件配置
  - [x] 熟悉 Jupyter Notebook

- [x] 1.3 第一个 LLM 调用 ✅
  - [x] 注册 DeepSeek / 智谱 API（国内免费额度）
  - [x] 用 Python 调用大模型 API
  - [x] 理解 prompt、temperature、max_tokens 等参数

---

## 第2周：LangChain 入门 + Prompt Engineering

- [x] 2.1 LangChain 基础 ✅
  - [x] 安装 langchain, langchain-community
  - [x] 理解 Chain 的概念
  - [x] 实现简单的 LLMChain

- [x] 2.2 Prompt Engineering ✅
  - [x] 学习 prompt 模板设计
  - [x] Few-shot learning 实践
  - [x] Chain-of-Thought 提示技巧
  - [x] 练习：优化一个问答 prompt

- [x] 2.3 输出解析 ✅
  - [x] 使用 OutputParser 结构化输出
  - [x] JSON 格式输出
  - [x] 练习：让 LLM 输出结构化数据

---

## 第3周：RAG 系统搭建（重点！）

- [ ] 3.1 向量数据库
  - [ ] 理解 Embedding 原理（你已学过余弦相似度）
  - [ ] 安装使用 Chroma / FAISS
  - [ ] 文档切分策略

- [ ] 3.2 RAG 完整流程
  - [ ] 文档加载（PDF、Word、网页）
  - [ ] 文本切分（chunk_size, overlap）
  - [ ] 向量化存储
  - [ ] 相似度检索
  - [ ] 结合 LLM 生成回答

- [ ] 3.3 RAG 项目实战
  - [ ] 构建一个"个人知识库问答系统"
  - [ ] 支持上传文档、提问、获取答案
  - [ ] 这个项目可以写进简历！

- [ ] 3.4 个性化 RAG 与记忆系统（进阶）
  - [ ] 理解 LLM 无状态性的局限
  - [ ] 学习 LangChain Memory 类型（ConversationBufferMemory, ConversationSummaryMemory, VectorStoreRetrieverMemory）
  - [ ] 实现用户专属记忆向量库
    - [ ] 对话信息提取与存储
    - [ ] 用户偏好自动学习
    - [ ] 记忆检索与融合
  - [ ] 了解 MemGPT / Zep 等记忆管理方案
  - [ ] 练习：为 RAG 系统添加"会记住用户"的能力
  - [ ] 思考：记忆冲突、遗忘机制、隐私问题

---

## 第4周：Agent 开发

- [ ] 4.1 Agent 基础概念
  - [ ] 理解 Agent = LLM + Tools + Memory
  - [ ] ReAct 模式（推理+行动）
  - [ ] 工具调用（Function Calling）

- [ ] 4.2 LangChain Agent
  - [ ] 创建自定义 Tool
  - [ ] 使用 AgentExecutor
  - [ ] 实现一个能搜索网页的 Agent

- [ ] 4.3 多 Agent 协作（了解）
  - [ ] 了解 AutoGen / CrewAI 框架
  - [ ] 理解多 Agent 协作模式

---

## 第5周：低代码平台 + Web 开发

- [ ] 5.1 Dify 平台实战
  - [ ] 注册 Dify 账号
  - [ ] 搭建一个 RAG 应用
  - [ ] 搭建一个 Agent 工作流
  - [ ] 导出 API 供外部调用

- [ ] 5.2 FastAPI 基础
  - [ ] 创建 REST API
  - [ ] 请求参数处理
  - [ ] 异步处理
  - [ ] 练习：把你的 RAG 系统封装成 API

- [ ] 5.3 简单前端（可选）
  - [ ] Streamlit 快速搭建 UI
  - [ ] Gradio 交互界面
  - [ ] 让你的项目有个可展示的界面

---

## 第6周：项目整合 + 简历项目

- [ ] 6.1 完善 RAG 项目
  - [ ] 添加对话历史（Memory）
  - [ ] 优化检索效果
  - [ ] 添加来源引用
  - [ ] 部署到云服务器（可选）

- [ ] 6.2 第二个项目：智能客服/助手
  - [ ] 结合 Agent + RAG
  - [ ] 支持多轮对话
  - [ ] 可以调用外部工具

- [ ] 6.3 整理项目文档
  - [ ] 写清楚项目背景、技术栈、你的贡献
  - [ ] 准备 GitHub 仓库
  - [ ] 录制演示视频（加分项）

---

## 第7周：面试准备 + 查漏补缺

- [ ] 7.1 技术面试准备
  - [ ] RAG 原理和优化方法
  - [ ] Agent 工作流程
  - [ ] Prompt Engineering 技巧
  - [ ] 向量数据库选型对比
  - [ ] LangChain vs LlamaIndex 区别

- [ ] 7.2 Java + AI 结合点
  - [ ] Spring Boot 调用 LLM API
  - [ ] Java 项目中集成 AI 能力
  - [ ] 微服务架构中的 AI 模块设计

- [ ] 7.3 简历优化
  - [ ] 突出 AI 项目经验
  - [ ] 量化项目成果
  - [ ] 准备项目讲解话术

---

## 第8周：投递 + 面试 + 持续学习

- [ ] 8.1 批量投递
  - [ ] 北京/天津 LLM 相关岗位
  - [ ] Java + AI 方向岗位
  - [ ] 每天投递 10-20 个

- [ ] 8.2 面试复盘
  - [ ] 记录面试问题
  - [ ] 针对性补充知识
  - [ ] 优化回答方式

- [ ] 8.3 持续学习方向
  - [ ] 模型微调（LoRA）- 进阶
  - [ ] 多模态应用 - 进阶
  - [ ] AI + 蛋白质预测 - 你的长期目标

---

## 学习资源推荐

**视频课程：**
- B站：吴恩达 LangChain 课程（中文字幕）
- B站：动手学大模型应用开发

**文档：**
- LangChain 官方文档：https://python.langchain.com/
- Dify 官方文档：https://docs.dify.ai/

**实践平台：**
- DeepSeek API（国产，便宜）
- 智谱 AI（有免费额度）
- Dify（低代码平台）

---

## 进度追踪

| 周次 | 重点内容 | 开始日期 | 完成日期 | 状态 |
|------|----------|----------|----------|------|
| 第1周 | Python + 环境 | 2026-01-08 | 2026-01-10 | ✅ 完成 |
| 第2周 | LangChain + Prompt | 2026-01-13 | 2026-01-13 | ✅ 完成 |
| 第3周 | RAG 系统 | | | ⬜ |
| 第4周 | Agent 开发 | | | ⬜ |
| 第5周 | Dify + FastAPI | | | ⬜ |
| 第6周 | 项目整合 | | | ⬜ |
| 第7周 | 面试准备 | | | ⬜ |
| 第8周 | 投递面试 | | | ⬜ |

---

## 与原计划的对比

**跳过/简化的内容：**
- 神经网络手写实现（理解原理即可）
- RNN/LSTM（Transformer 时代不是重点）
- 从零训练模型（应用层不需要）

**新增的重点：**
- RAG 系统（面试必问）
- Agent 开发（热门方向）
- Dify 等低代码平台（企业常用）
- FastAPI（Python Web 框架）
- 项目实战（简历亮点）

**保留的基础：**
- 你已完成的向量、矩阵知识 ✅
- 梯度下降理解（帮助理解模型训练）
- Transformer 架构理解（面试会问原理）
