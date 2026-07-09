import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Custom CSS to inject Royal Caribbean's exact App Design Language
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
        padding: 10px;
        text-align: center;
        font-weight: bold;
        border-radius: 0px 0px 15px 15px;
        margin-top: -60px;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }

    /* Floating White Card Styles (just like the app's 'Welcome Aboard' banner) */
    .rc-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0px 10px 30px rgba(0, 35, 102, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.8);
        margin-bottom: 20px;
    }
    
    /* Dynamic interactive tab selectors */
    .stTabs [data-baseweb="tab"] {
        color: #0073E6;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #002366;
        border-bottom-color: #0073E6;
    }
    </style>
""", unsafe_allow_html=True)

# Fake top status bar matching the phone screen shot
st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — VOYAGE TRACKER</div>", unsafe_allow_html=True)

# Main Title Section
st.markdown("<h2 style='text-align: center; color: #002366; font-weight: 800;'>My Dream Holiday</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #0073E6; font-weight: 500; margin-top: -10px;'>Interactive Route & Deck Ledger</p>", unsafe_allow_html=True)

# --- APP LAYOUT NAVIGATION TABS ---
app_mode = st.tabs(["🗺️ Full Cruise Course", "🚢 Deck-by-Deck Explorer"])

# ================= TAB 1: FULL MAP COURSE =================
with app_mode[0]:
    st.markdown("<div class='rc-card'><strong>Welcome Aboard!</strong> Tap any pin on the cruise map or select a destination below to look through the holiday logs and photo captures.</div>", unsafe_allow_html=True)
    
    # Coordinates for the Western Med route starting in Rome (Civitavecchia)
    ports_data = {
        "Rome (Civitavecchia)": {"coords": [42.0925, 11.7952], "day": "Day 1: Embarkation", "desc": "Joined the ship! Capturing the massive scale of the hull from the pier."},
        "Naples / Capri": {"coords": [40.8359, 14.2694], "day": "Day 2: Southern Italy", "desc": "Exploring the dramatic coastal clips and historic streets."},
        "Barcelona": {"coords": [41.3851, 2.1734], "day": "Day 4: Catalonia", "desc": "Sunny avenues, beautiful architecture, and vibrant food markets."},
        "Marseille": {"coords": [43.2965, 5.3698], "day": "Day 5: French Riviera", "desc": "Stunning coastlines and old-world port charm."}
    }
    
    # Base map focused on the Mediterranean
    m = folium.Map(location=[41.5, 9.5], zoom_start=5, tiles="CartoDB positron")
    
    # Draw the cruise track line connecting the course
    route_coordinates = [info["coords"] for info in ports_data.values()]
    folium.PolyLine(route_coordinates, color="#0073E6", weight=4, opacity=0.8, dash_array="10").add_to(m)
    
    # Add beautiful custom pins for each destination
    for name, info in ports_data.items():
        folium.Marker(
            location=info["coords"],
            popup=f"<b>{name}</b><br>{info['day']}",
            icon=folium.Icon(color="blue", icon="ship", prefix="fa")
        )
    
    # Render map cleanly in the UI
    st_folium(m, width=700, height=380, returned_objects=[])
    
    # Interactive Details Dropdown directly under the map
    selected_port = st.selectbox("Select a destination to view memories:", list(ports_data.keys()))
    
    # Content Card for Selected Port
    st.markdown(f"""
    <div class='rc-card'>
        <h3 style='color: #002366; margin-top:0px;'>{selected_port}</h3>
        <p style='color: #0073E6; font-weight: bold; margin-top: -5px;'>{ports_data[selected_port]['day']}</p>
        <p>{ports_data[selected_port]['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dynamically look for the local image file
    port_filename = selected_port.lower().replace(" ", "_").split("/")[0].strip()
    try:
        st.image(f"images/ports/{port_filename}.jpg", use_container_width=True)
    except FileNotFoundError:
        st.info(f"📷 Once you're home, drop your photo named '{port_filename}.jpg' into your 'images/ports/' folder to replace this preview!")
        st.image("https://images.unsplash.com/photo-1548574505-5e239809ee19?w=800", use_container_width=True)


# ================= TAB 2: DECK BY DECK EXPLORER =================
with app_mode[1]:
    st.markdown("### Ship Neighborhoods")
    
    # Slider mimicking tapping through different areas of the ship view
    selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 11, 16])
    
    if selected_deck == 8:
        st.markdown("""
        <div class='rc-card'>
            <h4 style='color: #002366; margin-top: 0px;'>🌳 Central Park (Deck 8)</h4>
            <p>An open-air neighborhood layout with real paths, lush trees, dining tables, and ambient nighttime sounds.</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            st.image("images/decks/deck8_central_park.jpg", use_container_width=True)
        except FileNotFoundError:
            st.image("https://images.unsplash.com/photo-1544025162-d76694265947?w=800", caption="Central Park Dining Space", use_container_width=True)
            
    elif selected_deck == 16:
        st.markdown("""
        <div class='rc-card'>
            <h4 style='color: #002366; margin-top: 0px;'>🌊 Chill Island & Thrill Deck (Deck 16)</h4>
            <p>Top deck resort pool spaces, waterslides, and wide horizon ocean viewing decks.</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            st.image("images/decks/deck16_pool.jpg", use_container_width=True)
        except FileNotFoundError:
            st.image("https://images.unsplash.com/photo-1500339808621-7a3a33a41145?w=800", caption="Top Deck Pools", use_container_width=True)
    else:
        st.markdown(f"<div class='rc-card'>Deck {selected_deck} Venue profiles and personal cruise captures will load here.</div>", unsafe_allow_html=True)
