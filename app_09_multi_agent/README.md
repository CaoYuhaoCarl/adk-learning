# L6 Multi-agent orchestration

In this lesson you'll learn production-grade multi-agent patterns where you'll refactor your system into a three-tier architecture with proper separation of concerns.

### Building on previous lessons

So far in this course, you've built:

- **Lesson 1**: Basic agents with Google search capabilities
- **Lesson 2**: Session, State & Memory in agents
- **Lesson 3**: Interactive chat agents with financial data integration (get_financial_context)
- **Lesson 4**: Coordinator agents with file persistence (save_news_to_markdown) and structured workflows
- **Lesson 5**: Programmatic control systems to ensure your agents behave reliably in production environments

### What's new in Lesson 6

Now you'll add the final piece- a scalable foundation for complex applications by building:

- A two-person podcast that relays the latest news based upon the requirements given to our agent.

## 6.1 Setting up your development environment

Before you dive into building production-ready agents with advanced control mechanisms, let's set up a new folder structure with ADK's built-in project scaffolding using the `adk create` command.

You'll continue to use the gemini-2.0-flash-live model and the Google Gemini API Key.
