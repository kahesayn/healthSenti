import streamlit as st
import pandas as pd
import numpy as np
import tweepy as tw
from src.twitter_data import *
import altair as alt
import wbgapi as wb
import matplotlib.pyplot as plt
from src.official_health import *
from PIL import Image
import datetime

st.set_page_config(layout="wide")

def main():
    """main streamlit function"""
    # load and display logo in the center
    image = Image.open('data/logo.png')
    col1, col2, col3 = st.columns([3,2,2])
    with col1:
        st.write("")
    with col2:
        st.image(image, width=200)
    with col3:
        st.write("")


    st.header("Welcome to HealthSenti!")
    st.write("HealthSenti is an easy to use interactive application that is designed to visualize the public sentiment of a certain health topic and compare it to official health datasets, thus allowing for a clearer understanding of the state of health in the repective country or location. Please follow this link for more information.")

    st.write("")

    st.subheader("Application Mode:")
    st.write("There are two ways to run this application, either the open data version or the closed data version. The open data version lets the user specify all the individual parameters, thus allowing for a more controlled and precise data visualization based on the user's specificities, which at the same time can be harder to operate. But this mode also requires that the user have their own Twitter API tokens with an Academic Research access level.")
    st.write("The closed version on the other hand is the easier and more close ended version. It loads the data from already saved and processed data files. As such, there are limitations to what can be visualized, but it is much faster and simpler to run. Please choose one according to your specificities.")

    mode = st.selectbox("Please choose the application mode: ", ("Closed Version", "Open Version"))
    if mode == "Closed Version":
        closed_ver()
    if mode == "Open Version":
        open_ver()


def closed_ver():
    topic = st.selectbox("Please choose a topic to research: ", (None, "Tuberculosis", "Malaria", "HIV/AIDS"))
    country = st.selectbox("Please choose a country: ", (None, "Ethiopia", "Nigeria", "India"))

    if topic and country:
        start_time, end_time = st.select_slider("Please select a time range:",
                            options=[2010, 2011, 2012, 2013, 2014, 2015],
                            value=(2010, 2015))
        official, public = st.columns(2)
        with official:
            official_option(topic, country, start_time, end_time)
        with public:
            public_option(topic, country, start_time, end_time, "closed")


def open_ver():
    topic = st.selectbox("Please choose a topic to research: ", (None, "Tuberculosis", "Malaria", "HIV/AIDS"))
    country = st.selectbox("Please choose a country: ", (None, "Ethiopia", "Nigeria", "India", "Other"))
    if country == "Other":
        country = ("Please input the name of the country")
    if topic and country:
        current_year = datetime.datetime.today().year
        years_list = list(range(current_year, 2005, -1))
        years_list.reverse()
        start_time, end_time = st.select_slider("Please select a time range:",
                            options=years_list,
                            value=(2006, int(current_year)))
        official, public = st.columns(2)
        with official:
            official_option(topic, country, start_time, end_time)
        with public:
            df = None
            data_type = st.selectbox("Please choose Twitter data source: ", (None, "Upload file", "Access Twitter API"))
            if data_type == "Upload file":
                df = upload()
            elif data_type == "Access Twitter API":
                df = live_twitter(topic, country, start_time, end_time)
            public_option(topic, country, start_time, end_time, "open", df)


def official_option(topic, country, start_time, end_time):
    st.subheader("Official HealthData:")
    type_source = st.radio("Please choose an offcial source: ", ("World Bank", "Gapminder"))
    if type_source == "World Bank":
        type_off = st.radio("Please choose between either downloaded or live twitter data. (For faster processing time, downloaded option is recommended.)", ("Downloaded", "Live"))
        if type_off == "Downloaded":
            downloaded_offdata(topic, country, start_time, end_time)
        if type_off == "Live":
            live_offdata(topic, country, start_time, end_time)
    if type_source == "Gapminder":
        gapminder(topic, country, start_time, end_time)


def public_option(topic, country, start_time, end_time, type, df_open=None):
    df = None
    st.subheader("Public Sentiment:")
    type_sent = st.radio("Please choose a sentiment analyzer: ", ("spaCy", "Flair"))
    if type == "closed":
        df, df_dict = downloaded_twitter(topic, country, start_time, end_time)
    if type == "open" and df_open is not None:
        df, df_dict = open_twitter(topic, country, start_time, end_time, df_open)
    if df is not None:
        df2 = analyzer(df, type_sent)
        sent_dict = avg_sentiment(df_dict, type_sent)
        graphsent(sent_dict, topic, country)

        st.write("If you would like to view any other analysis, please select the one you wish to view from the below:")
        check1 = st.checkbox("Wordcloud of top 50 prevelant words")
        if check1:
            word_cloud(df, country, topic)
        check2 = st.checkbox("Top 10 words by frequency")
        if check2:
            check_freq(df)


if __name__ == "__main__":
    main()
