# Google ADK Runner and Session Management Guide

## Overview

This document explains how the Finance Manager Agent uses Google ADK's `Runner` with `InMemorySessionService` for proper agent orchestration following official ADK patterns.

## Why Use ADK Runner?

The ADK Runner is the **correct way** to execute agents in Google ADK. It provides:

1. **Session Management** - Maintains conversation context across turns
2. **Tool Orchestration** - Automatically handles tool calling and execution
3. **Multi-Agent Coordination** - Manages subagent delegation
4. **State Persistence** - Tracks conversation history and state
5. **Error Handling** - Built-in error management for agent interactions

## Implementation

### Import Statements

```python
import asyncio
from google.adk import Runner, InMemorySessionService
from google.genai import types
```

### Initialize Session Service

```python
# For local development, use InMemorySessionService
session_service = InMemorySessionService()

# Create a session (must await - it's async)
APP_NAME = "finance_manager_app"
USER_ID = "default_user"
SESSION_ID = f"session_{USER_ID}_001"

session = await session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
```

### Initialize Runner

```python
runner = Runner(
    agent=root_agent,  # Your main agent
    app_name=APP_NAME,
    session_service=session_service
)
```

### Run Agent (Async)

```python
async def call_agent_async(runner, session_id: str, query: str):
    # Prepare the user's message
    new_message = types.Content(
        role='user',
        parts=[types.Part(text=query)]
    )
    
    # Execute the agent and process events
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=new_message  # Parameter name is 'new_message', not 'content'
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                return event.content.parts[0].text
    
    return "No response"

# Use asyncio to run
response = await call_agent_async(runner, session.id, "Show my expenses")
```

## Complete Example

```python
import os
import asyncio
from google.adk import Runner, InMemorySessionService
from google.genai import types
from root_agent import root_agent

async def call_agent_async(runner, session_id: str, query: str):
    """Send query to agent and get response."""
    new_message = types.Content(
        role='user',
        parts=[types.Part(text=query)]
    )
    
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=new_message  # Use 'new_message', not 'content'
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                return event.content.parts[0].text
    return ""

async def main():
    # Initialize session service
    session_service = InMemorySessionService()
    
    APP_NAME = "finance_manager_app"
    USER_ID = "default_user"
    
    # Create session (must await)
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=f"session_{USER_ID}_001"
    )
    
    # Initialize runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    # Conversation loop
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            break
        
        # Run agent with session
        response = await call_agent_async(runner, session.id, user_input)
        print(f"Agent: {response}")

# Run the async main
asyncio.run(main())
```

## Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│                       User Input                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    LocalRunner                               │
│                                                              │
│  • Manages agent execution                                  │
│  • Handles tool orchestration                               │
│  • Maintains session state                                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       Session                                │
│                                                              │
│  • Stores conversation history                              │
│  • Tracks tool call results                                 │
│  • Maintains context                                        │
│  • Manages state across turns                               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Root Agent                                │
│                                                              │
│  • Processes user request                                   │
│  • Decides which tools to use                               │
│  • Delegates to subagents if needed                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
┌─────────────────────┐   ┌─────────────────────┐
│   Root Agent Tools  │   │   Expenses Agent    │
│                     │   │    (Subagent)       │
│  • setGoal()        │   │                     │
│  • getGoal()        │   │  • setExpense()     │
└─────────────────────┘   │  • getExpenses()    │
                          │  • getBalance()     │
                          └─────────────────────┘
                                    │
                                    ▼
                          ┌─────────────────────┐
                          │     MongoDB         │
                          └─────────────────────┘
```

## Key Differences from Direct API Calls

### ❌ Old Way (Incorrect)

```python
# Don't do this - bypasses ADK orchestration
response = agent.generate_content(contents=conversation_history)
```

**Problems:**
- Manual history management
- No automatic tool orchestration
- No session state
- Subagent coordination not handled
- Limited error handling

### ✅ Correct Way

```python
import asyncio
from google.adk import Runner, InMemorySessionService
from google.genai import types

