import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Regional Education Comparison",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external CSS file
def load_css():
    with open("styles/dashboard.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Header
st.markdown("""
<div class="main-header">
    <h1>🌍 Regional Education Comparison</h1>
    <p>Compare education metrics across geographic and economic regions</p>
</div>
""", unsafe_allow_html=True)

# Load and process data
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

# Define regional groupings
def create_regional_data(df):
    # Geographic regions
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
    
    # Economic regions
    economic_regions = {
        "High Income": ["Australia", "Austria", "Belgium", "Canada", "Chile", "Croatia", "Czech Republic", 
                       "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", 
                       "Iceland", "Ireland", "Israel", "Italy", "Japan", "Latvia", "Lithuania", 
                       "Luxembourg", "Malta", "Netherlands", "New Zealand", "Norway", "Poland", 
                       "Portugal", "Saudi Arabia", "Singapore", "Slovakia", "Slovenia", "South Korea", 
                       "Spain", "Sweden", "Switzerland", "Taiwan", "United Arab Emirates", "United Kingdom", "United States"],
        
        "Upper Middle Income": ["Albania", "Argentina", "Armenia", "Azerbaijan", "Belarus", "Bosnia and Herzegovina", 
                               "Botswana", "Brazil", "Bulgaria", "China", "Colombia", "Costa Rica", "Cuba", 
                               "Dominican Republic", "Ecuador", "Georgia", "Guyana", "Indonesia", "Iran", 
                               "Iraq", "Jamaica", "Kazakhstan", "Kosovo", "Lebanon", "Libya", "Malaysia", 
                               "Maldives", "Mauritius", "Mexico", "Moldova", "Montenegro", "Namibia", 
                               "North Macedonia", "Panama", "Paraguay", "Peru", "Romania", "Russia", 
                               "Serbia", "South Africa", "Suriname", "Thailand", "Turkey", "Turkmenistan", 
                               "Uruguay", "Venezuela"],
        
        "Lower Middle Income": ["Algeria", "Angola", "Bangladesh", "Benin", "Bhutan", "Bolivia", "Cambodia", 
                               "Cameroon", "Cape Verde", "Congo", "Côte d'Ivoire", "Egypt", "El Salvador", 
                               "Eswatini", "Ghana", "Guatemala", "Haiti", "Honduras", "India", "Kenya", 
                               "Kyrgyzstan", "Laos", "Lesotho", "Mauritania", "Micronesia", "Mongolia", 
                               "Morocco", "Myanmar", "Nicaragua", "Nigeria", "Pakistan", "Papua New Guinea", 
                               "Philippines", "Senegal", "Sri Lanka", "Sudan", "Tajikistan", "Tanzania", 
                               "Tunisia", "Ukraine", "Uzbekistan", "Vietnam", "Zambia"],
        
        "Low Income": ["Afghanistan", "Burkina Faso", "Burundi", "Central African Republic", "Chad", 
                      "Comoros", "Democratic Republic of the Congo", "Djibouti", "Eritrea", "Ethiopia", 
                      "Gambia", "Guinea", "Guinea-Bissau", "Liberia", "Madagascar", "Malawi", "Mali", 
                      "Mozambique", "Niger", "Rwanda", "Sao Tome and Principe", "Sierra Leone", 
                      "Somalia", "South Sudan", "Syria", "Togo", "Uganda", "Yemen", "Zimbabwe"]
    }
    
    # Fix country names
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
    
    df = df.copy()
    df["country"] = df["country"].replace(country_name_map)
    
    # Add regional classifications
    df["geographic_region"] = "Other"
    df["economic_region"] = "Other"
    
    for region, countries in geographic_regions.items():
        df.loc[df["country"].isin(countries), "geographic_region"] = region
    
    for region, countries in economic_regions.items():
        df.loc[df["country"].isin(countries), "economic_region"] = region
    
    return df

df = create_regional_data(df_raw)

# Sidebar controls
st.sidebar.markdown("## 🎛️ Regional Analysis Controls")

# Year range filter
year_range = st.sidebar.slider(
    "📅 **Year Range**",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    value=(2015, 2024),
    help="Filter data by year range"
)

# Filter data by year range
df_filtered = df[df["year"].between(*year_range)]

# Region type selection
region_type = st.sidebar.radio(
    "🌍 **Region Type**",
    ["Geographic Regions", "Economic Regions"],
    help="Choose between geographic or economic regional groupings"
)

# Metric selection
metric_options = {
    "Completion Index": ["comp_prim_v2_m", "comp_lowsec_v2_m", "comp_upsec_v2_m"],
    "Attainment Index": ["edu2_2024_m", "edu4_2024_m"],
    "Higher Education Index": ["comp_higher_2yrs_2529_m", "comp_higher_4yrs_2529_m"],
    "Dropout Index": ["eduout_prim_m", "eduout_lowsec_m", "eduout_upsec_m"]
}

selected_metric = st.sidebar.selectbox(
    "📊 **Education Metric**",
    list(metric_options.keys()),
    help="Select the education metric to analyze"
)

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

# Export regional comparison data
if st.sidebar.button("📊 Export Regional Data", help="Download the regional comparison data as a CSV file"):
    # Get region column based on selection
    region_col = "geographic_region" if region_type == "Geographic Regions" else "economic_region"
    
    # Calculate regional averages
    metric_cols = metric_options[selected_metric]
    regional_data_export = calculate_regional_averages(df_filtered, region_col, metric_cols)
    
    # Filter out "Other" regions
    regional_data_export = regional_data_export[regional_data_export[region_col] != "Other"]
    
    if not regional_data_export.empty:
        # Prepare data for export
        export_data = regional_data_export[[region_col, f"{selected_metric.lower().replace(' ', '_')}_average"]].copy()
        export_data = export_data.sort_values(f"{selected_metric.lower().replace(' ', '_')}_average", ascending=False)
        export_data.insert(0, "Rank", range(1, len(export_data) + 1))
        
        # Rename columns for clarity
        export_data = export_data.rename(columns={
            region_col: region_type.replace(" Regions", ""),
            f"{selected_metric.lower().replace(' ', '_')}_average": f"{selected_metric} Average"
        })
        
        # Convert to CSV
        csv_data = export_data.to_csv(index=False)
        
        # Create download button
        st.sidebar.download_button(
            label="💾 Download Regional CSV",
            data=csv_data,
            file_name=f"regional_comparison_{selected_metric.replace(' ', '_').lower()}_{region_type.replace(' ', '_').lower()}_{year_range[0]}_{year_range[1]}.csv",
            mime="text/csv",
            help="Download the regional comparison data as a CSV file"
        )
        
        st.sidebar.success(f"✅ Regional data ready for download! ({len(export_data)} regions)")
    else:
        st.sidebar.error("❌ No regional data available for export")

# Export detailed country data by region
if st.sidebar.button("🌍 Export Country Data by Region", help="Download detailed country data grouped by region"):
    # Get region column based on selection
    region_col = "geographic_region" if region_type == "Geographic Regions" else "economic_region"
    
    # Prepare detailed country data
    metric_cols = metric_options[selected_metric]
    df_detailed = df_filtered[["country", region_col] + metric_cols].copy()
    
    # Calculate average metric for each country
    for col in metric_cols:
        df_detailed[col] = df_detailed[col].apply(lambda x: x / 100 if pd.notna(x) and x > 1.0 else x)
    
    df_detailed[f"{selected_metric.lower().replace(' ', '_')}_average"] = df_detailed[metric_cols].mean(axis=1)
    
    # Filter out "Other" regions and countries with no data
    df_detailed = df_detailed[df_detailed[region_col] != "Other"]
    df_detailed = df_detailed.dropna(subset=[f"{selected_metric.lower().replace(' ', '_')}_average"])
    
    if not df_detailed.empty:
        # Select relevant columns and rename
        export_columns = ["country", region_col, f"{selected_metric.lower().replace(' ', '_')}_average"]
        df_export = df_detailed[export_columns].copy()
        
        df_export = df_export.rename(columns={
            "country": "Country",
            region_col: region_type.replace(" Regions", ""),
            f"{selected_metric.lower().replace(' ', '_')}_average": f"{selected_metric} Average"
        })
        
        # Sort by region and then by metric value
        df_export = df_export.sort_values([region_type.replace(" Regions", ""), f"{selected_metric} Average"], ascending=[True, False])
        
        # Convert to CSV
        csv_data = df_export.to_csv(index=False)
        
        # Create download button
        st.sidebar.download_button(
            label="💾 Download Country Data CSV",
            data=csv_data,
            file_name=f"country_data_by_region_{selected_metric.replace(' ', '_').lower()}_{region_type.replace(' ', '_').lower()}_{year_range[0]}_{year_range[1]}.csv",
            mime="text/csv",
            help="Download detailed country data grouped by region as a CSV file"
        )
        
        st.sidebar.success(f"✅ Country data ready for download! ({len(df_export)} countries)")
    else:
        st.sidebar.error("❌ No country data available for export")

# Calculate regional averages
def calculate_regional_averages(df, region_col, metric_cols):
    # Normalize values (convert percentages if needed)
    for col in metric_cols:
        df[col] = df[col].apply(lambda x: x / 100 if pd.notna(x) and x > 1.0 else x)
    
    # Calculate average for each region
    regional_data = df.groupby(region_col)[metric_cols].mean().reset_index()
    regional_data[f"{selected_metric.lower().replace(' ', '_')}_average"] = regional_data[metric_cols].mean(axis=1)
    
    return regional_data

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📊 Regional Performance Analysis")
    
    # Get region column based on selection
    region_col = "geographic_region" if region_type == "Geographic Regions" else "economic_region"
    
    # Calculate regional averages
    metric_cols = metric_options[selected_metric]
    regional_data = calculate_regional_averages(df_filtered, region_col, metric_cols)
    
    # Filter out "Other" regions
    regional_data = regional_data[regional_data[region_col] != "Other"]
    
    if not regional_data.empty:
        # Create bar chart
        fig = px.bar(
            regional_data,
            x=region_col,
            y=f"{selected_metric.lower().replace(' ', '_')}_average",
            title=f"{selected_metric} by {region_type}",
            color=region_col,
            color_discrete_sequence=px.colors.qualitative.Set3,
            labels={
                f"{selected_metric.lower().replace(' ', '_')}_average": f"{selected_metric} Average",
                region_col: region_type.replace(" Regions", "")
            }
        )
        
        fig.update_layout(
            title=dict(font=dict(size=20, color='#2c3e50'), x=0.5),
            xaxis=dict(title=region_type.replace(" Regions", ""), tickangle=45),
            yaxis=dict(title=f"{selected_metric} Average"),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Regional comparison table
        st.markdown("## 📋 Regional Comparison Table")
        
        # Prepare table data
        table_data = regional_data[[region_col, f"{selected_metric.lower().replace(' ', '_')}_average"]].copy()
        table_data = table_data.sort_values(f"{selected_metric.lower().replace(' ', '_')}_average", ascending=False)
        table_data[f"{selected_metric.lower().replace(' ', '_')}_average"] = table_data[f"{selected_metric.lower().replace(' ', '_')}_average"].round(3)
        
        # Display table
        st.dataframe(
            table_data,
            use_container_width=True,
            column_config={
                region_col: st.column_config.TextColumn(
                    region_type.replace(" Regions", ""),
                    help="Regional grouping"
                ),
                f"{selected_metric.lower().replace(' ', '_')}_average": st.column_config.NumberColumn(
                    f"{selected_metric} Average",
                    help=f"Average {selected_metric} for the region",
                    format="%.3f"
                )
            }
        )
        
    else:
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ No Data Available</h3>
            <p>No data found for the selected criteria. Please try different year range or metric.</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("## 📈 Regional Insights")
    
    if not regional_data.empty:
        # Regional statistics
        st.markdown("### 📊 Regional Statistics")
        
        # Best performing region
        best_region = regional_data.loc[regional_data[f"{selected_metric.lower().replace(' ', '_')}_average"].idxmax()]
        worst_region = regional_data.loc[regional_data[f"{selected_metric.lower().replace(' ', '_')}_average"].idxmin()]
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>🏆 Best Performing Region</h4>
            <p><strong>{best_region[region_col]}</strong></p>
            <p><strong>Score:</strong> {best_region[f'{selected_metric.lower().replace(" ", "_")}_average']:.3f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>📉 Needs Improvement</h4>
            <p><strong>{worst_region[region_col]}</strong></p>
            <p><strong>Score:</strong> {worst_region[f'{selected_metric.lower().replace(" ", "_")}_average']:.3f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Regional gap analysis
        gap = best_region[f"{selected_metric.lower().replace(' ', '_')}_average"] - worst_region[f"{selected_metric.lower().replace(' ', '_')}_average"]
        
        st.markdown(f"""
        <div class="info-box">
            <h4>📊 Regional Gap</h4>
            <p>The gap between best and worst performing regions is <strong>{gap:.3f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("## ℹ️ About Regional Analysis")
    
    region_descriptions = {
        "Geographic Regions": "Analysis based on continental and geographic groupings",
        "Economic Regions": "Analysis based on World Bank income classifications"
    }
    
    st.markdown(f"""
    <div class="info-box">
        <h4>🌍 {region_type}</h4>
        <p>{region_descriptions[region_type]}</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="dashboard-footer">
    <p>🌍 Regional Education Comparison Dashboard | Data Source: World Bank Education Statistics</p>
</div>
""", unsafe_allow_html=True) 