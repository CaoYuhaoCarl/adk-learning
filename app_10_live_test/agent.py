from google.adk.agents import Agent

###------------------------------------###
# ADK Live 功能测试 Agent
# 目的：用最简单的单 agent 快速验证 Live 功能是否正常
# 模型：gemini-3.1-flash-live-preview
###------------------------------------###

root_agent = Agent(
    name="live_test_agent",
    model="gemini-3.1-flash-live-preview",
    instruction="""
    你是一个简单的测试助手，用于验证 ADK Live 功能是否正常工作。

    你可以：
    1. 回答任何问题
    2. 做基础的数学计算
    3. 讲一个简短的笑话

    保持回答简洁，用中文回复。
    """,
)
