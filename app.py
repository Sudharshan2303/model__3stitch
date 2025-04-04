import cv2
import numpy as np
import streamlit as st
from PIL import Image

def stitch_images(img1, img2, img3):
    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch([img1, img2, img3])
    
    if status == cv2.Stitcher_OK:
        return stitched
    else:
        st.error(f"Image stitching failed with status code {status}")
        return None

def process_images(img1, img2, img3):
    # Convert images from PIL to OpenCV format
    img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
    img3 = cv2.cvtColor(np.array(img3), cv2.COLOR_RGB2BGR)
    
    stitched_result = stitch_images(img1, img2, img3)
    
    if stitched_result is not None:
        return Image.fromarray(cv2.cvtColor(stitched_result, cv2.COLOR_BGR2RGB))
    else:
        return None

def main():
    st.title("Image Stitching with OpenCV")
    st.write("Upload three overlapping images to create a panorama.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        img1 = st.file_uploader("Upload Image 1", type=["jpg", "jpeg", "png"])
    with col2:
        img2 = st.file_uploader("Upload Image 2", type=["jpg", "jpeg", "png"])
    with col3:
        img3 = st.file_uploader("Upload Image 3", type=["jpg", "jpeg", "png"])
    
    if img1 and img2 and img3:
        img1 = Image.open(img1)
        img2 = Image.open(img2)
        img3 = Image.open(img3)
        
        st.subheader("Uploaded Images")
        st.image([img1, img2, img3], width=200, caption=["Image 1", "Image 2", "Image 3"])
        
        if st.button("Stitch Images"):
            with st.spinner("Stitching images..."):
                result = process_images(img1, img2, img3)
                
            if result is not None:
                st.subheader("Stitched Panorama")
                st.image(result, use_column_width=True)
                
                # Add download button
                from io import BytesIO
                buf = BytesIO()
                result.save(buf, format="JPEG")
                byte_im = buf.getvalue()
                st.download_button(
                    label="Download Panorama",
                    data=byte_im,
                    file_name="panorama.jpg",
                    mime="image/jpeg"
                )

if __name__ == "__main__":
    main()
