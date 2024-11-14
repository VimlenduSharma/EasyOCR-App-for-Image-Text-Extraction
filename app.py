import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="Image Text Extraction with EasyOCR",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Title of the app
st.title("📄 Image Text Extraction with EasyOCR")

# Sidebar for language selection
st.sidebar.header("Configuration")
langs = ['en', 'fr', 'de', 'es', 'it', 'pt', 'zh']
selected_lang = st.sidebar.selectbox("Select OCR Language", langs, index=0)

# File uploader
uploaded_image = st.file_uploader("📤 Upload an Image", type=['png', 'jpg', 'jpeg'])

if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    img_array = np.array(image)
    st.image(image, caption='Uploaded Image', use_container_width=True)

    # Initialize EasyOCR reader
    with st.spinner("Loading OCR model..."):
        reader = easyocr.Reader([selected_lang])

    # Perform OCR
    with st.spinner("Reading image..."):
        result = reader.readtext(img_array)

    # Extract and display text
    st.subheader("📝 Extracted Text:")
    extracted_text = "\n".join([detection[1] for detection in result])
    st.text_area("Extracted Text", extracted_text, height=200)

    # Annotate image
    annotated_image = img_array.copy()
    for detection in result:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        cv2.rectangle(annotated_image, top_left, bottom_right, (0, 255, 0), 2)

    # Display annotated image
    st.subheader("🔍 Annotated Image:")
    st.image(annotated_image, caption='Image with Detected Text', use_container_width=True)
else:
    st.info("Please upload an image to proceed.")
