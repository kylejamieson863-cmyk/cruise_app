import streamlit as st
import pathlib
import base64

# 1. Page Config & High-End Royal Caribbean Styling
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
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — DECK EXPLORER</div>", unsafe_allow_html=True)

# Helper function to convert photos for overlay view
def get_image_b64(path):
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

base_dir = pathlib.Path(__file__).parent
deck_dir = base_dir / "images" / "decks"

st.markdown("<div class='rc-card'>📷 <strong>Tap any camera icon</strong> directly on the deck plan to open full-screen venue photos!</div>", unsafe_allow_html=True)

selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16], value=5)

if selected_deck == 5:
    deck_plan_path = deck_dir / "deck5_plan.png"
    deck_b64 = get_image_b64(deck_plan_path)

    if deck_b64:
        # -------------------------------------------------------------
        # CAMERA ICON PLACEMENT (% distance x from left, % y from top)
        # -------------------------------------------------------------
        camera_hotspots = [
            {"id": "sorrentos", "x": 48, "y": 28, "photo": "sorrentos.jpg"},
            {"id": "pearl", "x": 48, "y": 52, "photo": "the_pearl.jpg"},
            {"id": "karaoke", "x": 48, "y": 76, "photo": "karaoke.jpg"},
        ]

        pins_html = ""
        popups_html = ""

        for spot in camera_hotspots:
            photo_b64 = get_image_b64(deck_dir / spot["photo"])
            if not photo_b64:
                continue

            # Camera Icon Pin
            pins_html += f"""
            <div onclick="document.getElementById('{spot['id']}').style.display='flex'" 
                 style="position: absolute; left: {spot['x']}%; top: {spot['y']}%; transform: translate(-50%, -50%); cursor: pointer; z-index: 100;">
                <div style="background: #00E5FF; color: #000; border: 2px solid #FFFFFF; box-shadow: 0 0 12px rgba(0,229,255,0.9); font-size: 16px; display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 50%;">
                    📷
                </div>
            </div>
            """

            # Pure Photo Popup Overlay (No text/titles, top-right 'X' button to close)
            popups_html += f"""
            <div id="{spot['id']}" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.92); z-index: 999999; justify-content: center; align-items: center; touch-action: manipulation;">
                <span onclick="document.getElementById('{spot['id']}').style.display='none'" 
                      style="position: absolute; top: 20px; right: 25px; color: #FFFFFF; font-size: 38px; font-weight: bold; cursor: pointer; z-index: 1000000; font-family: Arial, sans-serif;">&times;</span>
                <img src="data:image/jpeg;base64,{photo_b64}" 
                     style="max-width: 95vw; max-height: 90vh; object-fit: contain; border-radius: 10px; box-shadow: 0 0 30px rgba(255,255,255,0.2);" />
            </div>
            """

        # Interactive Canvas container
        full_interactive_html = f"""
        <div style="position: relative; width: 100%; max-width: 480px; margin: 0 auto;">
            <img src="data:image/png;base64,{deck_b64}" style="width: 100%; height: auto; border-radius: 12px; display: block;" />
            {pins_html}
        </div>
        {popups_html}
        """

        st.components.v1.html(full_interactive_html, height=1000, scrolling=True)
    else:
        st.warning("Please upload `deck5_plan.png` inside `images/decks/` on GitHub.")
