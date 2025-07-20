import streamlit as st
import folium
from branca.colormap import LinearColormap
from streamlit_folium import st_folium
import pandas as pd
import json

# Load the dataset
df = pd.read_csv("education_data.csv")

# Fix country names to match GeoJSON
country_name_map = {
    "Rep. Moldova": "Moldova",
    "Trinidad/Tobago": "Trinidad and Tobago",
    "Viet Nam": "Vietnam",
    "North Macedonia": "Macedonia",
    "Maldives": "Maldives",
    "Comoros": "Comoros",
    "Papua N. Guinea": "Papua New Guinea",
    "Syrian A. R.": "Syria",
    "C. A. R.": "Central African Republic",
    "S. Tome/Principe": "Sao Tome and Principe",
    "Bosnia/Herzeg.": "Bosnia and Herzegovina",
    "Congo": "Republic of the Congo",
    "Palestine": "Palestinian Territories",
    "Timor-Leste": "East Timor",
    "U. R. Tanzania": "United Republic of Tanzania",
    "CГґte d'Ivoire": "Ivory Coast",
    "Venezuela, B. R.": "Venezuela",
    "D. R. Congo": "Democratic Republic of the Congo",
    "Saint Lucia": "St. Lucia",
    "Dominican Rep.": "Dominican Republic",
    "Equat. Guinea": "Equatorial Guinea",
    "Rep. of Korea": "South Korea",
    "Turks/Caicos Is": "Turks and Caicos Islands",
    "Russian Fed.": "Russia",
    "Lao PDR": "Laos",
    "Eswatini": "Swaziland",
    "United States": "United States of America",
    "Sao Tome and Principe": "São Tomé and Príncipe",
    "St. Lucia": "Saint Lucia"
}
df["country"] = df["country"].replace(country_name_map)

# Define the completion columns (already normalized 0–1)
completion_cols = [
    "comp_prim_v2_m",
    "comp_lowsec_v2_m",
    "comp_upsec_v2_m",
    "comp_prim_1524_m",
    "comp_lowsec_1524_m",
    "comp_upsec_2029_m"
]

# Fix columns that are in 0–100 scale by mistake (only scale down if > 1.0)
for col in completion_cols:
    df[col] = df[col].apply(lambda x: x / 100 if x > 1.0 else x)

# Drop rows with missing values
df = df.dropna(subset=completion_cols)

# Group by country and calculate column-wise mean
df_grouped = df.groupby("country", as_index=False)[completion_cols].mean()

# Directly compute the Completion Index (average of 6 normalized columns)
df_grouped["completion_index"] = df_grouped[completion_cols].mean(axis=1)

# Load GeoJSON
with open("world-countries.json", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Streamlit layout
st.set_page_config(page_title="Completion Map", layout="wide")
st.title("🌍 Global Education Completion Map")
st.markdown("This map shows the normalized completion index and education levels per country. All metrics are on a **0–1 scale**.")

# Sidebar metric selector
metric = st.sidebar.selectbox(
    "Choose a metric to display on the map",
    [
        "Completion Index",
        "Primary Completion Rate",
        "Lower Secondary Completion Rate",
        "Upper Secondary Completion Rate"
    ]
)

# Match metric to value_dict
if metric == "Completion Index":
    value_dict = dict(zip(df_grouped["country"], df_grouped["completion_index"]))
elif metric == "Primary Completion Rate":
    value_dict = dict(zip(df_grouped["country"], df_grouped["comp_prim_v2_m"]))
elif metric == "Lower Secondary Completion Rate":
    value_dict = dict(zip(df_grouped["country"], df_grouped["comp_lowsec_v2_m"]))
elif metric == "Upper Secondary Completion Rate":
    value_dict = dict(zip(df_grouped["country"], df_grouped["comp_upsec_v2_m"]))

# Get actual value range for dynamic scale
valid_values = [v for v in value_dict.values() if v is not None]
min_val = min(valid_values)
max_val = max(valid_values)

# Handle edge case: flat values
if min_val == max_val:
    min_val -= 0.01
    max_val += 0.01

# Create color gradient scale
colormap = LinearColormap(
    colors=[
        "#800026", "#BD0026", "#E31A1C", "#FC4E2A",
        "#FD8D3C", "#FEB24C", "#FED976", "#FFEDA0"
    ],
    vmin=min_val,
    vmax=max_val
)
colormap.caption = f"{metric} (Scale: {round(min_val, 2)} — {round(max_val, 2)})"

# Create the map
m = folium.Map(location=[0, 0], zoom_start=2)

def style_function(feature):
    country = feature["properties"]["name"]
    value = value_dict.get(country)
    return {
        "fillOpacity": 0.7,
        "weight": 0.2,
        "color": "black",
        "fillColor": colormap(value) if value is not None else "lightgray"
    }

# Add countries
folium.GeoJson(
    geojson,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Country:"], localize=True)
).add_to(m)

# Add legend and controls
colormap.add_to(m)
folium.LayerControl().add_to(m)

# Show map in Streamlit
st.subheader("🗺️ World Map")
st_folium(m, width=1000, height=550)

# Show Completion Index Table
st.subheader("📊 Country Ranking by Completion Index")

# Prepare table (sort descending by default)
df_table = df_grouped[["country", "completion_index"]].sort_values(
    by="completion_index", ascending=False
).reset_index(drop=True)

# Format for better readability
df_table["completion_index"] = df_table["completion_index"].round(3)

st.dataframe(df_table, use_container_width=True)

st.subheader("🔍 Maldives Debug Info")

# Filter for Maldives
maldives_row = df[df["country"] == "Maldives"][completion_cols]

if maldives_row.empty:
    st.write("No data found for Maldives.")
else:
    st.write("Raw Completion Values for Maldives:")
    st.write(maldives_row)

    # Show mean (completion index logic)
    maldives_index = maldives_row.mean(axis=1).values[0]
    st.write(f"Calculated Completion Index for Maldives: **{maldives_index:.3f}**")

st.subheader("🇰🇷 South Korea Completion Data")

# Filter using official name as it appears in your data
korea_rows = df[df["country"] == "South Korea"][completion_cols]

if korea_rows.empty:
    st.write("No data found for 'Rep. of Korea'. Check spelling or ISO code.")
else:
    st.write("Raw Completion Values:")
    st.dataframe(korea_rows)

    # Average across all rows and all completion columns
    korea_index = korea_rows.mean(axis=1).mean()
    st.write(f"Calculated Completion Index for South Korea: **{korea_index:.3f}**")

# Filter for China 
china_row = df[df["country"] == "China"][completion_cols]

if china_row.empty:
    st.write("No data found for China.")
else:
    st.write("Raw Completion Values for China:")
    st.write(maldives_row)

    # Show mean (completion index logic)
    china_index = china_row.mean(axis=1).values[0]
    st.write(f"Calculated Completion Index for China: **{maldives_index:.3f}**")

 