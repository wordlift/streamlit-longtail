import streamlit as st
import SessionState
from src.Interface import *

PAGE_CONFIG = {
    "page_title":"Free SEO Tools by WordLift",
    "page_icon":"img/fav-ico.png",
    "layout":"wide"
    }
st.set_page_config(**PAGE_CONFIG)

# This will hide the hamburger menu of streamlit completely.
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

language = ''
country = ''
WL_key = ''
list_size = 0

def main():

    local_css("style.css")
    set_png_as_page_bg('img/pattern.png')

    state = SessionState.get(name="", button_submit=False)

    pages = {
        "WordLift": page_WordLift,
        "SpaCy": page_SpaCy,
    }

    st.sidebar.image("img/logo-wordlift.png", width=200)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select your API", tuple(pages.keys()))
    st.sidebar.info("You will need a WordLift key. You can [get one for free](https://wordlift.io/checkout/) for 14 days.")

    st.markdown('<p class="subject"> Content Idea Generator </p>', unsafe_allow_html=True)
    st.markdown('<p class="payoff"> Get instant, untapped content ideas </p>', unsafe_allow_html=True)
    st.markdown('<p class="question"> How does this work? </p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="answer">
        WordLift will “read” autocomplete data from Google, scan it using the
        Knowledge Graph from your website (or the SpaCy API) then quickly analyze
        every search opportunity to help you create super-useful content.”
    </p>
    """, unsafe_allow_html=True)

    # Display the selected page with the session state
    pages[page](state)

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        languages = ["EN", "IT", "ES", "DE"]
        state.lang_option = st.selectbox("Select Language", languages)
    with col2:
        countries = ["US", "UK", "IN", "ES", "IT", "DE"]
        state.country_option = st.selectbox("Select Country", countries)
    with col3:
        state.WL_key_ti = st.text_input("Enter your WordLift key")

    col4, col5, col6 = st.beta_columns(3)
    with col4:
        state.first_idea = st.text_input("What is the first idea?")
    with col5:
        state.second_idea = st.text_input("What is the second idea?")
    with col6:
        state.third_idea = st.text_input("What is the third idea?")
    size = ['Small (25 Queries)', 'Medium (50 Queries)', 'Large (100 Queries)', 'X-Large (700 Queries)']
    state.size_navigation = st.radio('Please specify preferred queries list size, then press Submit', size)

    button_submit = st.button("Submit")

    if button_submit:
        state.button_submit = True

    if state.button_submit:

        if state.WL_key_ti:
            WL_key = state.WL_key_ti
        elif not state.WL_key_ti:
            st.error("Please provide your WordLift key to proceed.")
            st.stop()

        if state.size_navigation == 'Small (25 Queries)':
            list_size = 25
        elif size_navigation == 'Medium (50 Queries)':
            state.list_size = 50
        elif size_navigation == 'Large (100 Queries)':
            state.list_size = 100
        elif size_navigation == 'X-Large (700 Queries)':
            state.list_size = 700

        if not (state.first_idea or state.second_idea or state.third_idea):
            st.error("You have not typed any ideas! Please type at least two ideas, then press Submit")
            st.stop()
        elif state.first_idea:
            if state.second_idea:
                if state.third_idea:
                    st.success("SUCCESS!")
                    keyword_list = state.first_idea + ', ' + state.second_idea + ', ' + state.third_idea
                elif not state.third_idea:
                    st.success("SUCCESS!")
                    keyword_list = state.first_idea + ', ' + state.second_idea
            elif not (state.second_idea or state.third_idea):
                st.error("You have typed only one idea! Please type at least two ideas, then press Submit")
                st.stop()
        keyword_list = keyword_list.strip('][').split(', ')

def page_WordLift(state):
    st.text("WordLift page")
    st.write("---")

def page_SpaCy(state):
    st.text("SpaCy page")
    st.write("---")

if __name__ == "__main__":
    main()
