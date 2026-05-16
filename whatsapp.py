import streamlit as st
import pandas as pd
import pyautogui
import webbrowser
import time
import keyboard

# Enable image not found exception
pyautogui.useImageNotFoundException()

st.title("📤 WhatsApp Bulk Messenger (Auto + Manual Confirm)")

# Country code dropdown
country_code = st.selectbox("Select Country Code", ["+91", "+1", "+44", "+61", "+971"])

# Excel upload
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# Delay before WhatsApp Web opens
delay = st.slider("Delay before WhatsApp opens (seconds)", 2, 10, 4)

# Timeout for user confirmation (now allows 5 seconds minimum)
timeout = st.slider("Timeout for confirmation (seconds)", 5, 60, 30)

# Icon path for auto detection
icon_path = "enter_icon.png"

def auto_press_enter_on_icon(icon_path, confidence=0.8, timeout=10):
    """Automatically press Enter when icon appears on screen."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(icon_path, confidence=confidence)
            if location:
                pyautogui.press("enter")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(1)
    return False

def wait_for_user_confirmation(timeout=30, unique_id=""):
    """Wait for Enter key or button click with countdown."""
    st.info("Press Enter or click 'Next' after sending the message to continue...")
    placeholder = st.empty()
    for remaining in range(timeout, 0, -1):
        placeholder.markdown(f"⏳ Waiting for confirmation... **{remaining} seconds left**")
        time.sleep(1)
        if keyboard.is_pressed("enter"):
            placeholder.empty()
            return True
    placeholder.empty()
    st.warning("⚠️ No confirmation detected. Click below to retry or skip.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Retry", key=f"retry_{unique_id}"):
            return wait_for_user_confirmation(timeout, unique_id)
    with col2:
        if st.button("⏭️ Skip", key=f"skip_{unique_id}"):
            return False
    return False

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if st.button("Send Messages", key="send_messages"):
        for index, row in df.iterrows():
            phone = str(row["PhoneNumber"]).strip()
            message = str(row["Message"]).strip()

            full_number = country_code + phone
            url = f"https://web.whatsapp.com/send?phone={full_number}&text={message}"
            webbrowser.open(url)
            time.sleep(delay)

            auto_sent = auto_press_enter_on_icon(icon_path, confidence=0.8, timeout=10)
            if not auto_sent:
                pyautogui.press("enter")

            time.sleep(2)

            confirmed = wait_for_user_confirmation(timeout, unique_id=index)
            if confirmed:
                st.success(f"✅ Proceeding to next message for {phone}")
            else:
                st.warning(f"⏭️ Skipped message for {phone}")

        st.success("🎉 All messages processed!")
