# <-- Libraries -->
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import json
import re
import time
from random import randint
from fake_useragent import UserAgent
from http.client import HTTPSConnection
from json import loads
from json import dumps
from pandas import json_normalize
from pandas import Series

from functions.download import download_button
from functions.interface import *

language = ''
country = ''
WL_key = ''
x = 0

@st.cache(show_spinner=False)
def autocomplete(query):
    ua = UserAgent(verify_ssl=False)
    tld = country
    lan = language
    time.sleep(randint(0, 2))
    URL = 'http://suggestqueries.google.com/complete/search?client=firefox&gl={0}&q={1}&hl={2}'.format(tld,query,lan)
    headers = {'User-agent':ua.random}
    response = requests.get(URL, headers=headers)
    result = json.loads(response.content.decode('utf-8'))
    return result[1]

@st.cache(suppress_st_warning=True, show_spinner=False)
def generate_keywords(query):
    seed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    st.write('Grabbing suggestions for ... ' + str(query))
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

def app():
    # <-- UI -->
    local_css("style.css")
    set_png_as_page_bg('img/pattern.png')
    st.title('WordLift API')
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
    size = ["Small (10 Queries)", "Medium (40 Queries)", "Large (100 Queries)"]
    size_navigation = st.selectbox("Please specify preferred queries list size, then press GO!", size)
    go_button = st.button("GO!")

    if go_button:
        # <-- user input conditions -->
        # 1- WordLift Key
        if WL_key_ti:
            WL_key = WL_key_ti
        elif not WL_key_ti:
            st.error("Please provide your WordLift key to proceed.")
            st.stop()
        # 2- query list size
        if size_navigation == 'Small (10 Queries)': list_size = 10
        elif size_navigation == 'Medium (40 Queries)': list_size = 40
        elif size_navigation == 'Large (100 Queries)': list_size = 100
        # 3- keywords list
        if not (first_idea or second_idea or third_idea):
            st.error("You have not typed any ideas! Please type at least two ideas, then press GO!")
            st.stop()
        elif first_idea:
            if second_idea:
                if third_idea:
                    st.success("success!")
                    keyword_list = first_idea + ', ' + second_idea + ', ' + third_idea
                elif not third_idea:
                    st.success("success!")
                    keyword_list = first_idea + ', ' + second_idea
            elif not (second_idea or third_idea):
                st.error("You have typed only one idea! Please type at least two ideas, then press GO!")
                st.stop()
        keyword_list = keyword_list.strip('][').split(', ')

        # <-- app functionality -->
        # 1- queries list
        st.subheader("1- Queries List")
        st.markdown("Please wait while we prepare your queries list...")
        keywords = [generate_keywords(q) for q in keyword_list]
        keywords = [query for sublist in keywords for query in sublist]
        keywords = list(set(keywords))
        df = pd.DataFrame(keywords, columns =['queries'])
        df = df.head(list_size)
        df['entities'] = ''
        df['types'] = ''
        progress_bar()
        balloons("list of queries")
        st.dataframe(df['queries'])

        # inner function
        @st.cache(show_spinner=False)
        def wl_nlp(text, language, key):
            API_URL = "https://api.wordlift.io/analysis/single"
            data_in = {
                "content": text, "annotations": {},
                "contentLanguage": language, "contentType": "text",
                "exclude": [], "scope": "local"}
            headers_in = {
                    "Content-Type": "application/json;charset=UTF-8",
                    "Accept": "application/json;charset=UTF-8",
                    "Authorization" : "Key " + key}
            response = requests.post(API_URL, headers = headers_in, json=data_in)
            if response.ok:
                json_response = json.loads(response.text)
                json_response = json_response.get('entities')
                entity_data = []
                type_data = []
                for key in json_response:
                   entity_data.append(json_response[key]['label'])
                   type_data.append(json_response[key]['mainType'])
            return entity_data, type_data

        # inner function
        @st.cache(allow_output_mutation=True, show_spinner=False)
        def string_to_entities(text, language=language, key=WL_key):
            entities = wl_nlp(text,language, key)
            entity_data = entities[0]
            type_data = entities[1]
            return entity_data, type_data

        # inner class
        class RestClient:
            domain = "api.wordlift.io"
            def request(self, path, method, data=None):
                connection = HTTPSConnection(self.domain)
                try:
                    headers = {'Authorization' : 'Key ' +  WL_key}
                    connection.request(method, path, headers=headers, body=data)
                    response = connection.getresponse()
                    return loads(response.read().decode())
                finally:
                    connection.close()
            def get(self, path):
                return self.request(path, 'GET')
            def post(self, path, data):
                if isinstance(data, str):
                    data_str = data
                else:
                    data_str = dumps(data)
                return self.request(path, 'POST', data_str)

        # 2- treemap
        st.subheader("2- Treemap")
        st.markdown("Please wait while we prepare your treemap...")
        for index, row in df.iterrows():
            data_x = string_to_entities(df['queries'][index])
            if len(data_x[0]) is not 0:
                df.at[index,'entities'] = data_x[0]
                df.at[index,'types'] = data_x[1]
            else:
                df.at[index,'entities'] = 'n.a.'
                df.at[index,'types'] = 'uncategorized'
        client = RestClient()
        post_data = dict()
        post_data[len(post_data)] = dict(location_name="United States", language_name="English", keywords=df['queries'].tolist())
        response = client.post("/keywords_data/google/search_volume/live", post_data)
        if response["status_code"] == 20000: st.write(response)
        else: st.error("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
        response.keys()
        keyword_df = json_normalize(data=response['tasks'][0]['result'])
        keyword_df.rename(columns={'keyword': 'queries'}, inplace=True)
        df4_merged = df.merge(keyword_df, how='right', on='queries')
        s = df4_merged.apply(lambda x: pd.Series(x['types'],), axis=1).stack().reset_index(level=1, drop=True)
        s.name = 'types'
        df5 = df4_merged.drop('types', axis=1).join(s)
        df5['types'] = pd.Series(df5['types'], dtype=object)
        p = df5.apply(lambda x: pd.Series(x['entities'],), axis=1).stack().reset_index(level=1, drop=True)
        p.name = 'entities'
        df6 = df5.drop('entities', axis=1).join(p)
        df6['entities'] = pd.Series(df6['entities'], dtype=object)
        fig = px.histogram(df6, x='entities').update_xaxes(categoryorder="total descending")
        df6['all'] = 'all'
        fig = px.treemap(df6, path=['all','types','entities','queries'], color='entities')
        df6 = df6.dropna(subset=['search_volume', 'competition'])
        fig = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='search_volume', color_continuous_scale='Blues')
        fig = px.treemap(df6, path=['all','entities','queries'], values='competition', color='competition', color_continuous_scale='purpor')
        fig = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='competition', color_continuous_scale='blues', color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))
        progress_bar()
        balloons("treemap")
        st.plotly_chart(fig)

        # 3- download csv file
        st.subheader("3- CSV")
        st.markdown("Please wait while we prepare your CSV file...")
        cleanQuery = re.sub('\W+','', keyword_list[0])
        file_name = cleanQuery + ".csv"
        df.to_csv(file_name, encoding='utf-8', index=True)
        csv_download_button = download_button(df, file_name, 'Click to download your data!')
        progress_bar()
        balloons("CSV")
        st.write("Total number of queries saved on (",file_name, ")is",len(df))
        st.markdown(csv_download_button, unsafe_allow_html=True)
