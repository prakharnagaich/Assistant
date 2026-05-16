import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

st.set_page_config(page_title="WhatsApp Contact Exporter", layout="centered")
st.title("📱 WhatsApp Group Contact Exporter")

group_name = st.text_input("Enter WhatsApp Group Name")

if st.button("Start Extraction"):
    st.info("Launching WhatsApp Web... Please scan the QR code in the browser window.")

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Keeps browser open

    # Launch browser
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com")

    st.warning("After scanning the QR code, press Enter in the terminal to continue.")
    input("✅ Scan QR code and press Enter here to continue...")

    # Search for group
    try:
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.send_keys(group_name)
        time.sleep(3)

        group_title = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]'))
        )
        group_title.click()
        time.sleep(3)

        # Open group info
        header = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//header'))
        )
        header.click()
        time.sleep(3)

        # Scroll inside participant container
        scroll_container = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="region"]'))
        )
        for _ in range(20):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
            time.sleep(0.5)

        # Extract contacts
        raw_elements = driver.find_elements(By.XPATH, '//div[@role="button"]//span[@dir="auto"]')
        contacts = [el.text for el in raw_elements if el.text.strip()]

        driver.quit()

        # Save to Excel
        df = pd.DataFrame(contacts, columns=["Contact"])
        file_path = "whatsapp_group_contacts.xlsx"
        df.to_excel(file_path, index=False)

        st.success("✅ Contacts extracted successfully!")
        st.dataframe(df)

        with open(file_path, "rb") as f:
            st.download_button("📥 Download Excel File", f, file_name="whatsapp_group_contacts.xlsx")

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
        driver.quit()