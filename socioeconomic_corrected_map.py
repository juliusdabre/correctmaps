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

# Suburb dropdown
suburb_options = sorted(df["Suburb"].dropna().unique())
selected_suburb = st.sidebar.selectbox("Select Suburb to Focus:", options=suburb_options)

# Filter data
filtered_df = df[df["Suburb"] == selected_suburb]

# Validate filtered data
if filtered_df.empty:
    st.warning("⚠️ No data found for the selected suburb.")
else:
    try:
        lat = float(filtered_df["Lat"].values[0])
        lon = float(filtered_df["Long"].values[0])
    except Exception as e:
        st.error(f"❌ Could not extract coordinates: {e}")
        st.stop()

    # Generate map
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Lat",
        lon="Long",
        color="Socio-economic Ranking",
        hover_name="Suburb",
        hover_data={"State": True, "Socio-economic Ranking": True, "Lat": False, "Long": False},
        color_continuous_scale=[
            "#d73027", "#f46d43", "#fdae61", "#fee08b", "#d9ef8b",
            "#a6d96a", "#66bd63", "#1a9850", "#006837", "#004529"
        ],
        range_color=(df["Socio-economic Ranking"].min(), df["Socio-economic Ranking"].max()),
        size_max=15,
        zoom=11,
        height=600,
        mapbox_style=map_styles[selected_style],
        center={"lat": lat, "lon": lon}
    )

    st.plotly_chart(fig, use_container_width=True)
