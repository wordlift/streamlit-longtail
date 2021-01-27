import streamlit as st
from fake_useragent import UserAgent
import time
from random import randint
import pprint
import pandas as pd
import re
import requests, json
import spacy
from collections import Counter
import en_core_web_sm
from http.client import HTTPSConnection
from json import loads
from json import dumps
from pandas import json_normalize
from pandas import Series
import plotly.express as px
import numpy as np
import base64 #
import pickle #
import uuid #
import codecs #
import streamlit.components.v1 as components #

language = ''
country = ''
WL_key = ''
x = 0

nlp = en_core_web_sm.load()

@st.cache(show_spinner=False)
def autocomplete(query):

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

@st.cache(suppress_st_warning=True, show_spinner=False)
def generate_keywords(query):
    '''
    Function to generate a large number of keyword suggestions
    '''
    seed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    st.write('Grabbing suggestions... ' + str(query))
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

def string_to_entities(text):
    entities = nlp(text)
    entity_data = [x.text for x in entities.ents]
    type_data = [x.label_ for x in entities.ents]
    return entity_data, type_data

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

@st.cache(show_spinner=False)
def download_button(object_to_download, download_filename, button_text, pickle_it=False):

    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None
    else:
        if isinstance(object_to_download, bytes):
            pass
        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)
        else:
            object_to_download = json.dumps(object_to_download)
    try:
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()
    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)
    dl_link = f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'
    return dl_link

def app():

    st.title('SpaCy API')

    from multiapp import MultiApp

    s_app = MultiApp()

    s_app.comp()

    language = s_app.lang_option
    country = s_app.country_option

    s_first_idea = s_app.first_idea
    s_second_idea = s_app.second_idea
    s_third_idea = s_app.third_idea

    s_WL_key_ti = s_app.WL_key_ti

    s_size_navigation = s_app.size_navigation

    s_go_button = s_app.go_button

    if s_WL_key_ti:
        WL_key = s_WL_key_ti
    elif not s_WL_key_ti:
        st.stop()

    if s_size_navigation == 'Small': x = 10
    elif s_size_navigation == 'Medium': x = 40
    elif s_size_navigation == 'Large': x = 100

    if s_go_button:

        if not (first_idea or second_idea or third_idea):
            # if users enter no ideas then press go(all are empty strings), they get an error.
            st.error("You have not typed any ideas! Please type at least two ideas, then press GO!")
            st.stop()
        elif first_idea:
            if second_idea:
                if third_idea:
                    # if users enter three ideas, then keyword_list will consist of three ideas
                    st.success("success!")
                    keyword_list = first_idea + ', ' + second_idea + ', ' + third_idea
                elif not third_idea:
                    # if users enter only two ideas, then keyword_list will consist of only two ideas.
                    st.success("success!")
                    keyword_list = first_idea + ', ' + second_idea

            elif not (second_idea or third_idea):
                # if users enter only one idea then press go, they get an error.
                st.error("You have typed only one idea! Please type at least two ideas, then press GO!")
                st.stop()
        keyword_list = keyword_list.strip('][').split(', ')

        # 1
        st.markdown("Please wait while we prepare the queries list of your intents...")
        progress_bar = st.progress(0)
        with st.spinner("Loading..."):
            time.sleep(2)

        keywords = [generate_keywords(q) for q in keyword_list]
        keywords = [query for sublist in keywords for query in sublist] # to flatten
        keywords = list(set(keywords)) # to de-duplicate

        df = pd.DataFrame(keywords, columns =['queries'])
        df = df.head(x)
        df['entities'] = ''
        df['types'] = ''

        st.balloons()
        st.text('Done! thanks for being patient.')
        st.text("Here's the queries list of your intents!")
        st.dataframe(df['queries'])

        # 2
        st.markdown("Please wait while we prepare your treemap...")
        progress_bar = st.progress(0)
        with st.spinner("Loading..."):
            time.sleep(2)
            
        for index, row in df.iterrows():
            data_x = string_to_entities(df['queries'][index]) # extracting entities
            if len(data_x[0]) is not 0: # make sure there are entities
                df.at[index,'entities'] = data_x[0]
                df.at[index,'types'] = data_x[1]
            else:
                df.at[index,'entities'] = 'n.a.'
                df.at[index,'types'] = 'uncategorized'

        client = RestClient()
        post_data = dict()

        post_data[len(post_data)] = dict(
            location_name="United States",
            language_name="English",
            keywords=df['queries'].tolist()
            )

        response = client.post("/keywords_data/google/search_volume/live", post_data)

        if response["status_code"] == 20000:
            sr.write(response)
        else:
            st.write("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

        response.keys()
        keyword_df = json_normalize(
          data=response['tasks'][0]['result'])

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

        df6['all'] = 'all' # in order to have a single root node
        fig = px.treemap(df6, path=['all','types','entities','queries'], color='entities')

        df6 = df6.dropna(subset=['search_volume', 'competition']) # remove rows when there are missing values

        fig = px.treemap(df6, path=['all','entities','queries'], values='search_volume',
                        color='search_volume',
                        color_continuous_scale='Blues')

        fig = px.treemap(df6, path=['all','entities','queries'], values='competition',
                        color='competition',
                        color_continuous_scale='purpor')

        fig = px.treemap(df6, path=['all','entities','queries'], values='search_volume',
                        color='competition',
                        color_continuous_scale='blues',
                        color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))

        st.balloons()
        st.text('Done! thanks for being patient.')
        st.text("Here's your treemap!")
        st.plotly_chart(fig)

        # step3
        cleanQuery = re.sub('\W+','', keyword_list[0])
        file_name = cleanQuery + ".csv"

        df.to_csv(file_name, encoding='utf-8', index=True)
        st.write("total number of queries saved on (",file_name, ")is",len(df))

        csv_download_button = download_button(df, file_name, 'Click to download your data!')
        st.markdown(csv_download_button, unsafe_allow_html=True)
