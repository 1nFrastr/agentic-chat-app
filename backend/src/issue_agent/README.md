# Issue Agent - GitHub Issue 分诊系统

这是一个基于 LangGraph 的智能 Issue 分诊系统,能够自动分析 GitHub Issue 并进行分类和分配。

## 功能特性

- 📖 **Issue 内容读取**: 自动提取和格式化 Issue 标题和正文
- 🏷️ **智能分类**: 使用 LLM 将 Issue 分类为 Bug、Feature Request 或 Question
- 👥 **自动分配**: 根据分类规则自动分配给对应的开发者

## Issue 示例数据 (JSON 格式)

### 示例 1: Bug 类型

```json
{
  "title": "Bug: App crashes on startup",
  "body": "当我点击启动按钮时,应用立即崩溃。\n\n复现步骤:\n1. 打开应用\n2. 点击 \"Start\" 按钮\n3. 应用崩溃并显示错误信息\n\n错误信息:\n```\nNullPointerException at line 42 in MainActivity.java\n```\n\n环境信息:\n- OS: Windows 10\n- App Version: 2.3.1\n- 浏览器: Chrome 120",
  "number": 101,
  "author": "user123",
  "labels": []
}
```

**预期分类**: Bug  
**预期分配**: 张三

---

### 示例 2: Feature Request 类型

```json
{
  "title": "Feature Request: Add dark mode support",
  "body": "希望能添加暗色模式支持。\n\n建议内容:\n- 在设置中添加主题切换选项\n- 支持跟随系统主题自动切换\n- 保存用户的主题偏好设置\n\n使用场景:\n很多用户在夜间使用应用时,希望有深色主题来保护眼睛,减少屏幕亮度对眼睛的刺激。\n\n参考:\n许多流行应用(如 Twitter, GitHub)都已经支持暗色模式。",
  "number": 102,
  "author": "designer456",
  "labels": ["enhancement"]
}
```

**预期分类**: Feature Request  
**预期分配**: 李四

---

### 示例 3: Question 类型

```json
{
  "title": "How to configure API endpoints?",
  "body": "我不太理解如何配置自定义的 API 端点。\n\n问题:\n1. 在哪个配置文件中设置 API URL?\n2. 是否需要重启应用才能生效?\n3. 支持哪些环境变量?\n\n我查看了文档,但没有找到相关说明。能否提供一些示例配置?\n\n谢谢!",
  "number": 103,
  "author": "newbie789",
  "labels": ["question"]
}
```

**预期分类**: Question  
**预期分配**: 王五

---

### 示例 4: Bug 类型 (内存泄漏)

```json
{
  "title": "Memory leak in background service",
  "body": "发现后台服务存在内存泄漏问题。\n\n症状:\n- 应用长时间运行后内存占用持续增长\n- 最终导致 OOM (Out of Memory) 错误\n- 重启后暂时恢复正常\n\n性能数据:\n- 初始内存: 150MB\n- 运行 1 小时后: 450MB\n- 运行 3 小时后: 1.2GB\n- 运行 6 小时后: 崩溃\n\n环境:\n- Android 12\n- 设备: Samsung Galaxy S21\n- App Version: 3.0.2",
  "number": 104,
  "author": "qa_team",
  "labels": ["bug", "performance", "critical"]
}
```

**预期分类**: Bug  
**预期分配**: 张三

---

### 示例 5: Feature Request 类型 (UX 改进)

```json
{
  "title": "Improve loading animation and user feedback",
  "body": "当前的加载动画不够明显,建议改进用户反馈体验。\n\n改进建议:\n1. 更新加载动画为骨架屏(Skeleton Screen)\n2. 添加操作成功/失败的 Toast 提示\n3. 增加进度条显示长时间操作的进度\n4. 添加空状态插图和友好提示文案\n\n设计参考:\n可以参考 Material Design 3 的加载模式和反馈组件。",
  "number": 105,
  "author": "ux_designer",
  "labels": ["enhancement", "ui/ux"]
}
```

**预期分类**: Feature Request  
**预期分配**: 李四

---

### 示例 6: Question 类型 (认证问题)

