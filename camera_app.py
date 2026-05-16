import streamlit as st
import numpy as np
from PIL import Image
import os
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing import image

st.title("Camera Emoji Resemblance")

st.write("Capture an image. The app will suggest which emoji it resembles most.")

# Load emoji images
emoji_folder = "emojis"
emoji_files = [f for f in os.listdir(emoji_folder) if f.endswith(".png")]
emoji_images = []
emoji_names = []

for ef in emoji_files:
    img = Image.open(os.path.join(emoji_folder, ef)).convert("RGB").resize((224, 224))
    emoji_images.append(np.array(img))
    emoji_names.append(os.path.splitext(ef)[0])

# Load MobileNetV2 model for feature extraction
model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")

def get_features(img):
    img = img.resize((224, 224)).convert("RGB")
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    return features[0]

img_file = st.camera_input("Capture Image")

if img_file:
    user_img = Image.open(img_file)
    user_features = get_features(user_img)

    # Compare with emoji features
    similarities = []
    for emoji_img in emoji_images:
        emoji_features = get_features(Image.fromarray(emoji_img))
        sim = np.dot(user_features, emoji_features) / (np.linalg.norm(user_features) * np.linalg.norm(emoji_features))
        similarities.append(sim)

    best_match_idx = int(np.argmax(similarities))
    st.write(f"Your image resembles: **{emoji_names[best_match_idx]}** emoji!")
    st.image(os.path.join(emoji_folder, emoji_files[best_match_idx]), caption=f"{emoji_names[best_match_idx]} emoji")