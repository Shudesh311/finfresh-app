from fastapi import APIRouter, Depends, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta
from bson import ObjectId
from app.database import transactions
from utils.auth_middleware import get_current_user

router = APIRouter(prefix="/financial-health", tags=["financial-health"])

def calculate_emergency_fund(all_transactions):
    """Calculate emergency fund score (max 25 pts)"""
    
    # Calculate total savings
    total_income = sum(t["amount"] for t in all_transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in all_transactions if t["type"] == "expense")
    total_savings = total_income - total_expense
    
    # Calculate average monthly expense over last 3 months
    three_months_ago = datetime.now() - timedelta(days=90)
    recent_expenses = [
        t["amount"] for t in all_transactions 
        if t["type"] == "expense" and t["date"] >= three_months_ago
    ]
    
    monthly_expense = sum(recent_expenses) / 3 if recent_expenses else 1
    
    if monthly_expense == 0:
        return 25
    
    months_coverage = total_savings / monthly_expense
    
    if months_coverage > 6:
        return 25
    elif months_coverage >= 3:
        return 20
    elif months_coverage >= 1:
        return 10
    else:
        return 5

def calculate_savings_rate(monthly_income, monthly_expense, monthly_debt):
    """Calculate savings rate score (max 25 pts)"""
    monthly_savings = monthly_income - (monthly_expense + monthly_debt)
    
    if monthly_income == 0:
        return 5
    
    savings_rate = (monthly_savings / monthly_income) * 100
    
    if savings_rate > 40:
        return 25
    elif savings_rate >= 20:
        return 20
    elif savings_rate >= 10:
        return 10
    else:
        return 5

def calculate_debt_ratio(monthly_income, monthly_debt):
    """Calculate debt ratio score (max 25 pts)"""
    if monthly_income == 0:
        return 5
    
    debt_ratio = (monthly_debt / monthly_income) * 100
    
    if debt_ratio < 10:
        return 25
    elif debt_ratio <= 30:
        return 20
    elif debt_ratio <= 50:
        return 10
    else:
        return 5

def calculate_investment_ratio(monthly_income, monthly_investment):
    """Calculate investment ratio score (max 25 pts)"""
    if monthly_income == 0:
        return 5
    
    investment_ratio = (monthly_investment / monthly_income) * 100
    
    if investment_ratio > 30:
        return 25
    elif investment_ratio >= 15:
        return 20
    elif investment_ratio >= 5:
        return 10
    else:
        return 5

def get_suggestions(components):
    """Generate suggestions based on component scores"""
    suggestions = []
    
    if components["emergencyFund"] < 20:
        suggestions.append("Increase your emergency fund to cover at least 6 months of expenses")
    
    if components["savingsRate"] < 20:
        suggestions.append("Try to save at least 20% of your income each month")
    
    if components["debtRatio"] < 20:
        suggestions.append("Work on reducing your debt-to-income ratio to below 30%")
    
    if components["investmentRatio"] < 20:
        suggestions.append("Consider increasing your investment contributions to at least 15% of income")
    
    if not suggestions:
        suggestions.append("Great job! Keep maintaining your healthy financial habits")
    
    return suggestions

@router.get("/")
async def get_financial_health(current_user: dict = Depends(get_current_user)):
    """Calculate financial health score"""
    
    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    # Get current month's transactions
    today = datetime.now()
    month_start = datetime(today.year, today.month, 1)
    
    if today.month == 12:
        month_end = datetime(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
    
    monthly_transactions = list(transactions.find({
        "userId": ObjectId(current_user["userId"]),
        "date": {"$gte": month_start, "$lte": month_end}
    }))
    
    # Get all transactions for emergency fund calculation
    all_transactions = list(transactions.find({
        "userId": ObjectId(current_user["userId"])
    }))
    
    # Calculate monthly totals
    monthly_income = sum(t["amount"] for t in monthly_transactions if t["type"] == "income")
    monthly_expense = sum(t["amount"] for t in monthly_transactions if t["type"] == "expense")
    monthly_debt = sum(t["amount"] for t in monthly_transactions if t["type"] == "debt")
    monthly_investment = sum(t["amount"] for t in monthly_transactions if t["type"] == "investment")
    
    # Calculate component scores
    emergency_fund_score = calculate_emergency_fund(all_transactions)
    savings_rate_score = calculate_savings_rate(monthly_income, monthly_expense, monthly_debt)
    debt_ratio_score = calculate_debt_ratio(monthly_income, monthly_debt)
    investment_ratio_score = calculate_investment_ratio(monthly_income, monthly_investment)
    
    # Calculate total score
    total_score = emergency_fund_score + savings_rate_score + debt_ratio_score + investment_ratio_score
    
    # Determine category
    if total_score >= 80:
        category = "Excellent"
    elif total_score >= 60:
        category = "Healthy"
    elif total_score >= 40:
        category = "Moderate"
    else:
        category = "At Risk"
    
    # Get suggestions
    suggestions = get_suggestions({
        "emergencyFund": emergency_fund_score,
        "savingsRate": savings_rate_score,
        "debtRatio": debt_ratio_score,
        "investmentRatio": investment_ratio_score
    })
    
    return {
        "score": total_score,
        "category": category,
        "breakdown": {
            "emergencyFund": emergency_fund_score,
            "savingsRate": savings_rate_score,
            "debtRatio": debt_ratio_score,
            "investmentRatio": investment_ratio_score
        },
        "suggestions": suggestions
    }