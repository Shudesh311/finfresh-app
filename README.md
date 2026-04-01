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
 Design Decisions
Why FastAPI over Django/Flask?
Performance: FastAPI is one of the fastest Python frameworks, on par with Node.js and Go

Type Safety: Built-in Pydantic validation ensures data integrity

Documentation: Automatic OpenAPI/Swagger docs reduce manual work

Async Support: Native async/await for better I/O performance

Developer Experience: Intuitive, modern, and well-documented

Why Next.js over Create React App?
App Router: Modern routing with layouts and nested routes

Server Components: Better performance and SEO

TypeScript: First-class support

Developer Experience: Fast refresh, great tooling

File-based Routing: Clean and intuitive

Why MongoDB over PostgreSQL?
Flexible Schema: Easy to evolve data model as requirements change

JSON Documents: Natural mapping to Python dicts and JavaScript objects

Scalability: Horizontal scaling with sharding

Atlas: Managed cloud service with free tier

Why Pure CSS over Tailwind?
No Build Issues: Avoids Tailwind configuration problems

Full Control: Every style is explicit and traceable

Smaller Bundle: No CSS framework overhead

Easier Debugging: Styles are where you expect them

🔧 Error Handling
Frontend
Loading States: Spinner while data loads

Error States: Friendly messages with retry buttons

Empty States: Guidance when no data exists

Number Parsing: Safe conversion (null, undefined, strings → 0)

Form Validation: Client-side email/password validation

Backend
HTTP Status Codes: Proper codes (200, 201, 400, 401, 404, 422, 500)

Error Messages: Clear, actionable error details

Validation: Pydantic models with custom validators

Database Errors: Graceful handling with appropriate responses

🚀 Future Improvements
With more time, I would add:

Security
Refresh tokens for better security

HTTP-only cookies instead of localStorage

Rate limiting on auth endpoints

Email verification on registration

Features
Transaction editing

Budget goals and tracking

Spending charts with Chart.js

Date range filters for transactions

Export to CSV/PDF

Recurring transactions

Dark mode

PWA support for mobile

Performance
Redis caching for frequently accessed data

Database query optimization

Image optimization for charts

Service workers for offline support

Testing
Unit tests for all components

Integration tests for API

End-to-end tests with Cypress

Load testing for performance

📝 License
MIT

👨‍💻 Author
Your Name

🙏 Acknowledgments
FinFresh Team for the challenge

FastAPI and Next.js communities for excellent documentation

MongoDB Atlas for free tier database hosting

Made with ❤️ for FinFresh Technical Challenge

text

## File 2: **api/README.md** (Save in `finfresh-app/api/`)

```markdown
# FinFresh API - Backend Documentation

## Overview
RESTful API for FinFresh personal finance tracker built with FastAPI and MongoDB.

## Tech Stack
- **Framework**: FastAPI 0.104.1
- **Database**: MongoDB Atlas
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Python**: 3.8+

## API Endpoints

### Authentication

#### POST /auth/register
Register a new user.

**Request:**
```json
{
  "name": "Arun Kumar",
  "email": "arun@example.com",
  "password": "securepassword"
}
Response (201):

json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "65f8a2b2c3d4e5f6a7b8c9d0",
    "name": "Arun Kumar",
    "email": "arun@example.com",
    "createdAt": "2026-04-01T10:00:00Z"
  }
}
Errors:

400: Email already registered

400: Username already taken

422: Validation failed

POST /auth/login
Login with email or username.

Request:

json
{
  "login": "arun@example.com",
  "password": "securepassword"
}
Response (200):

json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "65f8a2b2c3d4e5f6a7b8c9d0",
    "name": "Arun Kumar",
    "email": "arun@example.com",
    "createdAt": "2026-04-01T10:00:00Z"
  }
}
Errors:

401: Invalid credentials

Transactions
POST /transactions
Create a new transaction (requires authentication).

Request:

json
{
  "type": "expense",
  "category": "Food",
  "amount": 1200,
  "date": "2026-01-10",
  "description": "Lunch with team"
}
Response (201):

json
{
  "id": "65f8a2b2c3d4e5f6a7b8c9d1",
  "userId": "65f8a2b2c3d4e5f6a7b8c9d0",
  "type": "expense",
  "category": "Food",
  "amount": 1200,
  "date": "2026-01-10",
  "description": "Lunch with team",
  "createdAt": "2026-04-01T10:05:00Z"
}
Errors:

400: Validation failed

401: Unauthenticated

GET /transactions
Get paginated list of transactions.

Query Parameters:

Parameter	Type	Default	Description
page	integer	1	Page number
limit	integer	20	Items per page (max 100)
type	string	-	Filter by type
category	string	-	Filter by category
start_date	date	-	Filter by start date
end_date	date	-	Filter by end date
Response (200):

