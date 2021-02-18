import streamlit as st

from fake_useragent import UserAgent

import time
from random import randint
import pprint
import pandas as pd
import re
import requests, json

import SessionState
from src.Interface import *
from src.download import *

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

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        languages = ["en", "it", "es", "de"]
        state.lang_option = st.selectbox("Select Language", languages)
    with col2:
        countries = ["us", "uk", "in", "es", "it", "de"]
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

        language = state.lang_option
        country = state.country_option

        if state.WL_key_ti:
            WL_key = state.WL_key_ti
        elif not state.WL_key_ti:
            st.error("Please provide your WordLift key to proceed.")
            st.stop()

        if state.size_navigation == 'Small (25 Queries)':
            state.list_size = 25
        elif state.size_navigation == 'Medium (50 Queries)':
            state.list_size = 50
        elif state.size_navigation == 'Large (100 Queries)':
            state.list_size = 100
        elif state.size_navigation == 'X-Large (700 Queries)':
            state.list_size = 700

        if not (state.first_idea or state.second_idea or state.third_idea):
            st.error("You have not typed any ideas! Please type at least two ideas, then press Submit")
            st.stop()
        elif state.first_idea:
            if state.second_idea:
                if state.third_idea:
                    st.success("SUCCESS!")
                    state.keyword_list = state.first_idea + ', ' + state.second_idea + ', ' + state.third_idea
                elif not state.third_idea:
                    st.success("SUCCESS!")
                    state.keyword_list = state.first_idea + ', ' + state.second_idea
            elif not (state.second_idea or state.third_idea):
                st.error("You have typed only one idea! Please type at least two ideas, then press Submit")
                st.stop()
        state.keyword_list = state.keyword_list.strip('][').split(', ') # converting string into list

        @st.cache(show_spinner = False)
        def autocomplete(query):

            '''
            USING GOOGLE SEARCH AUTOCOMPLETE

            tld = the country to use for the Google Search. It's a two-letter country code. (e.g., us for the United States).
            Head to the Google countries for a full list of supported Google countries.

            lan = the language to use for the Google Search. It's a two-letter lan guage code. (e.g., en for English).
            Head to the Google languages for a full list of supported Google languages.

            '''
            ua = UserAgent(verify_ssl=False)
            tld = country
            lan = language

            time.sleep(randint(0, 2))

            import requests, json

            URL = 'http://suggestqueries.google.com/complete/search?client=firefox&gl={0}&q={1}&hl={2}'.format(tld,query,lan)

            headers = {'User-agent':ua.random}
            response = requests.get(URL, headers=headers)
            result = json.loads(response.content.decode('utf-8'))
            return result[1]

        @st.cache(suppress_st_warning = True, show_spinner = False)
        def generate_keywords(query):
            '''
            Function to generate a large number of keyword suggestions
            '''
            seed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            st.write('Grabbing suggestions for (' + str(query) + ') ...')
            first_pass = autocomplete(query)
            second_pass = [autocomplete(x) for x in first_pass]
            flat_second_pass = []
            flat_second_pass = [query for sublist in second_pass for query in sublist]
            third_pass = [autocomplete(query + ' ' + x) for x in seed]
            flat_third_pass = []
            flat_third_pass = [query for sublist in third_pass for query in sublist]

            keyword_suggestions = list(set(first_pass + flat_second_pass + flat_third_pass))
            keyword_suggestions.sort()
            st.write('SUCCESS!')
            return keyword_suggestions

        # i think i sould replace every st.write in loading with st.info and then after execution i get rid of it
        st.write("Expanding initial ideas using Google's autocomplete...")
        state.keywords = [generate_keywords(q) for q in state.keyword_list]
        state.keywords = [query for sublist in state.keywords for query in sublist] # to flatten
        state.keywords = list(set(state.keywords)) # to de-duplicate
        st.write("---")

        st.header(":rocket: Queries List")
        st.markdown("Please wait while we prepare your queries list...")

        st.info("Analyzing the queries we have generated...")
        state.df = pd.DataFrame(state.keywords, columns =['queries'])
        state.df = state.df.head(state.list_size)
        state.df['entities'] = ''
        state.df['types'] = ''
        # state.one = st.dataframe(state.df['queries'])
        # st.write("---")

        # Display the selected page with the session state
        pages[page](state)

        entity_data = []
        type_data = []

        @st.cache(show_spinner = False)
        def wl_nlp(text, language, key):

            API_URL = "https://api.wordlift.io/analysis/single"
            # preparing the data for the analysis
            data_in = {
                "content": text,
                "annotations": {},
                "contentLanguage": language,
                "contentType": "text",
                "exclude": [],
                "scope": "local"} # change this to "global" for all entities or to "local" to use only entities from the local KG
        	# adding headers and the key
            headers_in = {
                    "Content-Type": "application/json;charset=UTF-8",
                    "Accept": "application/json;charset=UTF-8",
                    "Authorization" : "Key " + key}
            response = requests.post(API_URL, headers = headers_in, json=data_in)
            if response.ok: # make sure connection is fine
                json_response = json.loads(response.text) # read the json response
                json_response = json_response.get('entities') # select "entities"
                entity_data = []
                type_data = []

                for key in json_response:
                    entity_data.append(json_response[key]['label']) # creating the list for labels
                    type_data.append(json_response[key]['mainType']) # creating the list for types

            return entity_data, type_data

        # Extracting entities and types using WordLift
        def string_to_entities(text, language=language, key=WL_key):
            entities = wl_nlp(text, language, key)
            entity_data = entities[0]
            type_data = entities[1]
            return entity_data, type_data

        st.info("Extracting entities from queries...")
        @st.cache(show_spinner = False)
        def extract():
            # Iterating through queries
            for index, row in state.df.iterrows():
                data_x = string_to_entities(state.df['queries'][index]) # extracting entities
                if len(data_x[0]) is not 0: # make sure there are entities
                  state.df.at[index,'entities'] = data_x[0]
                  state.df.at[index,'types'] = data_x[1]
                else:
                  state.df.at[index,'entities'] = 'n.a.'
                  state.df.at[index,'types'] = 'uncategorized'

        extract()

        # st.write('we have found:', len(state.df), 'intents to cover')
        # state.two = st.dataframe(state.df)
        # st.write('---')

        from http.client import HTTPSConnection
        from json import loads
        from json import dumps

        class RestClient:
            domain = "api.wordlift.io"

            @st.cache(show_spinner = False)
            def request(self, path, method, data=None):
                connection = HTTPSConnection(self.domain)
                try:
                    headers = {'Authorization' : 'Key ' +  WL_key}
                    connection.request(method, path, headers=headers, body=data)
                    response = connection.getresponse()
                    return loads(response.read().decode())
                finally:
                    connection.close()

            @st.cache(show_spinner = False)
            def get(self, path):
                return self.request(path, 'GET')

            @st.cache(show_spinner = False)
            def post(self, path, data):
                if isinstance(data, str):
                    data_str = data
                else:
                    data_str = dumps(data)
                return self.request(path, 'POST', data_str)

        st.info("Adding keyword data...")
        state.client = RestClient()
        state.post_data = dict()

        state.post_data[len(state.post_data)] = dict(
            location_name="United States",
            language_name="English",
            keywords=state.df['queries'].tolist()
        )

        state.response = state.client.post("/keywords_data/google/search_volume/live", state.post_data)

        if state.response["status_code"] == 20000:
            print(state.response)
        else:
            print("error. Code: %d Message: %s" % (state.response["status_code"], state.response["status_message"]))

        from pandas import json_normalize
        state.response.keys()
        state.keyword_df = json_normalize(data=state.response['tasks'][0]['result'])

        state.keyword_df.rename(columns={'keyword': 'queries'}, inplace=True)

        # st.text("Here is the list of queries augmented with keyword data (cpc, search volume and competition)")
        # state.three = st.dataframe(state.keyword_df)
        # st.write("---")

        st.info("Merging queries with keyword data...")
        state.df4_merged = state.df.merge(state.keyword_df, how='right', on='queries')

        st.info("Preparing your CSV file...")
        state.cleanQuery = re.sub('\W+','', state.keyword_list[0])
        state.file_name = state.cleanQuery + ".csv"
        state.df4_merged.to_csv(state.file_name, encoding='utf-8', index=True)
        state.csv_download_button = download_button(state.df4_merged, state.file_name, 'Download List')

        # شكللي حاررجع البروقرس بار القديم الي من دون تقدم
        state.pb1 = progress_bar(state.list_size)
        state.b1 = balloons("list of queries")
        state.four = st.dataframe(state.df4_merged)
        # st.write("---")
        st.write("Total number of queries saved on (", state.file_name, ")is",len(state.df))
        st.markdown(state.csv_download_button, unsafe_allow_html=True)
        st.write("---")





        # ---------------------------------------------------------------------------------------------------------------




        st.header(":rocket: Treemap")
        st.markdown("Please wait while we prepare your treemaps...")

        st.info("Preparing data for visualization...")
        from pandas import Series

        state.s = state.df4_merged.apply(lambda x: pd.Series(x['types'],), axis=1).stack().reset_index(level=1, drop=True)
        state.s.name = 'types'
        state.df5 = state.df4_merged.drop('types', axis=1).join(state.s)
        state.df5['types'] = pd.Series(state.df5['types'], dtype=object)

        state.p = state.df5.apply(lambda x: pd.Series(x['entities'],), axis=1).stack().reset_index(level=1, drop=True)
        state.p.name = 'entities'

        state.df6 = state.df5.drop('entities', axis=1).join(state.p)
        state.df6['entities'] = pd.Series(state.df6['entities'], dtype=object)

        state.five = st.dataframe(state.df6)

        st.info("Visualizing ...")

        import plotly.express as px
        import numpy as np

        state.fig = px.histogram(state.df6, x='entities').update_xaxes(categoryorder="total descending")

        state.pb2 = progress_bar(state.list_size)
        state.b2 = balloons("treemap")

        # make it a checkbox
        t1, t2, t3, t4, t5, t6 = st.beta_columns(6)
        with t1: state.treemap1 = st.checkbox("Show Top Entities", True)
        with t2: state.treemap2 = st.checkbox("Show Intents by Type and Entity")
        with t3: state.treemap3 = st.checkbox("Show Intents by Entity and Search Volume")
        with t4: state.treemap4 = st.checkbox("Show Intents by Search Volume and Competition")
        with t5: state.treemap5 = st.checkbox("Show Intents by Entity and Competition")
        with t6: state.treemap6 = st.checkbox("Show Intents by Entity, Search Volume and Competition")

        # 1
        if state.treemap1:
            st.subheader("Top Entities")
            state.first = st.plotly_chart(state.fig, use_container_width=True)

        # 2
        state.df6['all'] = 'all' # in order to have a single root node
        state.fig = px.treemap(state.df6, path=['all','types','entities','queries'], color='entities')
        if state.treemap2:
            st.subheader("Intents by Type and Entity")
            state.second = st.plotly_chart(state.fig, use_container_width=True)

        # 3
        state.fig = px.treemap(state.df6, path=['entities'], values='competition', color='competition', color_continuous_scale='Blues')
        if state.treemap3:
            st.subheader("Intents by Entity and Search Volume")
            state.third = st.plotly_chart(state.fig, use_container_width=True)

        # 4
        state.df6 = state.df6.dropna(subset=['search_volume', 'competition']) # remove rows when there are missing values
        state.fig = px.treemap(state.df6, path=['all','entities','queries'], values='search_volume',
                                color='search_volume',
                                color_continuous_scale='Blues')
        if state.treemap4:
            st.subheader("Intents by Search Volume and Competition")
            state.fourth = st.plotly_chart(state.fig, use_container_width=True)

        # 5
        state.fig = px.treemap(state.df6, path=['all','entities','queries'], values='competition',
                                color='competition',
                                color_continuous_scale='purpor')
        if state.treemap5:
            st.subheader("Show Intents by Entity and Competition")
            state.fifth = st.plotly_chart(state.fig, use_container_width=True)

        # 6
        state.fig = px.treemap(state.df6, path=['all','entities','queries'], values='search_volume',
                                color='competition',
                                color_continuous_scale='blues',
                                color_continuous_midpoint=np.average(state.df6['competition'], weights=state.df6['search_volume']))
        if state.treemap6:
            st.subheader("Intents by Entity, Search Volume and Competition")
            state.sixth = st.plotly_chart(state.fig, use_container_width=True)

        st.write("---")
        st.header("Thank you!")
        st.image("img/logo-wordlift.png", width=400)


        # chart_types = ['Top Entities',
        #                 'Intent by Type and Entity',
        #                 'Intent by Entity and Search Volume',
        #                 'Intent by Search Volume and Competition',
        #                 'Intent by Entity and Competition',
        #                 'Intent by Entity, Search Volume and Competition']
        # state.chart_navigation = st.selectbox('Please choose preferred chart type:', chart_types, index = 2)
        # if state.chart_navigation == 'Top Entities':
        # if state.chart_navigation == 'Intent by Type and Entity':
        # if state.chart_navigation == 'Intent by Entity and Search Volume':
        # if state.chart_navigation == 'Intent by Search Volume and Competition':
        # if state.chart_navigation == 'Intent by Entity and Competition':
        # if state.chart_navigation == 'Intent by Entity, Search Volume and Competition':

def page_WordLift(state):
    # st.text("WordLift page")
    # st.write("---")

    import requests, json

def page_SpaCy(state):
    # st.text("SpaCy page")
    # st.write("---")

    # Getting additional hourse power - adding more libraries
    import spacy
    from collections import Counter
    import en_core_web_sm
    nlp = en_core_web_sm.load()

    # Extracting entities and types using SpaCy
    def string_to_entities(text):
        entities = nlp(text)
        entity_data = [x.text for x in entities.ents]
        type_data = [x.label_ for x in entities.ents]
        return entity_data, type_data

if __name__ == "__main__":
    main()
