import os
import base64
import streamlit as st

# Path to the image directory
image_directory = r"C:\Users\Elijah Babatunde\Documents\testpy\images"

# Function to get an image as a base64 string
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()  # Read the file data
    return base64.b64encode(data).decode()  # Correctly encode and decode

# Load background images as base64
img_welcome = get_img_as_base64(os.path.join(image_directory, "564.jpg"))
img_data_availability = get_img_as_base64(os.path.join(image_directory, "background page_two.jpg"))
img_data_input = get_img_as_base64(os.path.join(image_directory, "background page_three.jpg"))
img_result = get_img_as_base64(os.path.join(image_directory, "background page_four.jpg"))

def load_css(page):
    if page == "WELCOME AND LOGIN PAGE":
        css = f"""
        <style>
            body {{
                background-image: url(data:image/jpeg;base64,{img_welcome});
                background-size: cover; /* Adjust as needed */
                background-repeat: no-repeat; /* Prevent repeating */
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    elif page == "RESERVOIR DESCRIPTION/ DATA AVAILABILITY PAGE":
        css = f"""
        <style>
            body {{
                background-image: url(data:image/jpeg;base64,{img_data_availability});
                background-size: cover;
                background-repeat: no-repeat;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    elif page == "DATA INPUT PAGE":
        css = f"""
        <style>
            body {{
                background-image: url(data:image/jpeg;base64,{img_data_input});
                background-size: cover;
                background-repeat: no-repeat;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    elif page == "RESULT AND RECOMMENDATION PAGE":
        css = f"""
        <style>
            body {{
                background-image: url(data:image/jpeg;base64,{img_result});
                background-size: cover;
                background-repeat: no-repeat;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# Call the function to load CSS for the specific page
load_css(st.session_state.get('page', "WELCOME AND LOGIN PAGE"))