json
{
  "data": [
    {
      "id": "...",
      "type": "expense",
      "category": "Food",
      "amount": 1200,
      "date": "2026-01-10",
      "description": "Lunch"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 143,
    "pages": 8
  }
}
DELETE /transactions/{id}
Delete a transaction.

Response (204): No content

Summary
GET /summary
Get monthly financial summary.

Response (200):

json
{
  "income": 80000,
  "expense": 52000,
  "investment": 5000,
  "debt": 3000,
  "savings": 20000,
  "savingsRate": 25.0,
  "categories": {
    "Housing": 20000,
    "Food": 12000,
    "Transport": 6000,
    "Entertainment": 4000
  }
}
Financial Health Score
GET /financial-health
Calculate comprehensive financial health score.

Algorithm:

The score ranges from 0-100, split equally across four components (25 points each):

Emergency Fund (0-25 pts)

Months coverage = totalSavings / monthlyExpenses

6 months: 25 pts

3-6 months: 20 pts

1-3 months: 10 pts

<1 month: 5 pts

Savings Rate (0-25 pts)

Rate = (monthlySavings / monthlyIncome) × 100

40%: 25 pts

20-40%: 20 pts

10-20%: 10 pts

<10%: 5 pts

Debt Ratio (0-25 pts)

Ratio = (monthlyDebt / monthlyIncome) × 100

<10%: 25 pts

10-30%: 20 pts

30-50%: 10 pts

50%: 5 pts

Investment Ratio (0-25 pts)

Ratio = (monthlyInvestment / monthlyIncome) × 100

30%: 25 pts

15-30%: 20 pts

5-15%: 10 pts

<5%: 5 pts

Score Categories:

80-100: Excellent

60-79: Healthy

40-59: Moderate

<40: At Risk

Response (200):

json
{
  "score": 74,
  "category": "Healthy",
  "breakdown": {
    "emergencyFund": 20,
    "savingsRate": 20,
    "debtRatio": 20,
    "investmentRatio": 14
  },
  "suggestions": [
    "Increase your emergency fund to cover at least 6 months of expenses",
    "Consider increasing your investment contributions"
  ]
}
MongoDB Schema
Users Collection
json
{
  "_id": ObjectId,
  "name": String,
  "email": String (unique, indexed),
  "passwordHash": String,
  "createdAt": Date
}
Transactions Collection
json
{
  "_id": ObjectId,
  "userId": ObjectId (indexed),
  "type": String (income, expense, investment, debt),
  "category": String,
  "amount": Number,
  "date": Date (indexed),
  "description": String (optional),
  "createdAt": Date
}
Indexes
transactions: { userId: 1, date: -1 } - Most common query pattern

transactions: { userId: 1, type: 1 } - Filter by type

users: { email: 1 } (unique) - Fast user lookup

Environment Variables
Create .env file from .env.example:

env
# Required
MONGODB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/finfresh

# Optional (defaults shown)
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
Setup Instructions
bash
# Clone repository
git clone <repo-url>
cd api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your MongoDB credentials

# Run server
uvicorn app.main:app --reload --port 8000
Testing with curl
bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"123456"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"login":"test@example.com","password":"123456"}'

# Create transaction (use token from login)
curl -X POST http://localhost:8000/transactions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"type":"expense","category":"Food","amount":1200,"date":"2026-01-10"}'

# Get summary
curl -X GET http://localhost:8000/summary/ \
  -H "Authorization: Bearer <your-token>"

# Get health score
curl -X GET http://localhost:8000/financial-health/ \
  -H "Authorization: Bearer <your-token>"
Error Handling
Status	Meaning
200	Success
201	Created
400	Bad Request (validation error)
401	Unauthorized
404	Not Found
422	Unprocessable Entity
500	Internal Server Error
Edge Cases Handled
Zero income → Savings Rate, Debt Ratio, Investment Ratio return 0 pts

No transactions → Emergency Fund scores minimum (5 pts)

Zero expenses → Emergency Fund scores maximum (25 pts)

Negative amounts → Clamped to 0

String numbers → Parsed safely

What I'd Improve
Add refresh tokens

Implement rate limiting

Add Redis caching

Add unit tests with pytest

Dockerize the application

Add CI/CD pipeline

text

## File 3: **frontend/README.md** (Save in `finfresh-app/frontend/`)

