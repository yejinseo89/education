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
    "Sao Tome and Principe": "Sao Tome and Principe",
    "St. Lucia": "Saint Lucia"
}
df["country"] = df["country"].replace(country_name_map)

# Define the completion columns
completion_cols = [
    "comp_prim_v2_m",
    "comp_lowsec_v2_m",
    "comp_upsec_v2_m",
    "comp_prim_1524_m",
    "comp_lowsec_1524_m",
    "comp_upsec_2029_m"
]

# Normalize values if needed
for col in completion_cols:
    df[col] = df[col].apply(lambda x: x / 100 if x > 1.0 else x)

df = df.dropna(subset=completion_cols)

df_grouped = df.groupby("country", as_index=False)[completion_cols].mean()
df_grouped["completion_index"] = df_grouped[completion_cols].mean(axis=1)

# Load GeoJSON
with open("world-countries.json", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Check for unmatched countries
geojson_names = set(f["properties"]["name"] for f in geojson["features"])
csv_names = set(df_grouped["country"].unique())
unmatched = csv_names - geojson_names
st.write("Unmatched countries:", unmatched)

# Create mapping values
display_column = "completion_index"
value_dict = dict(zip(df_grouped["country"], df_grouped[display_column]))

min_val = min(value_dict.values())
max_val = max(value_dict.values())

if min_val == max_val:
    min_val -= 0.01
    max_val += 0.01

colormap = LinearColormap(
    colors=["#800026", "#BD0026", "#E31A1C", "#FC4E2A",
            "#FD8D3C", "#FEB24C", "#FED976", "#FFEDA0"],
    vmin=min_val, vmax=max_val
)
colormap.caption = f"Completion Index (Scale: {round(min_val, 2)} — {round(max_val, 2)})"

# Create map
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

folium.GeoJson(
    geojson,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Country:"])
).add_to(m)

colormap.add_to(m)
folium.LayerControl().add_to(m)

st.title("🌍 Education Completion Index Map")
st.subheader("🗺️ World Map")
st_folium(m, width=1000, height=550)

# Table to verify South Korea presence
df_south_korea = df_grouped[df_grouped["country"] == "South Korea"]
st.subheader("🇰🇷 South Korea Completion Data")
st.dataframe(df_south_korea)