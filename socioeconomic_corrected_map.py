import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

# Set Mapbox token
px.set_mapbox_access_token("pk.eyJ1IjoiaW52ZXN0b3JzaG9yaXpvbiIsImEiOiJjbTk5Nm80NTUwYXJ0MnJxN3AyNWk2emgxIn0.vwAB8ce5FQpxMDxNLyrrMw")

# Load data
df = pd.read_excel("Socioeconomic.xlsx", sheet_name=0)
df.columns = df.columns.str.strip()

st.set_page_config(page_title="Socioeconomic Dashboard", layout="wide")
st.title("🌏 Socioeconomic Dashboard with Suburb Comparison")

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
map_styles = {
    "Streets": "mapbox://styles/mapbox/streets-v12",
    "Light": "mapbox://styles/mapbox/light-v11",
    "Dark": "mapbox://styles/mapbox/dark-v11",
    "Outdoors": "mapbox://styles/mapbox/outdoors-v12",
    "Satellite": "mapbox://styles/mapbox/satellite-v9"
}
selected_style = st.sidebar.selectbox("Select Mapbox Style", list(map_styles.keys()))

# State and Suburb Selection
state_options = sorted(df["State"].dropna().unique())
selected_state = st.sidebar.selectbox("Select State:", state_options)

# Searchable suburb selection
matching_suburbs = sorted(df[df["State"] == selected_state]["Suburb"].dropna().unique())
selected_suburbs = st.sidebar.multiselect("Select Suburb(s):", matching_suburbs, default=matching_suburbs[:1])

filtered_df = df[(df["Suburb"].isin(selected_suburbs)) & (df["State"] == selected_state)]

# PDF generation section
if len(selected_suburbs) == 1:
    suburb = selected_suburbs[0]
    suburb_df = filtered_df[filtered_df["Suburb"] == suburb]
    score = suburb_df["Socio-economic Ranking"].values[0]

    st.subheader(f"📄 Suburb Summary: {suburb}")
    st.metric(label="Socio-economic Ranking", value=score)

    top10_df = df[df["State"] == selected_state].nlargest(10, "Socio-economic Ranking")

    # Plot & Save chart
    plt.figure(figsize=(8, 4))
    top10_sorted = top10_df.sort_values("Socio-economic Ranking")
    plt.barh(top10_sorted["Suburb"], top10_sorted["Socio-economic Ranking"], color="skyblue")
    plt.title(f"Top 10 Suburbs in {selected_state}")
    plt.xlabel("Socio-economic Ranking")
    plt.tight_layout()
    chart_file = "chart.png"
    plt.savefig(chart_file)
    plt.close()

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Socioeconomic Suburb Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Suburb: {suburb}", ln=True)
    pdf.cell(200, 10, txt=f"State: {selected_state}", ln=True)
    pdf.cell(200, 10, txt=f"Socio-economic Ranking: {score}", ln=True)
    pdf.ln(10)
    pdf.image(chart_file, x=10, w=180)
    pdf_file = f"Suburb_Report_{suburb.replace(' ', '_')}.pdf"
    pdf.output(pdf_file)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="⬇️ Download Suburb PDF Report",
            data=f,
            file_name=pdf_file,
            mime="application/pdf"
        )

# Comparison Map
st.subheader("🗺️ Suburb Map (Comparison View)")
if not filtered_df.empty:
    map_fig = px.scatter_mapbox(
        filtered_df,
        lat="Long",
        lon="Lat",
        color="Socio-economic Ranking",
        hover_name="Suburb",
        hover_data={"State": True, "Socio-economic Ranking": True, "Lat": False, "Long": False},
        color_continuous_scale="Viridis",
        range_color=(df["Socio-economic Ranking"].min(), df["Socio-economic Ranking"].max()),
        zoom=8,
        height=600,
        mapbox_style=map_styles[selected_style]
    )
    st.plotly_chart(map_fig, use_container_width=True)
else:
    st.info("Select one or more suburbs to view them on the map.")