```markdown
# FinFresh Frontend - Next.js Application

## Overview
Modern, responsive personal finance dashboard built with Next.js 14 and pure CSS. The application provides a seamless user experience for tracking income, expenses, and financial health.

## Tech Stack
- **Framework**: Next.js 14.2.0 (App Router)
- **Language**: TypeScript 5.0+
- **Styling**: Pure CSS
- **HTTP Client**: Fetch API
- **Notifications**: React Hot Toast

## Screens

### Screen 1: Login / Register

**Features:**
- Single page toggle between login and register modes
- Login with username OR email
- Client-side validation
- Loading states during API calls
- Error messages displayed inline
- Secure JWT storage in localStorage
- Automatic redirect on success

**Validation:**
- Email format: `name@example.com`
- Password: minimum 6 characters
- Username: minimum 2 characters

### Screen 2: Dashboard

**Components:**
1. **Summary Cards**
   - Monthly Income
   - Monthly Expenses
   - Net Savings
   - Savings Rate (%)

2. **Financial Health Score**
   - Circular score indicator (0-100)
   - Category badge (Excellent/Healthy/Moderate/At Risk)
   - Component breakdown (4 parts, 25 pts each)
   - Personalized suggestions

3. **Category Breakdown**
   - Top 5 spending categories
   - Visual progress bars
   - Percentage of total expenses

**States Handled:**
- Loading: Spinner animation
- Error: Error message with retry button
- Empty: "No transactions found" message
- Zero Income: Savings Rate displays 0%

### Screen 3: Transactions

**Features:**
- Paginated list of transactions
- Add new transaction form
- Delete transactions with confirmation
- Summary cards for total income and expense
- Empty state for no transactions

**Transaction Display:**
- Date (formatted)
- Category badge
- Description (if available)
- Amount with +/- sign and color coding

## Component Structure
src/
├── app/
│ ├── components/
│ │ ├── SummaryCard.tsx # Financial summary cards
│ │ ├── HealthScoreCard.tsx # Health score display
│ │ ├── CategoryBreakdown.tsx # Spending by category
│ │ ├── TransactionList.tsx # Transaction list
│ │ ├── LoadingState.tsx # Loading spinner
│ │ ├── ErrorState.tsx # Error display
│ │ └── EmptyState.tsx # Empty state message
│ ├── login/
│ │ └── page.tsx # Login/Register page
│ ├── dashboard/
│ │ └── page.tsx # Dashboard page
│ ├── transactions/
│ │ └── page.tsx # Transactions page
│ ├── layout.tsx # Root layout
│ ├── globals.css # Global styles
│ └── page.tsx # Landing redirect
├── lib/
│ ├── api.ts # API service
│ └── auth.ts # Authentication helpers
├── types/
│ └── index.ts # TypeScript interfaces
└── utils/
└── formatters.ts # Currency/date formatting

text

## API Integration

### Centralized API Service (`lib/api.ts`)

```typescript
class ApiService {
  private async request(endpoint, options) {
    const token = localStorage.getItem('token');
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` })
    };
    // ... fetch implementation
  }
  
  // Auth endpoints
  register(data) { return this.request('/auth/register', { method: 'POST', body: data }) }
  login(data) { return this.request('/auth/login', { method: 'POST', body: data }) }
  
  // Transaction endpoints
  getTransactions(params) { return this.request(`/transactions/?${queryParams}`) }
  createTransaction(data) { return this.request('/transactions/', { method: 'POST', body: data }) }
  deleteTransaction(id) { return this.request(`/transactions/${id}`, { method: 'DELETE' }) }
  
  // Summary endpoints
  getSummary() { return this.request('/summary/') }
  getHealthScore() { return this.request('/financial-health/') }
}
Safe Number Parsing
All numbers are safely parsed to prevent UI crashes:

typescript
export const formatCurrency = (amount: number | string | null | undefined): string => {
  if (amount === null || amount === undefined) return '₹0';
  const num = typeof amount === 'string' ? parseFloat(amount) : amount;
  return isNaN(num) ? '₹0' : new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR'
  }).format(num);
};
Environment Variables
Create .env.local file:

env
NEXT_PUBLIC_API_URL=http://localhost:8000
Setup Instructions
bash
# Clone repository
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
# Edit .env.local if needed

# Run development server
npm run dev
Build for Production
bash
npm run build
npm start
State Management
All screens handle three states:

State	Expected Behaviour
Loading	Show spinner animation
Error	Show error message with retry button
Empty	Show "No data" message with action
Error Handling Strategy
Network Errors: Show "Network error - please check your connection"

API Errors: Parse error message from response

Validation Errors: Show inline messages below fields

Auth Errors: Redirect to login page

Unknown Errors: Show generic error message with retry

Design Decisions
Why Next.js?
App Router: Modern routing with layouts

TypeScript: Type safety

Developer Experience: Fast refresh, great tooling

Performance: Automatic code splitting

Why Pure CSS?
No Build Issues: Avoids configuration problems

Full Control: Every style is explicit

Smaller Bundle: No CSS framework overhead

Easier Debugging: Styles are where you expect them

Why Fetch API?
Native: No additional dependency

Simple: Easy to implement interceptors

Lightweight: Smaller bundle size

Responsive Design
The application is fully responsive and works on:

Desktop (1200px+)

Tablet (768px - 1199px)

Mobile (<768px)

Mobile optimizations:

Stacked layout for stats cards

Touch-friendly buttons

Simplified transaction display

Bottom navigation for mobile

What I'd Improve
Add form validation with react-hook-form

Implement date range filters

Add charts with Chart.js

Add budget tracking

Implement dark mode

Add PWA support

Add offline support

Add transaction editing

Add user profile settings

text

## How to Add These Files:

1. **Root README**: Save as `README.md` in `C:\Users\SHUDESH\Desktop\finfresh-app\`

2. **API README**: Save as `README.md` in `C:\Users\SHUDESH\Desktop\finfresh-app\api\`

3. **Frontend README**: Save as `README.md` in `C:\Users\SHUDESH\Desktop\finfresh-app\frontend\`

Just copy each section into the respective files and save them. These README files will document your entire project professionally!
