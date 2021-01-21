# -*- coding: utf-8 -*-
"""
Created on 21 Jan 2021

@author: AndreaVolpini
based on the 🤗 Zero Shot Pipeline by HuggingFace

"""

# we might not need all of these here
# <--- Installing Libraries --->
from transformers import pipeline
import streamlit as st
#from streamlit_toggle import st_toggleswitch


# <--- Page Configurations --->
PAGE_CONFIG = {
    "page_title":"Free SEO Tools by WordLift",
    "page_icon":"images/fav-ico.png",
    "layout":"centered"
    }
st.set_page_config(**PAGE_CONFIG)

# <--- Sidebar --->

st.sidebar.image("images/logo-wordlift.png", width=200)

english_only = st.sidebar.selectbox("Enable multilingual support", ('False','True'))

st.sidebar.info("If you enable multi-class classification the scores will be independent.")

multiclass_enabled = st.sidebar.selectbox("Enable multi-class classification", ('True','False'))




# <--- Page Components--->
st.title("Ready to Classify Your Content")
st.subheader("This is a demo of zero-shot text classification.")

# text inputs
col1, col2 = st.beta_columns(2)
with col1:
    st.markdown("""Add your text here 👇""")
    sequence = st.text_area("Type your the content you want to classify here...")
with col2:
    st.markdown("""What are the topics?""")
    candidate_labels = st.text_area("Type the list of topics here...")

submit = st.button("Let's classify your text!")




# <--- CSS --->
# st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# <--- HTML --->
# st_html('index.html')

def load_model():
    if english_only == 'False':
        classifier = pipeline("zero-shot-classification")
    else:
        classifier = pipeline("zero-shot-classification", model='joeddav/xlm-roberta-large-xnli')
    return classifier

# <--- Main Function --->
def main():
    classifier = load_model() # load the right model based on the english_only switch
    if submit:
        with st.spinner("Requesting completion..."):
            st.write(classifier(sequence, candidate_labels, multi_class=multiclass_enabled))

if __name__ == "__main__":
    main()
