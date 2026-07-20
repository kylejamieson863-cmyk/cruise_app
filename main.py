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
    
    # Realistic Maritime Route (Waypoints inserted to navigate around Sardinia & Corsica)
    # Combined Day 1 & Day 8 into a single explicit start/finish port entry to fix pin overlap
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
    
    # Rich Blue Oceans & Vibrant Green Topography Canvas
    m = folium.Map(
        location=[41.2, 7.5], 
        zoom_start=6, 
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri, HERE, Garmin, USGS, NGA, EPA, USDA, NPS"
    )

    # Draw Cruise Route (Glowing Cyan Line)
    route_coords = [info["coords"] for info in ports_data.values()]
    folium.PolyLine(route_coords, color="#00E5FF", weight=10, opacity=0.5).add_to(m) # Outer Glow
    folium.PolyLine(route_coords, color="#0052CC", weight=5, opacity=0.9).add_to(m) # Solid Line

    # Add Port Pins (Only real ports get pins)
    for port_name, info in ports_data.items():
        if info["is_port"]:
            folium.CircleMarker(
                location=info["coords"],
                radius=9,
                color="#FFFFFF",
                weight=3,
                fill=True,
                fill_color="#FF2A6D", # Vibrant Coral Pins
                fill_opacity=1,
                popup=f"<b>{port_name}</b><br>{info['date']}"
            ).add_to(m)

    # LEGEND OF THE SEAS REAL PHOTO SHIP ICON
    # Uses an image URL for Legend of the Seas directly as a map pin
    ship_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Legend_of_the_Seas_%28ship%2C_1995%29_001.jpg/320px-Legend_of_the_Seas_%28ship%2C_1995%29_001.jpg"
    
    ship_icon = folium.CustomIcon(
        ship_image_url,
        icon_size=(60, 40),
        icon_anchor=(30, 20)
    )

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

    # Display Map
    st_folium(m, width=1200, height=550, returned_objects=[])


# ================= VIEW 2: INTERACTIVE DECK FLOOR PLAN =================
else:
    st.markdown("<div class='rc-card'><strong>Deck Inspector:</strong> Choose a deck and tap directly on an attraction or venue to view your personal photos!</div>", unsafe_allow_html=True)
    
    selected_deck = st.select_slider("Select Deck Floor Plan:", options=[5, 8, 16], value=16)
    
    if selected_deck == 16:
        st.markdown("<h3 style='color: #00E5FF;'>Deck 16 — Thrill Island & Water Park</h3>", unsafe_allow_html=True)
        
        hotspots = {
            "🎢 Water Slides": {
                "x_min": 55, "x_max": 85, "y_min": 65, "y_max": 80, 
                "desc": "Captured right by the exit paths of the waterslides on Deck 16!", 
                "img": "waterslides.jpg"
            },
            "🏄‍♂️ FlowRider Surfing": {
                "x_min": 40, "x_max": 65, "y_min": 82, "y_max": 95, 
                "desc": "Surfing simulator at the aft of Deck 16.", 
                "img": "flowrider.jpg"
            },
            "🍹 Lime & Coconut Pool Bar": {
                "x_min": 35, "x_max": 65, "y_min": 30, "y_max": 48, 
                "desc": "Chilling by the pool deck lounges.", 
                "img": "lime_and_coconut.jpg"
            }
        }
        
        deck_plan_path = "images/decks/deck16_plan.png"
        
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
                        <p style='color: #4A5568; margin-bottom:0px;'>{venue_data['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    venue_img_path = f"images/decks/{venue_data['img']}"
                    if os.path.exists(venue_img_path):
                        st.image(venue_img_path, use_container_width=True)
                    else:
                        st.info(f"📷 Photo ready slot: Name your photo '{venue_data['img']}' inside your 'images/decks/' folder!")
                else:
                    st.write("💡 *Tap near the water slides near the bottom right of the deck map!*")
        else:
            st.warning("📋 Drop your deck blueprint screenshot as 'deck16_plan.png' inside 'images/decks/' to enable direct image tapping.")
            
            st.write("🧪 **Tap Simulator (Testing Mode):**")
            tap_sim = st.radio("Simulate tapping an icon on Deck 16:", ["None", "🎢 Water Slides", "🏄‍♂️ FlowRider Surfing"])
            
            if tap_sim != "None":
                venue_data = hotspots[tap_sim]
                st.markdown(f"""
                <div class='rc-card' style='border-left: 6px solid #FF2A6D;'>
                    <h3 style='color: #002366; margin-top:0px;'>📍 {tap_sim}</h3>
                    <p style='color: #4A5568; margin-bottom:0px;'>{venue_data['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1500339808621-7a3a33a41145?w=800", caption="Deck 16 Thrills", use_container_width=True)

    else:
        st.markdown(f"<div class='rc-card'>Slide back to <strong>Deck 16</strong> to test out the Water Slides interactive hotspot!</div>", unsafe_allow_html=True)
