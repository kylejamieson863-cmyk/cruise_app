import streamlit as st
import pathlib
import base64

st.set_page_config(page_title="Legend of the Seas", layout="wide")

# Royal Caribbean Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #030C1B; color: #FFFFFF; }
    .brand-header {
        background: linear-gradient(90deg, #001E4E 0%, #0066CC 100%);
        color: white; padding: 14px 20px; text-align: center;
        font-weight: 800; border-radius: 0 0 16px 16px; margin-top: -60px; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — DECK EXPLORER</div>", unsafe_allow_html=True)

base_dir = pathlib.Path(__file__).parent
deck_dir = base_dir / "images" / "decks"

def get_image_b64(path):
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16], value=5)

if selected_deck == 5:
    deck_plan_path = deck_dir / "deck5_plan.png"
    deck_b64 = get_image_b64(deck_plan_path)

    if deck_b64:
        # Camera Icon Positions (% from left, % from top)
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

            # Overlay Camera Pin
            pins_html += f"""
            <div onclick="openModal('{spot['id']}')" 
                 style="position: absolute; left: {spot['x']}%; top: {spot['y']}%; transform: translate(-50%, -50%); cursor: pointer; z-index: 100;">
                <div style="background: #00E5FF; color: #000; border: 2px solid #FFFFFF; box-shadow: 0 0 12px rgba(0,229,255,0.9); font-size: 16px; display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 50%;">
                    📷
                </div>
            </div>
            """

            # Light Modal Popup (Only Photo + Top-Right 'X' Close Button)
            popups_html += f"""
            <div id="{spot['id']}" class="photo-modal" onclick="closeModal('{spot['id']}')" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.95); z-index: 999999; justify-content: center; align-items: center;">
                <span onclick="closeModal('{spot['id']}')" style="position: absolute; top: 20px; right: 25px; color: #FFFFFF; font-size: 40px; font-weight: bold; cursor: pointer; z-index: 1000000;">&times;</span>
                <img src="data:image/jpeg;base64,{photo_b64}" style="max-width: 95vw; max-height: 90vh; object-fit: contain; border-radius: 8px;" />
            </div>
            """

        # HTML Container with auto-calculated height to show 100% of the deck plan
        full_html = f"""
        <script>
            function openModal(id) {{ document.getElementById(id).style.display = 'flex'; }}
            function closeModal(id) {{ document.getElementById(id).style.display = 'none'; }}
        </script>
        <div style="position: relative; width: 100%; max-width: 480px; margin: 0 auto;">
            <img src="data:image/png;base64,{deck_b64}" style="width: 100%; height: auto; border-radius: 12px; display: block;" />
            {pins_html}
        </div>
        {popups_html}
        """

        # Increased height to 1400px so full tall deck map displays without getting cut off
        st.components.v1.html(full_html, height=1400, scrolling=False)
    else:
        st.warning("Please upload `deck5_plan.png` inside `images/decks/` on GitHub.")
