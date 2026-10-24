import os
import streamlit as st
from PIL import Image
from pathlib import Path
import numpy as np
import tf_keras as keras

base_dir = Path(__file__).resolve().parent / "model2"

@st.cache_resource
def retrieve_model():
    return keras.models.load_model(base_dir / "keras_model.h5", compile=False)

model = retrieve_model()
labels_path = base_dir / "labels.txt"
with open(labels_path, 'r') as f:
    lines = [line.strip() for line in f.readlines()]

st.title("Beaver vs Nutria")
loaded_file = st.file_uploader("Upload Image", ["jpg", "png", "jpeg"])

if loaded_file != None:
    image = Image.open(loaded_file)
    st.image(image, caption='Uploaded Image')
    img = image.convert("RGB").resize((224, 224))
    img_array = np.array(img) / 255
    img_array = np.expand_dims(img_array, 0)

    if st.button('Classify'):
        classification = model.predict(img_array)
        rodent = lines[np.argmax(classification)]
        confidence = np.max(classification)
        st.success(rodent)
        st.info(f"Confidence: {confidence:.0%}")
        if confidence < 0.7:
            st.warning("WARNING: Confidence below 70%")
        if rodent == "1 Nutria":
            st.badge("INVASIVE", color="red")
        elif rodent == "0 North American Beaver":
            st.badge("NATIVE", color="green")