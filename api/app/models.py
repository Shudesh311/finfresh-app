from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"
    DEBT = "debt"

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str
    password: str = Field(..., min_length=6)
    
    @validator('email')
    def validate_email(cls, v):
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower().strip()

class UserLogin(BaseModel):
    login: str
    password: str

class TransactionCreate(BaseModel):
    type: TransactionType
    category: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    date: date
    description: Optional[str] = Field(None, max_length=500)

class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=500)

class GoalCreate(BaseModel):
    goalName: str = Field(..., min_length=1, max_length=100)
    targetAmount: float = Field(..., gt=0)
    currentAmount: float = Field(0, ge=0)
    targetDate: date

class GoalResponse(BaseModel):
    id: str
    userId: str
    goalName: str
    targetAmount: float
    currentAmount: float
    targetDate: date
    createdAt: datetime
    progress: float