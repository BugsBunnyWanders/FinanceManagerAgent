"""Investment Agent - Manages investment portfolio and advice."""
from const import MODEL_GEMINI_2_5_PRO
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from instructions.investment_agent_instructions import INVESTMENT_AGENT_INSTRUCTIONS
from subagents.search_agent import search_agent
from tools.investment_tools import (
    add_investment,
    get_portfolio,
    get_portfolio_value,
    get_investment_summary
)

AGENT_MODEL = "gemini-2.0-flash" # Using 2.0 Flash as per docs/workaround

# Define tools for the investment agent
investment_agent_tools = [
    add_investment,
    get_portfolio,
    get_portfolio_value,
    get_investment_summary,
    agent_tool.AgentTool(agent=search_agent)
]

investment_agent = Agent(
    name="investment_agent",
    model=AGENT_MODEL,
    description="Manages investment portfolio, tracks assets, and provides investment research and advice.",
    instruction=INVESTMENT_AGENT_INSTRUCTIONS,
    tools=investment_agent_tools
)
