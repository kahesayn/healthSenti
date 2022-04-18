import wbgapi as wb
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

def downloaded_offdata(topic, country):
    if country == "Ethiopia":
        df = pd.read_csv (r'data/Official/EthiopiaData.csv')
    if country == "Nigeria":
        df = pd.read_csv (r'data/Official/NigeriaData.csv')
    if country == "India":
        df = pd.read_csv (r'data/Official/IndiaData.csv')

    if (topic == "Malaria"):
        c = alt.Chart(df, title="Malaria Incidence").mark_line().encode(x='Year', y='Malaria-Incidence')
        st.altair_chart(c, use_container_width=True)
    if(topic == "Tuberculosis"):
        c = alt.Chart(df, title="Malaria Incidence").mark_line().encode(x='Year', y='TB-Incidence')
        st.altair_chart(c, use_container_width=True)
    if (topic == "HIV/AIDS"):
        c = alt.Chart(df, title="Malaria Incidence").mark_line().encode(x='Year', y='HIV-Incidence')
        st.altair_chart(c, use_container_width=True)

def live_offdata(topic, country, start_time, end_time):
    getWBdata(topic, country, start_time, end_time)

def getWBdata(topic, country, start_time, end_time):
    if (country == "Ethiopia"):
        ccode = 'ETH'
    if (country == "India"):
        ccode = 'IND'
    if (country == "Nigeria"):
        ccode = 'NGA'

    if (topic == "Malaria"):
        res = malaria(ccode, start_time, end_time)
    if(topic == "Tuberculosis"):
        res = tb(ccode, start_time, end_time)
    if (topic == "HIV/AIDS"):
        res = hiv(ccode, start_time, end_time)


def tb(ccode, start_time, end_time):
    n = wb.data.DataFrame(['SH.TBS.INCD'], ccode, range(start_time, end_time))
    n1 = n.transpose()
    n1 = n1.apply(pd.to_numeric)
    st.line_chart(n1[ccode])

def malaria(ccode, start_time, end_time):
    n = wb.data.DataFrame(['SH.MLR.INCD.P3'], ccode, range(start_time, end_time))
    n1 = n.transpose()
    n1 = n1.apply(pd.to_numeric)
    st.line_chart(n1[ccode])

def hiv(ccode, start_time, end_time):
    n = wb.data.DataFrame(['SH.HIV.INCD.TL.P3'], ccode, range(start_time, end_time))
    n1 = n.transpose()
    n1 = n1.apply(pd.to_numeric)
    st.line_chart(n1[ccode])
