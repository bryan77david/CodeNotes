# image processing
import base64
import requests
import streamlit as st

# for rendering HTML Content
import streamlit.components.v1 as components



# Function to encode image file to base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to render example notebook
def render_example(path):
    # Fetch the HTML content
    response = requests.get(path)
    html_content = response.text

    # Wrap the HTML content in a div with fixed height and overflow
    scrollable_html_content = f"""
    <div style="height: 800px; overflow: auto;">
    {html_content}
    </div>
    """
    
    # Display scrollable HTML content
    return components.html(scrollable_html_content, height=900)

    
# Function to set background image for sidebar
def set_background_SB(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .st-emotion-cache-6qob1r {
    background-image: url("data:image/png;base64,%s");
    background-size: contain;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to set background image for main content
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-color: black;
    background-size: repeat;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


# Function to set background image for main content
def set_background_container():
    page_bg_img = '''
    <style>
    .st-emotion-cache-1xw8zd0 {
    background-color: black;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)