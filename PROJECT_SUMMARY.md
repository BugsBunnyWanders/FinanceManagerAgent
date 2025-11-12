# Finance Manager Agent - Project Summary

## 🎯 Project Overview

A multi-agent AI system built with Google ADK and Gemini 2.5 Pro that helps users manage personal finances through intelligent monitoring, tracking, and advisory capabilities.

## ✨ Key Features

- 💰 **Financial Goal Management** - Create and track savings, investment, and debt reduction goals
- 📊 **Expense Tracking** - Record and categorize expenses automatically
- 💳 **Account Balance Monitoring** - Track balance and monthly spending thresholds
- 🎯 **Personalized Financial Advice** - AI-powered recommendations based on your goals
- ⚠️ **Smart Alerts** - Notifications when spending approaches or exceeds limits
- 🤖 **Multi-Agent Architecture** - Specialized agents for different financial tasks

## 🏗️ Architecture

### Agents

1. **Root Agent (Finance Advisor)**
   - Financial coaching and advice
   - Goal management
   - Spending analysis
   - Tools: `setGoal`, `getGoal`

2. **Expenses Agent (Subagent)**
   - Expense recording and retrieval
   - Balance tracking
   - Category analysis
   - Tools: `setExpense`, `getExpenses`, `getCurrentAccountBalance`, `setAccountBalance`

### Technology Stack

- **Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.5 Pro
- **Database**: MongoDB with Pydantic validation
- **Language**: Python 3.10+

## 📁 Project Structure

```
FinanceManagerAgent/
├── main.py                      # Application entry point
├── root_agent.py                # Root Agent definition
├── const.py                     # Configuration constants
├── requirements.txt             # Python dependencies
├── env_example.txt              # Environment template
├── README.md                    # Full documentation
├── QUICK_START.md              # Quick start guide
├── setup_guide.md              # Detailed setup instructions
├── .gitignore                  # Git ignore rules
│
├── database/                    # Database layer
│   ├── connection.py           # MongoDB connection
│   └── models.py               # Data models
│
├── tools/                       # Agent tools
│   ├── goal_tools.py           # Goal management tools
│   └── expense_tools.py        # Expense management tools
│
├── instructions/                # Agent instructions
│   ├── root_agent_instructions.py
│   └── expenses_agent_instructions.py
│
├── subagents/                   # Subagent definitions
│   └── expenses_agent.py
│
└── docs/                        # Documentation
    └── temp/
        ├── feature-design.md    # Architecture details
        ├── current-state.md     # Development status
        ├── changelog.md         # Change history
        └── memory.md            # Learnings & decisions
```

## 🚀 Getting Started

### Quick Setup (3 steps)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `env_example.txt` to `.env`
   - Add your Google API key
   - Configure MongoDB connection

3. **Run the application:**
   ```bash
   python main.py
   ```

For detailed instructions, see [QUICK_START.md](QUICK_START.md) or [setup_guide.md](setup_guide.md).

## 💡 Example Usage

```
You: Set my account balance to $5000 with monthly income of $4000 and spending limit of $3000

Finance Advisor: Great! I've set your account balance to $5000...

You: I want to save $10,000 for a vacation by December 2026

Finance Advisor: That's a great goal! 🎯 Let me set that up for you...

You: I spent $150 on groceries today

Finance Advisor: Expense recorded! You've spent $450 on groceries this month...

You: How am I doing this month?

Finance Advisor: Let me check your financial status...
📊 Spending: $2,150 / $2,500 (86% of your limit)
🎯 Savings Goal: 45% complete ($4,500 / $10,000)
💡 Recommendation: You're slightly over pace on spending...
```

## 📊 Current Status

**Version**: 0.1.1 (MVP with ADK Runner)  
**Status**: ✅ Complete - Ready for Testing  
**Last Updated**: November 12, 2025

### What's Working

- ✅ Multi-agent coordination
- ✅ Goal creation and tracking
- ✅ Expense recording and analysis
- ✅ Account balance management
- ✅ Financial advice generation
- ✅ Natural language interaction
- ✅ MongoDB data persistence

### What's Next

- 🔄 Integration testing
- 🔄 User feedback collection
- 📝 Unit test development
- 🎨 UI/UX improvements
- 📊 Advanced analytics features

## 🎓 Key Learnings

1. **Multi-Agent Design** - Separation of concerns improves maintainability
2. **Google ADK** - Native integration with Gemini provides powerful capabilities
3. **Pydantic Validation** - Type safety prevents data errors
4. **MongoDB Flexibility** - Schema flexibility allows rapid iteration

## 🔒 Security Considerations

- Environment variables for sensitive data
- API key not committed to version control
- Database connection with authentication support
- Input validation on all user data

## 📚 Documentation

- [README.md](README.md) - Complete project documentation
- [QUICK_START.md](QUICK_START.md) - Get started in 5 minutes
- [setup_guide.md](setup_guide.md) - Detailed setup instructions
- [docs/temp/feature-design.md](docs/temp/feature-design.md) - Architecture deep dive
- [docs/temp/current-state.md](docs/temp/current-state.md) - Development progress
- [docs/temp/changelog.md](docs/temp/changelog.md) - Change history
- [docs/temp/memory.md](docs/temp/memory.md) - Project learnings

## 🤝 Contributing

This is currently a personal project. Feel free to fork and adapt to your needs.

## 📝 License

MIT License

## 🙏 Acknowledgments

- Google ADK for the agent framework
- Gemini 2.5 Pro for powerful AI capabilities
- MongoDB for flexible data storage

---

**Built with ❤️ using Google ADK and Gemini 2.5 Pro**

For questions or issues, refer to the documentation or check the memory.md file for common solutions.

