"""Expenses Agent - Manages expense tracking and account balance."""
from const import MODEL_GEMINI_2_5_PRO
from google.adk.agents import Agent
from instructions.expenses_agent_instructions import EXPENSES_AGENT_INSTRUCTIONS
from tools.expense_tools import (
    set_expense,
    get_expenses,
    get_current_account_balance,
    set_account_balance
)

AGENT_MODEL = MODEL_GEMINI_2_5_PRO

# Define tools for the expenses agent
expenses_agent_tools = [
    set_expense,
    get_expenses,
    get_current_account_balance,
    set_account_balance
]

expenses_agent = Agent(
    name="expenses_agent",
    model=AGENT_MODEL,
    description="Manages expense tracking, account balance monitoring, and spending analysis.",
    instruction=EXPENSES_AGENT_INSTRUCTIONS,
    tools=expenses_agent_tools
)

