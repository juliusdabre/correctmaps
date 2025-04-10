import streamlit as st
import pandas as pd
import plotly.express as px

# Set Mapbox token
px.set_mapbox_access_token("pk.eyJ1IjoiaW52ZXN0b3JzaG9yaXpvbiIsImEiOiJjbTk5Nm80NTUwYXJ0MnJxN3AyNWk2emgxIn0.vwAB8ce5FQpxMDxNLyrrMw")

# Load data
df = pd.read_excel("Socioeconomic.xlsx", sheet_name=0)
df.columns = df.columns.str.strip()

st.set_page_config(page_title="Socioeconomic Geo Map", layout="wide")
st.title("🌏 Socioeconomic Indicator Map")

# Map styles
map_styles = {
    "Streets": "mapbox://styles/mapbox/streets-v12",
    "Light": "mapbox://styles/mapbox/light-v11",
    "Dark": "mapbox://styles/mapbox/dark-v11",
    "Outdoors": "mapbox://styles/mapbox/outdoors-v12",
    "Satellite": "mapbox://styles/mapbox/satellite-v9"
}

st.sidebar.header("🔍 Filter Options")
selected_style = st.sidebar.selectbox("Select Mapbox Style", list(map_styles.keys()))

# State filter
state_options = sorted(df["State"].dropna().unique())
selected_state = st.sidebar.selectbox("Select State:", options=state_options)

# Suburb dropdown (filtered by selected state)
suburb_options = sorted(df[df["State"] == selected_state]["Suburb"].dropna().unique())
selected_suburb = st.sidebar.selectbox("Select Suburb to Focus:", options=suburb_options)

# Filter for selected suburb within selected state
filtered_df = df[(df["Suburb"] == selected_suburb) & (df["State"] == selected_state)]

# Validate filtered data
if filtered_df.empty:
    st.warning("⚠️ No data found for the selected suburb.")
else:
    try:
        lat = float(filtered_df["Long"].values[0])
        lon = float(filtered_df["Lat"].values[0])
    except Exception as e:
        st.error(f"❌ Could not extract coordinates: {e}")
        st.stop()

    # Highlight the suburb using its score
    fig = px.choropleth_mapbox(
        filtered_df,
        geojson=None,  # scatter plot only — no boundary polygon
        lat="Long",
        lon="Lat",
        locations=filtered_df.index,
        color="Socio-economic Ranking",
        color_continuous_scale=[
            "#d73027", "#f46d43", "#fdae61", "#fee08b", "#d9ef8b",
            "#a6d96a", "#66bd63", "#1a9850", "#006837", "#004529"
        ],
        range_color=(df["Socio-economic Ranking"].min(), df["Socio-economic Ranking"].max()),
        mapbox_style=map_styles[selected_style],
        zoom=11,
        center={"lat": lat, "lon": lon},
        height=600
    )

    fig.update_traces(marker=dict(size=20))  # Highlight size

    st.plotly_chart(fig, use_container_width=True)
