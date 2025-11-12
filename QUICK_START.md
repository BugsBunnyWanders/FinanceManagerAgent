# Quick Start Guide

Get your Finance Manager Agent up and running in 5 minutes! ⚡

## Prerequisites

- Python 3.10+
- **MongoDB Atlas** account (free tier works great!) - [Sign up here](https://www.mongodb.com/cloud/atlas/register)
- Google API Key - [Get it here](https://aistudio.google.com/app/apikey)

## Setup (3 steps)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file (copy from `env_example.txt`):

```env
GOOGLE_API_KEY=your_actual_google_api_key_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=finance_manager
USER_ID=default_user
```

**Important:** Replace:
- `your_actual_google_api_key_here` with your actual Google API key
- `username:password@cluster.mongodb.net` with your MongoDB Atlas credentials

### 3. MongoDB Atlas Setup

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create a free cluster (M0)
3. Create a database user (Database Access)
4. Whitelist your IP address (Network Access) or use `0.0.0.0/0` for testing
5. Get your connection string from "Connect" → "Connect your application"
6. Add it to your `.env` file as `MONGODB_URI`

📖 **Detailed guide:** See [docs/MONGODB_ATLAS_SETUP.md](docs/MONGODB_ATLAS_SETUP.md)

## Run

```bash
python main.py
```

## First Conversation

```
You: Set my account balance to $5000 with monthly income of $4000 and spending limit of $3000

You: I want to save $10,000 for a vacation by December 2026

You: I spent $150 on groceries today

You: How am I doing this month?
```

## Common Commands

| What you want | Example command |
|---------------|----------------|
| Set balance | "Set my balance to $5000 with monthly limit of $3000" |
| Create goal | "I want to save $10,000 for vacation by June 2026" |
| Add expense | "I spent $75 on dinner" |
| Check status | "How am I doing this month?" |
| View goals | "Show me my goals" |
| View expenses | "Show my expenses for this month" |
| Get advice | "Give me financial advice" |

## Troubleshooting

**Can't connect to database?**
- Make sure MongoDB is running
- Check your connection string in `.env`

**API key error?**
- Verify your Google API key is correct
- Make sure `.env` file exists

**Module not found?**
- Run `pip install -r requirements.txt` again
- Use a virtual environment

## Next Steps

📖 Read [setup_guide.md](setup_guide.md) for detailed instructions  
📚 Check [README.md](README.md) for complete documentation  
🏗️ Review [docs/temp/feature-design.md](docs/temp/feature-design.md) for architecture

---

Happy financial planning! 💰

