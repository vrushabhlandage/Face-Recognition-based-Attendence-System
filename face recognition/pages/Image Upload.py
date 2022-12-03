import streamlit as st

import os

from PIL import Image

@st.cache
def load_image(img_input):
    img = Image.open(img_input)
    return img


img_input = st.file_uploader("upload image with 4 digit id followed by staff name,like : 0025Vrushabh", type=["jpg", "png"])

if img_input is not None:
    file_details = {"file_name": img_input.name, "file_type": img_input.type}
    img = load_image(img_input)

    st.image(load_image(img_input), width=250)

    with open(os.path.join("images", img_input.name), "wb") as f:
        f.write(img_input.getbuffer())




if st.button("upload"):
    # function_input(id_input)

    st.success("Record uploaded successfully ")
