import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import time
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# st.cache_data.clear()
st.title("📊 Indonesian Airport Schedule 8 May 2024")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

file_path = 'Indonesia-flight-data.xlsx'
df = pd.read_excel(file_path)
df.head()

# Filter Jam
st.sidebar.header("Pilih Jam: ")

# Convert the "TIME" column to datetime format with the correct format
df["TIME"] = pd.to_datetime(df["TIME"], format='%H:%M:%S')

# Proceed with the filtering
start_time = df["TIME"].min()
end_time = df["TIME"].max()

# Filter Bandara
sorted_airport = sorted(df["AIRPORT"].unique())
airport = st.sidebar.multiselect("Bandara", sorted_airport)
if airport:
    df = df[df["AIRPORT"].isin(airport)]

# Filter Pesawat
sorted_airline = sorted(df["AIRLINE"].unique())
airline = st.sidebar.multiselect("Pesawat", sorted_airline)
if airline:
    df = df[df["AIRLINE"].isin(airline)]

# Card
total_airport = df["AIRPORT"].nunique()
total_airline = df["AIRLINE"].nunique()
total_flights = df["FLIGHT"].nunique()

total1, total2, total3 = st.columns(3, gap="large")

with total1:
    st.info("Jumlah Bandara")
    st.metric(label="Total Airports", value=f"{total_airport}")

with total2:
    st.info("Jumlah Pesawat")
    st.metric(label="Total Airlines", value=f"{total_airline}")

with total3:
    st.info("Jumlah Penerbangan")
    st.metric(label="Total Flights", value=f"{total_flights}")


fig_geoplot = go.Figure()

fig_geoplot.add_trace(go.Scattergeo(
    lon = df['LONG_FROM'],
    lat = df['LAT_FROM'],
    hoverinfo = 'text',
    text = df['AIRPORT'],
    mode = 'markers',
    marker = dict(
        size = 2,
        color = 'rgb(255, 0, 0)'),
    name = 'Letak Bandara',
    ))

lons = np.empty(3 * len(df))
lons[::3] = df['LONG_FROM']
lons[1::3] = df['LONG_TO']
lons[2::3] = None
lats = np.empty(3 * len(df))
lats[::3] = df['LAT_FROM']
lats[1::3] = df['LAT_TO']
lats[2::3] = None

fig_geoplot.add_trace(
    go.Scattergeo(
        lon = lons,
        lat = lats,
        mode = 'lines+markers',
        line = dict(width = 1, color = 'blue'),
        opacity = 0.4,
        marker=dict(
            size=3,
            symbol='arrow-bar-up',
            angleref='previous'
        ),
    name = 'Rute Penerbangan',
    )
)

fig_geoplot.update_layout(
    showlegend = True,
    geo = go.layout.Geo(
        scope = 'world',
        projection_type = 'azimuthal equal area',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    )
)

#rute pesawat kedatangan

df_kedatangan = df[df['TYPE'] == 'Arrival']

fig_geoplot2 = go.Figure()

fig_geoplot2.add_trace(go.Scattergeo(
    lon = df['LONG_FROM'],
    lat = df['LAT_FROM'],
    hoverinfo = 'text',
    text = df['AIRPORT'],
    mode = 'markers',
    marker = dict(
        size = 2,
        color = 'rgb(255, 0, 0)'),
    name = 'Letak Bandara',
    ))

lons = np.empty(3 * len(df_kedatangan))
lons[::3] = df_kedatangan['LONG_FROM']
lons[1::3] = df_kedatangan['LONG_TO']
lons[2::3] = None
lats = np.empty(3 * len(df_kedatangan))
lats[::3] = df_kedatangan['LAT_FROM']
lats[1::3] = df_kedatangan['LAT_TO']
lats[2::3] = None

fig_geoplot2.add_trace(
    go.Scattergeo(
        lon = lons,
        lat = lats,
        mode = 'lines+markers',
        line = dict(width = 1, color = 'yellow'),
        opacity = 0.4,
        marker=dict(
            size=3,
            symbol='arrow-bar-up',
            angleref='previous'
        ),
    name = 'Rute Penerbangan',
    )
)

fig_geoplot2.update_layout(
    showlegend = True,
    geo = go.layout.Geo(
        scope = 'world',
        projection_type = 'azimuthal equal area',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    )
)

df_keberangkatan = df[df['TYPE'] == 'Departure']

