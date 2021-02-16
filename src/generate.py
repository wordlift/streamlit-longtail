import streamlit as st
from fake_useragent import UserAgent
from random import randint
import requests
import json
import time

language = ''
country = ''

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
