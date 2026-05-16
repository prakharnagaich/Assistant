import streamlit as st
import sqlite3
import requests
from streamlit_autorefresh import st_autorefresh
import google.generativeai as genai

# 🔄 Auto-refresh every 5 seconds
st_autorefresh(interval=500, limit=None, key="refresh")

# 📦 Connect to SQLite database
conn = sqlite3.connect('whatsapp_messages.db')
cursor = conn.cursor()

# 🛠 Ensure messages table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message TEXT,
    direction TEXT,
    wa_id TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

st.title("💬 WhatsApp Chat Interface")

# 🔀 Reply mode toggle (top-level control)
reply_mode = st.radio("Choose reply mode", ["Human Reply", "Auto Reply with Gemini AI"])

# 📥 Select user to chat with
cursor.execute("SELECT DISTINCT name FROM messages ORDER BY name ASC")
senders = [row[0] for row in cursor.fetchall()]
selected_user = st.selectbox("Choose a contact", senders) if senders else None

# 🤖 Auto-reply logic (takes precedence)
if reply_mode == "Auto Reply with Gemini AI":
    cursor.execute("""
        SELECT message, name, wa_id FROM messages
        WHERE direction = 'incoming'
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    last_msg = cursor.fetchone()

    if last_msg:
        genai.configure(api_key="AIzaSyAHKPqEZ66TiHlG660ncBR-eIP-ehJo8OY")
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(f"Reply to this WhatsApp message: '{last_msg[0]}'")
        ai_reply = response.text

        ACCESS_TOKEN = "EAAWPP5vnJPoBPWtO3ZALoYrUyOZBZAw0MVhDRSjfwvEuqqZCOQhuDBjpZCzO0WWBA3NsVM1pjA7CrZBJv1i4xPmG7ZB5ExIOMTj1kfKzOpM5qZCQGuaTIlZCuKWSa8bLwKx4HZALTRjotNxERPURxbW0PTBQpZBRKJAjvOrU4NhRlYK9BXU5STvHv3RQVhROdVkhFs1TosP5dLBnbWZAV6lDzv4ZA4xYFtwRjQ7WwXO4HXuZA1RR6bYmyQFig9wijAwwZDZD"
        PHONE_NUMBER_ID = "841738542350350"

        payload = {
            "messaging_product": "whatsapp",
            "to": last_msg[2],
            "type": "text",
            "text": {"body": ai_reply}
        }
        requests.post(f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages",
                      headers={
                          "Authorization": f"Bearer {ACCESS_TOKEN}",
                          "Content-Type": "application/json"
                      },
                      json=payload)
        cursor.execute("INSERT INTO messages (name, message, direction, wa_id) VALUES (?, ?, ?, ?)",
                       (last_msg[1], ai_reply, "outgoing", last_msg[2]))
        conn.commit()
        st.success("AI reply sent!")
    else:
        st.info("No incoming messages found.")

# 📤 Human reply section (only active if selected)
if reply_mode == "Human Reply":
    st.subheader("Type your message")
    message_body = st.text_area("Message", key="message_input")
    if st.button("Send"):
        if selected_user and message_body:
            cursor.execute("SELECT wa_id FROM messages WHERE name = ?", (selected_user,))
            result = cursor.fetchone()

            if result and result[0]:
                ACCESS_TOKEN = "EAAWPP5vnJPoBPWtO3ZALoYrUyOZBZAw0MVhDRSjfwvEuqqZCOQhuDBjpZCzO0WWBA3NsVM1pjA7CrZBJv1i4xPmG7ZB5ExIOMTj1kfKzOpM5qZCQGuaTIlZCuKWSa8bLwKx4HZALTRjotNxERPURxbW0PTBQpZBRKJAjvOrU4NhRlYK9BXU5STvHv3RQVhROdVkhFs1TosP5dLBnbWZAV6lDzv4ZA4xYFtwRjQ7WwXO4HXuZA1RR6bYmyQFig9wijAwwZDZD"
                PHONE_NUMBER_ID = "841738542350350"
                RECIPIENT_PHONE = result[0]

                payload = {
                    "messaging_product": "whatsapp",
                    "to": RECIPIENT_PHONE,
                    "type": "text",
                    "text": {"body": message_body}
                }
                requests.post(f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages",
                              headers={
                                  "Authorization": f"Bearer {ACCESS_TOKEN}",
                                  "Content-Type": "application/json"
                              },
                              json=payload)
                cursor.execute("INSERT INTO messages (name, message, direction, wa_id) VALUES (?, ?, ?, ?)",
                               (selected_user, message_body, "outgoing", RECIPIENT_PHONE))
                conn.commit()
                st.success("Message sent!")
            else:
                st.error("Recipient phone number not found.")
        else:
            st.warning("Please select a user and enter a message.")

st.divider()

# 🧾 Chat history
if selected_user:
    st.subheader(f"📜 Chat with {selected_user}")
    cursor.execute("SELECT message, direction, timestamp FROM messages WHERE name = ? ORDER BY timestamp DESC", (selected_user,))
    chat = cursor.fetchall()

    for msg, direction, time in chat:
        if direction == "incoming":
            st.markdown(f"🟢 **{selected_user}** ({time}): {msg}")
        else:
            st.markdown(f"🔵 **You** ({time}): {msg}")
else:
    st.info("Waiting for messages or user selection...")

conn.close()