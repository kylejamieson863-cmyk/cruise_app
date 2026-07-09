import streamlit as dt

# 1. Custom CSS Inject to force a high-end Royal Caribbean digital style
st.markdown("""
    <style>
    /* Premium background color scaling and font styles */
    .stApp {
        background-color: #0A192F;
        color: #F4F6F9;
    }
    h1 {
        color: #FFFFFF;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        letter-spacing: 2px;
        text-align: center;
    }
    h2, h3 {
        color: #00A8E8; /* Electric Blue Accent */
        font-family: 'Inter', sans-serif;
    }
    .promo-card {
        background-color: #172A45;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #FF6B6B; /* Sunset Orange accent */
        margin-bottom: 25px;
    }
    .metric-text {
        font-size: 24px;
        font-weight: bold;
        color: #00E676;
    }
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
with st.sidebar:
    st.image("https://www.royalcaribbean.com/content/dam/royal/resources/images/logos/royal-caribbean-international-logo.png", width=150)
    st.markdown("## EXPLORE THE LEGEND")
    view_mode = st.radio(
        "Choose Your Perspective:",
        ["✨ The Grand Storyboard", "🗺️ The Voyage Map", "🚢 Deck-by-Deck Explorer"]
    )
    st.write("---")
    st.info("💡 **Developer Note:** This dashboard updates automatically as assets match predefined directory structures.")

# --- VIEW 1: THE GRAND STORYBOARD (PROMO TEXT + STATS) ---
if view_mode == "✨ The Grand Storyboard":
    st.markdown("# LEGEND OF THE SEAS")
    st.markdown("<p style='text-align: center; font-style: italic; color: #8892B0;'>This is what your dream holiday looks like.</p>", unsafe_allow_html=True)
    st.write("---")
    
    # Hero Intro Section
    st.markdown("""
    <div class='promo-card'>
        <h3>Welcome to the Next Chapter of Adventure</h3>
        <p>A cinematic look back at an unforgettable summer voyage through the Western Mediterranean. 
        From embarking in the historic port of Rome to exploring world-class neighborhoods at sea, 
        this interactive experience tracks every deck, every dining room, and every milestone.</p>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Live Metrics Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Total Decks Explored**")
        st.markdown("<p class='metric-text'>20 Decks</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("**Dining Venues Conquered**")
        st.markdown("<p class='metric-text'>14 / 28</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("**Voyage Length**")
        st.markdown("<p class='metric-text'>7 Glorious Nights</p>", unsafe_allow_html=True)

# --- VIEW 2: THE VOYAGE MAP & PORTS ---
elif view_mode == "🗺️ The Voyage Map":
    st.markdown("# THE WESTERN MEDITERRANEAN VOYAGE")
    st.write("---")
    
    # Dropdown to simulate clicking map pins or choosing ports cleanly on a mobile layout
    selected_port = st.selectbox(
        "Select a Destination Port:",
        ["Rome (Civitavecchia), Italy", "Naples, Italy", "Barcelona, Spain", "Marseille, France", "Florence (La Spezia), Italy"]
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if selected_port == "Rome (Civitavecchia), Italy":
            st.subheader("Day 1: Embarkation in Rome")
            st.markdown("""
            * **The Vibe:** Stepping foot onto the world's newest engineering marvel. 
            * **Highlight:** The first glimpse of the massive structural engineering layout before boarding.
            """)
            image_path = "images/ports/rome.jpg"
            
        elif selected_port == "Barcelona, Spain":
            st.subheader("Day 4: The Heart of Catalonia")
            st.markdown("""
            * **The Vibe:** Vibrant architecture, sunny avenues, and incredible tapas.
            * **Highlight:** Strolling through the Gothic Quarter before returning to our ship profile.
            """)
            image_path = "images/ports/barcelona.jpg"
            
        else:
            st.subheader(f"Exploring {selected_port}")
            st.markdown("* Data, memories, and tracking files will populate here dynamically once added.")
            image_path = None

    with col2:
        if image_path:
            try:
                st.image(image_path, caption=f"My Luxury Capture - {selected_port}", use_container_width=True)
            except FileNotFoundError:
                # High-end placeholder look so it runs seamlessly right away
                st.warning(f"📷 Drop your file named '{image_path.split('/')[-1]}' into the folder to see it go live instantly here!")
                st.image("https://images.unsplash.com/photo-1548574505-5e239809ee19?w=800", use_container_width=True)

# --- VIEW 3: DECK-BY-DECK EXPLORER ---
elif view_mode == "🚢 Deck-by-Deck Explorer":
    st.markdown("# ARCHITECTURE AT SEA")
    st.write("---")
    
    deck = st.select_slider(
        "Slide to Explore the Ship Decks:",
        options=[5, 8, 15, 16]
    )
    
    st.markdown(f"## Current Location: Deck {deck}")
    
    if deck == 8:
        st.markdown("### 🌳 Central Park Neighborhood")
        st.write("An open-air sanctuary featuring thousands of real plants, high-end specialty dining, and sophisticated acoustic music in the evening.")
        
        # Tabs for different venues on this deck
        venue = st.tabs(["Chops Grille", "Central Park Café", "150 Central Park"])
        with venue[0]:
            st.markdown("#### Chops Grille Steakhouse")
            st.write("The hallmark specialty restaurant layout serving prime cuts in an elegant, white-linen setting.")
            try:
                st.image("images/decks/deck8_central_park.jpg", use_container_width=True)
            except FileNotFoundError:
                st.image("https://images.unsplash.com/photo-1544025162-d76694265947?w=800", caption="Placeholder: Specialty Dinner Capture", use_container_width=True)
                
    elif deck == 16:
        st.markdown("### 🌊 Thrill Island & Waterpark")
        st.write("Home to Category 6, the largest waterpark at sea, plus adrenaline-pumping cliffside drops.")
        try:
            st.image("images/decks/deck16_waterpark.jpg", use_container_width=True)
        except FileNotFoundError:
            st.image("https://images.unsplash.com/photo-1500339808621-7a3a33a41145?w=800", caption="Placeholder: Top Deck Ocean View", use_container_width=True)
            
    else:
        st.write("Select Deck 8 or Deck 16 to check out the pre-coded premium structural examples.")
