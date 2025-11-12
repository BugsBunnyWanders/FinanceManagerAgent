# Finance Manager Agent

A multi-agent system for personal finance management using Google ADK (Agent Development Kit) with Gemini 2.5 Pro.

## Overview

This project implements an intelligent finance coach that monitors your finances, expenses, and savings. It provides personalized recommendations based on your financial goals, alerts when expenses exceed thresholds, and helps optimize your wealth management.

## Architecture

![Architecture Diagram](https://i.imgur.com/your-diagram.png)
*Multi-agent architecture showing Root Agent, Expenses Agent, and MongoDB interactions*

The system consists of two main agents:

### Root Agent (Finance Advisor)
- **Purpose**: Provides financial suggestions and savings recommendations
- **Responsibilities**:
  - Set and manage financial goals
  - Provide personalized financial advice
  - Set expense thresholds per month
  - Monitor overall financial health
  - Generate wealth-building recommendations
- **Tools**: setGoal, getGoal
- **LLM**: Gemini 2.5 Pro

### Expenses Agent (Subagent)
- **Purpose**: Manages expense tracking and account balance
- **Responsibilities**:
  - Add new expenses to database
  - Fetch expense history
  - Update and retrieve account balance
  - Track spending patterns
- **Tools**: setExpense, getExpenses, getCurrentAccountBalance
- **LLM**: Gemini 2.5 Pro

## Technology Stack

- **Agent Framework**: Google ADK (Agent Development Kit) with LocalRunner
- **LLM**: Google Gemini 2.5 Pro
- **Database**: MongoDB
- **Language**: Python 3.10+
- **Session Management**: ADK built-in session handling

## Project Structure

```
FinanceManagerAgent/
├── README.md
├── requirements.txt
├── .env.example
├── const.py                    # Constants and configuration
├── database/
│   ├── connection.py          # MongoDB connection
│   └── models.py              # Database models
├── tools/
│   ├── goal_tools.py          # Goal management tools
│   └── expense_tools.py       # Expense management tools
├── instructions/
│   ├── root_agent_instructions.py
│   └── expenses_agent_instructions.py
├── subagents/
│   └── expenses_agent.py
├── root_agent.py
├── main.py                     # Application entry point
└── docs/
    └── temp/
        ├── feature-design.md
        ├── current-state.md
        ├── changelog.md
        └── memory.md
```

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FinanceManagerAgent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Add your Google API key and MongoDB connection string
   ```bash
   cp .env.example .env
   ```

4. **Set up MongoDB**
   - **MongoDB Atlas** (Recommended): Add your connection string to `.env`
   - **Local MongoDB**: Ensure MongoDB is running locally
   - The application will create necessary collections and indexes automatically
   - See [MongoDB Atlas Setup Guide](docs/MONGODB_ATLAS_SETUP.md) for detailed instructions

5. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Setting Financial Goals
```python
# The agent will help you set financial goals through conversation
"I want to save $10,000 for a vacation by next year"
```

### Tracking Expenses
```python
# Add expenses through natural conversation
"I spent $150 on groceries today"
"Add an expense of $50 for dinner"
```

### Getting Financial Advice
```python
# Ask for recommendations
"How am I doing with my budget this month?"
"Should I increase my savings?"
```

## Features

- ✅ Multi-agent architecture with specialized roles
- ✅ Natural language interaction with ADK Runner
- ✅ Session-based conversation management
- ✅ Goal-based financial planning
- ✅ Automated expense tracking
- ✅ Account balance monitoring
- ✅ Spending alerts and recommendations
- ✅ MongoDB persistence
- ✅ Automatic tool orchestration

## Development Status

See `docs/temp/current-state.md` for detailed development progress.

## Contributing

This is a personal project. Feel free to fork and adapt to your needs.

## License

MIT License

