import streamlit as st
import folium
from branca.colormap import LinearColormap
from streamlit_folium import st_folium
import pandas as pd
import json
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Education Map Dashboard",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external CSS file
def load_css():
    with open("styles/dashboard.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Country to flag emoji mapping
def get_country_flag(country_name):
    flag_map = {
        "Afghanistan": "🇦🇫", "Albania": "🇦🇱", "Algeria": "🇩🇿", "Andorra": "🇦🇩", "Angola": "🇦🇴",
        "Antigua and Barbuda": "🇦🇬", "Argentina": "🇦🇷", "Armenia": "🇦🇲", "Australia": "🇦🇺", "Austria": "🇦🇹",
        "Azerbaijan": "🇦🇿", "Bahamas": "🇧🇸", "Bahrain": "🇧🇭", "Bangladesh": "🇧🇩", "Barbados": "🇧🇧",
        "Belarus": "🇧🇾", "Belgium": "🇧🇪", "Belize": "🇧🇿", "Benin": "🇧🇯", "Bhutan": "🇧🇹",
        "Bolivia": "🇧🇴", "Bosnia and Herzegovina": "🇧🇦", "Botswana": "🇧🇼", "Brazil": "🇧🇷", "Brunei": "🇧🇳",
        "Bulgaria": "🇧🇬", "Burkina Faso": "🇧🇫", "Burundi": "🇧🇮", "Cambodia": "🇰🇭", "Cameroon": "🇨🇲",
        "Canada": "🇨🇦", "Cape Verde": "🇨🇻", "Central African Republic": "🇨🇫", "Chad": "🇹🇩", "Chile": "🇨🇱",
        "China": "🇨🇳", "Colombia": "🇨🇴", "Comoros": "🇰🇲", "Congo": "🇨🇬", "Costa Rica": "🇨🇷",
        "Croatia": "🇭🇷", "Cuba": "🇨🇺", "Cyprus": "🇨🇾", "Czech Republic": "🇨🇿", "Democratic Republic of the Congo": "🇨🇩",
        "Denmark": "🇩🇰", "Djibouti": "🇩🇯", "Dominica": "🇩🇲", "Dominican Republic": "🇩🇴", "East Timor": "🇹🇱",
        "Ecuador": "🇪🇨", "Egypt": "🇪🇬", "El Salvador": "🇸🇻", "Equatorial Guinea": "🇬🇶", "Eritrea": "🇪🇷",
        "Estonia": "🇪🇪", "Eswatini": "🇸🇿", "Ethiopia": "🇪🇹", "Fiji": "🇫🇯", "Finland": "🇫🇮",
        "France": "🇫🇷", "Gabon": "🇬🇦", "Gambia": "🇬🇲", "Georgia": "🇬🇪", "Germany": "🇩🇪",
        "Ghana": "🇬🇭", "Greece": "🇬🇷", "Grenada": "🇬🇩", "Guatemala": "🇬🇹", "Guinea": "🇬🇳",
        "Guinea-Bissau": "🇬🇼", "Guyana": "🇬🇾", "Haiti": "🇭🇹", "Honduras": "🇭🇳", "Hungary": "🇭🇺",
        "Iceland": "🇮🇸", "India": "🇮🇳", "Indonesia": "🇮🇩", "Iran": "🇮🇷", "Iraq": "🇮🇶",
        "Ireland": "🇮🇪", "Israel": "🇮🇱", "Italy": "🇮🇹", "Ivory Coast": "🇨🇮", "Jamaica": "🇯🇲",
        "Japan": "🇯🇵", "Jordan": "🇯🇴", "Kazakhstan": "🇰🇿", "Kenya": "🇰🇪", "Kiribati": "🇰🇮",
        "Kuwait": "🇰🇼", "Kyrgyzstan": "🇰🇬", "Laos": "🇱🇦", "Latvia": "🇱🇻", "Lebanon": "🇱🇧",
        "Lesotho": "🇱🇸", "Liberia": "🇱🇷", "Libya": "🇱🇾", "Lithuania": "🇱🇹", "Luxembourg": "🇱🇺",
        "Macedonia": "🇲🇰", "Madagascar": "🇲🇬", "Malawi": "🇲🇼", "Malaysia": "🇲🇾", "Maldives": "🇲🇻",
        "Mali": "🇲🇱", "Malta": "🇲🇹", "Marshall Islands": "🇲🇭", "Mauritania": "🇲🇷", "Mauritius": "🇲🇺",
        "Mexico": "🇲🇽", "Micronesia": "🇫🇲", "Moldova": "🇲🇩", "Monaco": "🇲🇨", "Mongolia": "🇲🇳",
        "Montenegro": "🇲🇪", "Morocco": "🇲🇦", "Mozambique": "🇲🇿", "Myanmar": "🇲🇲", "Namibia": "🇳🇦",
        "Nauru": "🇳🇷", "Nepal": "🇳🇵", "Netherlands": "🇳🇱", "New Zealand": "🇳🇿", "Nicaragua": "🇳🇮",
        "Niger": "🇳🇪", "Nigeria": "🇳🇬", "North Korea": "🇰🇵", "Norway": "🇳🇴", "Oman": "🇴🇲",
        "Pakistan": "🇵🇰", "Palau": "🇵🇼", "Panama": "🇵🇦", "Papua New Guinea": "🇵🇬", "Paraguay": "🇵🇾",
        "Peru": "🇵🇪", "Philippines": "🇵🇭", "Poland": "🇵🇱", "Portugal": "🇵🇹", "Qatar": "🇶🇦",
        "Republic of the Congo": "🇨🇬", "Romania": "🇷🇴", "Russia": "🇷🇺", "Rwanda": "🇷🇼", "Saint Kitts and Nevis": "🇰🇳",
        "Saint Lucia": "🇱🇨", "Saint Vincent and the Grenadines": "🇻🇨", "Samoa": "🇼🇸", "San Marino": "🇸🇲", "Sao Tome and Principe": "🇸🇹",
        "Saudi Arabia": "🇸🇦", "Senegal": "🇸🇳", "Serbia": "🇷🇸", "Seychelles": "🇸🇨", "Sierra Leone": "🇸🇱",
        "Singapore": "🇸🇬", "Slovakia": "🇸🇰", "Slovenia": "🇸🇮", "Solomon Islands": "🇸🇧", "Somalia": "🇸🇴",
        "South Africa": "🇿🇦", "South Korea": "🇰🇷", "South Sudan": "🇸🇸", "Spain": "🇪🇸", "Sri Lanka": "🇱🇰",
        "Sudan": "🇸🇩", "Suriname": "🇸🇷", "Sweden": "🇸🇪", "Switzerland": "🇨🇭", "Syria": "🇸🇾",
        "Taiwan": "🇹🇼", "Tajikistan": "🇹🇯", "Tanzania": "🇹🇿", "Thailand": "🇹🇭", "Togo": "🇹🇬",
        "Tonga": "🇹🇴", "Trinidad and Tobago": "🇹🇹", "Tunisia": "🇹🇳", "Turkey": "🇹🇷", "Turkmenistan": "🇹🇲",
        "Tuvalu": "🇹🇻", "Uganda": "🇺🇬", "Ukraine": "🇺🇦", "United Arab Emirates": "🇦🇪", "United Kingdom": "🇬🇧",
        "United States": "🇺🇸", "United States of America": "🇺🇸", "Uruguay": "🇺🇾", "Uzbekistan": "🇺🇿", "Vanuatu": "🇻🇺",
        "Vatican City": "🇻🇦", "Venezuela": "🇻🇪", "Vietnam": "🇻🇳", "Yemen": "🇾🇪", "Zambia": "🇿🇲",
        "Zimbabwe": "🇿🇼"
    }
    return flag_map.get(country_name, "🏳️")  # Return neutral flag if country not found

# Header
st.markdown("""
<div class="main-header">
    <h1>🗺️ Global Education Disparity Map</h1>
    <p>Explore education metrics across countries with interactive visualizations</p>
</div>
""", unsafe_allow_html=True)

# Load and filter dataset
@st.cache_data
def load_data():
    use_columns = [
        "country", "year",
        "comp_prim_v2_m", "comp_lowsec_v2_m", "comp_upsec_v2_m",
        "comp_prim_1524_m", "comp_lowsec_1524_m", "comp_upsec_2029_m",
        "edu2_2024_m", "edu4_2024_m",
        "comp_higher_2yrs_2529_m", "comp_higher_4yrs_2529_m",
        "eduout_prim_m", "eduout_lowsec_m", "eduout_upsec_m"
    ]
    df = pd.read_csv("education_data.csv", usecols=use_columns)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year", "country"])
    return df

df_raw = load_data()

# Sidebar with improved styling
st.sidebar.markdown("## 🎛️ Map Controls")

# Year range filter
year_range = st.sidebar.slider(
    "📅 **Year Range**",
    min_value=int(df_raw["year"].min()),
    max_value=int(df_raw["year"].max()),
    value=(2015, 2024),
    help="Filter data by year range"
)

df_raw = df_raw[df_raw["year"].between(*year_range)]

# Fix Country Names
country_name_map = {
    "Rep. of Korea": "South Korea",
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
    "CГҧte d'Ivoire": "Ivory Coast",
    "Venezuela, B. R.": "Venezuela",
    "D. R. Congo": "Democratic Republic of the Congo",
    "Saint Lucia": "St. Lucia",
    "Dominican Rep.": "Dominican Republic",
    "Equat. Guinea": "Equatorial Guinea",
    "Turks/Caicos Is": "Turks and Caicos Islands",
    "Russian Fed.": "Russia",
    "Lao PDR": "Laos",
    "Eswatini": "Swaziland",
    "United States": "United States of America",
    "Sao Tome and Principe": "Sao Tome and Principe",
    "St. Lucia": "Saint Lucia"
}
df_raw["country"] = df_raw["country"].replace(country_name_map)

# Define Column Groups
completion_cols = [
    "comp_prim_v2_m", "comp_lowsec_v2_m", "comp_upsec_v2_m",
    "comp_prim_1524_m", "comp_lowsec_1524_m", "comp_upsec_2029_m"
]
attain_cols = ["edu2_2024_m", "edu4_2024_m"]
higher_ed_cols = ["comp_higher_2yrs_2529_m", "comp_higher_4yrs_2529_m"]
dropout_cols = ["eduout_prim_m", "eduout_lowsec_m", "eduout_upsec_m"]

def filter_latest_valid(df, columns):
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=columns)
    df = df.sort_values(by=["country", "year"], ascending=[True, False])
    return df.drop_duplicates(subset="country", keep="first")

