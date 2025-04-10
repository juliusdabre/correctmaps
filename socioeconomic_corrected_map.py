# Apply the map fix (flipped lat/lon) and clean summary formatting for display
fixed_clean_code = """import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# Set Mapbox token
px.set_mapbox_access_token("pk.eyJ1IjoiaW52ZXN0b3JzaG9yaXpvbiIsImEiOiJjbTk5Nm80NTUwYXJ0MnJxN3AyNWk2emgxIn0.vwAB8ce5FQpxMDxNLyrrMw")

# Load data
df = pd.read_excel("Socioeconomic.xlsx")
df.columns = df.columns.str.strip()

# Streamlit UI setup
st.set_page_config(page_title="Socioeconomic Map", layout="wide")
st.title("🌏 Socioeconomic Indicator Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
selected_state = st.sidebar.selectbox("Select State:", sorted(df['State'].dropna().unique()))
df_filtered_state = df[df['State'] == selected_state]

selected_suburb = st.sidebar.selectbox("Select Suburb:", sorted(df_filtered_state['Suburb'].dropna().unique()))
df_filtered = df_filtered_state[df_filtered_state['Suburb'] == selected_suburb]

# Map plot
if not df_filtered.empty:
    center_lat = df_filtered["Long"].values[0]  # Long = Latitude
    center_lon = df_filtered["Lat"].values[0]   # Lat = Longitude

    fig = px.scatter_mapbox(
        df_filtered,
        lat="Long",  # Corrected
        lon="Lat",   # Corrected
        color="Socio-economic Ranking",
        size_max=15,
        zoom=12,
        hover_name="Suburb",
        hover_data=["State", "Socio-economic Ranking"],
        mapbox_style="carto-positron",
        color_continuous_scale="Viridis",
        height=600,
        center={"lat": center_lat, "lon": center_lon}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Clean summary stats
    st.subheader("📊 Suburb Snapshot")
    score = df_filtered['Socio-economic Ranking'].values[0]
    st.markdown(f\"\"\"
    - **Suburb**: `{selected_suburb}`  
    - **State**: `{selected_state}`  
    - **Socio-economic Ranking**: `{score}`
    \"\"\")

    # PDF Report Generation
    def generate_pdf(suburb_info):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Socioeconomic Report - " + selected_suburb, ln=True, align="C")
        for col in suburb_info.columns:
            val = suburb_info[col].values[0]
            pdf.cell(200, 10, txt=f"{col}: {val}", ln=True)
        pdf.output("report.pdf")

    if st.button("Generate PDF Report"):
        generate_pdf(df_filtered)
        with open("report.pdf", "rb") as file:
            st.download_button(
                label="📥 Download PDF",
                data=file,
                file_name=f"{selected_suburb}_Socioeconomic_Report.pdf",
                mime="application/pdf"
            )
else:
    st.warning("No data available for the selected suburb. Please check the data file.")
"""

# Save new version to file
script_path = "/mnt/data/socioeconomic_final_clean.py"
with open(script_path, "w") as f:
    f.write(fixed_clean_code)

# Bundle
bundle_path = "/mnt/data/socioeconomic_final_clean_bundle.zip"
with zipfile.ZipFile(bundle_path, "w") as zipf:
    zipf.write(script_path, arcname="socioeconomic_final_clean.py")
    zipf.write("/mnt/data/Socioeconomic.xlsx", arcname="Socioeconomic.xlsx")
    zipf.write("/mnt/data/requirements.txt", arcname="requirements.txt")

bundle_path
