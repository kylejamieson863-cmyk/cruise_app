import streamlit as st
import folium
from streamlit_folium import st_folium
import os
from streamlit_image_coordinates import streamlit_image_coordinates

# 1. Full Page Config
st.set_page_config(page_title="Legend of the Seas", layout="wide")

# Custom App Design Language
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
st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — VOYAGE TRACKER</div>", unsafe_allow_html=True)

# Navigation View Switcher
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "Course Map"

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h2 style='color: #00E5FF; margin-top: 0px; font-weight: 800;'>Western Mediterranean Cruise</h2>", unsafe_allow_html=True)
with col2:
    view_choice = st.radio("View Mode:", ["🗺️ Course Map", "🚢 Deck Floor Plans"], horizontal=True, key="nav_radio")

if view_choice == "🚢 Deck Floor Plans":
    st.session_state["current_view"] = "Deck Explorer"
else:
    st.session_state["current_view"] = "Course Map"

# ================= VIEW 1: VIBRANT FULL ITINERARY MAP =================
if st.session_state["current_view"] == "Course Map":
    
    # 1. Full Itinerary Coordinates based on your official itinerary
    ports_data = {
        "Day 1: Rome (Civitavecchia), Italy": {"coords": [42.0925, 11.7952], "date": "Sat, Jul 11"},
        "Day 2: Naples / Capri, Italy": {"coords": [40.8359, 14.2694], "date": "Sun, Jul 12"},
        "Day 3: At Sea (Legend of the Seas)": {"coords": [39.5000, 8.0000], "date": "Mon, Jul 13"},
        "Day 4: Barcelona, Spain": {"coords": [41.3851, 2.1734], "date": "Tue, Jul 14"},
        "Day 5: Palma De Mallorca, Spain": {"coords": [39.5696, 2.6502], "date": "Wed, Jul 15"},
        "Day 6: Marseille (Provence), France": {"coords": [43.2965, 5.3698], "date": "Thu, Jul 16"},
        "Day 7: La Spezia (Florence/Pisa), Italy": {"coords": [44.1025, 9.8241], "date": "Fri, Jul 17"},
        "Day 8: Rome (Civitavecchia), Italy": {"coords": [42.0925, 11.7952], "date": "Sat, Jul 18"}
    }
    
    # 2. Rich Blue and Lush Green Map Tiles (Esri World Topo)
    m = folium.Map(
        location=[41.2, 7.5], 
        zoom_start=6, 
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri, HERE, Garmin, USGS, NGA, EPA, USDA, NPS"
    )

    # 3. Connect the Cruise Route Loop (Neon Blue Line)
    route_coords = [info["coords"] for info in ports_data.values()]
    folium.PolyLine(route_coords, color="#00E5FF", weight=10, opacity=0.5).add_to(m) # Outer Glow
    folium.PolyLine(route_coords, color="#0052CC", weight=5, opacity=0.9).add_to(m) # Solid Line

    # 4. Add Port Pins for every port in your itinerary
    for port_name, info in ports_data.items():
        if "At Sea" not in port_name:
            folium.CircleMarker(
                location=info["coords"],
                radius=8,
                color="#FFFFFF",
                weight=3,
                fill=True,
                fill_color="#FF2A6D", # Bright Coral Pins
                fill_opacity=1,
                popup=f"<b>{port_name}</b><br>{info['date']}"
            ).add_to(m)

    # 5. LEGEND OF THE SEAS SHIP MARKER (Positioned along the route)
    ship_popup_html = """
    <div style='text-align: center; font-family: sans-serif; padding: 5px;'>
        <h4 style='color: #002366; margin: 0;'>🚢 Legend of the Seas</h4>
        <p style='color: #0073E6; font-size: 12px; margin: 5px 0;'>Sailing Western Mediterranean</p>
        <p><b>Switch to 'Deck Floor Plans' above to inspect ship venues!</b></p>
    </div>
    """
    
    folium.Marker(
        location=ports_data["Day 3: At Sea (Legend of the Seas)"]["coords"],
        popup=folium.Popup(ship_popup_html, max_width=250),
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
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
        
        # Hotspots tailored for Deck 16
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
        
        # Interactive Image Click Listener
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
            # Testing fallback while traveling
            st.warning("📋 Drop your deck screenshot as 'deck16_plan.png' inside 'images/decks/' to enable direct blueprint tapping.")
            
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
                st.image("https://images.unsplash.com/photo-1500339808621-7a3a33a41145?w=800", caption="Deck 16 Action Capture", use_container_width=True)

    else:
        st.markdown(f"<div class='rc-card'>Slide back to <strong>Deck 16</strong> to test out the Water Slides interactive hotspot!</div>", unsafe_allow_html=True)
