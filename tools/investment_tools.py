"""Investment management tools for Investment Agent."""
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from database.connection import get_database
from database.models import Investment, InvestmentType
from google.genai import types

def add_investment(
    symbol: str,
    quantity: float,
    purchase_price: float,
    investment_type: str,
    name: str,
    date: Optional[str],
    notes: Optional[str]
) -> Dict[str, Any]:
    """
    Record a new investment.
    
    Args:
        symbol: Ticker symbol (e.g., AAPL, BTC)
        quantity: Quantity purchased
        purchase_price: Price per unit at purchase
        investment_type: Type of investment (stock, crypto, etf, etc.)
        name: Name of the investment
        date: Optional purchase date in ISO format (defaults to now)
        notes: Optional notes
    
    Returns:
        Dictionary with investment details
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        # Parse date
        if date:
            try:
                purchase_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            except ValueError:
                purchase_date = datetime.strptime(date, '%Y-%m-%d')
        else:
            purchase_date = datetime.utcnow()
            
        # Create investment object
        investment = Investment(
            investment_id=str(uuid.uuid4()),
            user_id=user_id,
            symbol=symbol.upper(),
            name=name,
            quantity=quantity,
            purchase_price=purchase_price,
            investment_type=InvestmentType(investment_type.lower()),
            purchase_date=purchase_date,
            notes=notes,
            created_at=datetime.utcnow()
        )
        
        # Insert into database
        result = db.investments.insert_one(investment.to_dict())
        
        if not result.inserted_id:
            return {
                "success": False,
                "message": "Failed to add investment",
                "error": "Database insertion failed"
            }
            
        return {
            "success": True,
            "message": f"Investment in {symbol} added successfully",
            "investment": investment.to_dict()
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
            "message": "Error adding investment",
            "error": str(e)
        }

def get_portfolio(
    investment_type: Optional[str]
) -> Dict[str, Any]:
    """
    Retrieve current investments.
    
    Args:
        investment_type: Optional filter by investment type
        
    Returns:
        Dictionary with list of investments
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        query = {"user_id": user_id}
        if investment_type:
            query["investment_type"] = investment_type.lower()
            
        investments_cursor = db.investments.find(query).sort("purchase_date", -1)
        
        investments_list = []
        for inv_data in investments_cursor:
            # Convert to model and back to dict to ensure consistency
            inv = Investment(**inv_data)
            investments_list.append(inv.to_dict())
            
        return {
            "success": True,
            "count": len(investments_list),
            "investments": investments_list
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": "Error retrieving portfolio",
            "error": str(e)
        }

def get_portfolio_value() -> Dict[str, Any]:
    """
    Calculate total value of all investments based on purchase price (cost basis).
    Note: Real-time price updates would require an external API.
    
    Returns:
        Dictionary with total value breakdown
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        investments_cursor = db.investments.find({"user_id": user_id})
        
        total_cost_basis = 0.0
        type_breakdown = {}
        
        for inv_data in investments_cursor:
            inv = Investment(**inv_data)
            cost = inv.total_cost
            total_cost_basis += cost
            
            inv_type = inv.investment_type
            type_breakdown[inv_type] = type_breakdown.get(inv_type, 0.0) + cost
            
        return {
            "success": True,
            "total_cost_basis": round(total_cost_basis, 2),
            "breakdown_by_type": {k: round(v, 2) for k, v in type_breakdown.items()}
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": "Error calculating portfolio value",
            "error": str(e)
        }

def get_investment_summary() -> Dict[str, Any]:
    """
    Get a summary of the investment portfolio for the agent.
    
    Returns:
        Dictionary with summary statistics
    """
    portfolio_value = get_portfolio_value()
    if not portfolio_value.get("success"):
        return portfolio_value
        
    portfolio = get_portfolio()
    
    return {
        "success": True,
        "total_invested": portfolio_value.get("total_cost_basis", 0.0),
        "asset_allocation": portfolio_value.get("breakdown_by_type", {}),
        "total_positions": portfolio.get("count", 0)
    }


