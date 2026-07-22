import streamlit as st
import pathlib
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# 1. Page Configuration
st.set_page_config(page_title="Legend of the Seas", layout="wide")

# Custom Royal Caribbean High-End Theme
st.markdown("""
    <style>
    /* Dark Ocean Background */
    .stApp {
        background-color: #030C1B;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Top Header Bar */
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

    /* Glassmorphism Navigation Card */
    .rc-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #FFFFFF;
        border-radius: 16px;
        padding: 15px 20px;
        margin-bottom: 15px;
    }
    
    /* Clean up modal padding so image fills pop-up */
    div[data-testid="stDialog"] div[data-testid="stVerticalBlock"] {
        gap: 0px !important;
        padding: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Top Banner Header
st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — DECK EXPLORER</div>", unsafe_allow_html=True)

# Directory references
base_dir = pathlib.Path(__file__).parent
deck_dir = base_dir / "images" / "decks"


# ================= CLEAN PHOTO-ONLY DIALOG MODAL =================
@st.dialog(" ", width="large")
def show_photo_modal(img_name):
    venue_img_path = deck_dir / img_name
    if venue_img_path.exists():
        # Display image directly in modal
        st.image(str(venue_img_path), use_container_width=True)
    else:
        st.info(f"📷 Upload photo named **'{img_name}'** to `images/decks/` on GitHub!")


# Select Deck View
st.markdown("<div class='rc-card'>📷 Tap any <strong>camera icon</strong> or location on the deck map to instantly trigger the photo pop-up window.</div>", unsafe_allow_html=True)

selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16], value=5)


# ================= DECK 5 =================
if selected_deck == 5:
    st.markdown("<h3 style='color: #00E5FF;'>Deck 5 — Royal Promenade & Central Hub</h3>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------------------
    # 📍 PLACING YOUR CAMERA ICONS / HOTSPOTS
    # Simply adjust x_min, x_max, y_min, y_max to place or move icons anywhere on Deck 5!
    # ---------------------------------------------------------------------------------
    hotspots_deck5 = {
        "📷 Sorrento's Pizza": {
            "x_min": 50, "x_max": 180, 
            "y_min": 620, "y_max": 750,
            "img": "sorrentos.jpg"
        },
        "📷 The Pearl": {
            "x_min": 50, "x_max": 180, 
            "y_min": 800, "y_max": 950,
            "img": "the_pearl.jpg"
        },
        "📷 Spotlight Karaoke": {
            "x_min": 50, "x_max": 180, 
            "y_min": 450, "y_max": 580,
            "img": "karaoke.jpg"
        }
    }
    
    # Find Deck 5 image file
    possible_deck5 = [deck_dir / "deck5_plan.png", deck_dir / "deck5_plan.jpg", deck_dir / "deck5_plan.jpeg"]
    found_deck5 = next((p for p in possible_deck5 if p.exists()), None)

    if found_deck5:
        loaded_img = Image.open(found_deck5)
        
        # Scale for phone screens
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
            
            # Check if tap falls inside camera zone
            clicked_venue = None
            for venue_name, zone in hotspots_deck5.items():
                if zone["x_min"] <= click_x <= zone["x_max"] and zone["y_min"] <= click_y <= zone["y_max"]:
                    clicked_venue = venue_name
                    break
            
            if clicked_venue:
                # Triggers instant pure photo pop-up
                show_photo_modal(hotspots_deck5[clicked_venue]['img'])
            else:
                # Live coordinate tracker for placing new camera icons
                st.caption(f"📍 Tapped at X: {click_x} | Y: {click_y}")

    else:
        st.warning("📋 Upload 'deck5_plan.png' inside 'images/decks/' folder on GitHub to display deck map.")


# ================= DECK 16 =================
elif selected_deck == 16:
    st.markdown("<h3 style='color: #00E5FF;'>Deck 16 — Thrill Island</h3>", unsafe_allow_html=True)
    
    hotspots_deck16 = {
        "📷 Category 6 Waterslides": {
            "x_min": 50, "x_max": 200, 
            "y_min": 200, "y_max": 400, 
            "img": "waterslides.jpg"
        },
        "📷 FlowRider Surf Simulator": {
            "x_min": 50, "x_max": 200, 
            "y_min": 420, "y_max": 600, 
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
                    show_photo_modal(zone['img'])
                    break
            else:
                st.caption(f"📍 Tapped at X: {click_x} | Y: {click_y}")
    else:
        st.warning("📋 Upload 'deck16_plan.png' to 'images/decks/' folder.")
