"""
Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """

    lang_option=st.empty()
    country_option=st.empty()
    WL_key_ti=''
    size_navigation=st.empty()
    go_button=st.empty()
    first_idea=''
    second_idea=''
    third_idea=''

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def comp(self):

        col1, col2, col3 = st.beta_columns(3)
        with col1:
            languages = ["en", "it", "es", "de"]
            lang_option = st.selectbox("Select Language", languages)
            first_idea = st.text_area("What is the first idea?")
        with col2:
            countries = ["us", "uk", "in", "es", "it", "de"]
            country_option = st.selectbox("Select Country", countries)
            second_idea = st.text_area("What is the second idea?")
        with col3:
            WL_key_ti = st.text_input("Enter your WordLift key")
            third_idea = st.text_area("What is the third idea?")

        size = ["Small", "Medium", "Large"]
        size_navigation = st.selectbox("Please specify preferred queries list size, then press GO!", size)

        st.info("Please provide your WordLift key to proceed.")
        go_button = st.button("GO!")

        return self


    def run(self):
        st.sidebar.image("img/logo-wordlift.png", width=200)
        st.sidebar.title("Navigation")
        app = st.sidebar.radio(
            'API:',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()
