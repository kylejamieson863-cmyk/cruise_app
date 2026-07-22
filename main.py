import streamlit as st
import pathlib
from PIL import Image

# 1. Full Page Setup
st.set_page_config(page_title="Legend of the Seas", layout="wide")

st.markdown("""
    <style>
    /* Premium Royal Caribbean Dark Mode Aesthetic */
    .stApp {
        background-color: #030C1B;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Elegant Top Banner */
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
    }

    .rc-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #FFFFFF;
        border-radius: 16px;
        padding: 12px 18px;
        margin-bottom: 15px;
    }

    /* Style Streamlit Buttons to look like Floating Camera Hotspot Pins */
    div.stButton > button {
        background-color: #00E5FF !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        font-size: 20px !important;
        padding: 0px !important;
        box-shadow: 0 0 15px rgba(0,229,255,0.8) !important;
        margin: auto !important;
        display: block !important;
    }
    div.stButton > button:hover {
        transform: scale(1.15);
        background-color: #FFFFFF !important;
    }

    /* Remove padding around dialog photo modal */
    div[role="dialog"] {
        background-color: rgba(0,0,0,0.95) !important;
        border: none !important;
        padding: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — DECK EXPLORER</div>", unsafe_allow_html=True)

base_dir = pathlib.Path(__file__).parent
deck_dir = base_dir / "images" / "decks"

# ================= PHOTO-ONLY POPUP DIALOG =================
@st.dialog(" ")
def open_photo_popup(photo_filename):
    img_path = deck_dir / photo_filename
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)
    else:
        st.warning(f"Upload '{photo_filename}' to your `images/decks/` folder on GitHub!")


# Select Deck View
st.markdown("<div class='rc-card'>📷 <strong>Tap any camera pin</strong> below to open high-res photos instantly.</div>", unsafe_allow_html=True)

selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16], value=5)

# ================= DECK 5 =================
if selected_deck == 5:
    deck_plan_path = deck_dir / "deck5_plan.png"
    
    if deck_plan_path.exists():
        # Display the Deck 5 Image
        st.image(str(deck_plan_path), use_container_width=True)
        
        st.markdown("<h4 style='color: #00E5FF; text-align: center; margin-top: 10px;'>📷 Tap a Venue Camera Pin:</h4>", unsafe_allow_html=True)
        
        # Position Camera Pins in a clean mobile grid directly underneath
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📷", key="btn_sorrentos"):
                open_photo_popup("sorrentos.jpg")
            st.caption("<div style='text-align: center;'><b>Sorrento's Pizza</b></div>", unsafe_allow_html=True)
            
        with col2:
            if st.button("📷", key="btn_pearl"):
                open_photo_popup("the_pearl.jpg")
            st.caption("<div style='text-align: center;'><b>The Pearl</b></div>", unsafe_allow_html=True)
            
        with col3:
            if st.button("📷", key="btn_karaoke"):
                open_photo_popup("karaoke.jpg")
            st.caption("<div style='text-align: center;'><b>Spotlight Karaoke</b></div>", unsafe_allow_html=True)

    else:
        st.warning("Please upload `deck5_plan.png` inside the `images/decks/` folder on GitHub.")
