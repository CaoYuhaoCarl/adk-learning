In this lesson, you'll transform your agent from a conversational interface into a research coordinator that works behind the scenes. You'll learn to implement a **coordinator-dispatcher** pattern where the root agent delegates research work to background processes and saves structured reports for later use.

This architectural shift is crucial for building production AI systems that can handle complex workflows without overwhelming users with intermediate processing details.

**Key Learning Objectives:**

- Create coordinator agents that delegate work silently
- Build agents optimized for background processing
- Implement file persistence with structured markdown reports
- Understand when to use structured schemas vs. free-form output

**Note:** This lesson introduces patterns essential for multi-agent systems and production deployment.

## 4.3 The Coordinator-Dispatcher Architecture Pattern

In this lesson, you'll be implementing a sophisticated architectural pattern that separates user interaction from background processing. This pattern is essential for production AI systems.

### The Challenge: Information Overload

In previous lessons, your agent would research news and immediately read all findings to the user. This creates several problems:

- **Cognitive overload**: Users get overwhelmed with raw research data
- **Poor user experience**: Long delays while listening to unfiltered information
- **Inefficient workflows**: No separation between data gathering and content creation

### The Solution: Coordinator-Dispatcher Pattern

The coordinator-dispatcher pattern solves this by implementing a two-phase workflow:

1. **Coordination Phase**: Root agent acknowledges the request and coordinates background work
2. **Execution Phase**: Agent silently executes research, analysis, and file persistence

### Implementation Strategy

You'll add a save_news_to_markdown tool that:

- Takes research from google_search and get_financial_context
- Structures the data into a readable markdown report
- Saves results as ai_research_report.md
- Enables the root agent to work as a coordinator, not a presenter

This architectural shift prepares you for the podcast generation system you'll build in later lessons.

### Financial Context Tool: Reusing Existing Components

You'll start by implementing the same financial data tool from Lesson 2.

## 4.3 The Coordinator-Dispatcher Architecture Pattern

In this lesson, you'll be implementing a sophisticated architectural pattern that separates user interaction from background processing. This pattern is essential for production AI systems.

### The Challenge: Information Overload

In previous lessons, your agent would research news and immediately read all findings to the user. This creates several problems:

- **Cognitive overload**: Users get overwhelmed with raw research data
- **Poor user experience**: Long delays while listening to unfiltered information
- **Inefficient workflows**: No separation between data gathering and content creation

### The Solution: Coordinator-Dispatcher Pattern

The coordinator-dispatcher pattern solves this by implementing a two-phase workflow:

1. **Coordination Phase**: Root agent acknowledges the request and coordinates background work
2. **Execution Phase**: Agent silently executes research, analysis, and file persistence

### Implementation Strategy

You'll add a save_news_to_markdown tool that:

- Takes research from google_search and get_financial_context
- Structures the data into a readable markdown report
- Saves results as ai_research_report.md
- Enables the root agent to work as a coordinator, not a presenter

This architectural shift prepares you for the podcast generation system you'll build in later lessons.

### Financial Context Tool: Reusing Existing Components

You'll start by implementing the same financial data tool from Lesson 2.

---

Attention when building agents with ADK:

1. **记得导入 `pathlib` 模块**：如果在工具函数中使用 `pathlib.Path.cwd()` 来获取当前路径并保存文件，必须在文件顶部加上 `import pathlib`。否则运行时会抛出 `NameError`，但大模型可能不会报错，而是直接回复"文件已保存"（幻觉），导致难以排查。

2. **使用 `AgentTool` 包装子 Agent 时，必须为每个子 Agent 添加 `description` 字段**：ADK 框架的 `AgentTool` 在调用子 Agent 时，要求根模型传入一个名为 `request` 的参数。如果子 Agent 没有 `description`，根模型不知道这个约定，就不会传 `request`，导致运行时 `KeyError: 'request'`。`description` 需要清晰说明子 Agent 的功能，以及 `request` 参数应该传什么内容。示例：

   ```python
   search_agent = Agent(
       name="news_searcher",
       description="搜索最新 AI 新闻。request 参数为搜索指令，例如：'搜索关于美国上市公司的最新 AI 新闻'。",
       instruction="...",
       tools=[google_search],
   )
   ```

运行下面指令打印md文件内容：

```bash
adk run '/Users/carl/Downloads/adk-learning/app_07'
```

应该能顺利生成 ai_research_report.md 文件了！
