# Agentic Chat App

[English](README.md) | 简体中文

一个全栈智能对话应用，fork 自 [agent-chat-ui](https://github.com/langchain-ai/agent-chat-ui)，具有高级 AI 智能体交互、人机协同、任务规划和并行工具执行等功能。

## 🚀 技术栈

### 前端
- **Next.js 15** - React 框架，使用 App Router
- **TypeScript** - 类型安全开发
- **Tailwind CSS** - 实用优先的样式框架
- **Radix UI** - 无障碍组件原语
- **Framer Motion** - 动画库
- **React Markdown** - Markdown 渲染，支持 KaTeX

### 后端
- **LangGraph** - 多智能体工作流编排
- **LangChain** - LLM 集成框架
- **Python 3.11+** - 后端运行时
- **Tavily** - 网络搜索能力
- **OpenAI/Anthropic** - LLM 提供商

## ✨ 核心特性

### 🤝 人机协同 (HITL)
- **交互式中断**：智能体在执行关键操作前可请求人工批准
- **实时审查**：审查、编辑、批准或拒绝智能体的工具调用
- **灵活控制**：为每个工具配置细粒度的中断行为和权限

### 📋 待办事项规划与任务管理
- **智能规划**：智能体为复杂任务创建结构化待办事项列表
- **状态跟踪**：实时进度更新（待处理 → 进行中 → 已完成）
- **动态更新**：随着任务演进动态修改计划

### 🔧 高级工具执行
- **并行工具调用**：同时执行多个工具以提高效率
- **工具调用界面**：丰富的界面显示工具参数和结果
- **双面板布局**：对话和工具执行详情并排显示

### 🎨 丰富的 UI 组件
- **Artifact 渲染**：在专用面板中显示生成的内容
- **语法高亮**：支持特定语言的代码块高亮
- **响应式设计**：针对桌面和移动设备优化
- **深色/浅色主题**：支持用户偏好设置

## 🛠️ 快速开始

### 前置要求
- Node.js 18+ 和 pnpm
- Python 3.11+
- LLM 提供商的 API 密钥（OpenAI/Anthropic）
- Tavily API 密钥用于网络搜索

### 克隆仓库

```bash
git clone https://github.com/1nFrastr/agentic-chat-app.git
cd agentic-chat-app
```

### 前端设置

1. **安装依赖：**
```bash
pnpm install
```

2. **启动开发服务器：**
```bash
pnpm dev
```

前端将在 `http://localhost:3000` 上运行。

### 后端设置

1. **进入后端目录：**
```bash
cd backend
```

2. **使用 uv 安装依赖：**
```bash
uv sync
```

3. **配置环境变量：**
```bash
cp .env.example .env
```

编辑 `backend/.env` 文件，填入你的 API 密钥：
```bash
# LLM 提供商 (openai 或 anthropic)
LLM_PROVIDER=openai

# OpenAI 配置
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic 配置（如果使用 anthropic）
ANTHROPIC_API_KEY=your_anthropic_key
ANTHROPIC_MODEL=claude-3-5-haiku-20241022
ANTHROPIC_BASE_URL=https://api.anthropic.com

# Tavily 网络搜索
TAVILY_API_KEY=your_tavily_key
```

4. **启动 LangGraph 服务器：**
```bash
uv run langgraph dev
```

后端将在 `http://localhost:2024` 上运行