fig_geoplot3 = go.Figure()

fig_geoplot3.add_trace(go.Scattergeo(
    lon = df['LONG_FROM'],
    lat = df['LAT_FROM'],
    hoverinfo = 'text',
    text = df['AIRPORT'],
    mode = 'markers',
    marker = dict(
        size = 2,
        color = 'rgb(255, 0, 0)'),
    name = 'Letak Bandara',
    ))

lons = np.empty(3 * len(df_keberangkatan))
lons[::3] = df_keberangkatan['LONG_FROM']
lons[1::3] = df_keberangkatan['LONG_TO']
lons[2::3] = None
lats = np.empty(3 * len(df_keberangkatan))
lats[::3] = df_keberangkatan['LAT_FROM']
lats[1::3] = df_keberangkatan['LAT_TO']
lats[2::3] = None

fig_geoplot3.add_trace(
    go.Scattergeo(
        lon = lons,
        lat = lats,
        mode = 'lines+markers',
        line = dict(width = 1, color = 'green'),
        opacity = 0.4,
        marker=dict(
            size=3,
            symbol='arrow-bar-up',
            angleref='previous'
        ),
    name = 'Rute Penerbangan',
    )
)

fig_geoplot3.update_layout(
    showlegend = True,
    geo = go.layout.Geo(
        scope = 'world',
        projection_type = 'azimuthal equal area',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    ),  
)


# Top 10 pesawat
top_10_airline = df['AIRLINE'].value_counts().reset_index()
top_10_airline.columns = ['AIRLINE', 'TOTAL FLIGHTS']
top_10_airline = top_10_airline.head(10).sort_values(by='TOTAL FLIGHTS', ascending=True)
fig_topairlines = px.bar(top_10_airline, x="TOTAL FLIGHTS", y="AIRLINE", orientation="h")

# Top 10 bandara
top_10_airport = df['CODE_AIRPORT'].value_counts().reset_index()
top_10_airport.columns = ['AIRPORT', 'TOTAL FLIGHTS']
top_10_airport = top_10_airport.head(10).sort_values(by='TOTAL FLIGHTS', ascending=True)
fig_topairports = px.bar(top_10_airport, x="TOTAL FLIGHTS", y="AIRPORT", orientation="h")

# Pie Chart Type
fig_types = px.pie(df, names="TYPE")
fig_types.update_traces(textinfo='percent+label')

# Top 3 Arrival Airport
arrival = df[df['TYPE'] == 'Arrival'].groupby('CODE_AIRPORT')['TYPE'].count().reset_index(name='ARRIVAL COUNT')
arrival = arrival.rename(columns={'CODE_AIRPORT': 'AIRPORT'})
arrival = arrival.nlargest(3, 'ARRIVAL COUNT')
fig_arrival = px.bar(arrival, x='AIRPORT', y='ARRIVAL COUNT', text=['{:,.0f}'.format(x) for x in arrival['ARRIVAL COUNT']])
fig_arrival.update_traces(textposition='outside')

# Top 3 departures Airport
departure = df[df['TYPE'] == 'Departure'].groupby('CODE_AIRPORT')['TYPE'].count().reset_index(name='DEPARTURE COUNT')
departure = departure.rename(columns={'CODE_AIRPORT': 'AIRPORT'})
departure = departure.nlargest(3, 'DEPARTURE COUNT')
fig_departure = px.bar(departure, x='AIRPORT', y='DEPARTURE COUNT', text=['{:,.0f}'.format(x) for x in departure['DEPARTURE COUNT']])
fig_departure.update_traces(textposition='outside')

# 5 Pesawat yang Sering Delay
delay_airlines = df[df['STATUS'] == 'Delayed'].groupby("AIRLINE")["STATUS"].count().reset_index(name='DELAY COUNT')
delay_airlines = delay_airlines.nlargest(5, 'DELAY COUNT')
fig_airlinesdelay = px.bar(delay_airlines, x="AIRLINE", y="DELAY COUNT", text=['{:,.0f}'.format(x) for x in delay_airlines['DELAY COUNT']])
fig_airlinesdelay.update_traces(textposition='outside')

