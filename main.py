import streamlit as st
import pathlib
import base64

# 1. Page Setup & Styling
st.set_page_config(page_title="Legend of the Seas", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0A192F;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
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

st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — DECK EXPLORER</div>", unsafe_allow_html=True)

base_dir = pathlib.Path(__file__).parent
deck_dir = base_dir / "images" / "decks"

def get_image_b64(path):
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def render_deck_page(deck_filename, camera_hotspots):
    """Handles rendering the plan, hotspots, modals, and coordinate finder for ANY deck."""
    deck_plan_path = deck_dir / deck_filename
    deck_b64 = get_image_b64(deck_plan_path)

    if not deck_b64:
        st.warning(f"Please upload `{deck_filename}` inside `images/decks/` on GitHub.")
        return

    pins_html = ""
    popups_html = ""

    for spot in camera_hotspots:
        filename = spot["file"]
        file_path = deck_dir / filename
        file_b64 = get_image_b64(file_path)
        
        if not file_b64:
            continue

        is_video = filename.lower().endswith(".mp4")
        pin_icon = "📹" if is_video else "📷"

        pins_html += f"""
        <div onclick="openModal('{spot['id']}'); event.stopPropagation();"
             style="position: absolute; left: {spot['x']}%; top: {spot['y']}%; transform: translate(-50%, -50%); cursor: pointer; z-index: 100;">
            <div style="background: #00E5FF; color: #000; border: 2px solid #FFFFFF; box-shadow: 0 0 12px rgba(0,229,255,0.9); font-size: 16px; display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 50%;">
                {pin_icon}
            </div>
        </div>
        """

        if is_video:
            media_html = f"""
            <video controls autoplay loop muted playsinline style="max-width: 95vw; max-height: 85vh; border-radius: 8px; box-shadow: 0 0 25px rgba(0,229,255,0.3);">
                <source src="data:video/mp4;base64,{file_b64}" type="video/mp4">
                Your browser does not support video playback.
            </video>
            """
        else:
            media_html = f"""
            <img src="data:image/jpeg;base64,{file_b64}" style="max-width: 95vw; max-height: 90vh; object-fit: contain; border-radius: 8px;" />
            """

        popups_html += f"""
        <div id="{spot['id']}" class="photo-modal" onclick="closeModal('{spot['id']}')" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.95); z-index: 999999; justify-content: center; align-items: center;">
            <span onclick="closeModal('{spot['id']}')" style="position: absolute; top: 20px; right: 25px; color: #FFFFFF; font-size: 40px; font-weight: bold; cursor: pointer; z-index: 1000000;">&times;</span>
            {media_html}
        </div>
        """

    full_html = f"""
    <script>
        function openModal(id) {{
            let modal = document.getElementById(id);
            if (modal) {{
                modal.style.display = 'flex';
                let vid = modal.querySelector('video');
                if (vid) {{ vid.play(); }}
            }}
        }}
        function closeModal(id) {{
            let modal = document.getElementById(id);
            if (modal) {{
                modal.style.display = 'none';
                let vid = modal.querySelector('video');
                if (vid) {{ vid.pause(); }}
            }}
        }}
       
        function showCoords(e) {{
            let rect = e.target.getBoundingClientRect();
            let x = Math.round(((e.clientX - rect.left) / rect.width) * 100);
            let y = Math.round(((e.clientY - rect.top) / rect.height) * 100);
            document.getElementById('coord-box').innerText = '📍 Clicked Location -> "x": ' + x + ', "y": ' + y;
        }}
    </script>
   
    <div id="coord-box" style="background: #002366; color: #00E5FF; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; font-family: sans-serif; font-size: 16px; margin-bottom: 12px; border: 1px solid #00E5FF;">
        📍 Tap anywhere on the deck plan to reveal its exact X and Y coordinates!
    </div>

    <div style="position: relative; width: 100%; max-width: 480px; margin: 0 auto;">
        <img src="data:image/png;base64,{deck_b64}" onclick="showCoords(event)" style="width: 100%; height: auto; border-radius: 12px; display: block; cursor: crosshair;" />
        {pins_html}
    </div>
    {popups_html}
    """

    st.components.v1.html(full_html, height=2200, scrolling=True)


# -----------------------------------------------------------------
# DECK DATA CONFIGURATION (DECKS 2 TO 20)
# -----------------------------------------------------------------
# Simply add your photos/videos into the list for whichever deck they belong to!
deck_data = {
    2: [],
    3: [],
    4: [],
    5: [
        {"id": "sorrentos", "x": 31, "y": 41, "file": "sorrentos.jpg"},
        {"id": "pearl", "x": 30, "y": 51, "file": "the_pearl.jpg"},
        {"id": "pearl_1", "x": 50, "y": 52, "file": "pearl.jpg"},
        {"id": "duck", "x": 40, "y": 62, "file": "the_duck.jpg"},
        {"id": "dog", "x": 51, "y": 60, "file": "dog.jpg"},
        {"id": "wonka", "x": 51, "y": 22, "file": "wonka.mp4"},
    ],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    11: [],
    12: [],
    13: [],
    14: [],
    15: [],
    16: [],
    17: [],
    18: [],
    19: [],
    20: []
}

# Slider from Deck 2 to Deck 20
selected_deck = st.select_slider("Select Deck Level:", options=list(range(2, 21)), value=5)

# Automatic Plan Image Naming: deck2_plan.png, deck3_plan.png, etc.
image_filename = f"deck{selected_deck}_plan.png"
hotspots = deck_data.get(selected_deck, [])

# Render the selected deck page
render_deck_page(image_filename, hotspots)
