"""Goal management tools for Root Agent."""
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from database.connection import get_database
from database.models import Goal, GoalType, Priority


def set_goal(
    goal_type: str,
    name: str,
    target_amount: float,
    deadline: str,
    priority: Optional[str],
    current_amount: float
) -> Dict[str, Any]:
    """
    Create or update a financial goal.
    
    Args:
        goal_type: Type of goal (savings, investment, debt_reduction, emergency_fund)
        name: Goal name or description
        target_amount: Target amount to achieve
        deadline: Deadline in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
        priority: Goal priority (high, medium, low)
        current_amount: Current progress
    
    Returns:
        Dictionary with goal information and confirmation
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        # Parse deadline
        try:
            deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        except ValueError:
            deadline_dt = datetime.strptime(deadline, '%Y-%m-%d')
        
        # Handle optional parameters
        priority_val = priority if priority else "medium"
        
        # Create goal object
        goal = Goal(
            goal_id=str(uuid.uuid4()),
            user_id=user_id,
            goal_type=GoalType(goal_type.lower()),
            name=name,
            target_amount=target_amount,
            current_amount=current_amount,
            deadline=deadline_dt,
            priority=Priority(priority_val.lower()),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Insert into database
        result = db.goals.insert_one(goal.to_dict())
        
        if result.inserted_id:
            return {
                "success": True,
                "message": f"Goal '{name}' created successfully!",
                "goal_id": goal.goal_id,
                "goal": {
                    "name": name,
                    "type": goal_type,
                    "target_amount": target_amount,
                    "current_amount": current_amount,
                    "deadline": deadline,
                    "priority": priority_val,
                    "progress_percentage": goal.progress_percentage()
                }
            }
        else:
            return {
                "success": False,
                "message": "Failed to create goal",
                "error": "Database insertion failed"
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
            "message": "Error creating goal",
            "error": str(e)
        }


def get_goal(goal_id: Optional[str]) -> Dict[str, Any]:
    """
    Retrieve financial goal(s).
    
    Args:
        goal_id: Optional specific goal ID. If None, returns all goals.
    
    Returns:
        Dictionary with goal information or list of goals
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        if goal_id:
            # Get specific goal
            goal_data = db.goals.find_one({
                "user_id": user_id,
                "goal_id": goal_id
            })
            
            if goal_data:
                goal = Goal(**goal_data)
                return {
                    "success": True,
                    "goal": {
                        "goal_id": goal.goal_id,
                        "name": goal.name,
                        "type": goal.goal_type,
                        "target_amount": goal.target_amount,
                        "current_amount": goal.current_amount,
                        "deadline": goal.deadline.isoformat(),
                        "priority": goal.priority,
                        "progress_percentage": goal.progress_percentage(),
                        "created_at": goal.created_at.isoformat(),
                        "updated_at": goal.updated_at.isoformat()
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"Goal with ID '{goal_id}' not found"
                }
        else:
            # Get all goals
            goals_cursor = db.goals.find({"user_id": user_id}).sort("created_at", -1)
            goals_list = []
            
            for goal_data in goals_cursor:
                goal = Goal(**goal_data)
                goals_list.append({
                    "goal_id": goal.goal_id,
                    "name": goal.name,
                    "type": goal.goal_type,
                    "target_amount": goal.target_amount,
                    "current_amount": goal.current_amount,
                    "deadline": goal.deadline.isoformat(),
                    "priority": goal.priority,
                    "progress_percentage": goal.progress_percentage(),
                    "created_at": goal.created_at.isoformat()
                })
            
            return {
                "success": True,
                "count": len(goals_list),
                "goals": goals_list
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": "Error retrieving goals",
            "error": str(e)
        }


def update_goal_progress(goal_id: str, amount_to_add: float) -> Dict[str, Any]:
    """
    Update progress on a financial goal.
    
    Args:
        goal_id: Goal identifier
        amount_to_add: Amount to add to current progress
    
    Returns:
        Dictionary with updated goal information
    """
    try:
        db = get_database()
        user_id = os.getenv('USER_ID', 'default_user')
        
        # Get current goal
        goal_data = db.goals.find_one({
            "user_id": user_id,
            "goal_id": goal_id
        })
        
        if not goal_data:
            return {
                "success": False,
                "message": f"Goal with ID '{goal_id}' not found"
            }
        
        goal = Goal(**goal_data)
        new_amount = goal.current_amount + amount_to_add
        
        # Update goal
        result = db.goals.update_one(
            {"user_id": user_id, "goal_id": goal_id},
            {
                "$set": {
                    "current_amount": new_amount,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            goal.current_amount = new_amount
            return {
                "success": True,
                "message": f"Goal progress updated! Added ${amount_to_add:.2f}",
                "goal": {
                    "goal_id": goal.goal_id,
                    "name": goal.name,
                    "current_amount": new_amount,
                    "target_amount": goal.target_amount,
                    "progress_percentage": goal.progress_percentage()
                }
            }
        else:
            return {
                "success": False,
                "message": "Failed to update goal progress"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": "Error updating goal progress",
            "error": str(e)
        }
