"""
第4周 - 4.4 多 Agent 协作
目标：
- 了解 AutoGen / CrewAI 框架
- 理解多 Agent 协作模式
- 了解个人助手项目架构

这是一个概念性学习，重点理解原理和模式
"""

# ============================================================
# 第1部分：为什么需要多 Agent？
# ============================================================
"""
🤖🤖🤖 多 Agent 协作

一、单 Agent 的局限

单 Agent：
┌─────────────────────────────────────────┐
│               Agent                      │
│  一个大脑处理所有事情                     │
│  - 理解用户意图                          │
│  - 调用工具                              │
│  - 生成回答                              │
│  - 检查质量                              │
│  → 任务复杂时容易出错、效率低             │
└─────────────────────────────────────────┘

二、多 Agent 的思路

多 Agent（分工协作）：
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator (协调者)                 │
│                         ↓                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Planner  │  │ Coder    │  │ Reviewer │  │ Writer  │ │
│  │ 规划任务  │  │ 写代码   │  │ 审核代码  │  │ 写文档  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│       ↓              ↓             ↓            ↓       │
│                  互相协作、反馈、迭代                    │
└─────────────────────────────────────────────────────────┘

三、类比理解

单 Agent ≈ 一个人做所有工作
多 Agent ≈ 一个团队分工协作

就像软件开发团队：
- 产品经理：理解需求、规划任务
- 程序员：实现功能
- 测试员：发现问题
- 技术写手：写文档

每个人专注自己的领域，效率更高、质量更好
"""


# ============================================================
# 第2部分：多 Agent 协作模式
# ============================================================
"""
🔄 常见的多 Agent 协作模式

一、顺序模式（Sequential）

Agent A → Agent B → Agent C → 最终结果

示例：
┌────────────┐    ┌────────────┐    ┌────────────┐
│  Planner   │ →  │   Coder    │ →  │  Reviewer  │
│  分析需求   │    │  写代码     │    │  审核代码   │
└────────────┘    └────────────┘    └────────────┘

优点：流程清晰，易于调试
缺点：灵活性差，不能回头修改


二、层级模式（Hierarchical）

       ┌───────────────┐
       │   Manager     │
       │   (管理者)     │
       └───────┬───────┘
               │
    ┌──────────┼──────────┐
    ↓          ↓          ↓
┌───────┐  ┌───────┐  ┌───────┐
│Worker1│  │Worker2│  │Worker3│
└───────┘  └───────┘  └───────┘

Manager 分配任务给 Worker，收集结果汇总

优点：可并行执行，效率高
缺点：Manager 是瓶颈


三、对话模式（Conversational）

Agent A ←→ Agent B
    ↕         ↕
Agent C ←→ Agent D

多个 Agent 互相对话、讨论、辩论

示例：写作任务
- Writer：写初稿
- Critic：提出批评意见
- Writer：根据意见修改
- Critic：再次审核
- 循环直到满意

优点：可以迭代优化
缺点：可能陷入无限循环


四、投票/共识模式

多个 Agent 独立思考，然后投票决定

┌───────────┐
│  Agent A  │ → 答案 1 ─┐
└───────────┘           │
┌───────────┐           ├→ 投票/共识 → 最终答案
│  Agent B  │ → 答案 2 ─┤
└───────────┘           │
┌───────────┐           │
│  Agent C  │ → 答案 3 ─┘
└───────────┘

优点：降低单个 Agent 的错误率
缺点：成本高（多次 LLM 调用）
"""


