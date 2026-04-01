# FinFresh - Personal Finance Tracker

A complete personal finance management application that helps users track their income, expenses, investments, debt, and overall financial health.

## 🚀 Project Overview

FinFresh is a 3-tier application that allows users to:
- Register and login securely with JWT authentication
- Record income, expense, investment, and debt transactions
- View monthly financial summaries with category breakdowns
- Get a comprehensive financial health score (0-100)
- Receive actionable suggestions to improve financial wellness

## 📋 Table of Contents
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Features](#features)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Design Decisions](#design-decisions)
- [Error Handling](#error-handling)
- [Future Improvements](#future-improvements)

## 🛠 Tech Stack

| Tier | Technology | Version | Purpose |
|------|------------|---------|---------|
| **Frontend** | Next.js | 14.2.0 | Modern React framework with App Router |
| | TypeScript | 5.0+ | Type safety and better developer experience |
| | Pure CSS | - | Custom styling without frameworks |
| **Backend** | FastAPI | 0.104.1 | High-performance Python web framework |
| | Python | 3.8+ | Clean, readable backend code |
| **Database** | MongoDB Atlas | 6.0+ | Flexible NoSQL database |
| | PyMongo | 4.5.0 | Official MongoDB Python driver |


## ✨ Features

### ✅ Authentication
- User registration with username and email
- Login with either username OR email
- JWT-based authentication (30-minute expiry)
- Password hashing with bcrypt
- Protected routes with token verification
- Automatic redirect on token expiry

### ✅ Transaction Management
- Create transactions (income, expense, investment, debt)
- View paginated transaction history
- Delete transactions with confirmation
- Filter by type and category
- Date range filtering
- Safe number parsing (handles strings, nulls, missing values)

### ✅ Financial Dashboard
- **Summary Cards**: Monthly income, expenses, savings, savings rate
- **Savings Rate**: Calculated as (savings / income) × 100
- **Category Breakdown**: Visual progress bars for top spending categories
- **Financial Health Score**: Comprehensive 0-100 score

### ✅ Financial Health Score Algorithm
| Component | Max Points | Calculation | Target |
|-----------|------------|-------------|--------|
| Emergency Fund | 25 | monthsCoverage = totalSavings / monthlyExpenses | >6 months |
| Savings Rate | 25 | (monthlySavings / monthlyIncome) × 100 | >40% |
| Debt Ratio | 25 | (monthlyDebt / monthlyIncome) × 100 | <10% |
| Investment Ratio | 25 | (monthlyInvestment / monthlyIncome) × 100 | >30% |

**Score Categories:**
- 80-100: Excellent 🏆
- 60-79: Healthy ✅
- 40-59: Moderate ⚠️
- <40: At Risk 🔴

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- MongoDB Atlas account
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/finfresh-app.git
cd finfresh-app
cd api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your MongoDB credentials

# Run the server
uvicorn app.main:app --reload --port 8000
cd ../frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
# Edit .env.local if needed (default: http://localhost:8000)

# Run development server
npm run dev
Step 4: Access Application
Frontend: http://localhost:3000

Backend API: http://localhost:8000

API Documentation: http://localhost:8000/docs

📡 API Endpoints
Authentication
Method	Endpoint	Description	Auth Required
POST	/auth/register	Register new user	No
POST	/auth/login	Login with email/username	No
Transactions
Method	Endpoint	Description	Auth Required
POST	/transactions/	Create transaction	Yes
GET	/transactions/	List transactions (paginated)	Yes
GET	/transactions/{id}	Get single transaction	Yes
PUT	/transactions/{id}	Update transaction	Yes
DELETE	/transactions/{id}	Delete transaction	Yes
Summary & Health
Method	Endpoint	Description	Auth Required
GET	/summary/	Monthly financial summary	Yes
GET	/financial-health/	Financial health score	Yes
📁 Project Structure
api/
├── app/
│   ├── __init__.py
│   ├── database.py          # MongoDB connection with indexes
│   ├── main.py              # FastAPI app configuration
│   ├── models.py            # Pydantic models with validation
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # Register/Login endpoints
│       ├── transactions.py  # CRUD operations
│       ├── summary.py       # Monthly summary
│       ├── health.py        # Health score algorithm
│       └── goals.py         # Goals management (optional)
├── utils/
│   ├── __init__.py
│   ├── security.py          # Password hashing (bcrypt)
│   ├── jwt_handler.py       # JWT create/decode
│   └── auth_middleware.py   # Auth dependency
├── .env.example
├── requirements.txt
└── README.md


frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── SummaryCard.tsx          # Stats cards
│   │   │   ├── HealthScoreCard.tsx      # Health score display
│   │   │   ├── CategoryBreakdown.tsx    # Spending by category
│   │   │   ├── TransactionList.tsx      # Transaction list
│   │   │   ├── LoadingState.tsx         # Loading spinner
│   │   │   ├── ErrorState.tsx           # Error display
│   │   │   └── EmptyState.tsx           # Empty state
│   │   ├── login/
│   │   │   └── page.tsx                 # Login/Register page
│   │   ├── dashboard/
│   │   │   └── page.tsx                 # Dashboard page
│   │   ├── transactions/
│   │   │   └── page.tsx                 # Transactions page
│   │   ├── layout.tsx                   # Root layout
│   │   ├── globals.css                  # Global styles
│   │   └── page.tsx                     # Landing redirect
│   ├── lib/
│   │   ├── api.ts                       # API service with interceptors
│   │   └── auth.ts                      # Auth helpers
│   ├── types/
│   │   └── index.ts                     # TypeScript interfaces
│   └── utils/
│       └── formatters.ts                # Currency/date formatting
├── .env.local.example
├── package.json
└── README.md
