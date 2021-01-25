# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 2020

@author: AndreaVolpini
@co-author: RaffalShafiei
"""

import streamlit as st

# from streamlit_app import language, country


# language = lang_option
# country = country_option

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

def st_html(calc_html,width=700,height=500):
    '''
    Function to embed HTML, CSS, JavaScript
    '''
    calc_file = codecs.open(calc_html,'r')
    page = calc_file.read()
    components.html(page,width=width,height=height,scrolling=False)
