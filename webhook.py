from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# You choose this token yourself (must match what you entered in Meta dashboard)
VERIFY_TOKEN = "MY_SECRET_TOKEN"

# Ensure DB and table exist
def init_db():
    conn = sqlite3.connect("whatsapp_messages.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wa_id TEXT,
            name TEXT,
            message TEXT,
            timestamp TEXT
            direction TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Run at startup

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Meta (Facebook) webhook verification
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification token mismatch", 403

    elif request.method == "POST":
        # Incoming WhatsApp messages
        data = request.json
        print("Received data:", data)

        try:
            # Safely navigate the structure (handle multiple messages if needed)
            entry = data.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            contacts = value.get("contacts", [])
            direction = "incoming"

            if messages and contacts:
                message = messages[0]
                contact = contacts[0]

                wa_id = contact.get("wa_id")
                name = contact.get("profile", {}).get("name")
                msg_text = message.get("text", {}).get("body")
                timestamp = message.get("timestamp")

                # Store into SQLite DB
                conn = sqlite3.connect("whatsapp_messages.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO messages (wa_id, name, message, timestamp, direction)
                    VALUES (?, ?, ?, ?, ?)
                """, (wa_id, name, msg_text, timestamp, direction))
                conn.commit()
                conn.close()

                print(f"Stored message from {name}: {msg_text}")

        except Exception as e:
            print("Error processing webhook:", e)

        return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    # Run on port 8080 for ngrok
    app.run(host="0.0.0.0", port=8080)

