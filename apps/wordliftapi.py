# <-- Libraries -->
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import re
from pandas import json_normalize
from pandas import Series

# from session_state import *
from functions.download import download_button
from functions.interface import *
from functions.generate import *
from functions.restclient import RestClient
from functions.NER_wl import *



# az group create --name LongTailApp --location eastus
# az acr create --resource-group LongTailApp --name LongTailAppRegistry --sku Basic
# pip install azure-storage-blob
# az acr build --registry LongTailAppRegistry --resource-group LongTailApp --image longtail-app https://github.com/wordlift/streamlit-longtail.git

# az appservice plan create -g LongTailApp -n LongTailAppServicePlan -l eastus --is-linux --sku B1

# az webapp create -g LongTailApp -p LongTailAppServicePlan -n longtail-web-app -i longtailappregistry.azurecr.io/mushroom-app:latest





# az group create --name MushroomApp --location eastus
# az acr create --resource-group MushroomApp --name TheMushroomAppRegistry10 --sku Basic
# pip install azure-storage-blob
# az acr build --registry TheMushroomAppRegistry10 --resource-group MushroomApp --image mushroom-app https://github.com/RaffalShafiei/mushroom-webapp.git



# /////////////////////////
# TEST
# /////////////////////////

from streamlit.hashing import _CodeHasher

try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server

def display_state_values(state):
    st.write("Input state:", state.input)
    st.write("Slider state:", state.slider)
    st.write("Radio state:", state.radio)
    st.write("Checkbox state:", state.checkbox)
    st.write("Selectbox state:", state.selectbox)
    st.write("Multiselect state:", state.multiselect)

    for i in range(3):
        st.write(f"Value {i}:", state[f"State value {i}"])

    if st.button("Clear state"):
        state.clear()

class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state

# /////////////////////////
# TEST
# /////////////////////////






language = ''
country = ''
WL_key = ''
list_size = 0
pb_speed = 0.0

