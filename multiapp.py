"""
running multiple pages as a single app.
"""
import streamlit as st

class MultiApp:
    """
    Framework for combining multiple streamlit applications.
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

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """
        Adds a new application.
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

    def run(self):
        st.sidebar.image("img/logo-wordlift.png", width=200)
        st.sidebar.title("Navigation")
        app = st.sidebar.radio(
            'API:',
            self.apps,
            format_func=lambda app: app['title'])
        st.sidebar.title("About")
        st.sidebar.info('WordLift will “read” autocomplete data from Google, scan it using the Knowledge Graph from your website (or the SpaCy API) then quickly analyze every search opportunity to help you create super-useful content.” ')

        app['function']()
