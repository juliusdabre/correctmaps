import streamlit as st
import pandas as pd
import plotly.express as px

# Set your Mapbox access token
px.set_mapbox_access_token("pk.eyJ1IjoiaW52ZXN0b3JzaG9yaXpvbiIsImEiOiJjbTk5Nm80NTUwYXJ0MnJxN3AyNWk2emgxIn0.vwAB8ce5FQpxMDxNLyrrMw")

# Load data
df = pd.read_excel("Socioeconomic.xlsx")
df.columns = df.columns.str.strip()

st.set_page_config(page_title="Socioeconomic Geo Map", layout="wide")
st.title("🌏 Socioeconomic Indicator Map")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
map_styles = {
    "Streets": "mapbox://styles/mapbox/streets-v12",
    "Light": "mapbox://styles/mapbox/light-v11",
    "Dark": "mapbox://styles/mapbox/dark-v11",
    "Outdoors": "mapbox://styles/mapbox/outdoors-v12",
    "Satellite": "mapbox://styles/mapbox/satellite-v9"
}
selected_style = st.sidebar.selectbox("Map Style", list(map_styles.keys()))

state_options = sorted(df["State"].dropna().unique())
selected_states = st.sidebar.multiselect("Select State(s):", state_options, default=state_options)

# Filter based on state
filtered_df = df[df["State"].isin(selected_states)]

# Suburb dropdown after filtering by state
suburb_options = sorted(filtered_df["Suburb"].dropna().unique())
selected_suburb = st.sidebar.selectbox("Select Suburb to Focus", options=suburb_options)

# Further filter for selected suburb
focused_df = filtered_df[filtered_df["Suburb"] == selected_suburb]

# Determine center and score range
if not focused_df.empty:
    center_lat = focused_df["Lat"].iloc[0]
    center_lon = focused_df["Long"].iloc[0]
    min_rank = int(df["Socio-economic Ranking"].min())
    max_rank = int(df["Socio-economic Ranking"].max())

    fig = px.scatter_mapbox(
        focused_df,
        lat="Lat",
        lon="Long",
        color="Socio-economic Ranking",
        color_continuous_scale="Viridis",
        size_max=15,
        zoom=12,
        height=600,
        mapbox_style=map_styles[selected_style],
        hover_name="Suburb",
        hover_data={"State": True, "Socio-economic Ranking": True, "Lat": False, "Long": False},
        center={"lat": center_lat, "lon": center_lon},
        range_color=(min_rank, max_rank)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data found for selected suburb and state.")
