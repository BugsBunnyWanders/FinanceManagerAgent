# MongoDB Atlas Setup Guide

## ✅ Your Current Setup

You're using MongoDB Atlas, which is perfect for this application! The Finance Manager Agent is already configured to work with Atlas.

## Configuration

### Your `.env` File Should Look Like This:

```env
# Google AI Configuration
GOOGLE_API_KEY=your_actual_google_api_key

# MongoDB Atlas Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=finance_manager

# Application Configuration
USER_ID=default_user
DEFAULT_CURRENCY=USD
LOG_LEVEL=INFO
```

### MongoDB Atlas Connection String Format

Your `MONGODB_URI` should follow this pattern:

```
mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority
```

**Example:**
```
mongodb+srv://john:myPassword123@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

## What Happens When You Run the Application

1. **Connection Test**: The application will automatically connect to MongoDB Atlas
2. **Database Creation**: If the database doesn't exist, it will be created automatically
3. **Index Creation**: Performance indexes will be created for:
   - Goals collection
   - Expenses collection
   - Account balance collection

You'll see these success messages:
```
✓ Connected to MongoDB: finance_manager
✓ Database indexes created
```

## MongoDB Atlas Collections

The application will create three collections:

### 1. `goals` Collection
Stores financial goals:
```json
{
  "goal_id": "uuid",
  "user_id": "default_user",
  "goal_type": "savings",
  "name": "Vacation Fund",
  "target_amount": 10000,
  "current_amount": 0,
  "deadline": "2026-12-31T00:00:00",
  "priority": "high",
  "created_at": "2025-11-12T...",
  "updated_at": "2025-11-12T..."
}
```

### 2. `expenses` Collection
Stores expense records:
```json
{
  "expense_id": "uuid",
  "user_id": "default_user",
  "amount": 150.00,
  "category": "groceries",
  "description": "Weekly groceries",
  "date": "2025-11-12T...",
  "created_at": "2025-11-12T..."
}
```

### 3. `account_balance` Collection
Stores account information:
```json
{
  "user_id": "default_user",
  "current_balance": 5000.00,
  "last_updated": "2025-11-12T...",
  "monthly_income": 4000.00,
  "monthly_expense_threshold": 3000.00
}
```

## Verifying Your MongoDB Atlas Setup

### 1. Check Connection String
Make sure your `.env` file has:
- ✅ Correct username
- ✅ Correct password (URL-encoded if it contains special characters)
- ✅ Correct cluster URL
- ✅ `retryWrites=true&w=majority` parameters

### 2. Network Access
In MongoDB Atlas Dashboard:
- Go to **Network Access**
- Ensure your IP address is whitelisted
- Or allow access from anywhere: `0.0.0.0/0` (for development only)

### 3. Database User Permissions
In MongoDB Atlas Dashboard:
- Go to **Database Access**
- Ensure your user has **Read and write to any database** permission
- Or at least read/write access to your specific database

## Testing the Connection

When you run the application:

```bash
python main.py
```

You should see:
```
============================================================
Finance Manager Agent - Personal Finance Coach
============================================================

✓ Google API key configured
✓ Connected to MongoDB: finance_manager
✓ Database indexes created
✓ Session created: session_default_user_001
✓ Runner initialized for agent 'finance_advisor_agent'

============================================================
Welcome! I'm your personal finance advisor. 💰
...
```

If you see these ✓ marks, your MongoDB Atlas connection is working perfectly!

## Common Issues & Solutions

### Issue 1: Authentication Failed
```
✗ Failed to connect to MongoDB: Authentication failed
```

**Solution:**
- Check username and password in your connection string
- Ensure password is URL-encoded (special characters like @, :, / need encoding)
- Example: `myP@ss` should be `myP%40ss`

### Issue 2: Network Error
```
✗ Failed to connect to MongoDB: connection timeout
```

**Solution:**
- Add your IP to Network Access whitelist in Atlas
- Check your internet connection
- Verify cluster URL is correct

### Issue 3: Database Access Denied
```
✗ Failed to connect to MongoDB: user is not allowed to do action
```

**Solution:**
- Check database user permissions in Atlas
- Ensure user has read/write access to the database

## Special Characters in Password

If your MongoDB Atlas password contains special characters, URL-encode them:

| Character | Encoded |
|-----------|---------|
| @ | %40 |
| : | %3A |
| / | %2F |
| ? | %3F |
| # | %23 |
| [ | %5B |
| ] | %5D |

**Example:**
- Password: `My@Pass:123`
- Encoded: `My%40Pass%3A123`

## Viewing Your Data in MongoDB Atlas

1. Go to [MongoDB Atlas Console](https://cloud.mongodb.com/)
2. Navigate to your cluster
3. Click **"Browse Collections"**
4. Select your database (e.g., `finance_manager`)
5. View your collections: `goals`, `expenses`, `account_balance`

## MongoDB Atlas Free Tier

The application works perfectly with MongoDB Atlas **Free Tier (M0)**:
- ✅ 512 MB storage (plenty for personal finance data)
- ✅ Shared RAM
- ✅ Shared vCPU
- ✅ No credit card required

Perfect for personal use!

## Connection Settings (Already Configured)

The application is already set up with best practices:

✅ **Retry Writes**: Automatically retries failed write operations
✅ **Write Concern**: Ensures data is written to majority of nodes
✅ **Connection Pooling**: Efficient connection management
✅ **Timeout Handling**: Graceful handling of connection issues
✅ **Indexes**: Optimized for query performance

## Next Steps

1. ✅ Verify your `.env` file has the correct `MONGODB_URI`
2. ✅ Ensure your IP is whitelisted in MongoDB Atlas
3. ✅ Run `python main.py` to test the connection
4. ✅ Start using your finance manager!

## Database Backup (Recommended)

MongoDB Atlas provides automatic backups, but you can also:

1. **Export Data** (from Atlas UI):
   - Go to your cluster
   - Click on "..." → "Export Data"

2. **Manual Backup** (using Python):
   ```python
   # Coming soon: Export tool for local backup
   ```

## Support

If you encounter any issues:
1. Check MongoDB Atlas status: https://status.mongodb.com/
2. Review connection string format
3. Verify network access settings
4. Check database user permissions

---

**Your MongoDB Atlas setup is ready to go! 🚀**

The application will automatically:
- Connect to your Atlas cluster
- Create necessary collections
- Set up indexes for performance
- Handle all database operations

Just run `python main.py` and start managing your finances!

