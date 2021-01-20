# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 2020

@author: AndreaVolpini
@co-author: RaffalShafiei
"""

# we might not need all of these here
# <--- Installing Libraries --->
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit.components.v1 as components

import spacy
import en_core_web_sm
import requests, json
import pprint
import time
import re
import trafilatura
import base64
import os
import pickle
import uuid
import codecs

from fake_useragent import UserAgent
from random import randint
from http.client import HTTPSConnection
from json import loads
from json import dumps
from pandas import json_normalize
from collections import Counter

# <--- Page Configurations --->
PAGE_CONFIG = {
    "page_title":"Free SEO Tools by WordLift",
    "page_icon":"images/fav-ico.png",
    "layout":"centered"
    }
st.set_page_config(**PAGE_CONFIG)

# <--- Sidebar --->
languages = ["en", "it", "es", "de"]
countries = ["us", "uk", "in", "es", "it", "de"]
api_options = ["Run NER with WordLift", "Run NER with SpaCy"]

st.sidebar.image("images/logo-wordlift.png", width=200)

lang_option = st.sidebar.selectbox("Select Language", languages)
country_option = st.sidebar.selectbox("Select Country", countries)

language = lang_option
country = country_option

api_option = st.sidebar.selectbox("Select Your Preferred API", api_options)
if api_option == 'Run NER with WordLift':
    WL_key_ti = st.sidebar.text_input("Please enter your WordLift key")
    # if st.sidebar.button("Enter"):
    WL_key = WL_key_ti

# <--- Page Components--->
st.title("Ready to stand out on Google?")
st.subheader("We will help you target thousands of high-intent long-tail queries.")
st.subheader("Let us find opportunities for you.")

# text inputs
col1, col2, col3 = st.beta_columns(3)
with col1:
    st.markdown("""What is the **first idea**?""")
    first_idea = st.text_area("Type your 1st intent here...")
with col2:
    st.markdown("""What is the **second idea**?""")
    second_idea = st.text_area("Type your 2nd intent here...")
with col3:
    st.markdown("""What is the **third idea**?""")
    third_idea = st.text_area("Type your 3rd intent here...")
x = st.slider("How many long-tail queries do you prefer? Please specify below, then press Go!",0,100,50)

# <--- CSS --->
# st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# <--- HTML --->
# st_html('index.html')

# <--- Main Function --->
def main():
    if api_option == 'Run NER with WordLift':
        if st.button("Go!"):
            # step1
            st.markdown("Thanks! We'll unleash our **superpowers** and find the best long tail queries for these intents.")
            st.markdown("Please wait while we prepare the queries list of your intents")

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                # Update progress bar.
                progress_bar.progress(i + 1)

                # Pretend we're doing some computation that takes time.
                time.sleep(0.1)

                @st.cache(show_spinner=False)
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

                @st.cache(show_spinner=False)
                def generate_keywords(query):
                    '''
                    Function to generate a large number of keyword suggestions
                    '''
                    seed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                    print('Grabbing suggestions... ' + str(query))
                    first_pass = autocomplete(query)
                    second_pass = [autocomplete(x) for x in first_pass]
                    flat_second_pass = []
                    flat_second_pass = [query for sublist in second_pass for query in sublist]
                    third_pass = [autocomplete(query + ' ' + x) for x in seed]
                    flat_third_pass = []
                    flat_third_pass = [query for sublist in third_pass for query in sublist]

                    keyword_suggestions = list(set(first_pass + flat_second_pass + flat_third_pass))
                    keyword_suggestions.sort()
                    print('SUCCESS!')
                    return keyword_suggestions

                keyword_list = first_idea + ', ' + second_idea + ', ' + third_idea
                keyword_list = keyword_list.strip('][').split(', ')

                keywords = [generate_keywords(q) for q in keyword_list]
                keywords = [query for sublist in keywords for query in sublist] # to flatten
                keywords = list(set(keywords)) # to de-duplicate

                df = pd.DataFrame(keywords, columns =['queries'])
                df = df.head(x)
                df['entities'] = ''
                df['types'] = ''

            st.balloons()
            status_text.text('Done! thanks for being patient.')
            st.text("Here's the queries list of your intents!")
            st.dataframe(df)

            # step2
            st.markdown("Please wait while we prepare your treemap")

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                # Update progress bar.
                progress_bar.progress(i + 1)

                # Pretend we're doing some computation that takes time.
                time.sleep(0.1)

                @st.cache(show_spinner=False)
                def wl_nlp(text, language, key):
                    #API_URL = "https://api.wordlift.io/analysis/single"
                    API_URL = "https://api-dev.wordlift.io/analysis/single"
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

                @st.cache(allow_output_mutation=True, show_spinner=False)
                def string_to_entities(text, language=language, key=WL_key):
                    entities = wl_nlp(text,language, key)
                    entity_data = entities[0]
                    type_data = entities[1]
                    return entity_data, type_data

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
                    response.keys()
                else:
                    st.error("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

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

                # visualizing
                fig = px.histogram(df6, x='entities').update_xaxes(categoryorder="total descending")

                df6['all'] = 'all' # in order to have a single root node
                fig = px.treemap(df6, path=['all','types','entities','queries'], color='entities')

                fig = px.treemap(df6, path=['all','entities','queries'], values='search_volume',
                              color='search_volume',
                              color_continuous_scale='purp',
                              color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))

                fig = px.treemap(df6, path=['types','entities','queries'], color='entities', values='competition')
                fig = px.treemap(df6, path=['all','entities','queries'], values='competition',
                              color='competition',
                              color_continuous_scale='purpor',
                              color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))

            st.balloons()
            status_text.text('Done! thanks for being patient.')
            st.text("Here's your treemap!")
            st.plotly_chart(fig)

            # step3
            cleanQuery = re.sub('\W+','', keyword_list[0])
            file_name = cleanQuery + ".csv"
            csv_df = df.to_csv(file_name, encoding='utf-8', index=True)
            st.write("total number of queries saved on (",file_name, ")is",len(df))
            csv_download_button = download_button(csv_df, file_name, 'Click to download your data!')
            st.markdown(csv_download_button, unsafe_allow_html=True)

    elif api_option == 'Run NER with SpaCy':
        if st.button("Go!"):
            # step1
            st.markdown("Thanks! We'll unleash our **superpowers** and find the best long tail queries for these intents.")
            st.markdown("Please wait while we prepare the queries list of your intents")

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                # Update progress bar.
                progress_bar.progress(i + 1)

                # Pretend we're doing some computation that takes time.
                time.sleep(0.1)

                @st.cache(show_spinner=False)
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

                @st.cache(show_spinner=False)
                def generate_keywords(query):
                    '''
                    Function to generate a large number of keyword suggestions
                    '''
                    seed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                    print('Grabbing suggestions... ' + str(query))
                    first_pass = autocomplete(query)
                    second_pass = [autocomplete(x) for x in first_pass]
                    flat_second_pass = []
                    flat_second_pass = [query for sublist in second_pass for query in sublist]
                    third_pass = [autocomplete(query + ' ' + x) for x in seed]
                    flat_third_pass = []
                    flat_third_pass = [query for sublist in third_pass for query in sublist]

                    keyword_suggestions = list(set(first_pass + flat_second_pass + flat_third_pass))
                    keyword_suggestions.sort()
                    print('SUCCESS!')
                    return keyword_suggestions

                keyword_list = first_idea + ', ' + second_idea + ', ' + third_idea
                keyword_list = keyword_list.strip('][').split(', ')

                keywords = [generate_keywords(q) for q in keyword_list]
                keywords = [query for sublist in keywords for query in sublist] # to flatten
                keywords = list(set(keywords)) # to de-duplicate

                df = pd.DataFrame(keywords, columns =['queries'])
                df = df.head(x)
                df['entities'] = ''
                df['types'] = ''

            st.balloons()
            status_text.text('Done! thanks for being patient.')
            st.text("Here's the queries list of your intents!")
            st.dataframe(df)

            # step2
            st.markdown("Please wait while we prepare your treemap")

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                # Update progress bar.
                progress_bar.progress(i + 1)

                # Pretend we're doing some computation that takes time.
                time.sleep(0.1)

                nlp = en_core_web_sm.load()

                @st.cache(allow_output_mutation=True, show_spinner=False)
                def string_to_entities(text):
                    entities = nlp(text)
                    entity_data = [x.text for x in entities.ents]
                    type_data = [x.label_ for x in entities.ents]
                    return entity_data, type_data

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
                    response.keys()
                else:
                    st.error("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

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

                # visualizing
                fig = px.histogram(df6, x='entities').update_xaxes(categoryorder="total descending")

                df6['all'] = 'all' # in order to have a single root node
                fig = px.treemap(df6, path=['all','types','entities','queries'], color='entities')

                fig = px.treemap(df6, path=['all','entities','queries'], values='search_volume',
                              color='search_volume',
                              color_continuous_scale='purp',
                              color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))

                fig = px.treemap(df6, path=['types','entities','queries'], color='entities', values='competition')
                fig = px.treemap(df6, path=['all','entities','queries'], values='competition',
                              color='competition',
                              color_continuous_scale='purpor',
                              color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))

            st.balloons()
            status_text.text('Done! thanks for being patient.')
            st.text("Here's your treemap!")
            st.plotly_chart(fig)

            # step3
            cleanQuery = re.sub('\W+','', keyword_list[0])
            file_name = cleanQuery + ".csv"
            csv_df = df.to_csv(file_name, encoding='utf-8', index=True)
            st.write("total number of queries saved on (",file_name, ")is",len(df))
            csv_download_button = download_button(csv_df, file_name, 'Click to download your data!')
            st.markdown(csv_download_button, unsafe_allow_html=True)

# <---- Classes ---->
@st.cache(show_spinner=False)
class RestClient:
    domain = "api.wordlift.io"

    @st.cache(show_spinner=False)
    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            headers = {'Authorization' : 'Key ' +  WL_key}
            connection.request(method, path, headers=headers, body=data)
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

# <--- Functions --->
@st.cache(show_spinner=False)
def download_button(object_to_download, download_filename, button_text, pickle_it=False):
    """
    Generates a link to download the given object_to_download.

    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.

    Returns:
    -------
    (str): the anchor tag to download object_to_download

    Examples:
    --------
    download_button(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_button(your_str, 'YOUR_STRING.txt', 'Click to download text!')

    """
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

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f"""
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;

            }}
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link

# Custom Components Fxn
def st_html(calc_html,width=700,height=500):
	calc_file = codecs.open(calc_html,'r')
	page = calc_file.read()
	components.html(page,width=width,height=height,scrolling=False)

if __name__ == "__main__":
    main()
