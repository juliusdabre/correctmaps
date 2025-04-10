import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import base64

# Load data
df = pd.read_excel("Socioeconomic.xlsx")
df.columns = df.columns.str.strip()

# Streamlit page setup
st.set_page_config(page_title="Socioeconomic Dashboard", layout="wide")
st.title("📍 Socioeconomic Indicator Map (Australia)")

# Sidebar filters
st.sidebar.header("🔍 Filters")
states = df['State'].dropna().unique()
suburbs = df['Suburb'].dropna().unique()

selected_state = st.sidebar.selectbox("Select State", sorted(states))
filtered_df = df[df["State"] == selected_state]

selected_suburb = st.sidebar.selectbox("Select Suburb", sorted(filtered_df["Suburb"].unique()))
suburb_data = filtered_df[filtered_df["Suburb"] == selected_suburb]

# Set Mapbox token and style
px.set_mapbox_access_token("pk.eyJ1IjoiaW52ZXN0b3JzaG9yaXpvbiIsImEiOiJjbTk5Nm80NTUwYXJ0MnJxN3AyNWk2emgxIn0.vwAB8ce5FQpxMDxNLyrrMw")

# Color scale from Red (low) to Dark Green (high)
color_scale = [
    "#d73027", "#f46d43", "#fdae61", "#fee08b", "#d9ef8b",
    "#a6d96a", "#66bd63", "#1a9850", "#006837", "#004529"
]

# Map plot
if not suburb_data.empty:
    map_fig = px.scatter_mapbox(
        suburb_data,
        lat="Long",
        lon="Lat",
        color="Socio-economic Ranking",
        size_max=15,
        zoom=12,
        hover_name="Suburb",
        hover_data={"State": True, "Socio-economic Ranking": True, "Lat": False, "Long": False},
        color_continuous_scale=color_scale,
        range_color=(1, 10),
        height=550,
        mapbox_style="mapbox://styles/mapbox/satellite-v9"
    )
    st.plotly_chart(map_fig, use_container_width=True)

    # Summary section
    st.subheader("📊 Suburb Summary")
    summary = suburb_data.iloc[0]
    st.markdown(
        f"""
        <div style='padding:1rem; background-color:#f8f9fa; border-radius:10px'>
        <b>Suburb:</b> {summary['Suburb']}<br>
        <b>State:</b> {summary['State']}<br>
        <b>Socioeconomic Rank:</b> {summary['Socio-economic Ranking']}<br>
        <b>Latitude:</b> {summary['Long']}<br>
        <b>Longitude:</b> {summary['Lat']}
        </div>
        """, unsafe_allow_html=True
    )

    # PDF generation
    def create_pdf(data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Socioeconomic Report", ln=True, align='C')
        pdf.ln(10)
        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
        return pdf.output(dest='S').encode('latin1')

    if st.button("📄 Download Suburb PDF Report"):
        pdf_data = create_pdf(summary)
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="{selected_suburb}_report.pdf">📥 Click to download your PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.warning("No data found for the selected suburb.")
