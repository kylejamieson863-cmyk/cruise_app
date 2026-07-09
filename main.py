
with app_mode[0]:
    st.markdown("<div class='rc-card'><strong>Welcome Aboard!</strong> Tap any pin on the cruise map or select a destination below to look through the holiday logs and photo captures.</div>", unsafe_allow_html=True)
    
    # 1. Coordinates and Data for your Western Med Route
    ports_data = {
        "Rome (Civitavecchia)": {"coords": [42.0925, 11.7952], "day": "Day 1: Embarkation", "desc": "Joined the ship! Capturing the massive scale of the hull from the pier."},
        "Naples / Capri": {"coords": [40.8359, 14.2694], "day": "Day 2: Southern Italy", "desc": "Exploring the dramatic coastal clips and historic streets."},
        "Barcelona": {"coords": [41.3851, 2.1734], "day": "Day 4: Catalonia", "desc": "Sunny avenues, beautiful architecture, and vibrant food markets."},
        "Marseille": {"coords": [43.2965, 5.3698], "day": "Day 5: French Riviera", "desc": "Stunning coastlines and old-world port charm."}
    }
    
    # 2. CREATE A CLEAN, MINIMALIST MAP (Stadia Smooth Dark or CartoDB Positron)
    # We use a clean canvas so our bright blue and gold colors stand out sharply!
    m = folium.Map(
        location=[41.6, 9.5], 
        zoom_start=5, 
        tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png",
        attr="&copy; OpenStreetMap contributors &copy; CARTO"
    )
    
    # 3. DRAW THE CRUISE TRACK (Thick, bright electric blue with a sleek glow effect)
    route_coordinates = [info["coords"] for info in ports_data.values()]
    
    # Outer glow line
    folium.PolyLine(route_coordinates, color="#00A8E8", weight=8, opacity=0.4).add_to(m)
    # Inner sharp line
    folium.PolyLine(route_coordinates, color="#0073E6", weight=4, opacity=0.9).add_to(m)
    
    # 4. ADD HIGH-CONTRAST PINS
    # Using vibrant Royal Caribbean blue circles with crisp white borders instead of generic map markers
    for name, info in ports_data.items():
        folium.CircleMarker(
            location=info["coords"],
            radius=8,
            color="#FFFFFF",
            weight=2,
            fill=True,
            fill_color="#002366", # Deep Royal Blue
            fill_opacity=1,
            popup=f"<b>{name}</b><br>{info['day']}"
        ).add_to(m)
    
    # Render map cleanly in the UI
    st_folium(m, width=700, height=380, returned_objects=[])
    
    # 5. Interactive Details Dropdown directly under the map
    selected_port = st.selectbox("Select a destination to view memories:", list(ports_data.keys()))
    
    # High-End Content Card for Selected Port
    st.markdown(f"""
    <div class='rc-card' style='border-top: 4px solid #0073E6;'>
        <h3 style='color: #002366; margin-top:0px;'>{selected_port}</h3>
        <p style='color: #0073E6; font-weight: bold; margin-top: -5px;'>{ports_data[selected_port]['day']}</p>
        <p style='color: #4A5568; font-size: 15px;'>{ports_data[selected_port]['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dynamically look for the local image file
    import os
    port_filename = selected_port.lower().replace(" ", "_").split("(")[0].strip()
    image_path = f"images/ports/{port_filename}.jpg"
    
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
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
import streamlit as st
import os
from streamlit_image_coordinates import streamlit_image_coordinates

# ... (Keep your existing Tab 1 code exactly the same!) ...

# ================= TAB 2: DECK BY DECK EXPLORER =================
with app_mode[1]:
    st.markdown("### 🚢 Interactive Deck Blueprints")
    st.write("Tap anywhere on the blueprint to unlock captured memories from that venue.")
    
    selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16])
    
    if selected_deck == 16:
        st.markdown("#### Deck 16 — Thrill Island & Chill Island")
        
        # 1. Define our hotspots using relative coordinate percentages (x, y)
        # This makes sure it works perfectly whether on a desktop or a phone screen!
        hotspots = {
            "FlowRider🏄‍♂️": {"x_min": 40, "x_max": 60, "y_min": 80, "y_max": 90, "desc": "Caught some waves here! (Or tried to without wiping out entirely).", "img": "flowrider.jpg"},
            "The Lime & Coconut🍹": {"x_min": 35, "x_max": 65, "y_min": 35, "y_max": 48, "desc": "Our favorite spot for sail-away drinks and live music.", "img": "lime_and_coconut.jpg"},
            "Basecamp Bar🍔": {"x_min": 20, "x_max": 50, "y_min": 65, "y_max": 75, "desc": "Grabbed a quick bite here between waterpark runs.", "img": "basecamp.jpg"}
        }
        
        deck_plan_path = "images/decks/deck16_plan.png"
        
        # Check if you have uploaded the deck plan asset yet
        if os.path.exists(deck_plan_path):
            # This special component displays the image and listens for touch events/clicks
            value = streamlit_image_coordinates(deck_plan_path, key="deck16_map")
            
            if value is not None:
                # Calculate percentages so it matches our hotspot boxes
                click_x = value["x"]
                click_y = value["y"]
                
                # Check if the user tapped inside any of our preset zones
                clicked_venue = None
                for venue_name, zone in hotspots.items():
                    if zone["x_min"] <= click_x <= zone["x_max"] and zone["y_min"] <= click_y <= zone["y_max"]:
                        clicked_venue = venue_name
                        break
                
                # 2. Display the floating asset card if they hit a target
                if clicked_venue:
                    venue_data = hotspots[clicked_venue]
                    st.markdown(f"""
                    <div class='rc-card' style='border-left: 5px solid #0073E6;'>
                        <h4 style='color: #002366; margin-top:0px;'>📍 {clicked_venue} Found!</h4>
                        <p>{venue_data['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display your personal holiday photo of that exact spot
                    venue_img_path = f"images/decks/{venue_data['img']}"
                    if os.path.exists(venue_img_path):
                        st.image(venue_img_path, use_container_width=True)
                    else:
                        st.info(f"📷 Once home, name your photo '{venue_data['img']}' and drop it in 'images/decks/' to link it here!")
                else:
                    st.write("💡 *Tip: Try tapping directly on the FlowRider at the bottom or the Pool bars near the center of the ship layout!*")
        else:
            # High-end interactive demo mode if the image file isn't on GitHub yet
            st.warning("📋 To activate this, save a screenshot of the deck blueprint as 'deck16_plan.png' inside your 'images/decks/' folder.")
            
            # Simulated click buttons for testing on the cruise ship right now!
            st.write("🛠️ **Simulate a Blueprint Tap while traveling:**")
            sim_click = st.radio("Choose a venue to simulate a tap:", ["None", "FlowRider🏄‍♂️", "The Lime & Coconut🍹"])
            
            if sim_click != "None":
                st.markdown(f"""
                <div class='rc-card' style='border-left: 5px solid #0073E6;'>
                    <h4 style='color: #002366; margin-top:0px;'>📍 {sim_click}</h4>
                    <p>{'Testing the surfing simulator waves!' if sim_click == 'FlowRider🏄‍♂️' else 'Perfect sunny afternoon drinks lounge.'}</p>
                </div>
                """, unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1500339808621-7a3a33a41145?w=800", use_container_width=True)

    else:
        st.markdown(f"<div class='rc-card'>Select **Deck 16** using the slider above to test out the live interactive mockup!</div>", unsafe_allow_html=True)
