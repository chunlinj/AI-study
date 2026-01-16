# 1.2 开发环境搭建

## 1. 虚拟环境（你已经有了！）

### 什么是虚拟环境？

虚拟环境是一个**隔离的 Python 环境**，每个项目可以有自己独立的依赖包，互不干扰。

类比 Java：就像每个项目有自己的 `pom.xml` 或 `build.gradle`，依赖不会冲突。

### 你当前的环境

```
AI-study/
├── .venv/              ← 虚拟环境目录
│   ├── Scripts/        ← Windows 下的可执行文件
│   │   ├── python.exe
│   │   └── pip.exe
│   └── Lib/
│       └── site-packages/  ← 安装的包都在这里
├── lessons/
└── ...
```

### 常用命令

```powershell
# 创建虚拟环境（你已经做过了）
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\Activate.ps1   # PowerShell
.venv\Scripts\activate.bat   # CMD

# 查看已安装的包
pip list

# 安装包
pip install numpy

# 导出依赖（类似 package.json）
pip freeze > requirements.txt

# 从 requirements.txt 安装所有依赖
pip install -r requirements.txt
```

---

## 2. Anaconda vs venv

| 特性 | venv | Anaconda |
|------|------|----------|
| 轻量级 | ✅ 只有 Python | ❌ 包含大量科学计算包 |
| 安装大小 | ~20MB | ~3GB |
| 包管理 | pip | conda（更强大） |
| 适合场景 | 一般开发 | 数据科学、机器学习 |

**建议**：你已经用 venv，继续用就行。需要什么包就 `pip install`。

---

## 3. Kiro + Python 配置

你已经在用 Kiro 了！确保：

1. **Python 解释器选择正确**
   - 按 `Ctrl+Shift+P` → 输入 "Python: Select Interpreter"
   - 选择 `.venv` 里的 Python

2. **已安装的扩展**
   - Python（语法高亮、调试）
   - Pylance（智能提示）

---

## 4. Jupyter Notebook

Jupyter 是交互式编程环境，适合数据探索和学习。

### 安装

```powershell
pip install jupyter
```

### 启动

```powershell
jupyter notebook
```

会在浏览器打开一个网页，可以逐行运行代码。

### 在 Kiro 中使用

Kiro 也支持 `.ipynb` 文件，可以直接在编辑器里运行 Notebook。

---

## 5. 你的环境检查清单

运行以下命令确认环境正常：

```powershell
# 检查 Python 版本
python --version

# 检查 pip
pip --version

# 检查已安装的 AI 相关包
pip list | findstr "numpy torch transformers"
```

---

## 练习

1. 运行 `pip freeze > requirements.txt` 导出当前依赖
2. 安装 Jupyter：`pip install jupyter`
3. 启动 Jupyter Notebook，创建一个新的 notebook，运行 `print("Hello AI")`
