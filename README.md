# 🌍 Global Education Completion Map

An interactive Streamlit web application that visualizes global education completion rates using a choropleth map. It allows users to compare countries based on primary, lower secondary, and upper secondary school completion rates — all scaled on a 0–1 index.

![App Screenshot](screenshot.png)

## 📊 Features

- Interactive world map powered by **Folium** and **GeoJSON**
- Dynamic education **Completion Index** calculated from six normalized completion metrics:
  - `comp_prim_v2_m`
  - `comp_lowsec_v2_m`
  - `comp_upsec_v2_m`
  - `comp_prim_1524_m`
  - `comp_lowsec_1524_m`
  - `comp_upsec_2029_m`
- Sidebar filter to toggle between:
  - Completion Index
  - Primary Completion Rate
  - Lower Secondary Completion Rate
  - Upper Secondary Completion Rate
- Country-level data table and per-country debug display
- Highlight support for countries with non-standard names (e.g., `"Rep. of Korea"` → `"South Korea"`)

## 🗂️ File Structure

