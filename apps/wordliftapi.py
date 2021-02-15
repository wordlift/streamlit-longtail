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
from functions.interface import *
from functions.generate import *
from functions.restclient import RestClient
from functions.NER_wl import *

language = ''
country = ''
WL_key = ''
list_size = 0
pb_speed = 0.0

# def ui():
#
#     st.markdown('<p class="subject"> Content Idea Generator </p>', unsafe_allow_html=True)
#     st.markdown('<p class="payoff"> Get instant, untapped content ideas </p>', unsafe_allow_html=True)
#     st.markdown('<p class="question"> How does this work? </p>', unsafe_allow_html=True)
#     st.markdown("""
#     <p class="answer">
#         WordLift will “read” autocomplete data from Google, scan it using the
#         Knowledge Graph from your website (or the SpaCy API) then quickly analyze
#         every search opportunity to help you create super-useful content.”
#     </p>
#     """, unsafe_allow_html=True)
#     col1, col2, col3 = st.beta_columns(3)
#     with col1:
#         languages = ["EN", "IT", "ES", "DE"]
#         lang_option = st.selectbox("Select Language", languages)
#         first_idea = st.text_input("What is the first idea?")
#     with col2:
#         countries = ["US", "UK", "IN", "ES", "IT", "DE"]
#         country_option = st.selectbox("Select Country", countries)
#         second_idea = st.text_input("What is the second idea?")
#     with col3:
#         WL_key_ti = st.text_input("Enter your WordLift key")
#         third_idea = st.text_input("What is the third idea?")
#     size = ['Small (25 Queries)', 'Medium (50 Queries)', 'Large (100 Queries)', 'X-Large (700 Queries)']
#     size_navigation = st.radio('Please specify preferred queries list size, then press Submit', size)
#     submit_button = st.button("Submit")
#
#     if submit_button:
#         # <-- user input conditions -->
#         # 1- WordLift Key
#         if WL_key_ti:
#             WL_key = WL_key_ti
#         elif not WL_key_ti:
#             st.error("Please provide your WordLift key to proceed.")
#             st.stop()
#         # 2- query list size
#         if size_navigation == 'Small (25 Queries)':
#             list_size = 25 # when i tried the funds queries, 10 gave me error because treemap couldnnt it is small
#             pb_speed = 2.5
#         elif size_navigation == 'Medium (50 Queries)':
#             list_size = 50
#             pb_speed = 5
#         elif size_navigation == 'Large (100 Queries)':
#             list_size = 100
#             pb_speed = 10
#         elif size_navigation == 'X-Large (700 Queries)':
#             list_size = 700
#             pb_speed = 70
#         # 3- keywords list
#         if not (first_idea or second_idea or third_idea):
#             st.error("You have not typed any ideas! Please type at least two ideas, then press Submit")
#             st.stop()
#         elif first_idea:
#             if second_idea:
#                 if third_idea:
#                     st.success("SUCCESS!")
#                     keyword_list = first_idea + ', ' + second_idea + ', ' + third_idea
#                 elif not third_idea:
#                     st.success("SUCCESS!")
#                     keyword_list = first_idea + ', ' + second_idea
#             elif not (second_idea or third_idea):
#                 st.error("You have typed only one idea! Please type at least two ideas, then press Submit")
#                 st.stop()
#         keyword_list = keyword_list.strip('][').split(', ')
#
# def step1():
#     # progress bar
#     # st.markdown("Analyzing keywords...")
#     # progress_bar(list_size, pb_speed)
#     # ممكن ندخل البروقرس بار جوة الفنكشن
#
#     # keywords = [generate_keywords(q) for q in keyword_list]
#     # keywords = [query for sublist in keywords for query in sublist]
#     # keywords = list(set(keywords))
#     # df = pd.DataFrame(keywords, columns =['queries'])
#     # df = df.head(list_size)
#     # df['entities'] = ''
#     # df['types'] = ''
#
#     # progress bar
#     # st.markdown("Extracting entities...")
#     # progress_bar(list_size, pb_speed)
#
#     # for index, row in df.iterrows():
#     #     data_x = string_to_entities(df['queries'][index])
#     #     if len(data_x[0]) is not 0:
#     #         df.at[index,'entities'] = data_x[0]
#     #         df.at[index,'types'] = data_x[1]
#     #     else:
#     #         df.at[index,'entities'] = 'n.a.'
#     #         df.at[index,'types'] = 'uncategorized'
#
#     # progress bar
#     # st.markdown("Adding information on keywords...")
#     # progress_bar(list_size, pb_speed)
#
#     client = RestClient(WL_key)
#     post_data = dict()
#     post_data[len(post_data)] = dict(location_name="United States", language_name="English", keywords=df['queries'].tolist())
#     response = client.post("/keywords_data/google/search_volume/live", post_data)
#     if response["status_code"] == 20000: response.keys()
#     else: print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
#     keyword_df = json_normalize(data=response['tasks'][0]['result'])
#     keyword_df.rename(columns={'keyword': 'queries'}, inplace=True)
#     df4_merged = df.merge(keyword_df, how='right', on='queries')
#
#     # download csv file
#     # progress bar
#     # st.markdown("Preparing CSV file...")
#     # progress_bar(list_size, pb_speed)
#
#     cleanQuery = re.sub('\W+','', keyword_list[0])
#     file_name = cleanQuery + ".csv"
#     df4_merged.to_csv(file_name, encoding='utf-8', index=True)
#     csv_download_button = download_button(df4_merged, file_name, 'Download List')
#
# def step2():
#
#     # Preparing data for visualization
#     # progress bar
#     # st.markdown("Preparing data for visualization...")
#     # progress_bar(list_size, pb_speed)
#
#     s = df4_merged.apply(lambda x: pd.Series(x['types'],), axis=1).stack().reset_index(level=1, drop=True)
#     s.name = 'types'
#     df5 = df4_merged.drop('types', axis=1).join(s)
#     df5['types'] = pd.Series(df5['types'], dtype=object)
#     p = df5.apply(lambda x: pd.Series(x['entities'],), axis=1).stack().reset_index(level=1, drop=True)
#     p.name = 'entities'
#     df6 = df5.drop('entities', axis=1).join(p)
#     df6['entities'] = pd.Series(df6['entities'], dtype=object)
#
#     # figures
#     # progress bar
#     # st.markdown("Preparing treemaps...")
#     # progress_bar(list_size, pb_speed)
#
#     fig1 = px.histogram(df6, x='entities').update_xaxes(categoryorder="total descending")
#     df6['all'] = 'all'
#     fig2 = px.treemap(df6, path=['all','types','entities','queries'], color='entities')
#     fig3 = px.treemap(df4_merged, path=['entities'], values='competition', color='competition', color_continuous_scale='Blues')
#     df6 = df6.dropna(subset=['search_volume', 'competition'])
#     fig4 = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='search_volume', color_continuous_scale='Blues')
#     fig5 = px.treemap(df6, path=['all','entities','queries'], values='competition', color='competition', color_continuous_scale='purpor')
#     fig6 = px.treemap(df6, path=['all','entities','queries'], values='search_volume', color='competition', color_continuous_scale='blues', color_continuous_midpoint=np.average(df6['competition'], weights=df6['search_volume']))
#
# def switch_chart():
#
#     chart_types = ['Top Entities', 'Intent by Type and Entity', 'Intent by Entity and Search Volume', 'Intent by Search Volume and Competition', 'Intent by Entity and Competition', 'Intent by Entity, Search Volume and Competition']
#     chart_navigation = st.selectbox('Please choose preferred chart type:', chart_types, index = 2)
#
#     if chart_navigation == 'Top Entities': output = st.plotly_chart(fig1)
#     elif chart_navigation == 'Intent by Type and Entity': output = st.plotly_chart(fig2)
#     elif chart_navigation == 'Intent by Entity and Search Volume': output = st.plotly_chart(fig3)
#     elif chart_navigation == 'Intent by Search Volume and Competition': output = st.plotly_chart(fig4)
#     elif chart_navigation == 'Intent by Entity and Competition': output = st.plotly_chart(fig5)
#     elif chart_navigation == 'Intent by Entity, Search Volume and Competition': output = st.plotly_chart(fig6)
#
#     return output
import uuid
@st.cache(show_spinner=False)
def custom_button(button_text):

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f"""
        <style>
            #{button_id} {{
                width: 150px;
                height: 50px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: #ff8401;
                color: #fbfbfb;
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 6px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
                box-shadow: 0 8px 18px 0 rgba(255, 132, 1, 0.26);
                font-stretch: normal;
                font-style: normal;
                letter-spacing: normal;
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

    btn = custom_css + f'<a id="{button_id}" >{button_text}</a><br></br>'

    return btn

def app():

    # <-- UI -->
    local_css("style.css")

    set_png_as_page_bg('img/pattern.png')

    # ui()
    st.markdown('<p class="subject"> Content Idea Generator </p>', unsafe_allow_html=True)
    st.markdown('<p class="payoff"> Get instant, untapped content ideas </p>', unsafe_allow_html=True)
    st.markdown('<p class="question"> How does this work? </p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="answer">
        WordLift will “read” autocomplete data from Google, scan it using the
        Knowledge Graph from your website (or the SpaCy API) then quickly analyze
        every search opportunity to help you create super-useful content.”
    </p>
    """, unsafe_allow_html=True)

    st.write("---")

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        languages = ["EN", "IT", "ES", "DE"]
        lang_option = st.selectbox("Select Language", languages)
        first_idea = st.text_input("What is the first idea?")
    with col2:
        countries = ["US", "UK", "IN", "ES", "IT", "DE"]
        country_option = st.selectbox("Select Country", countries)
        second_idea = st.text_input("What is the second idea?")
    with col3:
        WL_key_ti = st.text_input("Enter your WordLift key")
        third_idea = st.text_input("What is the third idea?")
    size = ['Small (25 Queries)', 'Medium (50 Queries)', 'Large (100 Queries)', 'X-Large (700 Queries)']
    size_navigation = st.radio('Please specify preferred queries list size, then press Submit', size)

    # submit_button = st.button("Submit")
    submit_button = custom_button('Submit')
    st.markdown(submit_button, unsafe_allow_html=True)

    if submit_button:

        # <-- user input conditions -->
        # 1- WordLift Key
        if WL_key_ti:
            WL_key = WL_key_ti
        elif not WL_key_ti:
            st.error("Please provide your WordLift key to proceed.")
            st.stop()
        # 2- query list size
        if size_navigation == 'Small (25 Queries)':
            list_size = 25 # when i tried the funds queries, 10 gave me error because treemap couldnnt it is small

        elif size_navigation == 'Medium (50 Queries)':
            list_size = 50

        elif size_navigation == 'Large (100 Queries)':
            list_size = 100

        elif size_navigation == 'X-Large (700 Queries)':
            list_size = 700

        # 3- keywords list
        if not (first_idea or second_idea or third_idea):
            st.error("You have not typed any ideas! Please type at least two ideas, then press Submit")
            st.stop()
        elif first_idea:
            if second_idea:
                if third_idea:
                    st.success("SUCCESS!")
                    keyword_list = first_idea + ', ' + second_idea + ', ' + third_idea
                elif not third_idea:
                    st.success("SUCCESS!")
                    keyword_list = first_idea + ', ' + second_idea
            elif not (second_idea or third_idea):
                st.error("You have typed only one idea! Please type at least two ideas, then press Submit")
                st.stop()
        keyword_list = keyword_list.strip('][').split(', ')

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

        # If i used session state or url get/set query parameters, i'll maintain the “button pushed” flag
        # which will allow us to persist the button pushed state across runs.
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
            st.plotly_chart(fig3)

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

    # <-- app functionality -->
    # f1,f2 = st.beta_columns(2)

    # 1- queries list
    # with f1:
    #     show1 = st.checkbox('Show Queries List')
    #     if show1:
    #         step1()
    #         st.subheader("1- Queries List")
    #         st.markdown("Please wait while we prepare your queries list...")
    #         progress_bar(list_size, pb_speed)
    #         balloons("list of queries")
    #         st.dataframe(df4_merged)
    #         st.write("Total number of queries saved on (",file_name, ")is",len(df))
    #         st.markdown(csv_download_button, unsafe_allow_html=True)

    # 2- treemap
    # with f2:
    #     show2 = st.checkbox('Show Treemaps')
    #     if show2:
    #         step2()
    #         st.subheader("2- Treemap")
    #         st.markdown("Please wait while we prepare your treemap...")
    #         progress_bar(list_size, pb_speed)
    #         balloons("treemap")
    #         switch_chart()
