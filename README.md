# Agentic Chat App

A full-stack agentic conversation application forked from [agent-chat-ui](https://github.com/langchain-ai/agent-chat-ui), featuring advanced AI agent interactions with human-in-the-loop capabilities, task planning, and parallel tool execution.

## 🚀 Tech Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **Framer Motion** - Animation library
- **React Markdown** - Markdown rendering with KaTeX support

### Backend
- **LangGraph** - Multi-agent workflow orchestration
- **LangChain** - LLM integration framework
- **Python 3.11+** - Backend runtime
- **Tavily** - Web search capabilities
- **OpenAI/Anthropic** - LLM providers

## ✨ Key Features

### 🤝 Human-in-the-Loop (HITL)
- **Interactive Interrupts**: Agents can request human approval before executing critical actions
- **Real-time Review**: Review, edit, approve, or reject agent tool calls
- **Flexible Controls**: Configure interrupt behavior per tool with granular permissions

### 📋 Todo Planning & Task Management
- **Intelligent Planning**: Agents create structured todo lists for complex tasks
- **Status Tracking**: Real-time progress updates (pending → in-progress → completed)
- **Dynamic Updates**: Modify plans as tasks evolve

### 🔧 Advanced Tool Execution
- **Parallel Tool Calls**: Execute multiple tools simultaneously for efficiency
- **Tool Call UI**: Rich interface displaying tool parameters and results
- **Dual-Pane Layout**: Side-by-side view of conversation and tool execution details

### 🎨 Rich UI Components
- **Artifact Rendering**: Display generated content in dedicated panels
- **Syntax Highlighting**: Code blocks with language-specific highlighting
- **Responsive Design**: Optimized for desktop and mobile devices
- **Dark/Light Themes**: User preference support

## 🛠️ Quick Start

### Prerequisites
- Node.js 18+ and pnpm
- Python 3.11+
- API keys for LLM providers (OpenAI/Anthropic)
- Tavily API key for web search

### Clone Repository

```bash
git clone https://github.com/1nFrastr/agentic-chat-app.git
cd agentic-chat-app
```

### Frontend Setup

1. **Install dependencies:**
```bash
pnpm install
```

2. **Start development server:**
```bash
pnpm dev
```

The frontend will be available at `http://localhost:3000`.

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Install dependencies with uv:**
```bash
uv sync
```

3. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `backend/.env` with your API keys:
```bash
# LLM Provider (openai or anthropic)
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic Configuration (if using anthropic)
ANTHROPIC_API_KEY=your_anthropic_key
ANTHROPIC_MODEL=claude-3-5-haiku-20241022
ANTHROPIC_BASE_URL=https://api.anthropic.com

# Tavily for web search
TAVILY_API_KEY=your_tavily_key
```

4. **Start LangGraph server:**
```bash
uv run langgraph dev
```

The backend will be available at `http://localhost:2024`