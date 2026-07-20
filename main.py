import streamlit as st
import folium
from streamlit_folium import st_folium
import os
from streamlit_image_coordinates import streamlit_image_coordinates

# 1. Full Page Setup
st.set_page_config(page_title="Legend of the Seas", layout="wide")

# Custom Royal Caribbean App Design System
st.markdown("""
    <style>
    /* Dark oceanic theme background */
    .stApp {
        background-color: #0A192F;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Top Banner Bar */
    .brand-header {
        background: linear-gradient(90deg, #002366 0%, #0073E6 100%);
        color: white;
        padding: 12px 20px;
        text-align: center;
        font-weight: 800;
        border-radius: 0px 0px 15px 15px;
        margin-top: -60px;
        margin-bottom: 15px;
        letter-spacing: 1.5px;
        font-size: 16px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }

    /* Vibrant floating info cards */
    .rc-card {
        background: rgba(255, 255, 255, 0.95);
        color: #002366;
        border-radius: 16px;
        padding: 15px 20px;
        box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — VOYAGE TRACKER</div>", unsafe_allow_html=True)

# Initialize Session View State
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "Course Map"

# Navigation Header Controls
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h2 style='color: #00E5FF; margin-top: 0px; font-weight: 800;'>Western Mediterranean Cruise</h2>", unsafe_allow_html=True)
with col2:
    view_choice = st.radio("View Mode:", ["🗺️ Course Map", "🚢 Deck Floor Plans"], horizontal=True, key="nav_radio")

if view_choice == "🚢 Deck Floor Plans":
    st.session_state["current_view"] = "Deck Explorer"
else:
    st.session_state["current_view"] = "Course Map"

# ================= VIEW 1: VIBRANT MAP WITH REALISTIC MARITIME PATH =================
if st.session_state["current_view"] == "Course Map":
    
    # Combined Day 1 & Day 8 into a single port entry to show both dates clearly on one pin
    ports_data = {
        "Rome (Civitavecchia) — Start & Finish": {
            "coords": [42.0925, 11.7952], 
            "date": "Day 1 (Sat, Jul 11) & Day 8 (Sat, Jul 18)", 
            "is_port": True
        },
        "Day 2: Naples / Capri, Italy": {
            "coords": [40.8359, 14.2694], 
            "date": "Sun, Jul 12", 
            "is_port": True
        },
        "Sea Waypoint 1 (South of Sardinia)": {
            "coords": [38.8000, 9.5000], 
            "date": "Mon, Jul 13", 
            "is_port": False
        },
        "Day 3: At Sea (Legend of the Seas)": {
            "coords": [38.5000, 6.2000], 
            "date": "Mon, Jul 13", 
            "is_port": False
        },
        "Day 4: Barcelona, Spain": {
            "coords": [41.3851, 2.1734], 
            "date": "Tue, Jul 14", 
            "is_port": True
        },
        "Day 5: Palma De Mallorca, Spain": {
            "coords": [39.5696, 2.6502], 
            "date": "Wed, Jul 15", 
            "is_port": True
        },
        "Sea Waypoint 2 (Gulf of Lion)": {
            "coords": [41.8000, 4.5000], 
            "date": "Wed, Jul 15", 
            "is_port": False
        },
        "Day 6: Marseille (Provence), France": {
            "coords": [43.2965, 5.3698], 
            "date": "Thu, Jul 16", 
            "is_port": True
        },
        "Day 7: La Spezia (Florence/Pisa), Italy": {
            "coords": [44.1025, 9.8241], 
            "date": "Fri, Jul 17", 
            "is_port": True
        },
        "Rome Return Route": {
            "coords": [42.0925, 11.7952], 
            "date": "Sat, Jul 18", 
            "is_port": False
        }
    }
    
    # Map configuration
    m = folium.Map(
        location=[41.2, 7.5], 
        zoom_start=6, 
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri, HERE, Garmin, USGS, NGA, EPA, USDA, NPS"
    )

    # Route line around islands
    route_coords = [info["coords"] for info in ports_data.values()]
    folium.PolyLine(route_coords, color="#00E5FF", weight=10, opacity=0.5).add_to(m)
    folium.PolyLine(route_coords, color="#0052CC", weight=5, opacity=0.9).add_to(m)

    # Add Port Pins
    for port_name, info in ports_data.items():
        if info["is_port"]:
            folium.CircleMarker(
                location=info["coords"],
                radius=9,
                color="#FFFFFF",
                weight=3,
                fill=True,
                fill_color="#FF2A6D",
                fill_opacity=1,
                popup=f"<b>{port_name}</b><br>{info['date']}"
            ).add_to(m)

    # Custom Ship Picture Icon
    ship_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Legend_of_the_Seas_%28ship%2C_1995%29_001.jpg/320px-Legend_of_the_Seas_%28ship%2C_1995%29_001.jpg"
    ship_icon = folium.CustomIcon(ship_image_url, icon_size=(60, 40), icon_anchor=(30, 20))

    ship_popup_html = """
    <div style='text-align: center; font-family: sans-serif; padding: 5px;'>
        <h4 style='color: #002366; margin: 0;'>🚢 Legend of the Seas</h4>
        <p style='color: #0073E6; font-size: 12px; margin: 5px 0;'>Cruising Open Mediterranean Waters</p>
        <p><b>Switch to 'Deck Floor Plans' above to inspect ship venues!</b></p>
    </div>
    """
    
    folium.Marker(
        location=ports_data["Day 3: At Sea (Legend of the Seas)"]["coords"],
        popup=folium.Popup(ship_popup_html, max_width=250),
        icon=ship_icon,
        tooltip="🚢 Legend of the Seas"
    ).add_to(m)

    st_folium(m, width=1200, height=550, returned_objects=[])


# ================= VIEW 2: INTERACTIVE DECK FLOOR PLAN =================
else:
    st.markdown("<div class='rc-card'><strong>Deck Inspector:</strong> Choose a deck and tap directly on an attraction or venue to view your personal photos!</div>", unsafe_allow_html=True)
    
    selected_deck = st.select_slider("Select Deck Floor Plan:", options=[5, 8, 16], value=5)
    
    # ------------------- DECK 5 -------------------
    if selected_deck == 5:
        st.markdown("<h3 style='color: #00E5FF;'>Deck 5 — Royal Promenade & The Pearl</h3>", unsafe_allow_html=True)
