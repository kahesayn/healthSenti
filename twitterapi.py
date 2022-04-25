import os
import re
import tweepy
import pandas as pd
from tweepy import Stream
import json
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import streamlit as st
import torch
from flair.models import TextClassifier
from flair.data import Sentence
import re
import altair as alt
from altair.expr import datum
import matplotlib.pyplot as plt
from matplotlib import style

sia = TextClassifier.load('en-sentiment')
# nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("xx_sent_ud_sm")
nlp.add_pipe('spacytextblob')

consumer_key = '6TF530DVabB3XZPRlWVojAwKF'
consumer_secret = 'xakc3egwiugqF6C0oxdgCQHx58JGhl3k0buKA9aoBgU76QLqvZ'
access_token = '1449559138875363333-WFglKEaF7esj11gntiO3RBqewhhd9r'
access_token_secret = '3Engzoxos04T2ry94cNfkYmUyiA2ozkBwukMXDoJhJmP6'

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

def spacySentiment(tweet):
    doc = nlp(tweet)
    pol = doc._.polarity
    return pol

def getTweets(topic, count):
    # tweets = getTweets(topic, count)
    # call twitter api to fetch tweets
    fetched_tweets = api.search_tweets(q = topic, count = count, lang="en")
    # empty list to store parsed tweets
    tweets = []
    # parsing tweets one by one
    for tweet in fetched_tweets:
        # empty dictionary to store required params of a tweet
        parsed_tweet = {}
        # saving text of tweet
        parsed_tweet['text'] = tweet.text
        # saving sentiment of tweet
        parsed_tweet['spacySentiment'] = sentiAnalysis(tweet.text)
        parsed_tweet['flairSentiment'] = flair_sent(tweet.text)
        parsed_tweet['time'] = tweet.created_at
        # appending parsed tweet to tweets list
        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)
    # return parsed tweets
    return tweets

def getTags(topic):
    if (topic == "Malaria"):
        query = "Malaria OR #malaria"
    if(topic == "Tuberculosis"):
        query = "Tuberculosis OR tb OR TB OR #tb OR #tuberculosis"
    if (topic == "HIV/AIDS"):
        query = "HIV/AIDS OR HIV OR AIDS OR HIV-AIDS OR HIVAIDS OR #hiv OR #aids OR #hivaids"
    return query

def live_twitter(topic, country):
    count = st.text_input("Please input the number of tweets to analyze here: ")
    tags = getTags(topic)
    tweets = getTweets(tags, count)
    tweet_text = pd.DataFrame(tweets)
    st.write(tweet_text)

def downloaded_twitter(topic, country, start_year, end_year):
    df_dict = {}
    years = []
    if topic == "Tuberculosis" and country == "Ethiopia":
        while start_year <= end_year:
            years.append(start_year)
            name = 'data/Twitter/EthTB' + str(start_year) + '.csv'
            df_dict[start_year] = pd.read_csv(name)
            df_dict[start_year]['Year'] = start_year
            start_year += 1
    if topic == "Tuberculosis" and country == "Nigeria":
        while start_year <= end_year:
            years.append(start_year)
            name = 'data/Twitter/NgrTB' + str(start_year) + '.csv'
            df_dict[start_year] = pd.read_csv(name)
            df_dict[start_year]['Year'] = start_year
            start_year += 1
    if topic == "Tuberculosis" and country == "India":
        while start_year <= end_year:
            years.append(start_year)
            name = 'data/Twitter/IndTB' + str(start_year) + '.csv'
            df_dict[start_year] = pd.read_csv(name)
            df_dict[start_year]['Year'] = start_year
            start_year += 1
    if topic == "Malaria" and country == "Ethiopia":
        while start_year <= end_year:
            years.append(start_year)
            name = 'data/Twitter/EthMal' + str(start_year) + '.csv'
            df_dict[start_year] = pd.read_csv(name)
            df_dict[start_year]['Year'] = start_year
            start_year += 1
    if topic == "Malaria" and country == "Nigeria":
        while start_year <= end_year:
            years.append(start_year)
            name = 'data/Twitter/NgrMal' + str(start_year) + '.csv'
            df_dict[start_year] = pd.read_csv(name)
            df_dict[start_year]['Year'] = start_year
            start_year += 1
    if topic == "Malaria" and country == "India":
        while start_year <= end_year:
            years.append(start_year)
            name = 'data/Twitter/IndMal' + str(start_year) + '.csv'
            df_dict[start_year] = pd.read_csv(name)
            df_dict[start_year]['Year'] = start_year
            start_year += 1
    if topic == "HIV/AIDS" and country == "Ethiopia":
        while start_year <= end_year:
            years.append(start_year)
            name = 'data/Twitter/EthHIV' + str(start_year) + '.csv'
            df_dict[start_year] = pd.read_csv(name)
            df_dict[start_year]['Year'] = start_year
            start_year += 1
    if topic == "HIV/AIDS" and country == "Nigeria":
        while start_year <= end_year:
            years.append(start_year)
            name = 'data/Twitter/NgrHIV' + str(start_year) + '.csv'
            df_dict[start_year] = pd.read_csv(name)
            df_dict[start_year]['Year'] = start_year
            start_year += 1
    if topic == "HIV/AIDS" and country == "India":
        while start_year <= end_year:
            years.append(start_year)
            name = 'data/Twitter/IndHIV' + str(start_year) + '.csv'
            df_dict[start_year] = pd.read_csv(name)
            df_dict[start_year]['Year'] = start_year
            start_year += 1

    df_total = pd.DataFrame()
    df_total = pd.concat(df_dict.values(), keys=years)
    return df_total, df_dict

def analyzer(df, sent):
    df2 = process_tweets(df)
    result = []
    for value in df2["text"]:
        if sent == "Flair":
            result.append(flair_sent(value))
        if sent == "spaCy":
            result.append(spacySentiment(value))
    df2["Sentiment"] = result
    return df2

def process_tweets(df):
    newdf = df.filter(['id','created_at','text','Year'], axis=1)
    return newdf

def string_to_num(string):
    temp = re.findall(r'\d+', string)
    res = list(map(int, temp))
    num = res[1]/10000
    return num

def flair_sent(tweets):
    sentence = Sentence(tweets)
    sia.predict(sentence)
    score = sentence.labels[0]
    if "POSITIVE" in str(score):
        sent = string_to_num(str(score))
    elif "NEGATIVE" in str(score):
        sent = -1 * string_to_num(str(score))
    else:
        sent = 0
    return sent

def avg_sentiment(df_dict, sent):
    sent_dict={}
    for year, df in df_dict.items():
        sentiments = []
        df_new = process_tweets(df_dict[year])
        for value in df_new["text"]:
            if sent == "Flair":
                sentiments.append(flair_sent(value))
            if sent == "spaCy":
                sentiments.append(spacySentiment(value))
        avg_sent = sum(sentiments)/len(sentiments)
        sent_dict[year] = avg_sent
    return sent_dict

def graphsent(df_dict):
    df = pd.DataFrame(df_dict.items(), columns=['Year', 'Sentiment'])
    fig, ax = plt.subplots()
    x = df['Year']
    y = df['Sentiment']
    ax.plot(x, y)
    st.pyplot(ax.figure)

def graph_sentiment(df):
    style.use("ggplot")
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    xar = []
    yar = []

    x = 0
    y = 0

    for value in df["Sentiment"]:
        x += 1
        y += float(value)

        xar.append(x)
        yar.append(y)

    ax1.plot(xar,yar)
    st.pyplot(ax1.figure)
