###Important : Streamlit is required to run the code. After that, run the code using streamlit run dash.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# Read Data
df = pd.read_csv("cowin_vaccine_data_statewise.csv")
df = df.fillna(0)

# Configuring layout
st.set_page_config(layout="wide")

# Getting states
states = df.State.unique()
states = np.array(states)

# Presets
w = 450
h = 350
########################################################################################################
# Configuring Sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 180px;
        margin-right: 0px;
        padding: 10px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 500px;
        margin-left: -500px;
        margin-right: 0px;
        padding-right: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.info("Select a date between 25 Jun and 30 August")
date = st.sidebar.text_input("Select Date", value="25/06/2021")
reg = st.sidebar.selectbox('Select Region', options=states)
#########################################################################################################
# Data Extraction

data_india = df[df.State == reg]
data_rest = df.iloc[290:]

current = data_rest[data_rest['Updated On'] == date]
currentIn = data_india[data_india['Updated On'] == date]

st.title("Covid-19 Vaccinations in India")
st.subheader('By Aganya Bajaj')

##########################################################################################################
# Choroplet Map
fig = px.choropleth(
    current,
    geojson=
    "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Total',
    color_continuous_scale=['#29292E', 'cyan'])

fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(title="Statewise Map of Vaccinations",
                  title_x=0.5,
                  paper_bgcolor='#19191E',
                  geo=dict(bgcolor='rgba(0,0,0,0)'),
                  width=925,
                  height=500)

fig.update_geos(landcolor='#19191E')

st.plotly_chart(fig)

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric(label='Total', value=int(currentIn['Total']))
col2.metric(label='First Dose', value=int(currentIn['First Dose']))
col3.metric(label='Second Dose', value=int(currentIn['Second Dose']))

########################################################################################################
col1, col2 = st.columns(2)

# Vaccination trend over time
fig = px.area(
    data_india,
    x='Updated On',
    y=['Total', 'First Dose', 'Second Dose'],
    labels={
        'Updated On': 'Date',
        'value': 'Number of doses',
        'variable': ''
    },
)

fig.update_layout(title="Vacination trend over time*",
                  title_x=0.5,
                  paper_bgcolor='#19191E',
                  plot_bgcolor="#19191E",
                  width=w,
                  height=h,
                  margin={
                      'l': 50,
                      'r': 50,
                      't': 50,
                      'b': 50,
                      'pad': 00
                  },
                  xaxis=(dict(showgrid=False)),
                  yaxis=(dict(showgrid=False)))

col1.plotly_chart(fig)

########################################################################################################
# Distribution by brand

x = int(currentIn.loc[:, 'CoviShield'])
y = int(currentIn.loc[:, 'Covaxin'])
z = int(currentIn.loc[:, 'Sputnik V'])

doss = pd.DataFrame({
    'Name': ['CoviShield', 'Covaxin', 'Sputnik V'],
    'amt': [x, y, z]
})

fig = px.pie(
    doss,
    names='Name',
    values='amt',
)
fig.update_layout(title="Vaccine Brand Used",
                  title_x=0.5,
                  paper_bgcolor='#19191E',
                  plot_bgcolor="#19191E",
                  width=w,
                  height=h,
                  margin={
                      'l': 50,
                      'r': 50,
                      't': 50,
                      'b': 50,
                      'pad': 00
                  },
                  grid={'xgap': 0.5})
fig.update_traces(textposition='outside', textinfo='percent+value')

col2.plotly_chart(fig)
#########################################################################################################
# Distribution by gender

col1, col2 = st.columns(2)

x = int(currentIn.loc[:, 'Male'])
y = int(currentIn.loc[:, 'Female'])
z = int(currentIn.loc[:, 'Transgender'])

dos = pd.DataFrame({
    'Gender': ['Male', 'Female', 'Transgender'],
    'amt': [x, y, z]
})

fig = px.pie(dos, names='Gender', values='amt', hole=0.4)

fig.update_layout(title="Gender Ratio of vaccinated people",
                  title_x=0.5,
                  paper_bgcolor='#19191E',
                  plot_bgcolor="#19191E",
                  width=w,
                  height=h,
                  margin={
                      'l': 50,
                      'r': 50,
                      't': 50,
                      'b': 50,
                      'pad': 00
                  },
                  grid={'xgap': 0.5})
fig.update_traces(textposition='outside', textinfo='percent+value')

col1.plotly_chart(fig)
########################################################################################################
# Distribution by Age group

x = int(currentIn.loc[:, '18-44 Years'])
y = int(currentIn.loc[:, '45-60 Years'])
z = int(currentIn.loc[:, '60+ Years'])

dos = pd.DataFrame({
    'Gender': ['18-44 Years', '45-60 Years', '60+ Years'],
    'amt': [x, y, z]
})

fig = px.bar(dos,
             x='Gender',
             y='amt',
             labels={
                 'Gender': 'Age Group',
                 'amt': 'Number of people',
                 'variable': ''
             })

fig.update_layout(title="Trend on Age Group",
                  title_x=0.5,
                  paper_bgcolor='#19191E',
                  plot_bgcolor="#19191E",
                  width=w,
                  height=h,
                  margin={
                      'l': 50,
                      'r': 50,
                      't': 50,
                      'b': 50,
                      'pad': 00
                  },
                  xaxis=(dict(showgrid=False)),
                  yaxis=(dict(showgrid=False)))
fig.update_traces(marker_color='purple')
col2.plotly_chart(fig)

########################################################################################################
########################################################################################################
col1, col2 = st.columns(2)

# Number of centers over time
fig = px.line(
    data_india,
    x='Updated On',
    y='Sites',
    labels={
        'Sites': 'Centers',
        'Updated On': 'Date',
        'variable': ''
    },
)

fig.update_layout(title="Number of centers over time*",
                  title_x=0.5,
                  paper_bgcolor='#19191E',
                  plot_bgcolor="#19191E",
                  width=w,
                  height=h,
                  margin={
                      'l': 50,
                      'r': 50,
                      't': 50,
                      'b': 50,
                      'pad': 00
                  },
                  xaxis=(dict(showgrid=False)),
                  yaxis=(dict(showgrid=False)))

col1.plotly_chart(fig)

######################################################################################################
# Sessions conducted over time
fig = px.line(
    data_india,
    x='Updated On',
    y='Sessions',
    labels={
        'Updated On': 'Date',
        'value': 'Number of doses',
        'variable': ''
    },
)

fig.update_layout(title="Sessions conducted over time*",
                  title_x=0.5,
                  paper_bgcolor='#19191E',
                  plot_bgcolor="#19191E",
                  width=w,
                  height=h,
                  margin={
                      'l': 50,
                      'r': 50,
                      't': 50,
                      'b': 50,
                      'pad': 00
                  },
                  xaxis=(dict(showgrid=False)),
                  yaxis=(dict(showgrid=False)))
fig.update_traces(line_color='turquoise')
col2.plotly_chart(fig)
##########################################################################################################
# App config
hide_streamlit_style = """<style>#MainMenu {visibility: hidden;}, #footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)