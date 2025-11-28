from const import MODEL_GEMINI_2_5_PRO
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from instructions.root_agent_instructions import ROOT_AGENT_INSTRUCTIONS
from tools.goal_tools import set_goal, get_goal
from subagents.expenses_agent import expenses_agent
from subagents.investment_agent import investment_agent


AGENT_MODEL = MODEL_GEMINI_2_5_PRO

# Define tools for the root agent
root_agent_tools = [
    set_goal,
    get_goal
]

root_agent = Agent(
    name="finance_advisor_agent",
    model=AGENT_MODEL,
    description="Provides financial advice and investment recommendations based on the user's financial goals and risk tolerance.",
    instruction=ROOT_AGENT_INSTRUCTIONS,
    tools=root_agent_tools,
    sub_agents=[expenses_agent, investment_agent]
)