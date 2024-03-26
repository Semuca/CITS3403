import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()

# Create users table
cursor.execute("CREATE TABLE users(username, passwordHash)")