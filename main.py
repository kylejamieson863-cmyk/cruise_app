import streamlit as st
import folium
from streamlit_folium import st_folium
import pathlib
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# 1. Full Page Setup & Royal Caribbean Styling
st.set_page_config(page_title="Legend of the Seas", layout="wide")

st.markdown("""
    <style>
    /* Premium Royal Caribbean Dark Mode Aesthetic */
    .stApp {
        background-color: #030C1B;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Elegant Header Bar */
    .brand-header {
        background: linear-gradient(90deg, #001E4E 0%, #0066CC 100%);
        color: white;
        padding: 14px 20px;
        text-align: center;
        font-weight: 800;
        border-radius: 0px 0px 16px 16px;
        margin-top: -60px;
        margin-bottom: 20px;
        letter-spacing: 2px;
        font-size: 17px;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.5);
    }

    /* Modern Glassmorphism Cards */
    .rc-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #FFFFFF;
        border-radius: 16px;
        padding: 15px 20px;
        margin-bottom: 15px;
    }
    
    /* Clean Radio Buttons & Slider Adjustments */
    div[data-testid="stRadio"] > label {
        color: #00E5FF !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Top Header
st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — INTERACTIVE DECK EXPLORER</div>", unsafe_allow_html=True)

# File Paths setup
base_dir = pathlib.Path(__file__).parent
deck_dir = base_dir / "images" / "decks"

# ================= HIGH-END POP-UP DIALOG MODAL =================
@st.dialog("📷 Venue Preview", width="large")
def show_photo_modal(venue_name, desc, img_name):
    st.markdown(f"<h2 style='color: #002366; margin-top:0px;'>{venue_name}</h2>", unsafe_allow_html=True)
    st.write(desc)
    
    venue_img_path = deck_dir / img_name
    if venue_img_path.exists():
        # native zoom enabled
        st.image(str(venue_img_path), use_container_width=True)
        st.caption("🔍 *Tip: Double-click or open image options in top right to zoom in detail!*")
    else:
        st.info(f"📷 Upload photo file named **'{img_name}'** to your `images/decks/` folder on GitHub!")


# Select Deck View
st.markdown("<div class='rc-card'>📷 <strong>Interactive Deck Plan:</strong> Tap on any hotspot or camera icon across the deck to open venue photos immediately in a pop-up viewer!</div>", unsafe_allow_html=True)

selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16], value=5)

# ================= DECK 5 =================
if selected_deck == 5:
    st.markdown("<h3 style='color: #00E5FF;'>Deck 5 — Royal Promenade & Central Hub</h3>", unsafe_allow_html=True)
    
    # Coordinates mapped for mobile view
    hotspots_deck5 = {
        "🍕 Sorrento's Pizza": {
            "x_min": 50, "x_max": 180, 
            "y_min": 620, "y_max": 750,
            "desc": "Fresh, late-night handcrafted pizza slices on the bustling Royal Promenade!",
            "img": "sorrentos.jpg"
        },
        "🔮 The Pearl": {
            "x_min": 50, "x_max": 180, 
            "y_min": 800, "y_max": 950,
            "desc": "The multi-deck structural masterpiece and photo hotspot in the center of Deck 5.",
            "img": "the_pearl.jpg"
        },
        "🎤 Spotlight Karaoke": {
            "x_min": 50, "x_max": 180, 
            "y_min": 450, "y_max": 580,
            "desc": "Sing your heart out or catch live performances at the Deck 5 lounge.",
            "img": "karaoke.jpg"
        }
    }
    
    possible_deck5 = [
        deck_dir / "deck5_plan.png",
        deck_dir / "deck5_plan.jpg",
        deck_dir / "deck5_plan.jpeg"
    ]
    
    found_deck5 = None
    for p in possible_deck5:
        if p.exists():
            found_deck5 = p
            break

    if found_deck5:
        st.write("👉 **Tap any venue or camera zone on Deck 5:**")
        loaded_img = Image.open(found_deck5)
        
        # Scale for seamless mobile viewing
        max_width = 360
        if loaded_img.width > max_width:
            ratio = max_width / float(loaded_img.width)
            new_height = int(float(loaded_img.height) * ratio)
            display_img = loaded_img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        else:
            display_img = loaded_img

        value = streamlit_image_coordinates(display_img, key="deck5_interactive")
        
        if value is not None:
            click_x = value["x"]
            click_y = value["y"]
            
            # Check for venue click
            clicked_venue = None
            for venue_name, zone in hotspots_deck5.items():
                if zone["x_min"] <= click_x <= zone["x_max"] and zone["y_min"] <= click_y <= zone["y_max"]:
                    clicked_venue = venue_name
                    break
            
            if clicked_venue:
                venue_data = hotspots_deck5[clicked_venue]
                # Trigger instant high-end popup dialog modal!
                show_photo_modal(clicked_venue, venue_data['desc'], venue_data['img'])
            else:
                st.caption(f"📍 Tapped at X: {click_x} | Y: {click_y}")

    else:
        st.warning("📋 Upload 'deck5_plan.png' inside 'images/decks/' folder on GitHub to render deck map.")

# ================= OTHER DECKS =================
elif selected_deck == 16:
    st.markdown("<h3 style='color: #00E5FF;'>Deck 16 — Thrill Island & Sun Deck</h3>", unsafe_allow_html=True)
    
    hotspots_deck16 = {
        "🎢 Category 6 Waterpark": {
            "x_min": 50, "x_max": 200, "y_min": 200, "y_max": 400, 
            "desc": "Record-breaking waterslides and high-speed water thrills!", 
            "img": "waterslides.jpg"
        },
        "🏄‍♂️ FlowRider Surf Simulator": {
            "x_min": 50, "x_max": 200, "y_min": 420, "y_max": 600, 
            "desc": "Catch a wave or watch surfers at the aft of Deck 16.", 
            "img": "flowrider.jpg"
        }
    }
    
    possible_deck16 = [deck_dir / "deck16_plan.png", deck_dir / "deck16_plan.jpg"]
    found_deck16 = next((p for p in possible_deck16 if p.exists()), None)
    
    if found_deck16:
        loaded_img = Image.open(found_deck16)
        max_width = 360
        ratio = max_width / float(loaded_img.width) if loaded_img.width > max_width else 1.0
        display_img = loaded_img.resize((max_width, int(loaded_img.height * ratio)), Image.Resampling.LANCZOS) if ratio != 1.0 else loaded_img

        value = streamlit_image_coordinates(display_img, key="deck16_interactive")
        if value is not None:
            click_x, click_y = value["x"], value["y"]
            for venue_name, zone in hotspots_deck16.items():
                if zone["x_min"] <= click_x <= zone["x_max"] and zone["y_min"] <= click_y <= zone["y_max"]:
                    show_photo_modal(venue_name, zone['desc'], zone['img'])
                    break
    else:
        st.warning("📋 Upload 'deck16_plan.png' to 'images/decks/' to enable Deck 16 view.")
else:
    st.info("Select Deck 5 or 16 from the top slider to inspect interactive camera spots!")