# ============================================================
# 第3部分：主流多 Agent 框架
# ============================================================
"""
📦 主流多 Agent 框架对比

一、AutoGen（微软）

特点：
- 微软开源，社区活跃
- 支持多种对话模式
- 内置代码执行能力
- 支持人类参与（Human-in-the-loop）

核心概念：
- AssistantAgent：AI 助手
- UserProxyAgent：用户代理（可执行代码）
- GroupChat：群聊（多 Agent 对话）

适合场景：
- 代码生成和执行
- 需要人类介入的任务
- 研究和实验


二、CrewAI

特点：
- 专注于"角色扮演"模式
- 每个 Agent 有明确的角色和目标
- 支持工具集成
- 更接近真实团队协作

核心概念：
- Agent：定义角色、目标、背景
- Task：具体任务
- Crew：Agent 团队
- Process：执行流程（顺序/层级）

适合场景：
- 模拟真实团队工作流
- 内容创作
- 研究分析


三、LangGraph（LangChain）

特点：
- LangChain 官方出品
- 基于图（Graph）的工作流
- 灵活的状态管理
- 可视化支持

核心概念：
- Node：节点（每个节点是一个 Agent 或函数）
- Edge：边（定义流转条件）
- State：共享状态

适合场景：
- 复杂的工作流
- 需要精细控制的场景
- 与 LangChain 生态集成


四、框架对比总结

┌───────────┬────────────┬────────────┬────────────┐
│   框架    │   学习成本  │   灵活性   │   适合场景  │
├───────────┼────────────┼────────────┼────────────┤
│ AutoGen   │    中等    │    高      │ 代码执行    │
│ CrewAI    │    低      │    中      │ 角色协作    │
│ LangGraph │    高      │    最高    │ 复杂工作流  │
└───────────┴────────────┴────────────┴────────────┘
"""


# ============================================================
# 第4部分：AutoGen 代码示例
# ============================================================
"""
安装：pip install pyautogen
"""

AUTOGEN_EXAMPLE = '''
"""
AutoGen 多 Agent 示例
两个 Agent 对话完成任务
"""

# pip install pyautogen
import autogen

# 配置 LLM
config_list = [
    {
        "model": "deepseek-chat",
        "api_key": "your-api-key",
        "base_url": "https://api.deepseek.com"
    }
]

llm_config = {"config_list": config_list}

# 创建 Assistant Agent（AI 助手）
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="""你是一个乐于助人的AI助手。
    你擅长分析问题并给出解决方案。
    回答时请使用中文。"""
)

# 创建 User Proxy Agent（用户代理）
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # 不需要人类输入
    max_consecutive_auto_reply=3,  # 最多自动回复3次
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="请分析一下 Python 和 Java 的主要区别，并给出选择建议。"
)
'''


# ============================================================
# 第5部分：CrewAI 代码示例
# ============================================================
"""
安装：pip install crewai
"""

CREWAI_EXAMPLE = '''
"""
CrewAI 多 Agent 示例
模拟一个内容创作团队
"""

# pip install crewai
from crewai import Agent, Task, Crew, Process

# 定义 Agent（角色）
researcher = Agent(
    role="研究员",
    goal="深入研究给定主题，收集准确的信息",
    backstory="""你是一位经验丰富的研究员，
    擅长从各种来源收集和分析信息。
    你总是追求事实准确性。""",
    verbose=True
)

writer = Agent(
    role="作家",
    goal="基于研究结果撰写引人入胜的文章",
    backstory="""你是一位才华横溢的作家，
    擅长将复杂的信息转化为易读的文章。
    你的文风清晰、生动、有吸引力。""",
    verbose=True
)

editor = Agent(
    role="编辑",
    goal="审核和优化文章，确保质量",
    backstory="""你是一位严谨的编辑，
    对文字有极高的要求。
    你擅长发现问题并提出改进建议。""",
    verbose=True
)

# 定义任务
research_task = Task(
    description="研究主题：人工智能的发展历史和未来趋势",
    agent=researcher,
    expected_output="一份详细的研究报告，包含关键事实和数据"
)

writing_task = Task(
    description="基于研究报告，撰写一篇 500 字的科普文章",
    agent=writer,
    expected_output="一篇结构清晰、内容准确的科普文章"
)

editing_task = Task(
    description="审核文章，提出修改建议，优化表达",
    agent=editor,
    expected_output="优化后的最终版文章"
)

# 创建 Crew（团队）
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,  # 顺序执行
    verbose=2
)

# 执行任务
result = crew.kickoff()
print(result)
'''


