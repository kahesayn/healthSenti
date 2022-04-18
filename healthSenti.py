import streamlit as st
import pandas as pd
import numpy as np
import tweepy as tw
from twitterapi import *
import altair as alt
import wbgapi as wb
import matplotlib.pyplot as plt
from official_health import *

st.set_page_config(layout="wide")
st.title("HealthSenti")
st.header("Welcome to HealthSenti!")

#get input and call twitter api
topic = st.selectbox("Please choose a topic to research: ", ("Tuberculosis", "Malaria", "HIV/AIDS"))

country = st.selectbox("Please choose a country: ", ("Ethiopia", "Nigeria", "India"))

#choose between live or downloaded data

start_time, end_time = st.select_slider("Please select a time range:",
                    options=[2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
                    value=(2006, 2022))


official, public = st.columns(2)

with official:
    st.subheader("Official HealthData:")
    type_off = st.radio("Please choose between either downloaded or live twitter data. (For faster processing time, downloaded option is recommended.)", ("Downloaded", "Live"))
    if type_off == "Downloaded":
        downloaded_offdata(topic, country)
    if type_off == "Live":
        live_offdata(topic, country, start_time, end_time)
with public:
    st.subheader("Public Sentiment:")
    type_sent = st.radio("Please choose a sentiment analyzer: ", ("Flair", "spaCy"))
    type_pub = st.radio("Please choose between either downloaded or live official data. (For faster processing time, downloaded option is recommended.)", ("Downloaded", "Live"))
    if type_pub == "Downloaded":
        df = downloaded_twitter(topic, country)
        df2 = analyzer(df, type_sent)
        st.write(df2)
        graph_sentiment(df2)
    if type_pub == "Live":
        live_twitter(topic, country)


#store and show aggregated tweets



# simple polarity chart for tweets
# c = alt.Chart(tweet_text).mark_circle().encode(x='time', y='sentiment')

# call the world bank api


# col1, col2 = st.beta_columns(2)
# with col1:
#     st.header("Twitter Sentiment Analysis")
#     st.altair_chart(c, use_container_width=True)
# with col2:
#     st.header("World Bank Data Analysis")
