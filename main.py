import streamlit as st
import pathlib
import base64

# 1. Page Setup & Royal Caribbean Styling
st.set_page_config(page_title="Legend of the Seas", layout="wide")

st.markdown("""
    <style>
    /* Dark Oceanic Theme */
    .stApp {
        background-color: #0A192F;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Top Header Bar */
    .brand-header {
        background: linear-gradient(90deg, #002366 0%, #0073E6 100%);
        color: white;
        padding: 14px 20px;
        text-align: center;
        font-weight: 800;
        border-radius: 0px 0px 16px 16px;
        margin-top: -60px;
        margin-bottom: 20px;
        letter-spacing: 1.5px;
        font-size: 16px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    }

    /* Glassmorphism Card */
    .rc-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #FFFFFF;
        border-radius: 16px;
        padding: 15px 20px;
        margin-bottom: 20px;
    }

    /* Styling for the Photo Dialog Modal */
    div[role="dialog"] {
        background-color: rgba(3, 12, 27, 0.98) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        border-radius: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — DECK EXPLORER</div>", unsafe_allow_html=True)

base_dir = pathlib.Path(__file__).parent
deck_dir = base_dir / "images" / "decks"

# Lightweight Base64 for map ONLY
def get_image_b64(path):
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Pure Photo Dialog Modal (No text, native mobile pinch-zoom, close X button)
@st.dialog(" ")
def view_photo(photo_filename):
    img_path = deck_dir / photo_filename
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)
    else:
        st.warning(f"Upload '{photo_filename}' inside `images/decks/` on GitHub!")

st.markdown("<div class='rc-card'>📷 <strong>Tap any camera icon</strong> directly on the deck plan to view venue photos!</div>", unsafe_allow_html=True)

selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16], value=5)

if selected_deck == 5:
    deck_plan_path = deck_dir / "deck5_plan.png"
    deck_b64 = get_image_b64(deck_plan_path)

    if deck_b64:
        # -------------------------------------------------------------
        # CAMERA ICON PLACEMENT (% distance x from left, % y from top)
        # -------------------------------------------------------------
        camera_hotspots = [
            {"id": "sorrentos", "x": 48, "y": 28, "label": "Sorrento's", "photo": "sorrentos.jpg"},
            {"id": "pearl", "x": 48, "y": 52, "label": "The Pearl", "photo": "the_pearl.jpg"},
            {"id": "karaoke", "x": 48, "y": 76, "label": "Karaoke", "photo": "karaoke.jpg"},
        ]

        # 1. Overlay Camera Pins directly over the Deck Map
        pins_html = ""
        for spot in camera_hotspots:
            pins_html += f"""
            <div style="position: absolute; left: {spot['x']}%; top: {spot['y']}%; transform: translate(-50%, -50%); z-index: 100;">
                <div style="background: #00E5FF; color: #000; border: 2px solid #FFFFFF; box-shadow: 0 0 12px rgba(0,229,255,0.9); font-size: 16px; display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 50%;">
                    📷
                </div>
            </div>
            """

        map_html = f"""
        <div style="position: relative; width: 100%; max-width: 450px; margin: 0 auto;">
            <img src="data:image/png;base64,{deck_b64}" style="width: 100%; height: auto; border-radius: 12px; display: block;" />
            {pins_html}
        </div>
        """
        
        # Display Map
        st.components.v1.html(map_html, height=850, scrolling=False)

        # 2. Touch Hotspot Triggers (Zero-memory crash risk)
        st.markdown("<h4 style='color: #00E5FF; text-align: center; margin-top: -30px;'>📷 Tap to View Location Photo:</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🍕 Sorrento's", key="btn_sorrentos", use_container_width=True):
                view_photo("sorrentos.jpg")
        with col2:
            if st.button("🔮 The Pearl", key="btn_pearl", use_container_width=True):
                view_photo("the_pearl.jpg")
        with col3:
            if st.button("🎤 Karaoke", key="btn_karaoke", use_container_width=True):
                view_photo("karaoke.jpg")

    else:
        st.warning("Please upload `deck5_plan.png` inside `images/decks/` on GitHub.")
