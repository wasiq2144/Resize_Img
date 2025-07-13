import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="🖼️ Image Resizer", layout="centered")

st.markdown("<h2 style='text-align:center;'>🖼️ Image Resizer Tool</h2>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    with col2:
        resize_method = st.radio("Resize by:", ["Width & Height", "Percentage"])

if uploaded_file:
    image = Image.open(uploaded_file)

    # st.image(image, caption="Original Image", use_container_width=True)

    with st.container():
        if resize_method == "Width & Height":
            col3, col4 = st.columns(2)
            with col3:
                width = st.number_input("Width", min_value=1, value=image.width)
            with col4:
                height = st.number_input("Height", min_value=1, value=image.height)
        else:
            percent = st.slider("Resize Percentage", 10, 200, 100)

    if st.button("Resize"):
        if resize_method == "Width & Height":
            resized = image.resize((int(width), int(height)))
        else:
            resized = image.resize((int(image.width * percent / 100), int(image.height * percent / 100)))

        if resized.mode == "RGBA":
            resized = resized.convert("RGB")

                    # Display side-by-side
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📷 Original Image")
            st.image(image, use_container_width=True)

        with col2:
            st.markdown("### ✂️ Resized Image")
            st.image(resized, use_container_width=True)

        buf = io.BytesIO()
        resized.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        st.download_button("Download Image", data=byte_im, file_name="resized.jpg", mime="image/jpeg")