# Compute Completion Index
df_completion = df_raw.copy()
for col in completion_cols:
    df_completion[col] = df_completion[col].apply(lambda x: x / 100 if pd.notna(x) and x > 1.0 else x)
df_completion = df_completion.dropna(subset=completion_cols)
df_completion_grouped = df_completion.groupby("country", as_index=False)[completion_cols].mean()
df_completion_grouped["completion_index"] = df_completion_grouped[completion_cols].mean(axis=1)

# Compute Attainment Index
df_attain = df_raw.copy()
for col in attain_cols:
    df_attain[col] = df_attain[col].apply(lambda x: x / 100 if pd.notna(x) and x > 1.0 else x)
df_attain = df_attain.dropna(subset=attain_cols)
df_attain_grouped = df_attain.groupby("country", as_index=False)[attain_cols].mean()
df_attain_grouped["attainment_index"] = df_attain_grouped[attain_cols].mean(axis=1)

# Compute Higher Ed Completion Index
df_higher = df_raw.copy()
for col in higher_ed_cols:
    df_higher[col] = df_higher[col].apply(lambda x: x / 100 if pd.notna(x) and x > 1.0 else x)
df_higher = df_higher.dropna(subset=higher_ed_cols)
df_higher_grouped = df_higher.groupby("country", as_index=False)[higher_ed_cols].mean()
df_higher_grouped["higher_ed_completion_index"] = df_higher_grouped[higher_ed_cols].mean(axis=1)

