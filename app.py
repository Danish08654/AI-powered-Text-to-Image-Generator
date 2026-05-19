import streamlit as st
import requests
from PIL import Image
import json
import os

# Page Config

st.set_page_config(
    page_title="AI Image Generator",
    layout="wide"
)

st.title(" AI Image Generator")


# Sidebar History

st.sidebar.title("🕘 History")

history_path = "../history/history.json"

if os.path.exists(history_path):

    with open(history_path, "r") as f:
        history = json.load(f)

    if len(history) > 0:

        for item in reversed(history[-10:]):

            try:
                st.sidebar.image(item["image"], width=150)
                st.sidebar.caption(item["prompt"])

            except:
                pass

    else:
        st.sidebar.write("No history found")

else:
    st.sidebar.write("History file not found")

# Main UI

prompt = st.text_area(
    "Enter Prompt",
    placeholder="A futuristic cyberpunk city at night..."
)

style = st.selectbox(
    "Choose Style",
    [
        "Cinematic",
        "Anime",
        "Cyberpunk",
        "Fantasy",
        "Realistic"
    ]
)

# Generate Button

if st.button(" Generate Image"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt")

    else:

        with st.spinner("Generating image..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json={
                        "prompt": prompt,
                        "style": style
                    }
                )

                data = response.json()

                image_path = data["image_path"]

                image = Image.open(image_path)

                st.success("Image Generated Successfully!")

                st.image(
                    image,
                    caption=data["prompt"],
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Error: {e}")