
import streamlit as st
import pandas as pd
import subprocess

st.set_page_config(page_title="Airtel SMS Sender", layout="centered")

st.title("📲 Airtel SMS Sender via KDE Connect")
st.markdown("Upload an Excel file with `PhoneNumber` and `Message` columns to send SMS using your Airtel SIM.")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# KDE Connect device ID input
device_id = st.text_input("🔗 Enter your KDE Connect Device ID")

# Trigger SMS sending
if uploaded_file and device_id:
    df = pd.read_excel(uploaded_file)

    if 'PhoneNumber' not in df.columns or 'Message' not in df.columns:
        st.error("Excel must contain 'PhoneNumber' and 'Message' columns.")
    else:
        if st.button("🚀 Send All SMS"):
            success_count = 0
            fail_count = 0

            for index, row in df.iterrows():
                phone = str(row['PhoneNumber'])
                message = str(row['Message'])

                command = [
                    "kdeconnect-cli",
                    "--device", device_id,
                    "--send-sms", message,
                    "--destination", phone
                ]

                try:
                    subprocess.run(command, check=True)
                    st.success(f"✅ Sent to {phone}")
                    success_count += 1
                except subprocess.CalledProcessError:
                    st.error(f"❌ Failed to send to {phone}")
                    fail_count += 1

            st.info(f"Done! {success_count} sent, {fail_count} failed.")

else:
    st.warning("Please upload a file and enter your device ID.")