# def ui():
#
#     st.markdown('<p class="subject"> Content Idea Generator </p>', unsafe_allow_html=True)
#     st.markdown('<p class="payoff"> Get instant, untapped content ideas </p>', unsafe_allow_html=True)
#     st.markdown('<p class="question"> How does this work? </p>', unsafe_allow_html=True)
#     st.markdown("""
#     <p class="answer">
#         WordLift will “read” autocomplete data from Google, scan it using the
#         Knowledge Graph from your website (or the SpaCy API) then quickly analyze
#         every search opportunity to help you create super-useful content.”
#     </p>
#     """, unsafe_allow_html=True)
#     col1, col2, col3 = st.beta_columns(3)
#     with col1:
#         languages = ["EN", "IT", "ES", "DE"]
#         lang_option = st.selectbox("Select Language", languages)
#         first_idea = st.text_input("What is the first idea?")
#     with col2:
#         countries = ["US", "UK", "IN", "ES", "IT", "DE"]
#         country_option = st.selectbox("Select Country", countries)
#         second_idea = st.text_input("What is the second idea?")
#     with col3:
#         WL_key_ti = st.text_input("Enter your WordLift key")
#         third_idea = st.text_input("What is the third idea?")
#     size = ['Small (25 Queries)', 'Medium (50 Queries)', 'Large (100 Queries)', 'X-Large (700 Queries)']
#     size_navigation = st.radio('Please specify preferred queries list size, then press Submit', size)
#     submit_button = st.button("Submit")
#
#     if submit_button:
#         # <-- user input conditions -->
#         # 1- WordLift Key
#         if WL_key_ti:
#             WL_key = WL_key_ti
#         elif not WL_key_ti:
#             st.error("Please provide your WordLift key to proceed.")
#             st.stop()
#         # 2- query list size
#         if size_navigation == 'Small (25 Queries)':
#             list_size = 25 # when i tried the funds queries, 10 gave me error because treemap couldnnt it is small
#             pb_speed = 2.5
#         elif size_navigation == 'Medium (50 Queries)':
#             list_size = 50
#             pb_speed = 5
#         elif size_navigation == 'Large (100 Queries)':
#             list_size = 100
#             pb_speed = 10
#         elif size_navigation == 'X-Large (700 Queries)':
#             list_size = 700
#             pb_speed = 70
#         # 3- keywords list
#         if not (first_idea or second_idea or third_idea):
#             st.error("You have not typed any ideas! Please type at least two ideas, then press Submit")
#             st.stop()
#         elif first_idea:
#             if second_idea:
#                 if third_idea:
#                     st.success("SUCCESS!")
#                     keyword_list = first_idea + ', ' + second_idea + ', ' + third_idea
#                 elif not third_idea:
#                     st.success("SUCCESS!")
#                     keyword_list = first_idea + ', ' + second_idea
#             elif not (second_idea or third_idea):
#                 st.error("You have typed only one idea! Please type at least two ideas, then press Submit")
#                 st.stop()
#         keyword_list = keyword_list.strip('][').split(', ')
#
# def step1():
#     # progress bar
#     # st.markdown("Analyzing keywords...")
#     # progress_bar(list_size, pb_speed)
#     # ممكن ندخل البروقرس بار جوة الفنكشن
#
#     # keywords = [generate_keywords(q) for q in keyword_list]
#     # keywords = [query for sublist in keywords for query in sublist]
#     # keywords = list(set(keywords))
#     # df = pd.DataFrame(keywords, columns =['queries'])
#     # df = df.head(list_size)
#     # df['entities'] = ''
#     # df['types'] = ''
#
#     # progress bar
#     # st.markdown("Extracting entities...")
#     # progress_bar(list_size, pb_speed)
#
#     # for index, row in df.iterrows():
#     #     data_x = string_to_entities(df['queries'][index])
#     #     if len(data_x[0]) is not 0:
#     #         df.at[index,'entities'] = data_x[0]
#     #         df.at[index,'types'] = data_x[1]
#     #     else:
#     #         df.at[index,'entities'] = 'n.a.'
#     #         df.at[index,'types'] = 'uncategorized'
#
#     # progress bar
#     # st.markdown("Adding information on keywords...")
#     # progress_bar(list_size, pb_speed)
#
#     client = RestClient(WL_key)
#     post_data = dict()
#     post_data[len(post_data)] = dict(location_name="United States", language_name="English", keywords=df['queries'].tolist())
#     response = client.post("/keywords_data/google/search_volume/live", post_data)
#     if response["status_code"] == 20000: response.keys()
#     else: print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
#     keyword_df = json_normalize(data=response['tasks'][0]['result'])
#     keyword_df.rename(columns={'keyword': 'queries'}, inplace=True)
#     df4_merged = df.merge(keyword_df, how='right', on='queries')
#
#     # download csv file
#     # progress bar
#     # st.markdown("Preparing CSV file...")
#     # progress_bar(list_size, pb_speed)
#
#     cleanQuery = re.sub('\W+','', keyword_list[0])
#     file_name = cleanQuery + ".csv"
#     df4_merged.to_csv(file_name, encoding='utf-8', index=True)
#     csv_download_button = download_button(df4_merged, file_name, 'Download List')
#
# def step2():
#
#     # Preparing data for visualization
#     # progress bar
#     # st.markdown("Preparing data for visualization...")
#     # progress_bar(list_size, pb_speed)
#
#     s = df4_merged.apply(lambda x: pd.Series(x['types'],), axis=1).stack().reset_index(level=1, drop=True)
#     s.name = 'types'
#     df5 = df4_merged.drop('types', axis=1).join(s)
#     df5['types'] = pd.Series(df5['types'], dtype=object)
#     p = df5.apply(lambda x: pd.Series(x['entities'],), axis=1).stack().reset_index(level=1, drop=True)
#     p.name = 'entities'
#     df6 = df5.drop('entities', axis=1).join(p)
#     df6['entities'] = pd.Series(df6['entities'], dtype=object)
#
#     # figures
#     # progress bar
#     # st.markdown("Preparing treemaps...")
#     # progress_bar(list_size, pb_speed)
#
#     fig1 = px.histogram(df6, x='entities').update_xaxes(categoryorder="total descending")
#     df6['all'] = 'all'
#     fig2 = px.treemap(df6, path=['all','types','entities','queries'], color='entities')
#     fig3 = px.treemap(df4_merged, path=['entities'], values='competition', color='competition', color_continuous_scale='Blues')
#     df6 = df6.dropna(subset=['search_volume', 'competition'])
#     fig4 = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='search_volume', color_continuous_scale='Blues')
#     fig5 = px.treemap(df6, path=['all','entities','queries'], values='competition', color='competition', color_continuous_scale='purpor')
#     fig6 = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='competition', color_continuous_scale='blues', color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))
#
# def switch_chart():
#
#     chart_types = ['Top Entities', 'Intent by Type and Entity', 'Intent by Entity and Search Volume', 'Intent by Search Volume and Competition', 'Intent by Entity and Competition', 'Intent by Entity, Search Volume and Competition']
#     chart_navigation = st.selectbox('Please choose preferred chart type:', chart_types, index = 2)
#
#     if chart_navigation == 'Top Entities': output = st.plotly_chart(fig1)
#     elif chart_navigation == 'Intent by Type and Entity': output = st.plotly_chart(fig2)
#     elif chart_navigation == 'Intent by Entity and Search Volume': output = st.plotly_chart(fig3)
#     elif chart_navigation == 'Intent by Search Volume and Competition': output = st.plotly_chart(fig4)
#     elif chart_navigation == 'Intent by Entity and Competition': output = st.plotly_chart(fig5)
#     elif chart_navigation == 'Intent by Entity, Search Volume and Competition': output = st.plotly_chart(fig6)
#
#     return output
#
def app():

    state = _get_state()

    # <-- UI -->
    local_css("style.css")

    set_png_as_page_bg('img/pattern.png')

    # ui()
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

    display_state_values(state)
    st.write("---")

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        languages = ["EN", "IT", "ES", "DE"]
        state.lang_option = st.selectbox("Select Language", languages, languages.index(state.lang_option) if state.lang_option else 0)
        state.first_idea = st.text_input("What is the first idea?", state.first_idea or "")
    with col2:
        countries = ["US", "UK", "IN", "ES", "IT", "DE"]
        state.country_option = st.selectbox("Select Country", countries, countries.index(state.country_option) if state.country_option else 0)
        state.second_idea = st.text_input("What is the second idea?", state.second_idea or "")
    with col3:
        state.WL_key_ti = st.text_input("Enter your WordLift key", state.WL_key_ti or "")
        state.third_idea = st.text_input("What is the third idea?", state.third_idea or "")
    size = ['Small (25 Queries)', 'Medium (50 Queries)', 'Large (100 Queries)', 'X-Large (700 Queries)']
    state.size_navigation = st.radio('Please specify preferred queries list size, then press Submit', size, size.index(state.size_navigation) if state.size_navigation else 0)
    state.submit_button = st.button("Submit", state.submit_button)

    if state.submit_button:
        # <-- user input conditions -->
        # 1- WordLift Key
        if state.WL_key_ti:
            WL_key = state.WL_key_ti
        elif not state.WL_key_ti:
            st.error("Please provide your WordLift key to proceed.")
            st.stop()
        # 2- query list size
        if state.size_navigation == 'Small (25 Queries)':
            list_size = 25 # when i tried the funds queries, 10 gave me error because treemap couldnnt it is small
            pb_speed = 2.5
        elif state.size_navigation == 'Medium (50 Queries)':
            list_size = 50
            pb_speed = 5
        elif state.size_navigation == 'Large (100 Queries)':
            list_size = 100
            pb_speed = 10
        elif state.size_navigation == 'X-Large (700 Queries)':
            list_size = 700
            pb_speed = 70
        # 3- keywords list
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

        list_size = 5
        pb_speed = 5

        # step1()

        keywords = [generate_keywords(q) for q in keyword_list]
        keywords = [query for sublist in keywords for query in sublist]
        keywords = list(set(keywords))
        df = pd.DataFrame(keywords, columns =['queries'])
        df = df.head(list_size)
        df['entities'] = ''
        df['types'] = ''

        for index, row in df.iterrows():
            data_x = string_to_entities(df['queries'][index])
            if len(data_x[0]) is not 0:
                df.at[index,'entities'] = data_x[0]
                df.at[index,'types'] = data_x[1]
            else:
                df.at[index,'entities'] = 'n.a.'
                df.at[index,'types'] = 'uncategorized'

        client = RestClient(WL_key)
        post_data = dict()
        post_data[len(post_data)] = dict(location_name="United States", language_name="English", keywords=df['queries'].tolist())
        response = client.post("/keywords_data/google/search_volume/live", post_data)
        if response["status_code"] == 20000: response.keys()
        else: print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
        keyword_df = json_normalize(data=response['tasks'][0]['result'])
        keyword_df.rename(columns={'keyword': 'queries'}, inplace=True)
        df4_merged = df.merge(keyword_df, how='right', on='queries')

        cleanQuery = re.sub('\W+','', keyword_list[0])
        file_name = cleanQuery + ".csv"
        df4_merged.to_csv(file_name, encoding='utf-8', index=True)
        csv_download_button = download_button(df4_merged, file_name, 'Download List')

        st.subheader("1- Queries List")
        st.markdown("Please wait while we prepare your queries list...")
        progress_bar(list_size, pb_speed)
        balloons("list of queries")
        st.dataframe(df4_merged)
        st.write("Total number of queries saved on (",file_name, ")is",len(df))
        st.markdown(csv_download_button, unsafe_allow_html=True)

        # step2()

        s = df4_merged.apply(lambda x: pd.Series(x['types'],), axis=1).stack().reset_index(level=1, drop=True)
        s.name = 'types'
        df5 = df4_merged.drop('types', axis=1).join(s)
        df5['types'] = pd.Series(df5['types'], dtype=object)
        p = df5.apply(lambda x: pd.Series(x['entities'],), axis=1).stack().reset_index(level=1, drop=True)
        p.name = 'entities'
        df6 = df5.drop('entities', axis=1).join(p)
        df6['entities'] = pd.Series(df6['entities'], dtype=object)

        fig1 = px.histogram(df6, x='entities').update_xaxes(categoryorder="total descending")
        df6['all'] = 'all'
        fig2 = px.treemap(df6, path=['all','types','entities','queries'], color='entities')
        fig3 = px.treemap(df4_merged, path=['entities'], values='competition', color='competition', color_continuous_scale='Blues')
        df6 = df6.dropna(subset=['search_volume', 'competition'])
        fig4 = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='search_volume', color_continuous_scale='Blues')
        fig5 = px.treemap(df6, path=['all','entities','queries'], values='competition', color='competition', color_continuous_scale='purpor')
        fig6 = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='competition', color_continuous_scale='blues', color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))

        st.subheader("2- Treemap")
        st.markdown("Please wait while we prepare your treemap...")
        progress_bar(list_size, pb_speed)
        balloons("treemap")

        # If i used session state or url get/set query parameters, i'll maintain the “button pushed” flag
        # which will allow us to persist the button pushed state across runs.
        chart_types = ['Top Entities', 'Intent by Type and Entity', 'Intent by Entity and Search Volume', 'Intent by Search Volume and Competition', 'Intent by Entity and Competition', 'Intent by Entity, Search Volume and Competition']
        state.chart_navigation = st.selectbox('Please choose preferred chart type:', chart_types, chart_types.index(state.chart_navigation) if state.chart_navigation else 2)

        if state.chart_navigation == 'Top Entities': st.plotly_chart(fig1)
        elif state.chart_navigation == 'Intent by Type and Entity': st.plotly_chart(fig2)
        elif state.chart_navigation == 'Intent by Entity and Search Volume': st.plotly_chart(fig3)
        elif state.chart_navigation == 'Intent by Search Volume and Competition': st.plotly_chart(fig4)
        elif state.chart_navigation == 'Intent by Entity and Competition': st.plotly_chart(fig5)
        elif state.chart_navigation == 'Intent by Entity, Search Volume and Competition': st.plotly_chart(fig6)

    state.sync()

    # <-- app functionality -->
    # f1,f2 = st.beta_columns(2)


    # 1- queries list
    # with f1:
    #     show1 = st.checkbox('Show Queries List')
    #     if show1:
    #         step1()
    #         st.subheader("1- Queries List")
    #         st.markdown("Please wait while we prepare your queries list...")
    #         progress_bar(list_size, pb_speed)
    #         balloons("list of queries")
    #         st.dataframe(df4_merged)
    #         st.write("Total number of queries saved on (",file_name, ")is",len(df))
    #         st.markdown(csv_download_button, unsafe_allow_html=True)

    # 2- treemap
    # with f2:
    #     show2 = st.checkbox('Show Treemaps')
    #     if show2:
    #         step2()
    #         st.subheader("2- Treemap")
    #         st.markdown("Please wait while we prepare your treemap...")
    #         progress_bar(list_size, pb_speed)
    #         balloons("treemap")
    #         switch_chart()
