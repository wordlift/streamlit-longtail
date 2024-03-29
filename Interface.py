import base64
from time import sleep

import streamlit as st
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
    .stApp {
        background-color: rgb(245, 250, 255);
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


def progress_bar(range_size):
    for _ in stqdm(range(range_size), desc="This is a slow task, please be patient"):
        sleep(0.1)
    return


def balloons(result):
    st.balloons()
    m1 = st.markdown('Done! thanks for being patient.')
    m2 = st.markdown("Here's your " + result)
    m1.empty()
    m2.empty()
    return
