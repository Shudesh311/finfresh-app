from fastapi import APIRouter, Depends, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta
from bson import ObjectId
from app.database import transactions
from utils.auth_middleware import get_current_user

router = APIRouter(prefix="/summary", tags=["summary"])

@router.get("/")
async def get_summary(current_user: dict = Depends(get_current_user)):
    """Get monthly financial summary"""
    
    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    # Get current month's start and end dates
    today = datetime.now()
    month_start = datetime(today.year, today.month, 1)
    
    if today.month == 12:
        month_end = datetime(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
    
    # Get all transactions for current month
    monthly_transactions = list(transactions.find({
        "userId": ObjectId(current_user["userId"]),
        "date": {"$gte": month_start, "$lte": month_end}
    }))
    
    # Calculate totals
    total_income = 0
    total_expense = 0
    total_investment = 0
    total_debt = 0
    categories = defaultdict(float)
    
    for t in monthly_transactions:
        amount = t["amount"]
        categories[t["category"]] += amount
        
        if t["type"] == "income":
            total_income += amount
        elif t["type"] == "expense":
            total_expense += amount
        elif t["type"] == "investment":
            total_investment += amount
        elif t["type"] == "debt":
            total_debt += amount
    
    savings = total_income - (total_expense + total_debt)
    
    # Calculate savings rate
    if total_income > 0:
        savings_rate = round((savings / total_income) * 100, 1)
    else:
        savings_rate = 0
    
    return {
        "income": total_income,
        "expense": total_expense,
        "investment": total_investment,
        "debt": total_debt,
        "savings": savings,
        "savingsRate": savings_rate,
        "categories": dict(categories)
    }