# ============================================================
# 第6部分：简单的多 Agent 实现（不依赖框架）
# ============================================================

import os
import httpx


def get_llm_response(messages, system_prompt=None):
    """调用 LLM 获取响应"""
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        http_client=httpx.Client(verify=False),
        temperature=0.7
    )
    
    msgs = []
    if system_prompt:
        msgs.append(SystemMessage(content=system_prompt))
    msgs.extend(messages)
    
    response = llm.invoke(msgs)
    return response.content


class SimpleAgent:
    """简单的 Agent 类"""
    
    def __init__(self, name: str, role: str, goal: str):
        self.name = name
        self.role = role
        self.goal = goal
        self.system_prompt = f"""你是 {name}，你的角色是 {role}。
你的目标是：{goal}
请始终保持这个角色，用中文回答。"""
    
    def respond(self, message: str) -> str:
        """生成响应"""
        from langchain_core.messages import HumanMessage
        return get_llm_response(
            [HumanMessage(content=message)],
            self.system_prompt
        )


def demo_simple_multi_agent():
    """演示简单的多 Agent 协作"""
    print("=" * 60)
    print("简单多 Agent 协作演示")
    print("=" * 60)
    
    # 创建两个 Agent
    planner = SimpleAgent(
        name="规划师",
        role="任务规划专家",
        goal="分析用户需求，制定清晰的执行计划"
    )
    
    executor = SimpleAgent(
        name="执行者",
        role="任务执行专家",
        goal="按照计划执行任务，完成具体工作"
    )
    
    reviewer = SimpleAgent(
        name="审核员",
        role="质量审核专家",
        goal="审核执行结果，提出改进建议"
    )
    
    # 用户任务
    user_task = "帮我写一个 Python 函数，计算斐波那契数列的第 n 项"
    
    print(f"\n用户任务：{user_task}")
    print("-" * 60)
    
    # 第一步：规划师分析任务
    print("\n【第1步：规划师分析】")
    plan = planner.respond(f"请分析这个任务并制定执行计划：{user_task}")
    print(f"规划师：{plan}")
    
    # 第二步：执行者执行任务
    print("\n【第2步：执行者执行】")
    execution = executor.respond(f"请按照以下计划执行任务：\n{plan}")
    print(f"执行者：{execution}")
    
    # 第三步：审核员审核结果
    print("\n【第3步：审核员审核】")
    review = reviewer.respond(f"请审核以下执行结果：\n{execution}")
    print(f"审核员：{review}")
    
    print("\n" + "=" * 60)
    print("多 Agent 协作完成！")


