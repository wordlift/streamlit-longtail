import streamlit as st
import streamlit.components.v1 as components
import base64
from time import sleep
from stqdm import stqdm

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def progress_bar():
    for _ in stqdm(range(50), desc="This is a slow task, please be patient", mininterval=1):
        sleep(5) # maybe it is better to be 1
    return

def balloons(result):
    st.balloons()
    st.text('Done! thanks for being patient.')
    st.text("Here's your " + result)
    return
