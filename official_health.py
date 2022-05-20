import wbgapi as wb
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import pycountry
from twitter_data import get_code

def downloaded_offdata(topic, country, start_time, end_time):
    df = None
    if country == "Ethiopia":
        df = pd.read_csv (r'data/Official/EthiopiaData.csv')
    if country == "Nigeria":
        df = pd.read_csv (r'data/Official/NigeriaData.csv')
    if country == "India":
        df = pd.read_csv (r'data/Official/IndiaData.csv')

    if not df.empty:
        start_time -= 2001
        end_time -= 2000
        df = df.iloc[start_time:end_time]
        ccode, tcode = get_code(country, topic)
        title = topic + " Incidence in " + country
        col = "" + tcode + "-Incidence"

        fig, ax = plt.subplots()
        x = df['Year']
        y = df[col]
        ax.plot(x, y)
        ax.set_title(title)
        ax.set_xlabel('Time')
        ax.set_ylabel(topic + ' Incidence')
        st.pyplot(ax.figure)

def gapminder(topic, country, start_time, end_time):
    df = pd.read_csv (r'data/Official/GapminderData.csv')
    df2 = df[df.Country == country]
    df2 = df2.set_index('Year')
    df2 = df2.loc[str(start_time):str(end_time)]
    ccode, tcode = get_code(country, topic)
    title = topic + " Incidence in " + country
    col = "" + tcode + "-Incidence"

    fig1, ax1 = plt.subplots()
    x = df2.index
    y = df2[col]
    ax1.plot(x, y)
    ax1.set_title(title)
    ax1.set_xlabel('Time')
    ax1.set_ylabel(topic + ' Incidence')
    st.pyplot(ax1.figure)

def live_offdata(topic, country, start_time, end_time):
    getWBdata(topic, country, start_time, end_time)

def getWBdata(topic, country, start_time, end_time):
    end_time +=1
    mapping = {country.name: country.alpha_3 for country in pycountry.countries}
    ccode = mapping.get(country)
    if (topic == "Malaria"):
        res = malaria(ccode, start_time, end_time, country, topic)
    if(topic == "Tuberculosis"):
        res = tb(ccode, start_time, end_time, country, topic)
    if (topic == "HIV/AIDS"):
        res = hiv(ccode, start_time, end_time, country, topic)


def tb(ccode, start_time, end_time, country, topic):
    df = wb.data.DataFrame(['SH.TBS.INCD'], ccode, range(start_time, end_time))
    df1 = df.transpose()
    df1 = df1.apply(pd.to_numeric)
    graph_official(topic, country, df1, ccode)

def malaria(ccode, start_time, end_time, country, topic):
    df = wb.data.DataFrame(['SH.MLR.INCD.P3'], ccode, range(start_time, end_time))
    df1 = df.transpose()
    df1 = df1.apply(pd.to_numeric)
    graph_official(topic, country, df1, ccode)

def hiv(ccode, start_time, end_time, country, topic):
    df = wb.data.DataFrame(['SH.HIV.INCD.TL.P3'], ccode, range(start_time, end_time))
    df1 = df.transpose()
    df1 = df1.apply(pd.to_numeric)
    graph_official(topic, country, df1, ccode)

def graph_official(topic, country, df1, ccode):
    df1.reset_index(inplace=True)
    fig, ax = plt.subplots()
    title = topic + " Incidence in " + country
    x = df1['index']
    y = df1[ccode]
    ax.plot(x,y)
    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel(topic + ' Incidence')
    st.pyplot(ax.figure)
