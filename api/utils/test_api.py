# test_api.py
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_api():
    print("=" * 50)
    print("Testing FinFresh API")
    print("=" * 50)
    
    # 1. Register a user
    print("\n1. Registering user...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 2. Login
    print("\n2. Logging in...")
    login_data = {
        "login": "test@example.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    token = result.get("token")
    print(f"Token obtained: {token[:50]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Add income transaction
    print("\n3. Adding income...")
    income = {
        "amount": 50000,
        "category": "Salary",
        "type": "income",
        "date": datetime.now().isoformat(),
        "description": "Monthly salary"
    }
    response = requests.post(f"{BASE_URL}/transactions/", json=income, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 4. Add expenses
    print("\n4. Adding expenses...")
    expenses = [
        {"amount": 15000, "category": "Rent", "type": "expense", "date": datetime.now().isoformat()},
        {"amount": 5000, "category": "Food", "type": "expense", "date": datetime.now().isoformat()},
        {"amount": 2000, "category": "Transport", "type": "expense", "date": datetime.now().isoformat()},
        {"amount": 3000, "category": "Shopping", "type": "expense", "date": datetime.now().isoformat()}
    ]
    
    for expense in expenses:
        response = requests.post(f"{BASE_URL}/transactions/", json=expense, headers=headers)
        print(f"Added {expense['category']}: {response.status_code}")
    
    # 5. Get all transactions
    print("\n5. Getting all transactions...")
    response = requests.get(f"{BASE_URL}/transactions/", headers=headers)
    result = response.json()
    print(f"Total transactions: {result['count']}")
    
    # 6. Get overview
    print("\n6. Getting monthly overview...")
    response = requests.get(f"{BASE_URL}/summary/overview", headers=headers)
    result = response.json()
    data = result['data']
    print(f"Month: {data['month']}")
    print(f"Total Income: ₹{data['total_income']}")
    print(f"Total Expense: ₹{data['total_expense']}")
    print(f"Net Savings: ₹{data['net_savings']}")
    print(f"Savings Rate: {data['savings_rate']}%")
    
    # 7. Get health score
    print("\n7. Getting financial health score...")
    response = requests.get(f"{BASE_URL}/summary/health-score", headers=headers)
    result = response.json()
    data = result['data']
    print(f"Score: {data['score']}/100")
    print(f"Rating: {data['rating']}")
    print(f"Message: {data['message']}")
    
    # 8. Get historical data
    print("\n8. Getting historical data...")
    response = requests.get(f"{BASE_URL}/summary/historical?months=3", headers=headers)
    result = response.json()
    data = result['data']
    print(f"Months: {data['months']}")
    print(f"Income: {data['income']}")
    print(f"Expense: {data['expense']}")
    
    print("\n" + "=" * 50)
    print("✅ API Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_api()