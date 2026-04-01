from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from bson import ObjectId
from app.database import goals
from app.models import GoalCreate, GoalResponse
from utils.auth_middleware import get_current_user

router = APIRouter(prefix="/goals", tags=["goals"])

def goal_helper(goal):
    """Helper function to convert MongoDB document to response"""
    progress = (goal["currentAmount"] / goal["targetAmount"]) * 100 if goal["targetAmount"] > 0 else 0
    
    return {
        "id": str(goal["_id"]),
        "userId": str(goal["userId"]),
        "goalName": goal["goalName"],
        "targetAmount": goal["targetAmount"],
        "currentAmount": goal["currentAmount"],
        "targetDate": goal["targetDate"],
        "createdAt": goal["createdAt"],
        "progress": round(progress, 2)
    }

@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal: GoalCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new financial goal"""
    
    if goals is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    goal_dict = goal.dict()
    goal_dict.update({
        "userId": ObjectId(current_user["userId"]),
        "createdAt": datetime.utcnow()
    })
    
    try:
        result = goals.insert_one(goal_dict)
        created_goal = goals.find_one({"_id": result.inserted_id})
        return goal_helper(created_goal)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[GoalResponse])
async def get_goals(current_user: dict = Depends(get_current_user)):
    """Get all goals for the authenticated user"""
    
    if goals is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    all_goals = list(goals.find({
        "userId": ObjectId(current_user["userId"])
    }).sort("targetDate", 1))
    
    return [goal_helper(g) for g in all_goals]

@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: str,
    goal_update: GoalCreate,
    current_user: dict = Depends(get_current_user)
):
    """Update a goal"""
    
    if goals is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    if not ObjectId.is_valid(goal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid goal ID"
        )
    
    existing = goals.find_one({
        "_id": ObjectId(goal_id),
        "userId": ObjectId(current_user["userId"])
    })
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    update_data = goal_update.dict()
    
    try:
        goals.update_one(
            {"_id": ObjectId(goal_id)},
            {"$set": update_data}
        )
        
        updated = goals.find_one({"_id": ObjectId(goal_id)})
        return goal_helper(updated)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a goal"""
    
    if goals is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    if not ObjectId.is_valid(goal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid goal ID"
        )
    
    result = goals.delete_one({
        "_id": ObjectId(goal_id),
        "userId": ObjectId(current_user["userId"])
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    return None