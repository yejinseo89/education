import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Education Trends Dashboard",
    page_icon="📊",
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
    <h1>📊 Global Education Disparity Trends</h1>
    <p>Explore education metrics across countries and time periods</p>
</div>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("education_data.csv")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    
    # Fix country names
    country_name_map = {
        "Rep. of Korea": "South Korea",
        "Rep. Moldova": "Moldova",
        "Trinidad/Tobago": "Trinidad and Tobago",
        "Viet Nam": "Vietnam",
        "North Macedonia": "Macedonia",
    }
    df["country"] = df["country"].replace(country_name_map)
    return df

df = load_data()

# Define metric categories and submetrics
index_map = {
    "Dropout Index": {
        "Primary Dropout Rate": "eduout_prim_m",
        "Lower Secondary Dropout Rate": "eduout_lowsec_m",
        "Upper Secondary Dropout Rate": "eduout_upsec_m",
    },
    "Completion Index": {
        "Primary Completion Rate": "comp_prim_v2_m",
        "Lower Secondary Completion Rate": "comp_lowsec_v2_m",
        "Upper Secondary Completion Rate": "comp_upsec_v2_m",
    },
    "Attainment Index": {
        "Primary Attainment Rate": "attain_prim_m",
        "Lower Secondary Attainment Rate": "attain_lowsec_m",
        "Upper Secondary Attainment Rate": "attain_upsec_m",
    },
    "Higher Ed Completion Index": {
        "Higher Ed Completion Rate": "higher_ed_comp_v2_m"
    }
}

# Sidebar with improved styling
st.sidebar.markdown("## 🎛️ Dashboard Controls")

# Metric selection
index_category = st.sidebar.selectbox(
    "📈 **Index Category**",
    list(index_map.keys()),
    help="Choose the type of education metric to analyze"
)

submetric_options = index_map[index_category]
selected_submetric_label = st.sidebar.selectbox(
    "📊 **Specific Metric**",
    list(submetric_options.keys()),
    help="Select the specific metric within the chosen category"
)
selected_submetric_column = submetric_options[selected_submetric_label]

# Country selection with search
available_countries = sorted(df["country"].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "🌍 **Select Countries**",
    available_countries,
    default=["South Korea", "United States", "Germany", "Japan"],
    help="Choose countries to compare (up to 8 recommended for clarity)"
)

# Year range filter
year_range = st.sidebar.slider(
    "📅 **Year Range**",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    value=(int(df["year"].min()), int(df["year"].max())),
    help="Filter data by year range"
)

# Additional options
st.sidebar.markdown("### 📊 **Display Options**")
show_markers = st.sidebar.checkbox("Show data points", value=True)
show_grid = st.sidebar.checkbox("Show grid", value=True)
show_confidence = st.sidebar.checkbox("Show trend lines", value=False)

# Export functionality
st.sidebar.markdown("### �� **Export Data**")

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

