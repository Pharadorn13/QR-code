import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

st.title("QR Code Scanner")

uploaded_file = st.file_uploader("Upload an image containing a QR Code", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Decode QR Code
    decoded_objects = decode(gray)
    for obj in decoded_objects:
        qr_data = obj.data.decode("utf-8")
        st.write(f"QR Code Data: {qr_data}")
