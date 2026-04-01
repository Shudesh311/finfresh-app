from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URL", "mongodb+srv://admin:admin123@finfresh-cluster.tsddbzt.mongodb.net/?retryWrites=true&w=majority")

if not MONGO_URL:
    raise ValueError("MONGODB_URL environment variable not set")

print("Connecting to MongoDB...")

client = None
db = None
users = None
transactions = None
goals = None

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ MongoDB connected successfully!")
    
    db = client["finfresh"]
    users = db["users"]
    transactions = db["transactions"]
    goals = db["goals"]
    
    # Create indexes
    try:
        # Users index
        users.create_index("email", unique=True)
        
        # Transactions indexes
        if transactions is not None:
            transactions.create_index([("userId", ASCENDING), ("date", DESCENDING)])
            transactions.create_index([("userId", ASCENDING), ("type", ASCENDING)])
            print("✅ Transaction indexes created")
        
        # Goals indexes
        if goals is not None:
            goals.create_index([("userId", ASCENDING)])
            print("✅ Goals indexes created")
            
    except Exception as e:
        print(f"⚠️ Index creation warning: {e}")
        
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    db = None
    users = None
    transactions = None
    goals = None