import streamlit as st
import folium
from streamlit_folium import st_folium
import os
from streamlit_image_coordinates import streamlit_image_coordinates

# 1. Full Page Setup
st.set_page_config(page_title="Legend of the Seas", layout="wide")

# Custom App Design System
st.markdown("""
    <style>
    /* Clean, full-bleed cruise app layout */
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

    /* Vibrant floating cards */
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

# Top Bar
st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — CRUISE COURSE MAP</div>", unsafe_allow_html=True)

# Session state to switch views smoothly when ship/deck is clicked
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "Course Map"

# Header Controls
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h2 style='color: #00E5FF; margin-top: 0px; font-weight: 800;'>Voyage of the Mediterranean</h2>", unsafe_allow_html=True)
with col2:
    view_choice = st.radio("Mode:", ["🗺️ Course Map", "🚢 Deck Floor Plans"], horizontal=True, key="nav_radio")

if view_choice == "🚢 Deck Floor Plans":
    st.session_state["current_view"] = "Deck Explorer"
else:
    st.session_state["current_view"] = "Course Map"

# ================= VIEW 1: VIBRANT FULL-PAGE MAP =================
if st.session_state["current_view"] == "Course Map":
    
    # 1. Vibrant Map Engine (Rich Blues for Ocean, Bright Greens for Land)
    # Using Esri WorldTopo for vivid natural colors
    m = folium.Map(
        location=[41.5, 8.5], 
        zoom_start=6, 
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri, HERE, Garmin, Intermap, increment P Corp., GEBCO, USGS, FAO, NPS, NRCAN, GeoBase, IGN, Kadaster, ORD, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), (c) OpenStreetMap contributors, and the GIS User Community"
    )

    # Route Coordinates
    ports_data = {
        "Rome (Civitavecchia)": [42.0925, 11.7952],
        "At Sea (Legend of the Seas)": [41.2000, 7.5000], # Position on the path
        "Barcelona": [41.3851, 2.1734],
        "Marseille": [43.2965, 5.3698]
    }
    
    route_coords = list(ports_data.values())

    # 2. Draw Vibrant Cruise Path (Neon Blue Track)
    folium.PolyLine(route_coords, color="#00E5FF", weight=10, opacity=0.5).add_to(m) # Glow
    folium.PolyLine(route_coords, color="#0052CC", weight=5, opacity=1.0).add_to(m) # Solid core

    # 3. Add Port Markers
    for port, coords in ports_data.items():
        if "Legend of the Seas" not in port:
            folium.CircleMarker(
                location=coords,
                radius=9,
                color="#FFFFFF",
                weight=3,
                fill=True,
                fill_color="#FF2A6D", # Vibrant Coral Pin
                fill_opacity=1,
                popup=f"<b>{port}</b>"
            ).add_to(m)

    # 4. Add the LEGEND OF THE SEAS SHIP ICON on the path
    ship_popup_html = """
    <div style='text-align: center; font-family: sans-serif; padding: 5px;'>
        <h4 style='color: #002366; margin: 0;'>🚢 Legend of the Seas</h4>
        <p style='color: #0073E6; font-size: 12px; margin: 5px 0;'>Currently Sailing - Deck 16 Active</p>
        <p><b>Tap 'Deck Floor Plans' above to inspect venues!</b></p>
    </div>
    """
    
    # Custom Ship Marker positioned directly on the path
    folium.Marker(
        location=ports_data["At Sea (Legend of the Seas)"],
        popup=folium.Popup(ship_popup_html, max_width=250),
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip="🚢 Click to inspect Legend of the Seas!"
    ).add_to(m)

    # Render Full Page Map
    st_folium(m, width=1200, height=580, returned_objects=[])


# ================= VIEW 2: INTERACTIVE DECK FLOOR PLAN =================
else:
    st.markdown("<div class='rc-card'><strong>Deck Inspector:</strong> Choose a deck and tap directly on a venue or attraction on the floor plan map to see your holiday photo!</div>", unsafe_allow_html=True)
    
    selected_deck = st.select_slider("Select Deck Floor Plan:", options=[5, 8, 16], value=16)
    
    if selected_deck == 16:
        st.markdown("<h3 style='color: #00E5FF;'>Deck 16 — Thrill Island & Water Slides</h3>", unsafe_allow_html=True)
        
        # Hotspot zones for Deck 16 (Percentages matching the layout image)
        hotspots = {
            "🎢 Perfect Storm Water Slides": {
                "x_min": 55, "x_max": 85, "y_min": 65, "y_max": 80, 
                "desc": "Captured right by the exit of the waterslides on Deck 16!", 
                "img": "waterslides.jpg"
            },
            "🏄‍♂️ FlowRider Surfing": {
                "x_min": 40, "x_max": 65, "y_min": 82, "y_max": 95, 
                "desc": "Surfing simulator at the aft of Deck 16.", 
                "img": "flowrider.jpg"
            },
            "🍹 Lime & Coconut Pool Bar": {
                "x_min": 35, "x_max": 65, "y_min": 30, "y_max": 48, 
                "desc": "Chilling by the pool decks.", 
                "img": "lime_and_coconut.jpg"
            }
        }
        
        deck_plan_path = "images/decks/deck16_plan.png"
        
        # Interactive Image Coordinates Map
        if os.path.exists(deck_plan_path):
            st.write("👉 **Tap directly on the Water Slides or FlowRider below:**")
            value = streamlit_image_coordinates(deck_plan_path, key="deck16_interactive")
            
            if value is not None:
                click_x = value["x"]
                click_y = value["y"]
                
                clicked_venue = None
                for venue_name, zone in hotspots.items():
                    if zone["x_min"] <= click_x <= zone["x_max"] and zone["y_min"] <= click_y <= zone["y_max"]:
                        clicked_venue = venue_name
                        break
                
                if clicked_venue:
                    venue_data = hotspots[clicked_venue]
                    st.markdown(f"""
                    <div class='rc-card' style='border-left: 6px solid #FF2A6D;'>
                        <h3 style='color: #002366; margin-top:0px;'>📍 {clicked_venue}</h3>
                        <p style='color: #4A5568;'>{venue_data['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    venue_img_path = f"images/decks/{venue_data['img']}"
                    if os.path.exists(venue_img_path):
                        st.image(venue_img_path, use_container_width=True)
                    else:
                        st.info(f"📷 Photo ready slot: Name your photo '{venue_data['img']}' inside your 'images/decks/' folder!")
                else:
                    st.write("💡 *Tap near the colored water slide exit paths on the lower right of the deck map!*")
        else:
            # Fallback simulator for when running without local files attached
            st.warning("📋 Place your deck blueprint image as 'deck16_plan.png' inside 'images/decks/' to enable direct image tapping.")
            
            st.write("🧪 **Tap Simulator (Testing Mode):**")
            tap_sim = st.radio("Simulate tapping an icon on Deck 16:", ["None", "🎢 Perfect Storm Water Slides", "🏄‍♂️ FlowRider Surfing"])
            
            if tap_sim != "None":
                venue_data = hotspots[tap_sim]
                st.markdown(f"""
                <div class='rc-card' style='border-left: 6px solid #FF2A6D;'>
                    <h3 style='color: #002366; margin-top:0px;'>📍 {tap_sim}</h3>
                    <p style='color: #4A5568;'>{venue_data['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1500339808621-7a3a33a41145?w=800", caption="Deck 16 Water Slide Thrills", use_container_width=True)

    else:
        st.markdown(f"<div class='rc-card'>Slide back to <strong>Deck 16</strong> to interact with the Water Slides hotspot!</div>", unsafe_allow_html=True)