# Compute Dropout Index
df_dropout = filter_latest_valid(df_raw.copy(), dropout_cols)
for col in dropout_cols:
    df_dropout[col] = df_dropout[col].apply(lambda x: x / 100 if pd.notna(x) and x > 1.0 else x)
df_dropout = df_dropout.dropna(subset=dropout_cols)
df_dropout_grouped = df_dropout.groupby("country", as_index=False)[dropout_cols].mean()
df_dropout_grouped["dropout_index"] = df_dropout_grouped[dropout_cols].mean(axis=1)

# Merge All
df_merged = df_completion_grouped.merge(df_attain_grouped, on="country", how="outer")
df_merged = df_merged.merge(df_higher_grouped, on="country", how="outer")
df_merged = df_merged.merge(df_dropout_grouped[["country", "dropout_index"]], on="country", how="outer")

# Map type selection
map_type = st.sidebar.radio(
    "🗺️ **Map Type**",
    ["Choropleth", "Circle Bubble"],
    help="Choose between filled regions or bubble markers"
)

# Metric selection
metric = st.sidebar.selectbox(
    "📊 **Choose Index**",
    [
        "Completion Index",
        "Attainment Index",
        "Higher Education Completion Index", 
        "Dropout Index"
    ],
    help="Select the education metric to visualize"
)

