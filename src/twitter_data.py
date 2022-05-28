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
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import string
import datetime
from datetime import timezone
from twarc.client2 import Twarc2
from twarc_csv import DataFrameConverter
import pycountry
import urllib
from urllib.error import HTTPError

# clean_text and word_cloud code from:
# https://www.kaggle.com/alankritamishra/covid-19-tweet-sentiment-analysis#Sentiment-analysis
EMOJI_PATTERN = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

sia = TextClassifier.load('en-sentiment')
# nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('spacytextblob')



def spacySentiment(tweet):
    doc = nlp(tweet)
    pol = doc._.polarity
    return pol

def getTweets(topic, location, count, token, start_time, end_time):
    start_year = start_time
    end_year = end_time
    # Your bearer token here
    t = Twarc2(bearer_token=token)
    # Start and end times must be in UTC
    if start_time == 2006:
        start_time = datetime.datetime(2006, 3, 21, 0, 0, 0, 0, datetime.timezone.utc)
    else:
        start_time = datetime.datetime(start_time, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
    if end_time == datetime.datetime.today().year:
        end_time = datetime.datetime.utcnow()
    else:
        end_time = datetime.datetime(end_time, 12, 31, 0, 0, 0, 0, datetime.timezone.utc)
    query = getTags(topic) + " lang:en -is:retweet place:" + location

    st.write(f"Searching for \"{query}\" tweets from {start_year} to {end_year} in {location}...")

    # search_results is a generator, max_results is max tweets per page, not total, 100 is max when using all expansions.
    search_results = t.search_all(query=query, start_time=start_time, end_time=end_time, max_results=count)

    # Get all results page by page:
    json_file_name = f"data/new/{location}-{topic}-{start_time}-{end_time}.json"
    for page in search_results:
        # Do something with the page of results:
        with open(json_file_name, "w+") as f:
            f.write(json.dumps(page) + "\n")
    st.write(f"Tweets have been saved into {json_file_name}.")
    df = pd.read_json(json_file_name)
    return df

def getTags(topic):
    if (topic == "Malaria"):
        query = "Malaria OR #malaria"
    if(topic == "Tuberculosis"):
        query = "Tuberculosis OR tb OR TB OR #tb OR #tuberculosis"
    if (topic == "HIV/AIDS"):
        query = "HIV/AIDS OR HIV OR AIDS OR HIV-AIDS OR HIVAIDS OR #hiv OR #aids OR #hivaids"
    return query

def live_twitter(topic, location, start_time, end_time):
    tweet_df = None
    token = st.text_input("Please enter your Academic research bearer token: ", type="password")
    count = st.number_input("Please input the number of tweets to analyze here: ", min_value = 10, max_value=500)
    tags = getTags(topic)
    if token != "":
        try:
            tweet_df = getTweets(topic, location, count, token, start_time, end_time)
        except:
            st.error("The token provided was invalid. Please input a valid token with an Academic Research access to the Twitter API.")
    return tweet_df

def upload():
    df = None
    st.write("Please upload either a CSV or JSON file that contains the tweets to analyze. Please make sure that they are formatted in the same way as a Twitter API response.")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        file_name = uploaded_file.name
        if file_name.lower().endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif file_name.lower().endswith('.json'):
            df = pd.read_json(uploaded_file)
        else:
            st.write("Wrong format! Please upload either a CSV or JSON file please.")
        return df

def get_code(country, topic):
    mapping = {country.name: country.alpha_3 for country in pycountry.countries}
    ccode = mapping.get(country)
    if (topic == "Malaria"):
        tcode = 'Mal'
    if(topic == "Tuberculosis"):
        tcode = 'TB'
    if (topic == "HIV/AIDS"):
        tcode = 'HIV'
    return ccode, tcode

def downloaded_twitter(topic, country, start_year, end_year):
    df_dict = {}
    years = []
    ccode, tcode = get_code(country, topic)
    while start_year <= end_year:
        years.append(start_year)
        if ccode == "NGA":
            ccode = "Ngr"
        else:
            ccode = ccode.capitalize()
        name = 'data/Twitter/' + ccode + tcode + str(start_year) + '.csv'
        df_dict[start_year] = pd.read_csv(name)
        df_dict[start_year]['Year'] = start_year
        start_year += 1

    df_total = pd.DataFrame()
    df_total = pd.concat(df_dict.values(), keys=years)
    return df_total, df_dict

def open_twitter(topic, country, start_year, end_year, df):
    df_dict = {}
    years = []
    df2 = df[['created_at']].copy()
    df2['created_at'] = df2['created_at'].str.slice(0, 4)
    df2.sort_values(by=['created_at'])
    df3 = df2.created_at.unique()
    years_data = df3.tolist()
    for years in years_data:
        df_dict[years] = df[df['created_at'].str.startswith(str(years))]
        df_dict[years]['Year'] = years
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
    for index, row in newdf.iterrows():
        clean_text(df.loc[index, "text"])
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
        try:
            avg_sent = sum(sentiments)/len(sentiments)
        except ZeroDivisionError:
            avg_sent = 0
        sent_dict[year] = avg_sent
    return sent_dict

def graphsent(df_dict, topic, country):
    df = pd.DataFrame(df_dict.items(), columns=['Year', 'Sentiment'])
    fig, ax = plt.subplots()
    x = df['Year']
    y = df['Sentiment']
    ax.plot(x, y)
    title = "Public Sentiment over " + topic + " in " + country
    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Sentiment')
    st.pyplot(ax.figure)

def clean_text(text):
    """
    Convert to lowercase.
    Rremove URL links, special characters and punctuation.
    Tokenize and remove stop words.
    """
    text = text.lower()
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('[’“”…]', '', text)

    text = EMOJI_PATTERN.sub(r'', text)

    # removing the stop-words
    stop_words = nlp.Defaults.stop_words
    text_without_sw = [
        word for word in text.split() if not word in stop_words]
    filtered_sentence = (" ").join(text_without_sw)
    return filtered_sentence

def word_cloud(df, country, topic):
    for index, row in df.iterrows():
        clean_text(df.loc[index, "text"])

    word_cloud = WordCloud(
                        background_color='white',
                        stopwords=set(STOPWORDS),
                        max_words=50,
                        max_font_size=40,
                        scale=1,
                        random_state=1).generate(str(df['text']))
    fig2 = plt.figure()
    plt.axis('off')
    fig2.suptitle(f'Word Cloud for Top 50 Prevelant Words About {topic} in {country}', fontsize=10, va='bottom')
    # fig2.subplots_adjust(top=2.3)
    plt.imshow(word_cloud)
    st.pyplot(plt)

def remove_single_letters(text):
    res = ' '.join( [w for w in text.split() if len(w)>1] )
    return res

def check_freq(df):
    df2 = df['text'].apply(clean_text)
    df2 = df2.apply(remove_single_letters)
    word_count = Counter(" ".join(df2).split()).most_common(10)
    word_frequency = pd.DataFrame(word_count, columns = ['Word', 'Frequency'])
    st.write(word_frequency)
