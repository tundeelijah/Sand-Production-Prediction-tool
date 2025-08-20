import streamlit as st

page_bg_img=""" 
<stlye>
[data-testid="stAppviewContainer"]{}
</stlye> """
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("",unsafe_allow_html=True )
st.title("it's summer!")


import base64  # Make sure to import the base64 module
import streamlit as st

def get_img_as_base64(file): 
    with open(file, "rb") as f:
        data = f.read()  # Read the file data
    return base64.b64encode(data).decode()  # Correctly encode and decode

# Get the image as base64
img = get_img_as_base64("images\564.jpg")

def load_css(page):
    if page == "WELCOME AND LOGIN PAGE":
        with open("background page_one.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        # Create a CSS string with the base64 image
        css = f"""
        <style>
            body {{
                background-image: url(data:image/jpeg;base64,{img});
                background-size: cover; /* Optional: adjust as needed */
                background-repeat: no-repeat; /* Optional: adjust as needed */
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)    
    elif page == "RESERVOIR DESCIPTION/ DATA AVAILABILITY PAGE":
        with open("background page_two.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        st.markdown('<style>body {background-image: url("images/background page_two.jpg");}</style>', unsafe_allow_html=True)
        
    elif page == "DATA INPUT PAGE":
        with open("background page_three.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        st.markdown('<style>body {background-image: url("images/background page_three.jpg");}</style>', unsafe_allow_html=True)
        
        st.session_state.par1 = par1
    st.session_state.par2 = par2
    st.session_state.par3 = par3
    st.session_state.par4 = par4
    st.session_state.par5 = par5
    st.session_state.par6 = par6

    elif page == "RESULT AND RECOMMENDATION PAGE":
        with open("background page_four.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        st.markdown('<style>body {background-image: url("images/background page_four.jpg");}</style>', unsafe_allow_html=True)