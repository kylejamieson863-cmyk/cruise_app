# ================= TAB 1: FULL MAP COURSE =================
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
