import streamlit as st
import pathlib
import base64

st.set_page_config(page_title="Legend of the Seas", layout="wide")

# Dark Royal Caribbean Theme
st.markdown("""
    <style>
    .stApp { background-color: #030C1B; color: #FFFFFF; }
    .brand-header {
        background: linear-gradient(90deg, #001E4E 0%, #0066CC 100%);
        color: white; padding: 14px 20px; text-align: center;
        font-weight: 800; border-radius: 0 0 16px 16px; margin-top: -60px; margin-bottom: 20px;
        letter-spacing: 2px;
    }
    .rc-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #FFFFFF; border-radius: 16px; padding: 12px 18px; margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — INTERACTIVE DECK PLAN</div>", unsafe_allow_html=True)

# Helper function to encode images so HTML renders them smoothly
def get_image_b64(path):
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

base_dir = pathlib.Path(__file__).parent
deck_dir = base_dir / "images" / "decks"

st.markdown("<div class='rc-card'>📷 <strong>Tap any camera icon</strong> on the deck map to instantly trigger full-screen photo view.</div>", unsafe_allow_html=True)

selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16], value=5)

if selected_deck == 5:
    deck_img_path = deck_dir / "deck5_plan.png"
    
    # -------------------------------------------------------------
    # CAMERA ICON PLACEMENT (% distance x from left, % y from top)
    # -------------------------------------------------------------
    camera_hotspots = [
        {"id": "sorrentos", "x": 45, "y": 25, "photo": "sorrentos.jpg"},
        {"id": "pearl", "x": 45, "y": 50, "photo": "the_pearl.jpg"},
        {"id": "karaoke", "x": 45, "y": 75, "photo": "karaoke.jpg"},
    ]

    deck_b64 = get_image_b64(deck_img_path)

    if deck_b64:
        pins_html = ""
        popups_html = ""
        
        for spot in camera_hotspots:
            photo_b64 = get_image_b64(deck_dir / spot["photo"])
            if not photo_b64:
                continue

            # Camera Icon Hotspot Button
            pins_html += f"""
            <div onclick="document.getElementById('{spot['id']}').style.display='flex'" 
                 style="position: absolute; left: {spot['x']}%; top: {spot['y']}%; transform: translate(-50%, -50%); cursor: pointer; z-index: 10;">
                <div style="background: #00E5FF; color: #000; border: 2px solid white; box-shadow: 0 0 12px rgba(0,229,255,0.9); font-size: 16px; display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 50%;">
                    📷
                </div>
            </div>
            """

            # Full-Screen Photo Modal Overlay (No text, native pinch-zoom on mobile, top-right 'X' button)
            popups_html += f"""
            <div id="{spot['id']}" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.95); z-index: 999999; justify-content: center; align-items: center; touch-action: manipulation;">
                <span onclick="document.getElementById('{spot['id']}').style.display='none'" 
                      style="position: absolute; top: 18px; right: 24px; color: #FFFFFF; font-size: 38px; font-weight: bold; cursor: pointer; z-index: 1000000; font-family: Arial, sans-serif;">&times;</span>
                <img src="data:image/jpeg;base64,{photo_b64}" 
                     style="max-width: 95vw; max-height: 90vh; object-fit: contain; border-radius: 10px; box-shadow: 0 0 30px rgba(255,255,255,0.25);" />
            </div>
            """

        # Interactive Deck Plan Canvas
        full_interactive_html = f"""
        <div style="position: relative; width: 100%; max-width: 480px; margin: 0 auto; user-select: none;">
            <img src="data:image/png;base64,{deck_b64}" style="width: 100%; height: auto; border-radius: 12px; display: block;" />
            {pins_html}
        </div>
        {popups_html}
        """

        # Expanded height from 750 to 1200px to fit full long deck maps!
        st.components.v1.html(full_interactive_html, height=1200, scrolling=True)
    else:
        st.warning("Please verify that `deck5_plan.png` is uploaded in `images/decks/` on GitHub.")
