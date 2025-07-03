import mysql.connector
con = mysql.connector.connect(
    user = 'root',
    host = 'localhost',
    passwd = 'mabelmanuel'
)
print(con)
cur = con.cursor()

cur.execute("CREATE database USERSDB;")
con.commit()

print("Database created successfully")
