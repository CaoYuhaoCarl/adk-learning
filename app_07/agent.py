
from typing import Dict, List
import pathlib
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
import yfinance as yf

def get_financial_context(tickers: List[str]) -> Dict[str, str]:
    """
    Fetches the current stock price and daily change for a list of stock tickers
    using the yfinance library.

    Args:
        tickers: A list of stock market tickers (e.g., ["GOOG", "NVDA"]).

    Returns:
        A dictionary mapping each ticker to its formatted financial data string.
    """
    financial_data: Dict[str, str] = {}
    for ticker_symbol in tickers:
        try:
            # Create a Ticker object
            stock = yf.Ticker(ticker_symbol)

            # Fetch the info dictionary
            info = stock.info

            # Safely access the required data points
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            change_percent = info.get("regularMarketChangePercent")

            if price is not None and change_percent is not None:
                # Format the percentage and the final string
                change_str = f"{change_percent * 100:+.2f}%"
                financial_data[ticker_symbol] = f"${price:.2f} ({change_str})"
            else:
                # Handle cases where the ticker is valid but data is missing
                financial_data[ticker_symbol] = "Price data not available."

        except Exception:
            # This handles invalid tickers or other yfinance errors gracefully
            financial_data[ticker_symbol] = "Invalid Ticker or Data Error"

    return financial_data

def save_news_to_markdown(filename: str, content: str) -> Dict[str, str]:
    """
    Saves the given content to a Markdown file in the current directory.

    Args:
        filename: The name of the file to save (e.g., 'ai_news.md').
        content: The Markdown-formatted string to write to the file.

    Returns:
        A dictionary with the status of the operation.
    """
    try:
        if not filename.endswith(".md"):
            filename += ".md"
        current_directory = pathlib.Path.cwd()
        file_path = current_directory / filename
        file_path.write_text(content, encoding="utf-8")
        return {
            "status": "success",
            "message": f"Successfully saved news to {file_path.resolve()}",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save file: {str(e)}"}

# 搜索新闻的 agent
search_agent = Agent(
    name="news_searcher",
    model="gemini-2.5-flash",
    description="搜索关于美国上市公司的最新 AI 新闻。request 参数为搜索请求，例如：'搜索最新的 AI 新闻，提取公司名称和股票代码'。",
    instruction="你是一个新闻搜索专家，负责使用 google_search 工具查找关于美国上市公司的最新 AI 新闻，并根据新闻提取出提到的公司及股票代码。",
    tools=[google_search],
)

# 获取股票价格的 agent
finance_agent = Agent(
    name="finance_analyst",
    model="gemini-2.5-flash",
    description="获取指定股票代码的最新价格和涨跌幅数据。request 参数为股票代码列表，例如：'获取 NVDA, GOOGL, MSFT 的股价数据'。",
    instruction="你是一个金融分析师，负责调用 get_financial_context 工具获取特定股票代码的最新价格和涨跌幅行情。",
    tools=[get_financial_context],
)

# 保存文档的 agent
writer_agent = Agent(
    name="report_writer",
    model="gemini-2.5-flash",
    description="将报告内容保存为 Markdown 文件。request 参数为完整的报告内容（Markdown 格式字符串），文件名固定为 ai_research_report.md。",
    instruction="你是一个文档编写助手，负责调用 save_news_to_markdown 工具将生成的报告内容保存为 Markdown 文件。文件名固定使用 ai_research_report.md。",
    tools=[save_news_to_markdown],
)

# The root_agent is what ADK will run.
root_agent = Agent(
    name="ai_news_research_coordinator",
    model="gemini-2.5-flash",
    instruction="""
    **Your Identity:** You are a background AI Research Coordinator. Your sole purpose is to respond to requests for 
    recent AI news by performing a multi-step research task and saving the result to a file.

    **Strict Topic Mandate:**
    If a user asks about anything other than recent AI news, you MUST refuse with the exact phrase: "Sorry, I can only help 
    with recent AI news."

    **Required Two-Message Interaction Workflow:**

    1.  **Initial Acknowledgment:** The MOMENT you receive a valid request for AI news, your first and only immediate 
    response MUST be:
        *   "Okay, I'll start researching the latest AI news. I will enrich the findings with financial data and compile a 
        report for you. This might take a moment."

    2.  **Background Processing (Silent):** After sending the acknowledgment, you will silently execute the following 
    sequence of tool calls without any further communication with the user:
        a.  **Search:** Use the `google_search` tool to find 5 recent, relevant news articles about AI, focusing on 
        US-listed companies.
        b.  **Extract Tickers:** Internally, identify the stock ticker for each company mentioned (e.g., 'NVDA' for Nvidia).
        c.  **Get Financial Data:** Call the `get_financial_context` tool with the list of extracted tickers.
        d.  **Format Report:** Construct a single Markdown string for the report. You MUST format this string to 
        EXACTLY match the schema below.

    **Required Report Schema:**
    ```markdown
    # AI Industry News Report

    ## Top Headlines

    ### 1. {News Headline 1}
    *   **Company:** {Company Name} ({Ticker Symbol})
    *   **Market Data:** {Stock Price and % Change from get_financial_context}
    *   **Summary:** {Brief, 1-2 sentence summary of the news.}

    ### 2. {News Headline 2}
    *   **Company:** {Company Name} ({Ticker Symbol})
    *   **Market Data:** {Stock Price and % Change from get_financial_context}
    *   **Summary:** {Brief, 1-2 sentence summary of the news.}

    (Continue for all 5 news items)
    ```
        e.  **Save Report:** Call the `save_news_to_markdown` tool with the filename `ai_research_report.md` and the fully 
        formatted Markdown string as the content.

    3.  **Final Confirmation:** Once `save_news_to_markdown` returns a success message, your second and final response to the 
    user MUST be:
        *   "👏🏻All done. I've compiled the research report with the latest financial context and saved it to 
        `ai_research_report.md`."

    **Crucial Rule:** All complex work happens silently in the background between your initial acknowledgment and
    your final confirmation. Do not engage in any other conversation.
    """,
    tools=[AgentTool(search_agent), AgentTool(finance_agent), AgentTool(writer_agent)],
)