metric_column_map = {
    "Completion Index": "completion_index",
    "Attainment Index": "attainment_index",
    "Higher Education Completion Index": "higher_ed_completion_index",
    "Dropout Index": "dropout_index"
}

# Metric descriptions
metric_descriptions = {
    "Completion Index": "Average completion rate of young students who completed primary and secondary education",
    "Attainment Index": "Average attainment rate of young students who attained primary and secondary education",
    "Higher Education Completion Index": "Average completion rate of higher education programs for adults aged 25-29",
    "Dropout Index": "Average of primary, lower secondary, and upper secondary dropout rates"
}

# Display metric description
with st.sidebar.expander("ℹ️ **Index Definition**"):
    st.markdown(f"""
    <div class="info-box">
        <h4>📚 {metric}</h4>
        <p>{metric_descriptions[metric]}</p>
    </div>
    """, unsafe_allow_html=True)

# Export functionality
st.sidebar.markdown("### 📥 **Export Data**")

# Download original dataset
if st.sidebar.button("📊 Download Original Dataset", help="Download the complete education_data.csv file"):
    try:
        with open("education_data.csv", 'r') as f:
            csv_data = f.read()
        
        st.sidebar.download_button(
            label="💾 Download education_data.csv",
            data=csv_data,
            file_name="education_data.csv",
            mime="text/csv",
            help="Download the complete original education dataset"
        )
        
        st.sidebar.success("✅ Original dataset ready for download!")
    except FileNotFoundError:
        st.sidebar.error("❌ education_data.csv file not found")
    except Exception as e:
        st.sidebar.error(f"❌ Error reading file: {str(e)}")

# Export country ranking data
if st.sidebar.button("📊 Export Country Rankings", help="Download the country ranking data as a CSV file"):
    # Prepare ranking data for export
    df_ranking_export = df_merged[["country", value_column]].dropna().copy()
    df_ranking_export = df_ranking_export.sort_values(value_column, ascending=False).reset_index(drop=True)
    df_ranking_export.insert(0, "Rank", range(1, len(df_ranking_export) + 1))
    
    # Rename columns for clarity
    df_ranking_export = df_ranking_export.rename(columns={
        "country": "Country",
        value_column: metric
    })
    
    # Convert to CSV
    csv_data = df_ranking_export.to_csv(index=False)
    
    # Create download button
    st.sidebar.download_button(
        label="💾 Download Rankings CSV",
        data=csv_data,
        file_name=f"education_rankings_{metric.replace(' ', '_').lower()}_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv",
        help="Download the country ranking data as a CSV file"
    )
    
    st.sidebar.success(f"✅ Rankings ready for download! ({len(df_ranking_export)} countries)")

