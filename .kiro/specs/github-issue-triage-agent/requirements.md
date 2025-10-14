# Requirements Document

## Introduction

本项目旨在构建一个自动化的 GitHub Issue 分诊（Triage）Agent，用于自动分类、打标签并分配 Issue 给合适的开发者。该 Agent 将使用 LangChain 框架和 LLM 技术，通过定义的工具函数自主完成 Issue 分析和分配任务，从而减少人工处理的时间成本。

## Requirements

### Requirement 1: Issue 内容读取

**User Story:** 作为一个 Issue 分诊系统，我需要能够读取和解析 Issue 数据，以便后续进行分类和分配。

#### Acceptance Criteria

1. WHEN 系统接收到一个 Issue JSON 对象 THEN 系统 SHALL 能够提取 Issue 的标题（title）字段
2. WHEN 系统接收到一个 Issue JSON 对象 THEN 系统 SHALL 能够提取 Issue 的描述正文（body）字段
3. WHEN Issue JSON 对象缺少必要字段 THEN 系统 SHALL 返回错误信息
4. WHEN 提取完成 THEN 系统 SHALL 返回格式化的文本内容供后续分析使用

### Requirement 2: Issue 智能分类

**User Story:** 作为一个 Issue 分诊系统，我需要能够自动将 Issue 分类为不同类型，以便快速识别 Issue 的性质。

#### Acceptance Criteria

1. WHEN 系统接收到 Issue 文本内容 THEN 系统 SHALL 调用 LLM 进行内容分析
2. WHEN LLM 分析完成 THEN 系统 SHALL 将 Issue 分类为 "Bug"、"Feature Request" 或 "Question" 中的一种
3. WHEN Issue 内容包含错误报告、异常堆栈或问题描述 THEN 系统 SHALL 倾向于分类为 "Bug"
4. WHEN Issue 内容包含新功能建议或改进请求 THEN 系统 SHALL 倾向于分类为 "Feature Request"
5. WHEN Issue 内容是询问使用方法或寻求帮助 THEN 系统 SHALL 倾向于分类为 "Question"
6. WHEN 分类完成 THEN 系统 SHALL 返回明确的分类结果字符串

### Requirement 3: 开发者自动分配

**User Story:** 作为一个 Issue 分诊系统，我需要能够根据 Issue 类型自动分配给合适的开发者，以便快速响应和处理。

#### Acceptance Criteria

1. WHEN 系统接收到 Issue 分类结果 THEN 系统 SHALL 根据预设的分配规则查找对应的开发者
2. WHEN 分类为 "Bug" THEN 系统 SHALL 分配给负责 Bug 修复的开发者
3. WHEN 分类为 "Feature Request" THEN 系统 SHALL 分配给负责新功能开发的开发者
4. WHEN 分类为 "Question" THEN 系统 SHALL 分配给负责技术支持的开发者
5. WHEN 分类结果在分配规则中不存在 THEN 系统 SHALL 返回默认分配人或错误提示
6. WHEN 分配完成 THEN 系统 SHALL 返回被分配开发者的名称

### Requirement 4: Agent 自主执行

**User Story:** 作为一个 Issue 分诊系统，我需要 Agent 能够自主思考并调用工具完成整个分诊流程，以便实现端到端的自动化。

#### Acceptance Criteria

1. WHEN Agent 接收到 Issue JSON 数据 THEN Agent SHALL 自主决定调用哪些工具以及调用顺序
2. WHEN Agent 执行过程中 THEN Agent SHALL 记录每一步的思考过程（Thought Process）
3. WHEN Agent 调用工具 THEN Agent SHALL 能够根据工具返回结果决定下一步行动
4. WHEN 所有必要工具都已调用 THEN Agent SHALL 生成最终的分诊结论
5. WHEN Agent 执行完成 THEN Agent SHALL 输出包含分类和分配人的完整结果
6. IF Agent 执行过程中遇到错误 THEN Agent SHALL 能够处理异常并给出合理的反馈

### Requirement 5: 工具定义与描述

**User Story:** 作为一个 Agent 系统，我需要清晰准确的工具描述，以便 LLM 能够正确理解和调用这些工具。

#### Acceptance Criteria

1. WHEN 定义工具函数 THEN 每个工具 SHALL 包含清晰的函数名称
2. WHEN 定义工具函数 THEN 每个工具 SHALL 包含详细的功能描述（description）
3. WHEN 定义工具函数 THEN 每个工具 SHALL 明确定义输入参数的类型和含义
4. WHEN 定义工具函数 THEN 每个工具 SHALL 明确定义返回值的类型和格式
5. WHEN LLM 读取工具描述 THEN 描述 SHALL 足够清晰以便 LLM 理解工具的用途和使用场景
6. WHEN 工具描述编写完成 THEN 描述 SHALL 包含使用示例或场景说明

### Requirement 6: 主程序执行与输出

**User Story:** 作为系统用户，我需要一个简单的主程序来运行 Agent 并查看结果，以便验证系统功能。

#### Acceptance Criteria

1. WHEN 用户运行主程序 THEN 程序 SHALL 接收一个模拟的 Issue JSON 对象作为输入
2. WHEN 主程序启动 THEN 程序 SHALL 初始化 Agent 并传入必要的工具
3. WHEN Agent 执行 THEN 程序 SHALL 实时打印 Agent 的思考过程
4. WHEN Agent 完成执行 THEN 程序 SHALL 打印最终的分诊结果（分类和分配人）
5. WHEN 程序执行完成 THEN 输出 SHALL 格式清晰、易于阅读
6. IF 执行过程中出现错误 THEN 程序 SHALL 捕获异常并输出错误信息

### Requirement 7: 系统可扩展性

**User Story:** 作为系统维护者，我需要系统具有良好的可扩展性，以便未来添加新的分类或功能。

#### Acceptance Criteria

1. WHEN 需要添加新的 Issue 分类（如 "Documentation"）THEN 系统 SHALL 只需修改分类逻辑和分配规则
2. WHEN 添加新分类 THEN 工具函数的核心逻辑 SHALL 不需要大幅修改
3. WHEN 需要添加新的工具 THEN 系统 SHALL 支持通过配置或简单代码添加
4. WHEN 修改开发者分配规则 THEN 系统 SHALL 支持通过配置文件或字典修改
5. WHEN 系统扩展 THEN 现有功能 SHALL 不受影响
6. WHEN 代码组织 THEN 系统 SHALL 采用模块化设计，工具、Agent 和主程序分离

### Requirement 8: 文档与示例

**User Story:** 作为系统用户或开发者，我需要完整的文档和示例，以便快速理解和使用系统。

#### Acceptance Criteria

1. WHEN 项目交付 THEN 项目 SHALL 包含 README.md 文件
2. WHEN 阅读 README THEN 文档 SHALL 包含安装依赖的说明
3. WHEN 阅读 README THEN 文档 SHALL 包含运行程序的步骤
4. WHEN 阅读 README THEN 文档 SHALL 提供至少一个完整的 Issue JSON 示例
5. WHEN 阅读 README THEN 文档 SHALL 包含设计思路说明，解释工具的 Prompt/Description 设计
6. WHEN 阅读 README THEN 文档 SHALL 展示一次完整的 Agent 执行轨迹示例
7. WHEN 阅读 README THEN 文档 SHALL 说明如何扩展系统（如添加新分类）
