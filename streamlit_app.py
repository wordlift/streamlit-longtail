# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 2020

@author: AndreaVolpini
@co-author: RaffalShafiei
"""

# <--- Installing Libraries --->
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests, json
import pprint
import time
import re
import trafilatura
import base64 # File Download
from fake_useragent import UserAgent
from random import randint
from http.client import HTTPSConnection
from json import loads
from json import dumps
from pandas import json_normalize
from transformers import AutoTokenizer, AutoModelWithLMHead
from google.colab import files

# <--- Page Configurations --->
PAGE_CONFIG = {
    "page_title":"Free SEO Tools by WordLift",
    "page_icon":"images/fav-ico.png",
    "layout":"centered"
    }
st.set_page_config(**PAGE_CONFIG)

# these has to change, they have to be according to user choice in the sidebar, but for now im using these because they are easier
language = 'en'
country = 'us'
WL_key = 'F2Td1mgTjbwuGlxq4pSQa0poicP4irsQAroaZYfVkbgBCBWbheLukNAgYbX22CZa'

#     if st.sidebar.button("Enter"):
#         if WL_key.strip():  # the way we test here has to change, to make sure the key exists or not, also green and red
#             st.sidebar.write("WordLift Key (", WL_key, ") is valid")
#             lang_option = st.sidebar.selectbox("Select Language", language)
#             country_option = st.sidebar.selectbox("Select Country", country)
#             if st.sidebar.button("Submit"): # i thinnk there should be a check here too
#                 st.sidebar.Write("something")
#         else:
#             st.sidebar.write("* WordLift Key (", WL_key, ") is invalid")
#
#     if st.sidebar.button("Enter"):
#         if WL_key.strip():  # the way we test here has to change, to make sure the email exists or not, also green and red
#             st.sidebar.write("WordLift Key (", WL_key, ") is valid")
#             lang_option = st.sidebar.selectbox("Select Language", language)
#             country_option = st.sidebar.selectbox("Select Country", country)
#             if st.sidebar.button("Submit"): # i thinnk there should be a check here too
#                 st.sidebar.Write("something")
#         else:
#             st.sidebar.write("* WordLift Key (", WL_key, ") is invalid")

# <--- Main Function --->
def main():
    """Streamlit encourages execution in a main() function. Run this to run the app"""
    st.sidebar.image("images/logo-wordlift.png", width=200)

    language = ["en", "it", "es", "de"]
    country = ["us", "uk", "in", "es", "it", "de"]
    selection = ["WordLift Key", "Email"]
    navigation = st.sidebar.radio("Enter your WordLift Key, or Email:", selection)
    if navigation == 'WordLift Key':
        WL_key = st.sidebar.text_input("WordLift Key")
    elif navigation == 'Email':
        email = st.sidebar.text_input("Email")

    lang_option = st.sidebar.selectbox("Select Language", language)
    country_option = st.sidebar.selectbox("Select Country", country)

    st.title("Ready to stand out on Google?")
    st.subheader("We will help you target thousands of high-intent long-tail queries.")

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        first_idea = st.text_area(
            "Type your first idea here:", "e.g., SEO"
        )
    with col2:
        second_idea = st.text_area(
            "Type your second idea here:", "e.g., Structured Data"
        )
    with col3:
        third_idea = st.text_area(
            "Type your third idea here:", "e.g., Artificial Intelligence"
        )

    # these also has to change, they have to be according to user input, but for now im using these because they are easier and faster
    keyword_list = 'seo, structured data'
    keyword_list = keyword_list.strip('][').split(', ')

    keywords = [generate_keywords(q) for q in keyword_list]
    keywords = [query for sublist in keywords for query in sublist] # to flatten
    keywords = list(set(keywords)) # to de-duplicate

    # a) The Queries List
    df = pd.DataFrame(keywords, columns =['queries'])
    df['entities'] = ''
    df['types'] = ''

    # b) Entities and Types
    for index, row in df.iterrows():
        data_x = string_to_entities(df['queries'][index]) # extracting entities
        if len(data_x[0]) is not 0: # make sure there are entities
            df.at[index,'entities'] = data_x[0]
            df.at[index,'types'] = data_x[1]
        else:
            df.at[index,'entities'] = 'n.a.'
            df.at[index,'types'] = 'uncategorized'

    # c) Keyword Data
    df = df.head(700) # adding here a limit to max 700 queries
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

    # d) cpc, search volume and competition
    keyword_df = json_normalize(
        data=response['tasks'][0]['result'])
    keyword_df.rename(columns={'keyword': 'queries'}, inplace=True)

    # e) merged queries with keyword data
    df4_merged = df.merge(keyword_df, how='right', on='queries')
    s = df4_merged.apply(lambda x: pd.Series(x['types'],), axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'types'
    df5 = df4_merged.drop('types', axis=1).join(s)
    df5['types'] = pd.Series(df5['types'], dtype=object)
    p = df5.apply(lambda x: pd.Series(x['entities'],), axis=1).stack().reset_index(level=1, drop=True)
    p.name = 'entities'
    df6 = df5.drop('entities', axis=1).join(p)
    df6['entities'] = pd.Series(df6['entities'], dtype=object)

    # Let's start visualizing
    # a) Visualize top entities
    fig = px.histogram(df6, x='entities').update_xaxes(categoryorder="total descending")
    # st.plotly_chart(fig)

    # b) Intent by Type and Entity
    df6['all'] = 'all' # in order to have a single root node
    fig = px.treemap(df6, path=['all','types','entities','queries'], color='entities')
    # st.plotly_chart(fig)

    # c) Intent by Entity and Search Volume
    fig = px.treemap(df6, path=['all','entities','queries'], values='search_volume',
                  color='search_volume',
                  color_continuous_scale='purp',
                  color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))
    # st.plotly_chart(fig)

    # d) Intent by Entity and Competition
    fig = px.treemap(df6, path=['types','entities','queries'], color='entities', values='competition')
    fig = px.treemap(df6, path=['all','entities','queries'], values='competition',
                  color='competition',
                  color_continuous_scale='purpor',
                  color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))
    st.plotly_chart(fig)

    # File (CSV) Download - A Workaround for small data
    """
    There is currently, no official way of downloading data from Streamlit.
    This is a workaround.
    """
    cleanQuery = re.sub('\W+','', keyword_list[0])
    file_name = cleanQuery + ".csv"
    csv = df.to_csv(file_name, encoding='utf-8', index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File Here</a>'
    st.write("total number of queries saved on (",file_name, ")is",len(df))
    st.markdown(href, unsafe_allow_html=True)

# <---- Classes ---->
class RestClient:
    domain = "api.wordlift.io"

    @st.cache
    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            headers = {'Authorization' : 'Key ' +  WL_key}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    @st.cache
    def get(self, path):
        return self.request(path, 'GET')

    @st.cache
    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)

# <--- Functions --->
@st.cache
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

@st.cache
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

@st.cache
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

if __name__ == "__main__":
    main()
