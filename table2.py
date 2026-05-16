import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect('whatsapp_messages.db')

# Create a cursor object to execute SQL
cursor = conn.cursor()

cursor.execute("SELECT * FROM messages")
rows = cursor.fetchall()

for row in rows:
    print(row)



# Commit and close
conn.commit()
conn.close()

print("Tab.")
