# <-- Libraries -->
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import re
from pandas import json_normalize
from pandas import Series

from functions.download import download_button
from functions.generate import *
from functions.restclient import RestClient
from functions.NER_wl import *

# import uuid
# @st.cache(show_spinner=False)
# def custom_button(button_text):
#
#     button_uuid = str(uuid.uuid4()).replace('-', '')
#     button_id = re.sub('\d+', '', button_uuid)
#     custom_css = f"""
#         <style>
#             #{button_id} {{
#                 width: 150px;
#                 height: 50px;
#                 display: inline-flex;
#                 align-items: center;
#                 justify-content: center;
#                 background-color: #ff8401;
#                 color: #fbfbfb;
#                 padding: .25rem .75rem;
#                 position: relative;
#                 text-decoration: none;
#                 border-radius: 6px;
#                 border-width: 1px;
#                 border-style: solid;
#                 border-color: rgb(230, 234, 241);
#                 border-image: initial;
#                 box-shadow: 0 8px 18px 0 rgba(255, 132, 1, 0.26);
#                 font-stretch: normal;
#                 font-style: normal;
#                 letter-spacing: normal;
#             }}
#             #{button_id}:hover {{
#                 border-color: rgb(246, 51, 102);
#                 color: rgb(246, 51, 102);
#             }}
#             #{button_id}:active {{
#                 box-shadow: none;
#                 background-color: rgb(246, 51, 102);
#                 color: white;
#                 }}
#         </style> """
#
#     btn = custom_css + f'<a id="{button_id}" >{button_text}</a><br></br>'
#     return btn

def app():

    # submit_button = custom_button('Submit')
    # st.markdown(submit_button, unsafe_allow_html=True)

        keywords = [generate_keywords(q) for q in keyword_list]
        keywords = [query for sublist in keywords for query in sublist]
        keywords = list(set(keywords))
        df = pd.DataFrame(keywords, columns =['queries'])
        df = df.head(list_size)
        df['entities'] = ''
        df['types'] = ''

        for index, row in df.iterrows():
            data_x = string_to_entities(df['queries'][index])
            if len(data_x[0]) is not 0:
                df.at[index,'entities'] = data_x[0]
                df.at[index,'types'] = data_x[1]
            else:
                df.at[index,'entities'] = 'n.a.'
                df.at[index,'types'] = 'uncategorized'

        client = RestClient(WL_key)
        post_data = dict()
        post_data[len(post_data)] = dict(location_name="United States", language_name="English", keywords=df['queries'].tolist())
        response = client.post("/keywords_data/google/search_volume/live", post_data)
        if response["status_code"] == 20000: response.keys()
        else: print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
        keyword_df = json_normalize(data=response['tasks'][0]['result'])
        keyword_df.rename(columns={'keyword': 'queries'}, inplace=True)
        df4_merged = df.merge(keyword_df, how='right', on='queries')

        cleanQuery = re.sub('\W+','', keyword_list[0])
        file_name = cleanQuery + ".csv"
        df4_merged.to_csv(file_name, encoding='utf-8', index=True)
        csv_download_button = download_button(df4_merged, file_name, 'Download List')

        st.subheader("1- Queries List")
        st.markdown("Please wait while we prepare your queries list...")
        progress_bar(list_size)
        balloons("list of queries")
        st.dataframe(df4_merged)
        st.write("Total number of queries saved on (",file_name, ")is",len(df))
        st.markdown(csv_download_button, unsafe_allow_html=True)

        st.subheader("2- Treemap")
        st.markdown("Please wait while we prepare your treemap...")
        progress_bar(list_size)
        balloons("treemap")

        s = df4_merged.apply(lambda x: pd.Series(x['types'],), axis=1).stack().reset_index(level=1, drop=True)
        s.name = 'types'
        df5 = df4_merged.drop('types', axis=1).join(s)
        df5['types'] = pd.Series(df5['types'], dtype=object)
        p = df5.apply(lambda x: pd.Series(x['entities'],), axis=1).stack().reset_index(level=1, drop=True)
        p.name = 'entities'
        df6 = df5.drop('entities', axis=1).join(p)
        df6['entities'] = pd.Series(df6['entities'], dtype=object)

        chart_types = ['Top Entities', 'Intent by Type and Entity', 'Intent by Entity and Search Volume', 'Intent by Search Volume and Competition', 'Intent by Entity and Competition', 'Intent by Entity, Search Volume and Competition']
        chart_navigation = st.selectbox('Please choose preferred chart type:', chart_types, index = 2)

        if chart_navigation == 'Top Entities':
            fig1 = px.histogram(df6, x='entities').update_xaxes(categoryorder="total descending")
            st.plotly_chart(fig1)

        elif chart_navigation == 'Intent by Type and Entity':
            df6['all'] = 'all'
            fig2 = px.treemap(df6, path=['all','types','entities','queries'], color='entities')
            st.plotly_chart(fig2)

        elif chart_navigation == 'Intent by Entity and Search Volume':
            df6['all'] = 'all'
            fig3 = px.treemap(df4_merged, path=['entities'], values='competition', color='competition', color_continuous_scale='Blues')
            st.plotly_chart(fig3, use_container_width=True)

        elif chart_navigation == 'Intent by Search Volume and Competition':
            df6['all'] = 'all'
            df6 = df6.dropna(subset=['search_volume', 'competition'])
            fig4 = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='search_volume', color_continuous_scale='Blues')
            st.plotly_chart(fig4)

        elif chart_navigation == 'Intent by Entity and Competition':
            df6['all'] = 'all'
            fig5 = px.treemap(df6, path=['all','entities','queries'], values='competition', color='competition', color_continuous_scale='purpor')
            st.plotly_chart(fig5)

        elif chart_navigation == 'Intent by Entity, Search Volume and Competition':
            df6['all'] = 'all'
            fig6 = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='competition', color_continuous_scale='blues', color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))
            st.plotly_chart(fig6)

# <--- my comments to ennhance ui and performance: --->
# i think that maybe it is better to display both outputs as beta columnns vertically side by side
# If i used session state or url get/set query parameters, i'll maintain the “button pushed” flag, which will allow us to persist the button pushed state across runs.
# maybe it is better to place the progress bars inside each function
# def ui, step1, step2, etc...
# st.markdown("Extracting entities...")
# st.markdown("Analyzing keywords...")
# st.markdown("Preparing treemaps...")
# st.markdown("Preparing data for visualization...")
# st.markdown("Preparing CSV file...")
# st.markdown("Adding information on keywords...")
#
# you can make use of the elemennts used in Colab
