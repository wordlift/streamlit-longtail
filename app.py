# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 2021

@author: AndreaVolpini
@co-author: RaffalShafiei
"""

# ---------------------------------------------------------------------------- #
# Imports
# ---------------------------------------------------------------------------- #

# from fake_useragent import UserAgent
#
# import time
# from random import randint

# import requests, json

from Interface import *
from download import *

# dirty fix for the SSL bug
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# ---------------------------------------------------------------------------- #
# App Config.
# ---------------------------------------------------------------------------- #
PAGE_CONFIG = {
    "page_title": "Free SEO Tools by WordLift", "page_icon": "img/fav-ico.png", "layout": "wide"}
st.set_page_config(**PAGE_CONFIG)

local_css("style.css")
set_png_as_page_bg('img/pattern.png')


# 1st API
def page_WordLift():
    st.write("---")


# 2nd API
def page_SpaCy():
    st.write("---")


pages = {
    "WordLift": page_WordLift,
    "SpaCy": page_SpaCy,
}

# ---------------------------------------------------------------------------- #
# Sidebar
# ---------------------------------------------------------------------------- #
st.sidebar.image("img/logo-wordlift.png", width=200)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select your API", tuple(pages.keys()))
st.sidebar.info(
    "You will need a WordLift key. You can [get one for free](https://wordlift.io) for 14 days.")

# ---------------------------------------------------------------------------- #
# Web Application
# ---------------------------------------------------------------------------- #
st.markdown('<p class="subject"> 🔥 Content Idea Generator 🔥 </p>',
            unsafe_allow_html=True)
st.markdown('<p class="payoff"> Get instant, untapped content ideas </p>',
            unsafe_allow_html=True)
pages[page]()
st.markdown('<p class="question"> How it works? </p>', unsafe_allow_html=True)
st.markdown("""
<p class="answer">
    WordLift will “read” autocomplete data from Google, scan it using the
    Knowledge Graph from your website (or the SpaCy API) then quickly analyze
    every search opportunity to help you create super-useful content.
</p>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------- #
# Getting ideas and Context
# ---------------------------------------------------------------------------- #  | Languages       | Countries
# ______________________________________
languages = ["en", "it", "de", "nl", "pt", "es", "fr"]
countries = ["us", "uk", "au", "in", "ca",
             # countries that speak English         | en (english)    | us, uk, au, in, ca
             # countries that speak Italian                                 | it (italian)    | it
             "it",
             # countries that speak German                                  | de (german)     | de
             "de",
             "nl", "bel",
             # countries that speak Dutch                            | nl (dutch)      | nl (netherlands), bel (Belgium)
             # countries that speak Portuguese                        | pt (portuguese) | pt, br
             "pt", "br",
             # countries that speak Spanish                                 | es (spanish)    | es
             "es",
             "fr"]  # countries that speak French                                  | fr (french)     | fr

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
st.write("---")

with col1:
    lang_option = st.selectbox("Select Language", languages)
with col2:
    country_option = st.selectbox("Select Country", countries)
with col3:
    WL_key_ti = st.text_input("Enter your WordLift key")

with col4:
    first_idea = st.text_input("What is the first idea?")
with col5:
    second_idea = st.text_input("What is the second idea?")
with col6:
    third_idea = st.text_input("What is the third idea?")

size = ['Small (25 Queries)', 'Medium (50 Queries)',
        'Large (100 Queries)', 'X-Large (700 Queries)']
size_navigation = st.radio(
    'Please specify preferred queries list size, then press Submit', size)

button_submit = st.button("Submit")
st.write("---")

language = ""
country = ""


