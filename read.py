import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from pyzbar.pyzbar import decode

class QRCodeScanner(VideoProcessorBase):
    def __init__(self):
        self.qr_data = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded_objects = decode(img)

        for obj in decoded_objects:
            self.qr_data = obj.data.decode("utf-8")
            (x, y, w, h) = obj.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, self.qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame.from_ndarray(img, format="bgr24")

st.title("QR Code Scanner")

webrtc_ctx = webrtc_streamer(
    key="qr-scanner",
    video_processor_factory=QRCodeScanner,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

if webrtc_ctx.video_processor and webrtc_ctx.video_processor.qr_data:
    st.write(f"QR Code Data: {webrtc_ctx.video_processor.qr_data}")
