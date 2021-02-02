import streamlit as st

PAGE_CONFIG = {
    "page_title":"Free SEO Tools by WordLift",
    "page_icon":"img/fav-ico.png",
    "layout":"wide"
    }
st.set_page_config(**PAGE_CONFIG)

# This will hide the hamburger menu completely.
hide_streamlit_style = """
<style>
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
from multiapp import MultiApp
from apps import wordliftapi, spacyapi

app = MultiApp()

app.add_app("WordLift", wordliftapi.app)
app.add_app("SpaCy", spacyapi.app)

app.run()
