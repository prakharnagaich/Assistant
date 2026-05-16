import streamlit as st
import sqlite3
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 5 seconds
st_autorefresh(interval=500, limit=None, key="refresh")

# Connect to the database
conn = sqlite3.connect('whatsapp_messages.db')
cursor = conn.cursor()

# Ensure the table exists
conn.commit()

# Fetch unique sender names
cursor.execute("SELECT DISTINCT name FROM messages ORDER BY name ASC")
senders = [row[0] for row in cursor.fetchall()]

# Dropdown to select user
selected_user = st.selectbox("Select WhatsApp user", senders)

# Fetch messages from the selected user
cursor.execute("SELECT message, timestamp FROM messages WHERE name = ? ORDER BY timestamp DESC", (selected_user,))
messages = cursor.fetchall()

# Track message count for the selected user
if "message_counts" not in st.session_state:
    st.session_state.message_counts = {}

previous_count = st.session_state.message_counts.get(selected_user, 0)
current_count = len(messages)

# Display latest message
if messages:
    latest_msg, latest_time = messages[0]
    st.subheader("🆕 Latest Message")
    st.markdown(f"{latest_msg}")

    # Display older messages
    st.subheader("📜 Previous Messages")
    for msg, time in messages[1:]:
        st.markdown(f"{msg}")

    # Notify if new messages arrived
    if current_count > previous_count:
        st.success("New message received!")

    # Update session state
    st.session_state.message_counts[selected_user] = current_count
else:
    st.warning("No messages found for this user.")

conn.close()