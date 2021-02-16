import streamlit as st
import requests

language = ''
country = ''
WL_key = ''

def wl_nlp(text, language, key):

    entity_data = []
    type_data = []

    API_URL = "https://api.wordlift.io/analysis/single"

    # preparing the data for the analysis
    data_in = {
        "content": text,
        "annotations": {},
        "contentLanguage": language,
        "contentType": "text",
        "exclude": [],
        "scope": "local" # change this to "global" for all entities or to "local" to use only entities from the local KG
    }

    # adding headers and the key
    headers_in = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json;charset=UTF-8",
        "Authorization" : "Key " + key
    }

    response = requests.post(API_URL, headers = headers_in, json=data_in)

    if response.ok: # make sure connection is fine

        json_response = json.loads(response.text) # read the json response
        json_response = json_response.get('entities') # select "entities"

        for key in json_response:
           entity_data.append(json_response[key]['label']) # creating the list for labels
           type_data.append(json_response[key]['mainType']) # creating the list for types

    return entity_data, type_data

# Extracting entities and types using WordLift
def string_to_entities(text, language=language, key=WL_key):

    entities = wl_nlp(text,language, key)
    entity_data = entities[0]
    type_data = entities[1]
    return entity_data, type_data