# ============================================================
# 第7部分：个人助手项目架构
# ============================================================
"""
🏠 个人助手项目架构示例

一、Moltbot 风格架构

┌─────────────────────────────────────────────────────────┐
│                    用户界面                              │
│              (Web / App / 命令行)                        │
└───────────────────────┬─────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                  协调器 (Orchestrator)                   │
│  - 理解用户意图                                          │
│  - 路由到合适的 Agent                                    │
│  - 整合多个 Agent 的结果                                 │
└───────────────────────┬─────────────────────────────────┘
                        ↓
    ┌───────────┬───────────┬───────────┬───────────┐
    ↓           ↓           ↓           ↓           ↓
┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐
│日程   │  │邮件   │  │文档   │  │搜索   │  │其他   │
│Agent  │  │Agent  │  │Agent  │  │Agent  │  │Agent  │
└───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘
    ↓          ↓          ↓          ↓          ↓
┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐
│日历API│  │邮件API│  │文件系统│  │搜索API│  │其他API│
└───────┘  └───────┘  └───────┘  └───────┘  └───────┘


二、关键组件

1. 用户界面层
   - Web 界面（React/Vue）
   - 移动 App
   - 命令行工具
   - 语音交互

2. 协调器层
   - 意图识别
   - Agent 路由
   - 结果整合
   - 对话管理

3. Agent 层
   - 各司其职
   - 可独立扩展
   - 互相协作

4. 工具/API 层
   - MCP Server
   - REST API
   - 数据库


三、技术选型建议

| 组件       | 推荐技术                          |
|------------|----------------------------------|
| 后端框架   | FastAPI / Flask                  |
| LLM 框架   | LangChain / LangGraph            |
| 多 Agent   | CrewAI / AutoGen / 自定义        |
| 工具协议   | MCP                              |
| 向量数据库 | Chroma / FAISS / Milvus          |
| 前端       | React / Vue / Streamlit          |
| 部署       | Docker / Kubernetes              |


四、开发路线图

Phase 1：单 Agent + 基础工具
- 一个通用 Agent
- 2-3 个核心工具（天气、搜索、计算）

Phase 2：多 Agent + 更多工具
- 专业 Agent（日程、邮件等）
- MCP 工具集成
- 简单的协调器

Phase 3：完整个人助手
- 完善的协调器
- 持久化记忆
- 用户个性化
- 多端支持
"""


# ============================================================
# 主程序
# ============================================================

def main():
    print("\n" + "=" * 60)
    print("第4周 - 4.4 多 Agent 协作")
    print("=" * 60)
    
    print("\n选择要查看的内容：")
    print("1. 多 Agent 协作模式")
    print("2. 主流框架对比")
    print("3. AutoGen 代码示例")
    print("4. CrewAI 代码示例")
    print("5. 运行简单多 Agent 演示（需要 API Key）")
    print("6. 个人助手项目架构")
    
    choice = input("\n请输入选项（1-6）：").strip()
    
    if choice == "1":
        print(__doc__)
        print("\n" + "=" * 60)
        print("请查看源代码中 '第2部分：多 Agent 协作模式' 的注释")
    elif choice == "2":
        print("\n请查看源代码中 '第3部分：主流多 Agent 框架' 的注释")
    elif choice == "3":
        print("\nAutoGen 代码示例：")
        print("-" * 60)
        print(AUTOGEN_EXAMPLE)
    elif choice == "4":
        print("\nCrewAI 代码示例：")
        print("-" * 60)
        print(CREWAI_EXAMPLE)
    elif choice == "5":
        if os.getenv("DEEPSEEK_API_KEY"):
            demo_simple_multi_agent()
        else:
            print("\n⚠️ 请先设置 DEEPSEEK_API_KEY 环境变量")
    elif choice == "6":
        print("\n请查看源代码中 '第7部分：个人助手项目架构' 的注释")
    else:
        print("无效选项")


if __name__ == "__main__":
    main()


# ============================================================
# 学习总结
# ============================================================
"""
📝 本节重点：

1. 为什么需要多 Agent？
   - 单 Agent 处理复杂任务效率低
   - 多 Agent 分工协作，类似团队
   
2. 多 Agent 协作模式：
   - 顺序模式：A → B → C
   - 层级模式：Manager → Workers
   - 对话模式：互相讨论、迭代
   - 投票模式：多个独立意见，共识决策

3. 主流框架：
   - AutoGen（微软）：代码执行、人类介入
   - CrewAI：角色扮演、团队协作
   - LangGraph：图工作流、精细控制

4. 个人助手架构：
   - 用户界面层
   - 协调器层
   - Agent 层
   - 工具/API 层

5. 建议学习路径：
   - 先理解概念和模式
   - 选一个框架深入学习（推荐 CrewAI 入门）
   - 从简单项目开始实践

下一步：第5周 低代码平台 + Web 开发
- Dify 平台实战
- FastAPI 基础
- 简单前端
"""
