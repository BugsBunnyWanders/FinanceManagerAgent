"""Data models for Finance Manager Agent."""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


class GoalType(str, Enum):
    """Types of financial goals."""
    SAVINGS = "savings"
    INVESTMENT = "investment"
    DEBT_REDUCTION = "debt_reduction"
    EMERGENCY_FUND = "emergency_fund"


class InvestmentType(str, Enum):
    """Types of investments."""
    STOCK = "stock"
    CRYPTO = "crypto"
    ETF = "etf"
    BOND = "bond"
    REAL_ESTATE = "real_estate"
    MUTUAL_FUND = "mutual_fund"
    OTHER = "other"


class Priority(str, Enum):
    """Priority levels for goals."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ExpenseCategory(str, Enum):
    """Expense categories."""
    GROCERIES = "groceries"
    DINING = "dining"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    EDUCATION = "education"
    HOUSING = "housing"
    INSURANCE = "insurance"
    OTHER = "other"


class Goal(BaseModel):
    """Financial goal model."""
    goal_id: str = Field(..., description="Unique identifier for the goal")
    user_id: str = Field(..., description="User identifier")
    goal_type: GoalType = Field(..., description="Type of financial goal")
    name: str = Field(..., description="Goal name/description")
    target_amount: float = Field(..., gt=0, description="Target amount to achieve")
    current_amount: float = Field(default=0.0, ge=0, description="Current progress amount")
    deadline: datetime = Field(..., description="Target deadline")
    priority: Priority = Field(default=Priority.MEDIUM, description="Goal priority")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB."""
        return {
            "goal_id": self.goal_id,
            "user_id": self.user_id,
            "goal_type": self.goal_type,
            "name": self.name,
            "target_amount": self.target_amount,
            "current_amount": self.current_amount,
            "deadline": self.deadline,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def progress_percentage(self) -> float:
        """Calculate progress percentage."""
        if self.target_amount <= 0:
            return 0.0
        return min(100.0, (self.current_amount / self.target_amount) * 100)


class Expense(BaseModel):
    """Expense model."""
    expense_id: str = Field(..., description="Unique identifier for the expense")
    user_id: str = Field(..., description="User identifier")
    amount: float = Field(..., gt=0, description="Expense amount")
    category: ExpenseCategory = Field(..., description="Expense category")
    description: str = Field(..., description="Expense description")
    date: datetime = Field(default_factory=datetime.utcnow, description="Expense date")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB."""
        return {
            "expense_id": self.expense_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "created_at": self.created_at
        }


class AccountBalance(BaseModel):
    """Account balance model."""
    user_id: str = Field(..., description="User identifier")
    current_balance: float = Field(..., description="Current account balance")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    monthly_income: float = Field(default=0.0, ge=0, description="Monthly income")
    monthly_expense_threshold: float = Field(default=0.0, ge=0, description="Monthly expense limit")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB."""
        return {
            "user_id": self.user_id,
            "current_balance": self.current_balance,
            "last_updated": self.last_updated,
            "monthly_income": self.monthly_income,
            "monthly_expense_threshold": self.monthly_expense_threshold
        }


class ExpenseFilter(BaseModel):
    """Filter criteria for expense queries."""
    user_id: str = Field(..., description="User identifier")
    start_date: Optional[datetime] = Field(None, description="Start date for filtering")
    end_date: Optional[datetime] = Field(None, description="End date for filtering")
    categories: Optional[List[ExpenseCategory]] = Field(None, description="Filter by categories")
    min_amount: Optional[float] = Field(None, ge=0, description="Minimum amount")
    max_amount: Optional[float] = Field(None, ge=0, description="Maximum amount")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True

    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class Investment(BaseModel):
    """Investment model."""
    investment_id: str = Field(..., description="Unique identifier for the investment")
    user_id: str = Field(..., description="User identifier")
    symbol: str = Field(..., description="Ticker symbol (e.g., AAPL, BTC)")
    name: str = Field(..., description="Name of the investment")
    quantity: float = Field(..., gt=0, description="Quantity owned")
    purchase_price: float = Field(..., gt=0, description="Price per unit at purchase")
    current_price: Optional[float] = Field(None, description="Current market price per unit")
    investment_type: InvestmentType = Field(..., description="Type of investment")
    purchase_date: datetime = Field(default_factory=datetime.utcnow, description="Date of purchase")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB."""
        return {
            "investment_id": self.investment_id,
            "user_id": self.user_id,
            "symbol": self.symbol,
            "name": self.name,
            "quantity": self.quantity,
            "purchase_price": self.purchase_price,
            "current_price": self.current_price,
            "investment_type": self.investment_type,
            "purchase_date": self.purchase_date,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @property
    def total_cost(self) -> float:
        """Calculate total cost basis."""
        return self.quantity * self.purchase_price
        
    @property
    def current_value(self) -> Optional[float]:
        """Calculate current total value if price is available."""
        if self.current_price is not None:
            return self.quantity * self.current_price
        return None
