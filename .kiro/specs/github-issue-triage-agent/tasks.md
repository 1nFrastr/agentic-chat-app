# Implementation Plan - GitHub Issue 自动分诊 Agent

- [x] 1. 创建项目基础结构和配置





  - 创建 `backend/src/issue_agent` 目录结构
  - 创建 `__init__.py` 文件
  - 设置模块导出和包结构
  - _Requirements: 7.1, 7.2, 7.3, 7.6_

- [x] 2. 实现数据模型和类型定义





  - 创建 `backend/src/issue_agent/models.py` 文件
  - 定义 `IssueData` TypedDict（包含 title, body, number, author, labels, created_at 字段）
  - 定义 `TriageResult` TypedDict（包含 issue_number, category, assigned_to, confidence, reasoning 字段）
  - 添加完整的类型注解和文档字符串
  - _Requirements: 1.1, 1.2, 6.1_

- [x] 3. 实现配置管理模块





  - 创建 `backend/src/issue_agent/config.py` 文件
  - 实现 `TriageConfig` 类，包含 categories 列表、assignments 字典、default_assignee 属性
  - 定义 `DEVELOPER_ASSIGNMENT` 字典（Bug->张三, Feature Request->李四, Question->王五）
  - 实现 `add_category(category, assignee)` 方法支持动态添加分类
  - 实现 `get_assignee(category)` 方法获取分配人
  - 创建全局配置实例 `config`
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 7.1, 7.4_

- [x] 4. 实现 Issue 读取工具






  - 创建 `backend/src/issue_agent/tools.py` 文件
  - 实现 `read_issue_content` 工具函数（使用 @tool 装饰器）
  - 添加详细的工具描述和参数说明（包含 Example）
  - 实现输入验证（检查 issue_data 是否为字典，检查必需字段 title 和 body）
  - 实现文本格式化逻辑（格式：Title: ...\n\nBody: ...）
  - 添加错误处理（缺失字段返回错误信息，空值使用 "N/A"）
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 5.1, 5.2, 5.3, 5.4_

- [x] 5. 实现 Issue 分类工具




  - 在 `tools.py` 中设计分类 Prompt（包含 Bug、Feature Request、Question 的明确定义和特征）
  - 实现 `categorize_issue` 工具函数（使用 @tool 装饰器）
  - 添加详细的工具描述，说明分类标准和返回格式
  - 集成 LLM 调用逻辑（从环境变量读取 API 密钥，支持 OpenAI 和 Anthropic）
  - 实现分类结果验证（检查是否在 ["Bug", "Feature Request", "Question"] 中）
  - 添加错误处理（LLM 调用失败时返回错误信息，无效分类默认为 "Question"）
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 5.1, 5.2, 5.3, 5.4, 5.5_
-

- [x] 6. 实现开发者分配工具





  - 在 `tools.py` 中实现 `assign_developer` 工具函数（使用 @tool 装饰器）
  - 添加详细的工具描述，说明分配规则（Bug->张三, Feature Request->李四, Question->王五）
  - 从 config 模块导入并使用配置的分配规则
  - 实现默认分配人逻辑（未知分类返回 "项目负责人"）
  - 添加错误处理（空分类字符串返回错误信息）
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 5.1, 5.2, 5.3, 5.4_




- [x] 7. 实现主 Agent 逻辑






  - 创建 `backend/src/issue_agent/agent.py` 文件
  - 实现 LLM 模型创建函数（根据环境变量选择 OpenAI 或 Anthropic，优先使用 gpt-4o-mini）
  - 设计 Agent System Prompt（明确三步工作流程：read_issue_content -> categorize_issue -> assign_developer）
  - 使用 `create_react_agent` 创建 Agent，传入 model、tools 和 prompt
  - 配置工具列表（包含 read_issue_content, categorize_issue, assign_developer）
  - 实现 Agent 导出函数或变量供 main.py 使用
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.5_

- [x] 8. 创建主程序和示例数据






  - 创建 `backend/src/issue_agent/main.py` 文件
  - 定义三个示例 Issue 数据常量（SAMPLE_BUG_ISSUE, SAMPLE_FEATURE_ISSUE, SAMPLE_QUESTION_ISSUE）
  - 实现主函数，接收 Issue JSON 并调用 Agent
  - 实现结果格式化和打印逻辑（显示分类和分配人）
  - 添加 Agent 思考过程的输出展示（打印中间步骤）
  - 添加命令行参数支持（使用 argparse 选择不同示例：--type bug/feature/question）
  - 添加 if __name__ == "__main__" 入口
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 8.4_

- [ ] 9. 实现错误处理和日志记录
  - 在 `tools.py` 顶部定义自定义异常类（TriageError, InvalidIssueDataError, ClassificationError）
  - 在所有工具函数中添加 try-except 错误处理
  - 在 `agent.py` 中配置日志记录（使用 Python logging 模块，设置合适的日志级别）
  - 在 `categorize_issue` 中实现 LLM 调用失败的降级策略（返回友好错误信息）
  - 在 `agent.py` 中记录工具调用和 LLM 响应用于调试
  - _Requirements: 4.6, 6.6_

- [ ] 10. 编写 README 文档
  - 创建 `backend/README_ISSUE_AGENT.md` 文件
  - 编写项目概述和功能说明（介绍 Agent 的作用和工作原理）
  - 添加安装依赖的说明（使用 uv，依赖已在 pyproject.toml 中）
  - 添加环境变量配置说明（OPENAI_API_KEY 或 ANTHROPIC_API_KEY）
  - 添加运行示例的步骤（cd backend && python -m issue_agent.main --type bug）
  - 提供完整的三个 Issue JSON 示例（Bug、Feature Request、Question）
  - 说明设计思路（工具 Prompt/Description 设计的关键点）
  - 展示完整的 Agent 执行轨迹示例（包含思考过程和工具调用）
  - 说明如何扩展系统（添加新分类 Documentation 的完整步骤）
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7_

- [ ] 11. 集成测试和验证
  - 设置环境变量（OPENAI_API_KEY 或 ANTHROPIC_API_KEY）
  - 运行 `python -m issue_agent.main --type bug` 测试 Bug Issue 分诊
  - 验证 Bug Issue 的分诊结果（应分类为 "Bug"，分配给 "张三"）
  - 运行 `python -m issue_agent.main --type feature` 测试 Feature Request 分诊
  - 验证 Feature Request Issue 的分诊结果（应分类为 "Feature Request"，分配给 "李四"）
  - 运行 `python -m issue_agent.main --type question` 测试 Question 分诊
  - 验证 Question Issue 的分诊结果（应分类为 "Question"，分配给 "王五"）
  - 测试错误处理（手动修改示例数据删除必需字段，验证错误信息）
  - 验证 Agent 思考过程的输出清晰可读（包含工具调用和推理步骤）
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 6.3, 6.4, 6.5_

- [ ] 12. 可扩展性验证
  - 在 `config.py` 中添加新分类 "Documentation" 和分配规则（分配给 "赵六"）
  - 在 `tools.py` 的 `categorize_issue` Prompt 中添加 Documentation 分类描述和特征
  - 在 `main.py` 中添加 SAMPLE_DOCUMENTATION_ISSUE 示例数据
  - 在 `main.py` 的命令行参数中添加 --type documentation 选项
  - 运行 `python -m issue_agent.main --type documentation` 测试新分类
  - 验证新分类工作正常（应分类为 "Documentation"，分配给 "赵六"）
  - 确认无需修改核心 Agent 逻辑（agent.py 无需改动）
  - 在 README 中记录扩展过程（作为扩展示例）
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8.7_