# 5 Bandara yang Sering Delay
delay_airports = df[df['STATUS'] == 'Delayed'].groupby("CODE_AIRPORT")["STATUS"].count().reset_index(name='DELAY COUNT')
delay_airports = delay_airports.rename(columns={'CODE_AIRPORT': 'AIRPORT'})
delay_airports = delay_airports.nlargest(5, 'DELAY COUNT')
fig_airportsdelay = px.bar(delay_airports, x="AIRPORT", y="DELAY COUNT", text=['{:,.0f}'.format(x) for x in delay_airports['DELAY COUNT']])
fig_airportsdelay.update_traces(textposition='outside')

# Pesawat yang Sering Batal Terbang
canceled1 = df[df['STATUS'] == 'Canceled'].groupby("AIRLINE")["STATUS"].count().reset_index(name='CANCEL COUNT')
canceled1 = canceled1.sort_values(by='CANCEL COUNT', ascending=False)
fig_canceled1 = px.bar(canceled1, x="AIRLINE", y="CANCEL COUNT", text=['{:,.0f}'.format(x) for x in canceled1['CANCEL COUNT']])
fig_canceled1.update_traces(textposition='outside')

#bandara yang paling sering membatalkan penerbangan
canceled2 = df[df['STATUS'] == 'Canceled'].groupby("CODE_AIRPORT")["STATUS"].count().reset_index(name='CANCEL COUNT')
canceled2 = canceled2.rename(columns={'CODE_AIRPORT': 'AIRPORT'})
canceled2 = canceled2.nlargest(5, 'CANCEL COUNT')
fig_canceled2 = px.bar(canceled2, x="AIRPORT", y="CANCEL COUNT", text=['{:,.0f}'.format(x) for x in canceled2['CANCEL COUNT']])
fig_canceled2.update_traces(textposition='outside')

# Pesawat yang Sering Dialihkan
diverted = df[df['STATUS'] == 'Diverted'].groupby("AIRLINE")["STATUS"].count().reset_index(name='DIVERTED COUNT')
diverted = diverted.sort_values(by='DIVERTED COUNT', ascending=False)
fig_diverted = px.bar(diverted, x="AIRLINE", y="DIVERTED COUNT", text=['{:,.0f}'.format(x) for x in diverted['DIVERTED COUNT']])
fig_diverted.update_traces(textposition='outside')

# 5 pesawat yang sudah mendarat paling banyak
landed = df[df['STATUS'] == 'Landed'].groupby("AIRLINE")["STATUS"].count().reset_index(name='LANDED COUNT')
landed = landed.nlargest(5, 'LANDED COUNT')
fig_landed = px.bar(landed, x="AIRLINE", y="LANDED COUNT", text=['{:,.0f}'.format(x) for x in landed['LANDED COUNT']])
fig_landed.update_traces(textposition='outside')

# 5 pesawat yang akan terbang paling banyak
scheduled = df[df['STATUS'] == 'Scheduled'].groupby("AIRLINE")["STATUS"].count().reset_index(name='SCHEDULE COUNT')
scheduled = scheduled.nlargest(5, 'SCHEDULE COUNT')
fig_scheduled = px.bar(scheduled, x="AIRLINE", y="SCHEDULE COUNT", text=['{:,.0f}'.format(x) for x in scheduled['SCHEDULE COUNT']])
fig_scheduled.update_traces(textposition='outside')

# 5 pesawat yang akan mendarat paling banyak
estimated = df[df['STATUS'] == 'Estimated'].groupby("AIRLINE")["STATUS"].count().reset_index(name='ESTIMATE COUNT')
estimated = estimated.nlargest(5, 'ESTIMATE COUNT')
fig_estimated = px.bar(estimated, x="AIRLINE", y="ESTIMATE COUNT", text=['{:,.0f}'.format(x) for x in estimated['ESTIMATE COUNT']])
fig_estimated.update_traces(textposition='outside')

# tabs
top, status, types, route = st.tabs(["Top Airlines & Airports","Flight Status","Flight Types","Flight Route"])
with top:
    # top
    top.markdown("<h3 style='text-align: center; color: black;'>Top 10 Airlines</h3>", unsafe_allow_html=True)
    top.plotly_chart(fig_topairlines, use_container_width=True)

    top.markdown("<h3 style='text-align: center; color: black;'>Top 10 Airports</h3>", unsafe_allow_html=True)
    top.plotly_chart(fig_topairports, use_container_width=True)

