import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect('whatsapp_messages.db')

# Create a cursor object to execute SQL
cursor = conn.cursor()

selected_user = "Prakhar Nagaich"

# Create table (if it doesn't exist)
cursor.execute("SELECT message, direction, timestamp FROM messages WHERE name = ? ORDER BY timestamp DESC", (selected_user,))
chat = cursor.fetchall()

for msg, time, direction in chat:
        if direction == "incoming":
            print(f"🟢 **{selected_user}** ({time}): {msg}")
        else:
            print(f"🔵 **Yo2u** ({time}): {msg}")


# Commit and close
conn.commit()
conn.close()

print("Table created successfully.")
