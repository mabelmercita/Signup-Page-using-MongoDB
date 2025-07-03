from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['usersdb']
users = db['users']

# Insert dummy data
users.insert_one({
    "username": "mabel",
    "password": "test123",
    "name": "Mabel Mercita",
    "age": 20,
    "dob": "2005-08-21",
    "contact": "9876543210",
    "email": "mabel@example.com"
})

print("Inserted! Now check MongoDB Compass 👀")