# Initialize session service
session_service = InMemorySessionService()
session = session_service.create_session(
    app_name="my_app",
    user_id="user_1",
    session_id="session_001"
)

# Initialize runner
runner = Runner(
    agent=root_agent,
    app_name="my_app",
    session_service=session_service
)

# Run agent asynchronously
async def call_agent(query):
    new_message = types.Content(role='user', parts=[types.Part(text=query)])
    async for event in runner.run_async(
        user_id="user_1",
        session_id=session.id,
        new_message=new_message  # Correct parameter name
    ):
        if event.is_final_response():
            return event.content.parts[0].text

response = await call_agent("Hello")
```

**Benefits:**
- Automatic history management
- Built-in tool orchestration
- Session state maintained
- Subagent coordination handled
- Robust error handling

## Session Features

### 1. Automatic History

Sessions automatically maintain conversation history:

```python
# Turn 1
runner.run(session_id=session.id, message="Set my balance to $5000")
# History: [User: "Set my balance..."]

# Turn 2 - Agent remembers context
runner.run(session_id=session.id, message="How much do I have?")
# Agent knows you're referring to the $5000 balance
```

### 2. Tool Call Tracking

Sessions track tool executions:

```python
# User: "I spent $150 on groceries"
# Session tracks:
# - User message
# - Agent's decision to call setExpense()
# - Tool execution and result
# - Agent's response using the result
```

### 3. Multi-Turn Context

Sessions maintain context across multiple turns:

```python
# Turn 1
User: "I want to save $10,000 for vacation"
Agent: "Great goal! Let me set that up..."

# Turn 2 - Agent remembers the goal
User: "When should I reach it?"
Agent: "Based on the vacation goal we just set..."
```

## Multi-Agent Coordination

The runner handles subagent delegation:

```python
# User asks about expenses
User: "Show me my expenses for this month"

# Flow:
# 1. Runner → Root Agent
# 2. Root Agent decides to delegate to Expenses Agent
# 3. Runner → Expenses Agent → getExpenses()
# 4. Tool result → Expenses Agent → Root Agent
# 5. Root Agent synthesizes response → User
```

All of this happens automatically through the runner!

## Error Handling

The runner provides robust error handling:

```python
try:
    response = runner.run(
        session_id=session.id,
        message=user_input
    )
except Exception as e:
    print(f"Error: {e}")
    # Runner handles:
    # - Tool execution errors
    # - API errors
    # - Timeout errors
    # - Invalid state errors
```

## Session Management Best Practices

### 1. One Session Per Conversation

```python
# Good - One session for entire conversation
session = runner.create_session()

while True:
    user_input = input("You: ")
    response = runner.run(session_id=session.id, message=user_input)
```

### 2. Create New Session for New Context

```python
# When starting a fresh conversation
old_session = session
session = runner.create_session()  # Fresh context
```

### 3. Session Cleanup

```python
# Sessions are automatically managed
# No manual cleanup needed
# Context is maintained until session ends
```

## Advanced: Session Persistence (Future)

For future enhancements, sessions can be persisted:

```python
# Save session state
session_data = {
    'id': session.id,
    'history': session.history,
    'created_at': datetime.now()
}
# Store in database

# Restore session later
# (Feature to be implemented in ADK)
```

## Debugging Tips

### 1. Check Session ID

```python
print(f"Current session: {session.id}")
```

### 2. Monitor Tool Calls

Runner logs tool executions automatically.

### 3. Test with Simple Messages

```python
# Test runner setup
response = runner.run(session_id=session.id, message="Hello")
```

## Summary

**Always use `LocalRunner` with sessions for Google ADK agents.**

This ensures:
- ✅ Proper conversation management
- ✅ Automatic tool orchestration
- ✅ Multi-agent coordination
- ✅ State persistence
- ✅ Error handling
- ✅ Context maintenance

**Never use direct `generate_content()` calls in production.**

## References

- Google ADK Documentation: https://cloud.google.com/products/agent-builder
- Agent Development Guide: Check official ADK docs
- Session Management: Built into LocalRunner

---

*Last Updated: November 12, 2025*