```json
{
  "title": "Authentication token expiration behavior?",
  "body": "请问关于认证令牌过期的处理机制是怎样的?\n\n具体问题:\n1. Token 的默认过期时间是多久?\n2. 过期后会自动刷新还是需要重新登录?\n3. 如何检测 Token 即将过期?\n4. Refresh Token 的有效期是多久?\n\n使用场景:\n我们正在集成你们的 API,需要了解如何妥善处理认证相关的边界情况。",
  "number": 106,
  "author": "backend_dev",
  "labels": ["question", "api", "documentation"]
}
```

**预期分类**: Question  
**预期分配**: 王五

---

### 示例 7: Bug 类型 (数据库连接)

```json
{
  "title": "Error: Cannot connect to database",
  "body": "应用无法连接到数据库,显示连接超时错误。\n\n错误堆栈:\n```\nTimeoutError: Connection timeout after 30000ms\n  at DatabaseConnection.connect (db.js:45)\n```\n\n环境:\n- Node.js: v18.17.0\n- Database: PostgreSQL 15\n- OS: Ubuntu 22.04",
  "number": 107,
  "author": "devops_team",
  "labels": ["bug", "database"]
}
```

**预期分类**: Bug  
**预期分配**: 张三

---

### 示例 8: Feature Request 类型 (导出功能)

```json
{
  "title": "Add export to PDF functionality",
  "body": "希望添加导出为 PDF 的功能。\n\n功能需求:\n- 支持导出当前报表为 PDF 格式\n- 保持原有样式和布局\n- 支持自定义页眉页脚\n- 支持添加水印\n\n业务价值:\n许多企业客户需要将报表打印或存档,PDF 是最常用的格式。",
  "number": 108,
  "author": "product_manager",
  "labels": ["enhancement", "export"]
}
```

**预期分类**: Feature Request  
**预期分配**: 李四

---

## 使用方法

### 基本用法

```python
from src.issue_agent.tools import read_issue_content, categorize_issue, assign_developer

# 1. 读取 Issue 内容
issue_content = read_issue_content(bug_issue)
print(issue_content)

# 2. 分类 Issue
category = categorize_issue(issue_content)
print(f"分类: {category}")

# 3. 分配开发者
developer = assign_developer(category)
print(f"分配给: {developer}")
```

### 使用 Agent 进行完整流程

```python
from src.issue_agent.agent import create_graph

# 创建 Agent 图
graph = create_graph()

# 处理 Issue
result = graph.invoke({
    "issue_data": bug_issue,
    "issue_content": "",
    "category": "",
    "assignee": ""
})

print(f"最终结果: {result}")
```

## 分配规则

| Issue 类型 | 负责人 | 职责 |
|-----------|--------|------|
| Bug | 张三 | Bug 修复和问题排查 |
| Feature Request | 李四 | 新功能开发和产品增强 |
| Question | 王五 | 技术支持和用户帮助 |
| 未知类型 | 项目负责人 | 默认分配和初步分流 |

## 测试所有示例

```python
# 测试脚本
test_issues = [
    ("Bug Issue", bug_issue),
    ("Feature Request", feature_request_issue),
    ("Question Issue", question_issue),
    ("Complex Bug", complex_bug_issue),
    ("UX Improvement", ux_improvement_issue),
    ("API Question", api_question_issue),
]

for name, issue in test_issues:
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print(f"{'='*60}")
    
    # 完整流程
    content = read_issue_content(issue)
    category = categorize_issue(content)
    developer = assign_developer(category)
    
    print(f"标题: {issue['title']}")
    print(f"分类: {category}")
    print(f"分配: {developer}")
```

## 配置说明

系统支持通过环境变量配置:

- `OPENAI_API_KEY`: OpenAI API 密钥 (优先使用)
- `ANTHROPIC_API_KEY`: Anthropic API 密钥 (备用)

分类模型:
- OpenAI: `gpt-4o-mini`
- Anthropic: `claude-3-5-sonnet-20241022`

## 项目结构

```
issue_agent/
├── __init__.py          # 包初始化
├── agent.py             # LangGraph Agent 定义
├── config.py            # 配置管理
├── main.py              # 主入口
├── models.py            # 数据模型
├── tools.py             # 工具函数
└── README.md            # 本文件
```

## 许可证

请参考项目根目录的 LICENSE 文件。
