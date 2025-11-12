# Setup Guide for Finance Manager Agent

This guide will help you set up and run the Finance Manager Agent on your system.

## Prerequisites

1. **Python 3.10 or higher**
   - Check your version: `python --version`
   - Download from: https://www.python.org/downloads/

2. **MongoDB**
   - Install MongoDB Community Edition: https://www.mongodb.com/try/download/community
   - Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas

3. **Google API Key**
   - Go to: https://aistudio.google.com/app/apikey
   - Create a new API key for Gemini

## Installation Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment

1. Copy the environment template:
   ```bash
   copy env_example.txt .env
   ```

2. Edit `.env` file with your actual values:
   ```env
   GOOGLE_API_KEY=your_actual_google_api_key
   MONGODB_URI=mongodb://localhost:27017/
   MONGODB_DATABASE=finance_manager
   USER_ID=default_user
   ```

### Step 3: Start MongoDB

#### For Local MongoDB:
```bash
# Windows
net start MongoDB

# macOS/Linux
sudo systemctl start mongod
```

#### For MongoDB Atlas:
- Update `MONGODB_URI` in `.env` with your Atlas connection string
- Example: `mongodb+srv://username:password@cluster.mongodb.net/`

### Step 4: Run the Application

```bash
python main.py
```

## First Time Setup

When you run the application for the first time:

1. **Set your account balance:**
   ```
   You: Set my account balance to $5000 with monthly income of $4000 and spending limit of $3000
   ```

2. **Create your first goal:**
   ```
   You: I want to save $10,000 for a vacation by December 2026
   ```

3. **Add an expense:**
   ```
   You: I spent $150 on groceries today
   ```

## Troubleshooting

### Error: "GOOGLE_API_KEY not configured"
- Make sure you created the `.env` file
- Verify your API key is correct
- Don't include quotes around the API key

### Error: "Database connection failed"
- Ensure MongoDB is running
- Check your connection string in `.env`
- For local MongoDB, verify it's installed and started

### Error: "Module not found"
- Run `pip install -r requirements.txt` again
- Consider using a virtual environment:
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  source venv/bin/activate  # macOS/Linux
  pip install -r requirements.txt
  ```

## Usage Examples

### Setting Goals
```
I want to save $5000 for emergency fund by June 2026, high priority
Create an investment goal of $20,000 for retirement by 2030
```

### Adding Expenses
```
I spent $75 on dinner at a restaurant
Add expense: $50 for gas
I bought groceries for $200
```

### Checking Status
```
How am I doing this month?
What's my account balance?
Show me my goals
Show my expenses for this month
```

### Getting Advice
```
How can I save more money?
Am I on track with my goals?
Give me financial advice
```

## Advanced Configuration

### Custom User ID
Set a unique user ID in `.env` if you want to support multiple users:
```env
USER_ID=john_doe
```

### MongoDB Database Name
Change the database name if needed:
```env
MONGODB_DATABASE=my_finance_db
```

### Logging
Adjust log level for debugging:
```env
LOG_LEVEL=DEBUG
```

## Next Steps

- Explore the agent's capabilities by asking questions
- Set realistic financial goals
- Track your expenses daily
- Review your progress weekly
- Use the financial advice to optimize your budget

## Support

For issues or questions:
- Check the `docs/temp/` folder for additional documentation
- Review `memory.md` for known issues and solutions
- Ensure all dependencies are installed correctly

Happy financial planning! 💰

