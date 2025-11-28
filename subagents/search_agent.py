"""Search Agent - Specialized agent for performing Google searches."""
from google.adk.agents import Agent
from google.adk.tools import google_search

# Using gemini-2.0-flash for search operations as it's fast and capable
AGENT_MODEL = "gemini-2.0-flash"

search_agent = Agent(
    name="search_agent",
    model=AGENT_MODEL,
    description="A specialist agent that performs Google searches to find real-time information.",
    instruction="You are a search specialist. Your only job is to use the google_search tool to find information requested by other agents. Provide concise summaries of the search results.",
    tools=[google_search]
)
