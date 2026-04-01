from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional, List
from datetime import datetime, date
from bson import ObjectId
from app.database import transactions
from app.models import TransactionCreate, TransactionUpdate, TransactionType
from utils.auth_middleware import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

def transaction_helper(transaction):
    """Helper function to convert MongoDB document to response"""
    return {
        "id": str(transaction["_id"]),
        "userId": str(transaction["userId"]),
        "type": transaction["type"],
        "category": transaction["category"],
        "amount": transaction["amount"],
        "date": transaction["date"],
        "description": transaction.get("description"),
        "createdAt": transaction["createdAt"]
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new transaction"""
    
    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    transaction_dict = transaction.dict()
    transaction_dict.update({
        "userId": ObjectId(current_user["userId"]),
        "createdAt": datetime.utcnow()
    })
    
    try:
        result = transactions.insert_one(transaction_dict)
        created = transactions.find_one({"_id": result.inserted_id})
        return transaction_helper(created)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/")
async def get_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    type: Optional[TransactionType] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all transactions with pagination and filters"""
    
    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    query = {"userId": ObjectId(current_user["userId"])}
    
    if type:
        query["type"] = type.value
    
    if category:
        query["category"] = category
    
    if start_date or end_date:
        date_filter = {}
        if start_date:
            date_filter["$gte"] = datetime.combine(start_date, datetime.min.time())
        if end_date:
            date_filter["$lte"] = datetime.combine(end_date, datetime.max.time())
        if date_filter:
            query["date"] = date_filter
    
    try:
        total = transactions.count_documents(query)
        skip = (page - 1) * limit
        all_transactions = list(transactions.find(query)
                               .sort("date", -1)
                               .skip(skip)
                               .limit(limit))
        
        return {
            "data": [transaction_helper(t) for t in all_transactions],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific transaction by ID"""
    
    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    if not ObjectId.is_valid(transaction_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID"
        )
    
    transaction = transactions.find_one({
        "_id": ObjectId(transaction_id),
        "userId": ObjectId(current_user["userId"])
    })
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction_helper(transaction)

@router.put("/{transaction_id}")
async def update_transaction(
    transaction_id: str,
    transaction_update: TransactionUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a transaction"""
    
    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    if not ObjectId.is_valid(transaction_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID"
        )
    
    existing = transactions.find_one({
        "_id": ObjectId(transaction_id),
        "userId": ObjectId(current_user["userId"])
    })
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    update_data = {}
    for key, value in transaction_update.dict().items():
        if value is not None:
            update_data[key] = value
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    try:
        transactions.update_one(
            {"_id": ObjectId(transaction_id)},
            {"$set": update_data}
        )
        
        updated = transactions.find_one({"_id": ObjectId(transaction_id)})
        return transaction_helper(updated)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a transaction"""
    
    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    if not ObjectId.is_valid(transaction_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID"
        )
    
    result = transactions.delete_one({
        "_id": ObjectId(transaction_id),
        "userId": ObjectId(current_user["userId"])
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return None