# Export regional statistics
if st.sidebar.button("🌍 Export Regional Stats", help="Download regional statistics as a CSV file"):
    # Calculate regional statistics
    geographic_regions = {
        "Europe": ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", 
                  "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "France", 
                  "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", 
                  "Luxembourg", "Macedonia", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", 
                  "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", 
                  "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom"],
        "Asia": ["Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", 
                "Cambodia", "China", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", 
                "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", 
                "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", 
                "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", 
                "Syria", "Taiwan", "Tajikistan", "Thailand", "Turkey", "Turkmenistan", "United Arab Emirates", 
                "Uzbekistan", "Vietnam", "Yemen"],
        "Africa": ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", 
                  "Cape Verde", "Central African Republic", "Chad", "Comoros", "Congo", "Democratic Republic of the Congo", 
                  "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia", "Gabon", "Gambia", 
                  "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", 
                  "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", 
                  "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", 
                  "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", 
                  "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"],
        "Americas": ["Antigua and Barbuda", "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", 
                    "Brazil", "Canada", "Chile", "Colombia", "Costa Rica", "Cuba", "Dominica", 
                    "Dominican Republic", "Ecuador", "El Salvador", "Grenada", "Guatemala", "Guyana", 
                    "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", 
                    "Peru", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
                    "Suriname", "Trinidad and Tobago", "United States", "Uruguay", "Venezuela"],
        "Oceania": ["Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", 
                   "New Zealand", "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", 
                   "Tuvalu", "Vanuatu"]
    }
    
    # Add regional classification to export data
    df_regional_export = df_merged[["country", value_column]].dropna().copy()
    df_regional_export["Region"] = "Other"
    
    for region, countries in geographic_regions.items():
        df_regional_export.loc[df_regional_export["country"].isin(countries), "Region"] = region
    
    # Calculate regional averages
    regional_stats = df_regional_export.groupby("Region")[value_column].agg(['mean', 'min', 'max', 'std', 'count']).reset_index()
    regional_stats = regional_stats.rename(columns={
        "Region": "Geographic Region",
        value_column: metric,
        "mean": "Average",
        "min": "Minimum",
        "max": "Maximum", 
        "std": "Standard Deviation",
        "count": "Number of Countries"
    })
    
    # Convert to CSV
    csv_data = regional_stats.to_csv(index=False)
    
    # Create download button
    st.sidebar.download_button(
        label="💾 Download Regional Stats CSV",
        data=csv_data,
        file_name=f"regional_education_stats_{metric.replace(' ', '_').lower()}_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv",
        help="Download regional statistics as a CSV file"
    )
    
    st.sidebar.success(f"✅ Regional stats ready for download! ({len(regional_stats)} regions)")

value_column = metric_column_map[metric]
value_dict = dict(zip(df_merged["country"], df_merged[value_column]))
value_dict = {k: float(v) for k, v in value_dict.items() if pd.notna(v) and np.isfinite(v)}