with status:
    # status
    status.markdown("<h3 style='text-align: center; color: black;'>Top 5 Airlines with Flight Delays</h3>", unsafe_allow_html=True)
    status.plotly_chart(fig_airlinesdelay, use_container_width=True)

    status.markdown("<h3 style='text-align: center; color: black;'>Top 5 Airport with Flight Delays</h3>", unsafe_allow_html=True)
    status.plotly_chart(fig_airportsdelay, use_container_width=True)

    status.markdown("<h3 style='text-align: center; color: black;'>Top 5 Airlines Canceling Flights</h3>", unsafe_allow_html=True)
    status.plotly_chart(fig_canceled1, use_container_width=True)

    status.markdown("<h3 style='text-align: center; color: black;'>Top 5 Airports Canceling Flights</h3>", unsafe_allow_html=True)
    status.plotly_chart(fig_canceled2, use_container_width=True)

    status.markdown("<h3 style='text-align: center; color: black;'>Airlines with the Most Frequently Diverted Flights</h3>", unsafe_allow_html=True)
    status.plotly_chart(fig_diverted, use_container_width=True)

    status.markdown("<h3 style='text-align: center; color: black;'>Top 5 Airlines Scheduled for Flight</h3>", unsafe_allow_html=True)
    status.plotly_chart(fig_scheduled, use_container_width=True)

    status.markdown("<h3 style='text-align: center; color: black;'>Top 5 Airlines Currently in Flight</h3>", unsafe_allow_html=True)
    status.plotly_chart(fig_estimated, use_container_width=True)

    status.markdown("<h3 style='text-align: center; color: black;'>Top 5 Airlines have Landed</h3>", unsafe_allow_html=True)
    status.plotly_chart(fig_landed, use_container_width=True)

with types:
    # types
    types.markdown("<h3 style='text-align: center; color: black;'>Percentage of Flight types</h3>", unsafe_allow_html=True)
    types.plotly_chart(fig_types, use_container_width=True)

    types.markdown("<h3 style='text-align: center; color: black;'>Top 3 Arrival Airports</h3>", unsafe_allow_html=True)
    types.plotly_chart(fig_arrival, use_container_width=True)

    types.markdown("<h3 style='text-align: center; color: black;'>Top 3 Departure Airports</h3>", unsafe_allow_html=True)
    types.plotly_chart(fig_departure, use_container_width=True)

with route:
    route.markdown("<h3 style='text-align: center; color: black;'>Flight route</h3>", unsafe_allow_html=True)
    route.plotly_chart(fig_geoplot)

    col1, col2 = st.columns((2))
    with col1 :
        route.subheader("Departure Flight route")
        route.plotly_chart(fig_geoplot2, use_container_width= True)

    with col2 :
        route.subheader("Arrival Flight route")
        route.plotly_chart(fig_geoplot3, use_container_width= True)

    # count_penerbangan = df.groupby('TYPE')['FLIGHT'].value_counts().reset_index(name='Counts')
    df_aggregated = df.groupby('TYPE', as_index=False)['FLIGHT'].value_counts()
    fig_barchart_flight = px.bar(df_aggregated, x='TYPE', y='FLIGHT', color='TYPE', title='Flight Counts by Type')
    route.plotly_chart(fig_barchart_flight)

    # df_map = pd.DataFrame({
    #     "latitude": df['LAT_FROM'],  # Rename the column to "latitude"
    #     "longitude": df['LONG_FROM'],  # Rename the column to "longitude"
    # })

    # st.map(df_map,
    #     latitude='latitude',  # Use 'latitude' as the latitude column
    #     longitude='longitude',  # Use 'longitude' as the longitude column
    #     size=20,  # Set the size of the markers
    #     color="#FF0000"  # Set the color of the markers to red
    # )

    st.subheader("Peta Rute Penerbangan Indonesia")
    
fig_map = px.scatter_mapbox(df, lat=df['LAT_FROM'], lon=df['LONG_FROM'], color="STATUS", mapbox_style="carto-positron")
fig_map.update_layout(
    mapbox_zoom=5,
    legend=dict(
        title_text='Penerbangan Indonesia',
        orientation="h",  # horizontal
        yanchor="bottom",  # posisi vertikal: bawah
        y=1.02,  # mendekati bagian atas
        xanchor="left",  # posisi horizontal: kiri
        x=0
    )
)

# Mengatur tata letak peta agar menyesuaikan konten
fig_map.update_layout(
    margin=dict(t=0, b=0, l=0, r=0)  # Menghapus margin pada layout
)

st.plotly_chart(fig_map, use_container_width=True)