if st.sidebar.button("📊 Export to CSV", help="Download the current filtered data as a CSV file"):
    # Filter data for export
    df_export = df[
        (df["country"].isin(selected_countries)) & 
        (df["year"] >= year_range[0]) & 
        (df["year"] <= year_range[1])
    ]
    
    if not df_export.empty:
        # Select relevant columns for export
        export_columns = ["country", "year", selected_submetric_column]
        df_export_clean = df_export[export_columns].copy()
        
        # Rename columns for clarity
        df_export_clean = df_export_clean.rename(columns={
            "country": "Country",
            "year": "Year",
            selected_submetric_column: selected_submetric_label
        })
        
        # Convert to CSV
        csv_data = df_export_clean.to_csv(index=False)
        
        # Create download button
        st.sidebar.download_button(
            label="💾 Download CSV",
            data=csv_data,
            file_name=f"education_trends_{selected_submetric_label.replace(' ', '_').lower()}_{year_range[0]}_{year_range[1]}.csv",
            mime="text/csv",
            help="Download the filtered data as a CSV file"
        )
        
        st.sidebar.success(f"✅ Data ready for download! ({len(df_export_clean)} rows)")
    else:
        st.sidebar.error("❌ No data available for export")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📈 Trend Analysis")
    
    # Filter data
    df_filtered = df[
        (df["country"].isin(selected_countries)) & 
        (df["year"] >= year_range[0]) & 
        (df["year"] <= year_range[1])
    ]
    
    if not df_filtered.empty and selected_submetric_column in df_filtered.columns:
        # Create interactive plot with Plotly
        fig = go.Figure()
        
        # Color palette
        colors = px.colors.qualitative.Set3
        
        for i, country in enumerate(selected_countries):
            country_df = df_filtered[df_filtered["country"] == country].sort_values("year")
            if not country_df.empty:
                color = colors[i % len(colors)]
                
                # Main line
                fig.add_trace(go.Scatter(
                    x=country_df["year"],
                    y=country_df[selected_submetric_column],
                    mode='lines+markers' if show_markers else 'lines',
                    name=country,
                    line=dict(color=color, width=3),
                    marker=dict(size=8, color=color),
                    hovertemplate=f'<b>{country}</b><br>' +
                                'Year: %{x}<br>' +
                                f'{selected_submetric_label}: %{{y:.2f}}%<br>' +
                                '<extra></extra>'
                ))
                
                # Add trend line if requested
                if show_confidence and len(country_df) > 2:
                    z = np.polyfit(country_df["year"], country_df[selected_submetric_column], 1)
                    p = np.poly1d(z)
                    fig.add_trace(go.Scatter(
                        x=country_df["year"],
                        y=p(country_df["year"]),
                        mode='lines',
                        name=f'{country} (Trend)',
                        line=dict(color=color, width=1, dash='dash'),
                        showlegend=False
                    ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=f"{selected_submetric_label} Over Time",
                font=dict(size=20, color='#2c3e50'),
                x=0.5
            ),
            xaxis=dict(
                title="Year",
                gridcolor='lightgray' if show_grid else 'rgba(0,0,0,0)',
                showgrid=show_grid
            ),
            yaxis=dict(
                title=f"{selected_submetric_label} (%)",
                gridcolor='lightgray' if show_grid else 'rgba(0,0,0,0)',
                showgrid=show_grid
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ No Data Available</h3>
            <p>No data found for the selected metric and countries in the specified year range. Please try different selections.</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("## 📊 Quick Stats")
    
    if not df_filtered.empty and selected_submetric_column in df_filtered.columns:
        # Calculate statistics
        stats_df = df_filtered.groupby('country')[selected_submetric_column].agg([
            'mean', 'min', 'max', 'std'
        ]).round(2)
        
        for country in selected_countries:
            if country in stats_df.index:
                stats = stats_df.loc[country]
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{get_country_flag(country)} {country}</h4>
                    <p><strong>Average:</strong> {stats['mean']}%</p>
                    <p><strong>Range:</strong> {stats['min']}% - {stats['max']}%</p>
                    <p><strong>Variability:</strong> {stats['std']}%</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("## ℹ️ About This Metric")
    
    metric_descriptions = {
        "Primary Dropout Rate": "Percentage of students who leave primary education before completion",
        "Lower Secondary Dropout Rate": "Percentage of students who leave lower secondary education before completion",
        "Upper Secondary Dropout Rate": "Percentage of students who leave upper secondary education before completion",
        "Primary Completion Rate": "Percentage of students who complete primary education",
        "Lower Secondary Completion Rate": "Percentage of students who complete lower secondary education",
        "Upper Secondary Completion Rate": "Percentage of students who complete upper secondary education",
        "Primary Attainment Rate": "Percentage of population with primary education attainment",
        "Lower Secondary Attainment Rate": "Percentage of population with lower secondary education attainment",
        "Upper Secondary Attainment Rate": "Percentage of population with upper secondary education attainment",
        "Higher Ed Completion Rate": "Percentage of population with higher education completion"
    }
    
    description = metric_descriptions.get(selected_submetric_label, "Education metric for tracking student outcomes and attainment levels.")
    
    st.markdown(f"""
    <div class="info-box">
        <h4>📚 {selected_submetric_label}</h4>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="dashboard-footer">
    <p>📊 Global Education Disparity Trends Dashboard | Data Source: World Bank Education Statistics</p>
</div>
""", unsafe_allow_html=True)
