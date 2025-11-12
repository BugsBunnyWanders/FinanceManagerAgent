"""Expense management tools for Expenses Agent."""
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from database.connection import get_database
from database.models import Expense, AccountBalance, ExpenseCategory, ExpenseFilter


def set_expense(
    amount: float,
    category: str,
    description: str,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a new expense and update account balance.
    
    Args:
        amount: Expense amount (must be positive)
        category: Expense category (groceries, dining, transport, etc.)
        description: Description of the expense
        date: Optional date in ISO format (defaults to now)
    
    Returns:
        Dictionary with expense information and updated balance
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        # Parse date
        if date:
            try:
                expense_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            except ValueError:
                expense_date = datetime.strptime(date, '%Y-%m-%d')
        else:
            expense_date = datetime.utcnow()
        
        # Create expense object
        expense = Expense(
            expense_id=str(uuid.uuid4()),
            user_id=user_id,
            amount=amount,
            category=ExpenseCategory(category.lower()),
            description=description,
            date=expense_date,
            created_at=datetime.utcnow()
        )
        
        # Insert expense into database
        result = db.expenses.insert_one(expense.to_dict())
        
        if not result.inserted_id:
            return {
                "success": False,
                "message": "Failed to add expense",
                "error": "Database insertion failed"
            }
        
        # Update account balance
        balance_data = db.account_balance.find_one({"user_id": user_id})
        
        if balance_data:
            new_balance = balance_data['current_balance'] - amount
            db.account_balance.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "current_balance": new_balance,
                        "last_updated": datetime.utcnow()
                    }
                }
            )
        else:
            # Create new balance record with negative balance (overdraft scenario)
            new_balance = -amount
            balance = AccountBalance(
                user_id=user_id,
                current_balance=new_balance,
                last_updated=datetime.utcnow()
            )
            db.account_balance.insert_one(balance.to_dict())
        
        return {
            "success": True,
            "message": f"Expense of ${amount:.2f} added successfully",
            "expense": {
                "expense_id": expense.expense_id,
                "amount": amount,
                "category": category,
                "description": description,
                "date": expense_date.isoformat()
            },
            "new_balance": new_balance
        }
            
    except ValueError as e:
        return {
            "success": False,
            "message": "Invalid input parameters",
            "error": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error adding expense",
            "error": str(e)
        }


def get_expenses(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Retrieve expenses with optional filters.
    
    Args:
        start_date: Start date for filtering (ISO format)
        end_date: End date for filtering (ISO format)
        category: Filter by specific category
        limit: Maximum number of expenses to return (default: 50)
    
    Returns:
        Dictionary with list of expenses and summary statistics
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        # Build query
        query = {"user_id": user_id}
        
        # Date filters
        date_filter = {}
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                date_filter["$gte"] = start_dt
            except ValueError:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                date_filter["$gte"] = start_dt
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                date_filter["$lte"] = end_dt
            except ValueError:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                date_filter["$lte"] = end_dt
        
        if date_filter:
            query["date"] = date_filter
        
        # Category filter
        if category:
            query["category"] = category.lower()
        
        # Fetch expenses
        expenses_cursor = db.expenses.find(query).sort("date", -1).limit(limit)
        expenses_list = []
        total_amount = 0.0
        category_totals: Dict[str, float] = {}
        
        for expense_data in expenses_cursor:
            expense = Expense(**expense_data)
            expenses_list.append({
                "expense_id": expense.expense_id,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date": expense.date.isoformat(),
                "created_at": expense.created_at.isoformat()
            })
            
            total_amount += expense.amount
            category_totals[expense.category] = category_totals.get(expense.category, 0.0) + expense.amount
        
        return {
            "success": True,
            "count": len(expenses_list),
            "total_amount": round(total_amount, 2),
            "category_breakdown": {k: round(v, 2) for k, v in category_totals.items()},
            "expenses": expenses_list
        }
            
    except Exception as e:
        return {
            "success": False,
            "message": "Error retrieving expenses",
            "error": str(e)
        }


def get_current_account_balance() -> Dict[str, Any]:
    """
    Get current account balance and related information.
    
    Returns:
        Dictionary with balance information
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        # Get balance
        balance_data = db.account_balance.find_one({"user_id": user_id})
        
        if not balance_data:
            return {
                "success": True,
                "message": "No account balance found. Please set initial balance.",
                "current_balance": 0.0,
                "monthly_income": 0.0,
                "monthly_expense_threshold": 0.0
            }
        
        balance = AccountBalance(**balance_data)
        
        # Calculate current month expenses
        now = datetime.utcnow()
        start_of_month = datetime(now.year, now.month, 1)
        
        month_expenses = list(db.expenses.find({
            "user_id": user_id,
            "date": {"$gte": start_of_month}
        }))
        
        monthly_spent = sum(exp['amount'] for exp in month_expenses)
        
        # Calculate threshold usage
        threshold_percentage = 0.0
        if balance.monthly_expense_threshold > 0:
            threshold_percentage = (monthly_spent / balance.monthly_expense_threshold) * 100
        
        return {
            "success": True,
            "current_balance": round(balance.current_balance, 2),
            "monthly_income": round(balance.monthly_income, 2),
            "monthly_expense_threshold": round(balance.monthly_expense_threshold, 2),
            "current_month_spent": round(monthly_spent, 2),
            "threshold_usage_percentage": round(threshold_percentage, 2),
            "last_updated": balance.last_updated.isoformat()
        }
            
    except Exception as e:
        return {
            "success": False,
            "message": "Error retrieving account balance",
            "error": str(e)
        }


def set_account_balance(
    balance: float,
    monthly_income: Optional[float] = None,
    monthly_expense_threshold: Optional[float] = None
) -> Dict[str, Any]:
    """
    Set or update account balance and monthly parameters.
    
    Args:
        balance: Current account balance
        monthly_income: Optional monthly income
        monthly_expense_threshold: Optional monthly expense limit
    
    Returns:
        Dictionary with confirmation
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        # Check if balance exists
        existing_balance = db.account_balance.find_one({"user_id": user_id})
        
        update_data = {
            "current_balance": balance,
            "last_updated": datetime.utcnow()
        }
        
        if monthly_income is not None:
            update_data["monthly_income"] = monthly_income
        
        if monthly_expense_threshold is not None:
            update_data["monthly_expense_threshold"] = monthly_expense_threshold
        
        if existing_balance:
            # Update existing
            result = db.account_balance.update_one(
                {"user_id": user_id},
                {"$set": update_data}
            )
            message = "Account balance updated successfully"
        else:
            # Create new
            balance_obj = AccountBalance(
                user_id=user_id,
                current_balance=balance,
                monthly_income=monthly_income or 0.0,
                monthly_expense_threshold=monthly_expense_threshold or 0.0
            )
            result = db.account_balance.insert_one(balance_obj.to_dict())
            message = "Account balance set successfully"
        
        return {
            "success": True,
            "message": message,
            "balance": update_data
        }
            
    except Exception as e:
        return {
            "success": False,
            "message": "Error setting account balance",
            "error": str(e)
        }

