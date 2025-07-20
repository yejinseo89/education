import streamlit as st #creating web interface 
import folium #creating interactive map 
from branca.colormap import LinearColormap
from streamlit_folium import st_folium #allowing folium map to be displayed in streamlit 
import pandas as pd
import json #reading the geojson file 

df = pd.read_csv("education_data.csv")
df = df.dropna(subset=["comp_prim_v2_m"]) #remove rows with missing values 
df = df[df["country"] != "Maldives"]

country_name_map = { #matching the country names 
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
df["country"] = df["country"].replace(country_name_map) #replacing the names 

columns_to_keep = ["comp_prim_v2_m", "comp_lowsec_v2_m", "eduyears_2024_m"]
df = df.groupby("country", as_index=False)[columns_to_keep].mean()

with open("world-countries.json", "r", encoding="utf-8") as f:
    geojson = json.load(f) #opening the geojson file 

geojson_names = set(f["properties"]["name"] for f in geojson["features"])
csv_names = set(df["country"].unique())
unmatched = csv_names - geojson_names

st.set_page_config(
    page_title="Global Education Map",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Education Inequality World Map")
st.markdown("""
More to be decided later""")
st.sidebar.title("Customize Your Education Index")

# Checkboxes to select components
use_primary = st.sidebar.checkbox("Primary Completion Rate", value=True)
use_lowersec = st.sidebar.checkbox("Lower Secondary Completion Rate", value=True)
use_years = st.sidebar.checkbox("Average Years of Schooling", value=True)

# Sliders for weights (only shown if selected)
weight_primary = st.sidebar.slider("Weight: Primary", 0.0, 1.0, 0.33) if use_primary else 0
weight_lowersec = st.sidebar.slider("Weight: Lower Sec", 0.0, 1.0, 0.33) if use_lowersec else 0
weight_years = st.sidebar.slider("Weight: Years of Schooling", 0.0, 1.0, 0.33) if use_years else 0

df["education_index"] = 0
total_weight = 0

if use_primary:
    df["education_index"] += df["comp_prim_v2_m"] * weight_primary
    total_weight += weight_primary

if use_lowersec:
    df["education_index"] += df["comp_lowsec_v2_m"] * weight_lowersec
    total_weight += weight_lowersec

if use_years:
    df["education_index"] += (df["eduyears_2024_m"] / 15) * weight_years  # Normalize to [0, 1]
    total_weight += weight_years

if total_weight > 0:
    df["education_index"] /= total_weight
else:
    df["education_index"] = None

df["comp_prim_v2_m"] = df["comp_prim_v2_m"] / 100

min_val = df["education_index"].min()
max_val = df["education_index"].max()

st.write("Min:", min_val)
st.write("Max:", max_val)

# Create 5–6 thresholds between min and max
# Only proceed if education_index has valid values
if df["education_index"].notna().any():
    min_val = df["education_index"].min()
    max_val = df["education_index"].max()

    # Fix if all values are the same
    if min_val == max_val:
        min_val = min_val - 0.01
        max_val = max_val + 0.01

    # Generate sorted and unique threshold scale
    threshold_scale = sorted(set([
        round(min_val + (max_val - min_val) * i / 5, 6) for i in range(6)
    ] + [round(max_val, 6)]))  # Ensure max is included and all are sorted

    st.write("Min:", min_val)
    st.write("Max:", max_val)
    st.write("Threshold scale:", threshold_scale)
else:
    st.warning("No valid education index values to generate the map.")
    min_val, max_val = 0, 1
    threshold_scale = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

df = df.dropna(subset=["education_index"])


st.write("Threshold scale:", threshold_scale)
# Create the folium ap
m = folium.Map(location=[0, 0], zoom_start=2)

# Define reversed color scale (dark red = low, light yellow = high)
reversed_colors = [
    "#800026",  # Dark red for low values
    "#BD0026",
    "#E31A1C",
    "#FC4E2A",
    "#FD8D3C",
    "#FEB24C",
    "#FED976",
    "#FFEDA0"   # Light yellow for high values
]

# Create color map
colormap = LinearColormap(
    colors=reversed_colors,
    vmin=min_val,
    vmax=max_val
)
colormap.caption = "Custom Education Index"

# Map values to countries
value_dict = dict(zip(df["country"], df["education_index"]))

# Style function for coloring each country
def style_function(feature):
    country = feature["properties"]["name"]
    value = value_dict.get(country)
    return {
        "fillOpacity": 0.7,
        "weight": 0.2,
        "color": "black",
        "fillColor": colormap(value) if value is not None else "lightgray"
    }

# Add styled GeoJSON to map
folium.GeoJson(
    geojson,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["name"],
        aliases=["Country:"],
        localize=True
    )
).add_to(m)

# Add legend
colormap.add_to(m)

# Optional layer control
folium.LayerControl().add_to(m)

# Display map in Streamlit
st.subheader("World Map")
st_data = st_folium(m, width=1000, height=500)
s