# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 2020

@author: AndreaVolpini
@co-author: RaffalShafiei
"""

import streamlit as st

@st.cache(allow_output_mutation=True, show_spinner=False)
def string_to_entities(text):
    entities = nlp(text)
    entity_data = [x.text for x in entities.ents]
    type_data = [x.label_ for x in entities.ents]
    return entity_data, type_data
