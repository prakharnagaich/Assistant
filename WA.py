import requests
import json

# 🔐 Replace with your actual credentials
ACCESS_TOKEN = "EAAWPP5vnJPoBPun1CDDYb2kHwfNOoJSAwDZBSvtU0AIDlgw6j5HTXhEPkf9PGIqjOvZAAkxiI1UkEzdZCB1dxiLWCMA9o5dWbSZCBGpGLcIZCZAkZCbZBqGOaFdkEwNealaxvVUizroLO0yZCy344rPKdpch9agsLpD5aZCtdR07ZAZABrZCXee4ZCZB1t5oIBkDnYkCwdUukZAfYeucz1m6KXwI4UpAEcmWZBJ0Cka9IgQr1nXx5rh1LoYrzTZCJDM0C7WQZDZD"
PHONE_NUMBER_ID = "841738542350350"
RECIPIENT_PHONE = "918527710741"  # Include country code, no spaces

# 🌐 WhatsApp API endpoint
url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

# 🧾 Headers for the request
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# 📨 Message payload
payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "type": "text",
    "text": {
        "body": "Hi there! This is a custom message sent from my Python script 🚀"
    }
}



# 🚀 Send the request
response = requests.post(url, headers=headers, json=payload)

# 📋 Output the result
if response.status_code == 200:
    print("✅ Message sent successfully!")
    print("Response:", response.json())
else:
    print("❌ Failed to send message")
    print("Status Code:", response.status_code)
    print("Error:", response.text)