# ---------------------------------------------------------------------------- #
# Main Function
# ---------------------------------------------------------------------------- #
def main():
    if button_submit:

        language = lang_option
        country = country_option

        if WL_key_ti:
            WL_key = WL_key_ti
        elif not WL_key_ti:
            st.error("Please provide your WordLift key to proceed.")
            st.stop()

        if size_navigation == 'Small (25 Queries)':
            list_size = 25
        elif size_navigation == 'Medium (50 Queries)':
            list_size = 50
        elif size_navigation == 'Large (100 Queries)':
            list_size = 100
        elif size_navigation == 'X-Large (700 Queries)':
            list_size = 700

        sucsess = st.empty()
        if not (first_idea or second_idea or third_idea):
            st.error(
                "You have not typed any ideas! Please type at least two ideas, then press Submit")
            st.stop()
        elif first_idea:
            if second_idea:
                if third_idea:
                    sucsess.success("SUCCESS!")
                    keyword_list = first_idea + ', ' + second_idea + ', ' + third_idea
                elif not third_idea:
                    sucsess.success("SUCCESS!")
                    keyword_list = first_idea + ', ' + second_idea
            elif not (second_idea or third_idea):
                sucsess.success("SUCCESS!")
                keyword_list = first_idea
        keyword_list = keyword_list.strip('][').split(
            ', ')  # converting string into list

        # autocomplete

        # placeholder1 = st.empty()
        # info1 = st.empty()
        # info2 = st.empty()

        # generate_keywords
        from autocomplete import generate_keywords

        # placeholder1.info("Expanding initial ideas using Google's autocomplete")
        keywords = [generate_keywords(q, country, language)
                    for q in keyword_list]
        # to flatten
        keywords = [query for sublist in keywords for query in sublist]
        keywords = list(set(keywords))  # to de-duplicate

        sucsess.empty()
        # info1.empty()
        # info2.empty()
        # placeholder1.empty()

        st.header(":rocket: Queries List")
        mark1 = st.empty()
        mark1.markdown("Please wait while we prepare your queries list...")

        placeholder2 = st.empty()
        placeholder2.info("Analyzing the queries we have generated ⏳ ...")

        df = pd.DataFrame(keywords, columns=['queries'])
        df = df.head(list_size)
        df['entities'] = ''
        df['types'] = ''

        # ---------------------------------------------------------------------------- #
        # Run NER with SpaCy
        # ---------------------------------------------------------------------------- #
        import en_core_web_sm
        nlp = en_core_web_sm.load()

        # Extracting entities and types using SpaCy
        def string_to_entities(text):
            entities = nlp(text)
            entity_data = [x.text for x in entities.ents]
            type_data = [x.label_ for x in entities.ents]
            return entity_data, type_data

        entity_data = []
        type_data = []

        # ---------------------------------------------------------------------------- #
        # Run NER with WordLift
        # ---------------------------------------------------------------------------- #
        # wl_nlp

        # Extracting entities and types using WordLift
        # wl_string_to_entities
        from wl_api import wl_string_to_entities

        placeholder2.info("Extracting entities from queries ⏳ ...")

        # ---------------------------------------------------------------------------- #
        # Extracting Entities from Queries
        # ---------------------------------------------------------------------------- #
        def extract():
            # Iterating through queries
            for index, row in df.iterrows():

                if page == "WordLift":  # 1) WordLift
                    data_x = wl_string_to_entities(
                        df['queries'][index], language, WL_key)  # extracting entities
                if page == "SpaCy":  # 2) SpaCy
                    data_x = string_to_entities(
                        df['queries'][index])  # extracting entities

                if len(data_x[0]) != 0:  # make sure there are entities
                    df.at[index, 'entities'] = data_x[0]
                    df.at[index, 'types'] = data_x[1]
                else:
                    df.at[index, 'entities'] = 'n.a.'
                    df.at[index, 'types'] = 'uncategorized'

        extract()

        # ---------------------------------------------------------------------------- #
        # Adding keyword data
        # ---------------------------------------------------------------------------- #
        from http.client import HTTPSConnection
        from json import loads
        from json import dumps

        class RestClient:
            domain = "api.wordlift.io"

            @st.cache(show_spinner=False)
            def request(self, path, method, data=None):
                connection = HTTPSConnection(self.domain)
                try:
                    headers = {'Authorization': 'Key ' + WL_key}
                    connection.request(
                        method, path, headers=headers, body=data)
                    response = connection.getresponse()
                    return loads(response.read().decode())
                finally:
                    connection.close()

            @st.cache(show_spinner=False)
            def get(self, path):
                return self.request(path, 'GET')

            @st.cache(show_spinner=False)
            def post(self, path, data):
                if isinstance(data, str):
                    data_str = data
                else:
                    data_str = dumps(data)
                return self.request(path, 'POST', data_str)

        placeholder2.info("Adding keyword data ⏳ ...")

        client = RestClient()

        if language == 'en':
            language_name1 = "English"
        elif language == 'it':
            language_name1 = "Italian"
        elif language == 'de':
            language_name1 = "German"
        elif language == 'nl':
            language_name1 = "German"
        elif language == 'pt':
            language_name1 = "Portuguese"
        elif language == 'es':
            language_name1 = "Spanish"
        elif language == 'fr':
            language_name1 = "French"

        if country == 'us':
            location_name1 = "United States"
        elif country == 'uk':
            location_name1 = "United Kingdom"
        elif country == 'au':
            location_name1 = "Australia"
        elif country == 'in':
            location_name1 = "India"
        elif country == 'ca':
            location_name1 = "Canada"
        elif country == 'it':
            location_name1 = "Italy"
        elif country == 'de':
            location_name1 = "Germany"
        elif country == 'nl':
            location_name1 = "Netherlands"
        elif country == 'bel':
            location_name1 = "Belgium"
        elif country == 'pt':
            location_name1 = "Portugal"
        elif country == 'br':
            location_name1 = "Brazil"
        elif country == 'es':
            location_name1 = "Spain"
        elif country == 'fr':
            location_name1 = "France"

        post_data = dict()
        # here is the basic settings
        post_data[len(post_data)] = dict(
            location_name=location_name1,
            language_name=language_name1,
            keywords=df['queries'].tolist()
        )

        #response = client.post("/keywords_data/google/search_volume/live", post_data)
        response = client.post(
            "/dataforseo_labs/google/historical_search_volume/live", post_data)

        if response["status_code"] == 20000:
            print(response)

        else:
            print("error. Code: %d Message: %s" %
                  (response["status_code"], response["status_message"]))

        from pandas import json_normalize
        response.keys()
        keyword_df = json_normalize(
            # data=response['tasks'][0]['result'])
            data=response['tasks'][0]['result'][0]['items'])
        keyword_df.rename(columns={'keyword': 'queries', 'impressions_info.daily_impressions_average': 'search_volume',
                          'keyword_info.competition': 'competition'}, inplace=True)

        placeholder2.info("Merging queries with keyword data ⏳ ...")
        df4_merged = df.merge(keyword_df, how='right', on='queries')

        placeholder2.info("Preparing your CSV file ⏳ ...")
        cleanQuery = re.sub('\W+', '', keyword_list[0])
        file_name = cleanQuery + ".csv"
        df4_merged.to_csv(file_name, encoding='utf-8', index=True)
        csv_download_button = download_button(
            df4_merged, file_name, 'Download List')
        placeholder2.empty()

        progress_bar(list_size)
        balloons("list of queries")
        mark1.empty()
        # four = st.dataframe(df4_merged)

        st.write("Total number of queries saved on (", file_name, ")is", len(df))
        st.markdown(csv_download_button, unsafe_allow_html=True)
        st.write("---")

        # ---------------------------------------------------------------------------- #
        # Treemaps
        # ---------------------------------------------------------------------------- #
        st.header(":rocket: Treemaps")
        mark2 = st.empty()
        mark2.markdown("Please wait while we prepare your treemaps...")

        placeholder3 = st.empty()
        placeholder3.info("Preparing data for visualization ⏳ ...")

        from pandas import Series

        s = df4_merged.apply(lambda x: pd.Series(
            x['types'], ), axis=1).stack().reset_index(level=1, drop=True)
        s.name = 'types'
        df5 = df4_merged.drop('types', axis=1).join(s)
        df5['types'] = pd.Series(df5['types'], dtype=object)

        p = df5.apply(lambda x: pd.Series(x['entities'], ), axis=1).stack(
        ).reset_index(level=1, drop=True)
        p.name = 'entities'

        df6 = df5.drop('entities', axis=1).join(p)
        df6['entities'] = pd.Series(df6['entities'], dtype=object)

        placeholder3.info("Visualizing ⏳ ...")

        import plotly.express as px
        import numpy as np

        # 1 Visualizing top entities
        fig1 = px.histogram(df6, x='entities').update_xaxes(
            categoryorder="total descending")

        # in order to have a single root node
        df6['all'] = 'all'

        # remove rows when there are missing values
        df6 = df6.dropna(subset=['search_volume', 'competition'])

        # 2 Intent by Entity, Search Volume and Competition
        fig2 = px.treemap(df6, path=['all', 'entities', 'queries'], values='search_volume',
                          color='competition',
                          color_continuous_scale='blues',
                          color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))

        placeholder3.empty()

        pb2 = progress_bar(list_size)
        b2 = balloons("treemap")
        mark2.empty()

        # 1
        st.subheader("Top Entities")  # ☑️
        first = st.plotly_chart(fig1, use_container_width=True)

        # 2
        st.subheader("Intents by Entity, Search Volume and Competition")  # ☑️
        second = st.plotly_chart(fig2, use_container_width=True)


if __name__ == "__main__":
    main()
