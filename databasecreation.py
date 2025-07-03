import mysql.connector

con = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd='mabelmanuel'
)
cur = con.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS USERSDB;")
con.commit()
print("Database created successfully")
con.close()

con = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd='mabelmanuel',
    database='USERSDB'
)
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(255),
    age INT,
    dob DATE,
    contact VARCHAR(15),
    email VARCHAR(50)
);''')

con.commit()
print("Table created successfully")

con.close()
