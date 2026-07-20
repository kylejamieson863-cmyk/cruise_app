import streamlit as st
import folium
from streamlit_folium import st_folium
import os
from streamlit_image_coordinates import streamlit_image_coordinates

# 1. CUSTOM CSS: Royal Caribbean App Design Language
st.markdown("""
    <style>
    /* Light, pristine cruise-app background */
    .stApp {
        background: linear-gradient(180deg, #E3F2FD 0%, #FFFFFF 100%);
        color: #1A365D;
        font-family: 'Inter', sans-serif;
    }
    
    /* Top Brand Bar mimicking "Ship Time" header */
    .brand-header {
        background-color: #002366;
        color: white;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        border-radius: 0px 0px 15px 15px;
        margin-top: -60px;
        margin-bottom: 25px;
        letter-spacing: 1px;
        font-size: 14px;
    }

    /* Floating White Cards */
    .rc-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0px 10px 30px rgba(0, 35, 102, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.8);
        margin-bottom: 20px;
    }
    
    /* Dynamic interactive tab selectors */
    .stTabs [data-baseweb="tab"] {
        color: #0073E6;
        font-weight: 600;
        font-size: 16px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #002366;
        border-bottom-color: #0073E6;
    }
    </style>
""", unsafe_allow_html=True)

# Fake top status bar
st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — VOYAGE TRACKER</div>", unsafe_allow_html=True)

# Main Title Section
st.markdown("<h2 style='text-align: center; color: #002366; font-weight: 800; margin-bottom: 0px;'>My Dream Holiday</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #0073E6; font-weight: 500; margin-bottom: 25px;'>Interactive Route & Deck Ledger</p>", unsafe_allow_html=True)

# --- APP LAYOUT NAVIGATION TABS ---
app_mode = st.tabs(["🗺️ Full Cruise Course", "🚢 Deck-by-Deck Explorer"])

