# L5: Instruction Tuning and Guardrails

In this lesson, you'll take everything you've learned from previous lessons and add advanced control mechanisms that transform your agents from helpful assistants into specialized, production-ready systems.

### Building on previous lessons

So far in this course, you've built:

- **Lesson 1**: Basic agents with Google search capabilities
- **Lesson 2**: Session, State & Memory in agents
- **Lesson 3**: Interactive chat agents with financial data integration (`get_financial_context`)
- **Lesson 4**: Coordinator agents with file persistence (`save_news_to_markdown`) and structured workflows

### What's new in Lesson 5

Now you'll add another piece: **programmatic control systems** to ensure your agents behave reliably in production environments:

- **Callback Systems**: Programmatic guardrails that automatically enforce policies
  1. **Domain Filtering**: Before Tool callback that blocks certain sources thus controlling information access
  2. **Response Enhancement**: After Tool callback that adds transparency and audit trails into agent outputs
- **Update agent's instructions**: We'll update the agent's instructions to make it callback-aware.

## By the end of this lesson, you'll have a production-ready agent that uses all the tools from previous lessons but with effective control mechanisms.

## 5.1 Setting up your development environment

Before you dive into building production-ready agents with advanced control mechanisms, let's set up a new folder structure with ADK's built-in project scaffolding using the `adk create` command.

You'll continue to use the gemini-2.0-flash-live model and the Google Gemini API Key.

```bash
adk create --type=code app_08 --model gemini-2.5-flash --api_key $GEMINI_API_KEY
# First we create our expected agent folder
# You can explore available option: !adk create --help
```

For more details go to take a look at `Lesson_5.ipynb`

## 5.3 Callbacks

Now you'll implement the core of this lesson: **callback-based control mechanisms**. Callbacks are Python functions that run at specific checkpoints in an agent's lifecycle, providing programmatic control over behavior.

### Understanding ADK Callback types

ADK provides several callback points:

- **before_agent_callback**: Runs before agent execution starts
- **after_agent_callback**: Runs after agent execution completes
- **before_tool_callback**: Runs before any tool is executed
- **after_tool_callback**: Runs after any tool completes
- **before_model_callback**: Runs before LLM calls
- **after_model_callback**: Runs after LLM responses

### Callback 1: Source filtering Callback (Before Tool Callback)

This callback demonstrates **programmatic policy enforcement**. It automatically blocks search queries that require the agent to fetch news from certain sources.

#### How It Works:

1. **Interception**: Runs before every `google_search` tool call
2. **Query analysis**: Examines the search query for blocked domains
3. **Policy enforcement**: Blocks searches targeting certain sources like Wikipedia, Reddit, Medium
4. **Error response**: Returns structured error messages when domains are blocked
5. **Transparency**: Logs allowed/blocked decisions for debugging

Note how the error messages are descriptive!

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

````

运行下面指令打印md文件内容：

```bash
adk run '/Users/carl/Downloads/adk-learning/app_07'
```

应该能顺利生成 ai_research_report.md 文件了！
````
