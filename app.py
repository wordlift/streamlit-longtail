import streamlit as st

PAGE_CONFIG = {
    "page_title":"Free SEO Tools by WordLift",
    "page_icon":"img/fav-ico.png",
    "layout":"wide"
    }
st.set_page_config(**PAGE_CONFIG)

from multiapp import MultiApp
from apps import wordliftapi, spacyapi

app = MultiApp()

# Add all your application here
app.add_app("WordLift", wordliftapi.app)
app.add_app("SpaCy", spacyapi.app)

# The main app
app.run()