# ================= TAB 1: FULL MAP COURSE =================
with app_mode[0]:
    st.markdown("<div class='rc-card'><strong>Welcome Aboard!</strong> Tap any pin on the cruise map or select a destination below to look through the holiday logs and photo captures.</div>", unsafe_allow_html=True)
    
    # Coordinates and Data for Western Med Route
    ports_data = {
        "Rome (Civitavecchia)": {"coords": [42.0925, 11.7952], "day": "Day 1: Embarkation", "desc": "Joined the ship! Capturing the massive scale of the hull from the pier."},
        "Naples / Capri": {"coords": [40.8359, 14.2694], "day": "Day 2: Southern Italy", "desc": "Exploring the dramatic coastal clips and historic streets."},
        "Barcelona": {"coords": [41.3851, 2.1734], "day": "Day 4: Catalonia", "desc": "Sunny avenues, beautiful architecture, and vibrant food markets."},
        "Marseille": {"coords": [43.2965, 5.3698], "day": "Day 5: French Riviera", "desc": "Stunning coastlines and old-world port charm."}
    }
    
    # Create clean canvas map
    m = folium.Map(
        location=[41.6, 9.5], 
        zoom_start=5, 
        tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png",
        attr="&copy; OpenStreetMap contributors &copy; CARTO"
    )
    
    # Draw route lines
    route_coordinates = [info["coords"] for info in ports_data.values()]
    folium.PolyLine(route_coordinates, color="#00A8E8", weight=8, opacity=0.4).add_to(m)
    folium.PolyLine(route_coordinates, color="#0073E6", weight=4, opacity=0.9).add_to(m)
    
    # Add port markers
    for name, info in ports_data.items():
        folium.CircleMarker(
            location=info["coords"],
            radius=8,
            color="#FFFFFF",
            weight=2,
            fill=True,
            fill_color="#002366", 
            fill_opacity=1,
            popup=f"<b>{name}</b><br>{info['day']}"
        ).add_to(m)
    
    # Render map
    st_folium(m, width=700, height=380, returned_objects=[])
    
    # Selector dropdown
    selected_port = st.selectbox("Select a destination to view memories:", list(ports_data.keys()))
    
    # Card for selected port
    st.markdown(f"""
    <div class='rc-card' style='border-top: 4px solid #0073E6;'>
        <h3 style='color: #002366; margin-top:0px;'>{selected_port}</h3>
        <p style='color: #0073E6; font-weight: bold; margin-top: -5px;'>{ports_data[selected_port]['day']}</p>
        <p style='color: #4A5568; font-size: 15px; margin-bottom: 0px;'>{ports_data[selected_port]['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Safely search for image file
    port_filename = selected_port.lower().replace(" ", "_").split("(")[0].strip()
    port_image_path = f"images/ports/{port_filename}.jpg"
    
    if os.path.exists(port_image_path):
        st.image(port_image_path, use_container_width=True)
    else:
        st.info(f"📷 Once you're home, drop your photo named '{port_filename}.jpg' into your 'images/ports/' folder to replace this preview!")
        st.image("https://images.unsplash.com/photo-1548574505-5e239809ee19?w=800", use_container_width=True)


# ================= TAB 2: DECK BY DECK EXPLORER =================
with app_mode[1]:
    st.markdown("### 🚢 Interactive Deck Blueprints")
    st.write("Tap anywhere on the blueprint to unlock captured memories from that venue.")
    
    selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16])
    
    if selected_deck == 16:
        st.markdown("#### Deck 16 — Thrill Island & Chill Island")
        
        hotspots = {
            "FlowRider🏄‍♂️": {"x_min": 40, "x_max": 60, "y_min": 80, "y_max": 90, "desc": "Caught some waves here! (Or tried to without wiping out entirely).", "img": "flowrider.jpg"},
            "The Lime & Coconut🍹": {"x_min": 35, "x_max": 65, "y_min": 35, "y_max": 48, "desc": "Our favorite spot for sail-away drinks and live music.", "img": "lime_and_coconut.jpg"},
            "Basecamp Bar🍔": {"x_min": 20, "x_max": 50, "y_min": 65, "y_max": 75, "desc": "Grabbed a quick bite here between waterpark runs.", "img": "basecamp.jpg"}
        }
        
        deck_plan_path = "images/decks/deck16_plan.png"
        
        if os.path.exists(deck_plan_path):
            value = streamlit_image_coordinates(deck_plan_path, key="deck16_map")
            
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
                    <div class='rc-card' style='border-left: 5px solid #0073E6;'>
                        <h4 style='color: #002366; margin-top:0px;'>📍 {clicked_venue} Found!</h4>
                        <p style='margin-bottom:0px;'>{venue_data['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    venue_img_path = f"images/decks/{venue_data['img']}"
                    if os.path.exists(venue_img_path):
                        st.image(venue_img_path, use_container_width=True)
                    else:
                        st.info(f"📷 Once home, name your photo '{venue_data['img']}' and drop it in 'images/decks/' to link it here!")
                else:
                    st.write("💡 *Tip: Try tapping directly on the FlowRider at the bottom or the Pool bars near the center of the ship layout!*")
        else:
            st.warning("📋 To activate full blueprint tapping, save a screenshot of the deck blueprint as 'deck16_plan.png' inside your 'images/decks/' folder.")
            
            st.write("🛠️ **Simulate a Blueprint Tap while traveling:**")
            sim_click = st.radio("Choose a venue to simulate a tap:", ["None", "FlowRider🏄‍♂️", "The Lime & Coconut🍹"])
            
            if sim_click != "None":
                st.markdown(f"""
                <div class='rc-card' style='border-left: 5px solid #0073E6;'>
                    <h4 style='color: #002366; margin-top:0px;'>📍 {sim_click}</h4>
                    <p style='margin-bottom:0px;'>{'Testing the surfing simulator waves!' if sim_click == 'FlowRider🏄‍♂️' else 'Perfect sunny afternoon drinks lounge.'}</p>
                </div>
                """, unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1500339808621-7a3a33a41145?w=800", use_container_width=True)

    else:
        st.markdown(f"<div class='rc-card'>Select **Deck 16** using the slider above to test out the live interactive blueprint layout mockup!</div>", unsafe_allow_html=True)