# Data validation
valid_values = sorted(value_dict.values())
if len(valid_values) < 2:
    st.markdown("""
    <div class="warning-box">
        <h3>⚠️ Insufficient Data</h3>
        <p>Not enough valid data to render the map. Please try a different year range or metric.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

min_val, max_val = valid_values[0], valid_values[-1]
if min_val == max_val:
    min_val -= 0.01
    max_val += 0.01

# Determine color scheme
reverse_colors = value_column == "dropout_index"
color_list = ["#800026", "#BD0026", "#E31A1C", "#FC4E2A", "#FD8D3C", "#FEB24C", "#FED976", "#FFEDA0"]
if reverse_colors:
    color_list = color_list[::-1]

# Create colormap
colormap = LinearColormap(
    colors=color_list,
    vmin=min_val,
    vmax=max_val
)
colormap.caption = f"{metric} (Scale: {round(min_val, 2)} — {round(max_val, 2)})"

# Create ranking dictionary
ranking_dict = {
    row["country"]: idx + 1
    for idx, row in df_merged[["country", value_column]]
        .dropna()
        .sort_values(by=value_column, ascending=False)
        .reset_index(drop=True)
        .iterrows()
}

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 🗺️ Interactive World Map")
    
    # Create map
    m = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodbpositron')
    
    # Load GeoJSON
    try:
        with open("world-countries.json", "r", encoding="utf-8") as f:
            geojson = json.load(f)
    except FileNotFoundError:
        st.error("GeoJSON file not found. Please ensure 'world-countries.json' is in the correct location.")
        st.stop()
    
    if map_type == "Choropleth":
        for feature in geojson["features"]:
            country = feature["properties"]["name"]
            value = value_dict.get(country)
            rank = ranking_dict.get(country)

            fill_color = colormap(value) if value is not None and np.isfinite(value) else "lightgray"
            
            # Enhanced tooltip
            if rank == 1:
                tooltip_text = f"🥇 {country}<br>Rank: 1st<br>{metric}: {value:.3f}"
            elif rank:
                tooltip_text = f"🏆 {country}<br>Rank: {rank}<br>{metric}: {value:.3f}"
            else:
                tooltip_text = f"❓ {country}<br>No data available"

            gj = folium.GeoJson(
                feature,
                style_function=lambda x, fc=fill_color: {
                    "fillOpacity": 0.7,
                    "weight": 0.3,
                    "color": "black",
                    "fillColor": fc
                },
                highlight_function=lambda x: {
                    "weight": 2,
                    "fillOpacity": 0.85,
                    "color": "green" if ranking_dict.get(x["properties"]["name"]) == 1 else "blue"
                }
            )
            gj.add_child(folium.Tooltip(tooltip_text))
            gj.add_to(m)

    elif map_type == "Circle Bubble":
        for country, value in value_dict.items():
            match = next((f for f in geojson["features"] if f["properties"]["name"] == country), None)
            if not match or not value:
                continue

            geometry = match["geometry"]
            if geometry["type"] == "Polygon":
                coords = np.array(geometry["coordinates"][0])
            elif geometry["type"] == "MultiPolygon":
                coords = np.array(geometry["coordinates"][0][0])
            else:
                continue

            lon, lat = coords.mean(axis=0)
            radius = 10 + 20 * (value - min_val) / (max_val - min_val)
            rank = ranking_dict.get(country)
            
            # Enhanced tooltip for bubbles
            if rank == 1:
                tooltip_text = f"🥇 {country}<br>Rank: 1st<br>{metric}: {value:.3f}"
            else:
                tooltip_text = f"🏆 {country}<br>Rank: {rank}<br>{metric}: {value:.3f}"

            folium.CircleMarker(
                location=[lat, lon],
                radius=radius,
                color="black",
                fill=True,
                fill_color=colormap(value),
                fill_opacity=0.8,
                weight=1,
                tooltip=tooltip_text
            ).add_to(m)

    colormap.add_to(m)
    folium.LayerControl().add_to(m)
    
    # Display map
    st_folium(m, width=800, height=500)

with col2:
    st.markdown("## 📊 Quick Insights")
    
    # Top performers
    top_countries = df_merged[["country", value_column]].dropna().sort_values(value_column, ascending=False).head(5)
    
    st.markdown("### 🏆 Top Performers")
    for idx, row in top_countries.iterrows():
        country = row["country"]
        value = row[value_column]
        rank = ranking_dict.get(country, "N/A")
        
        # Use country flag + medal for top 3, just flag for others
        if rank == 1:
            display_icon = f"{get_country_flag(country)} 🥇"
        elif rank == 2:
            display_icon = f"{get_country_flag(country)} 🥈"
        elif rank == 3:
            display_icon = f"{get_country_flag(country)} 🥉"
        else:
            display_icon = get_country_flag(country)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>{display_icon} {country}</h4>
            <p><strong>Rank:</strong> #{rank}</p>
            <p><strong>{metric}:</strong> {value:.3f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistics
    st.markdown("### 📈 Statistics")
    stats = df_merged[value_column].dropna()
    
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.metric("Countries with Data", len(stats))
        st.metric("Average", f"{stats.mean():.3f}")
    
    with col_stats2:
        st.metric("Minimum", f"{stats.min():.3f}")
        st.metric("Maximum", f"{stats.max():.3f}")

# Bottom section
st.markdown("---")

# Country ranking table
st.markdown("## 📋 Complete Country Ranking")

# Prepare table for display
df_metric_table = df_merged[["country", value_column]].dropna().copy()
df_metric_table[value_column] = df_metric_table[value_column].round(3)
df_metric_table = df_metric_table.rename(columns={
    "country": "Country",
    value_column: metric
})

# Add ranking column
df_metric_table = df_metric_table.sort_values(metric, ascending=False).reset_index(drop=True)
df_metric_table.insert(0, "Rank", range(1, len(df_metric_table) + 1))

# Display table with styling
st.dataframe(
    df_metric_table,
    use_container_width=True,
    column_config={
        "Rank": st.column_config.NumberColumn(
            "Rank",
            help="Global ranking position",
            format="%d"
        ),
        "Country": st.column_config.TextColumn(
            "Country",
            help="Country name"
        ),
        metric: st.column_config.NumberColumn(
            metric,
            help=f"{metric} value",
            format="%.3f"
        )
    }
)

# Footer
st.markdown("---")
st.markdown("""
<div class="dashboard-footer">
    <p>🗺️ Global Education Disparity Map Dashboard | Data Source: World Bank Education Statistics</p>
</div>
""", unsafe_allow_html=True)
