import streamlit as st
import folium
from streamlit_folium import st_folium
import pathlib
import base64
from PIL import Image

st.set_page_config(page_title="Legend of the Seas", layout="wide")

# Dark Royal Caribbean Aesthetic
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

st.markdown("<div class='brand-header'>⚓ LEGEND OF THE SEAS — DECK PLAN</div>", unsafe_allow_html=True)

base_dir = pathlib.Path(__file__).parent
deck_dir = base_dir / "images" / "decks"

def get_b64(path):
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

selected_deck = st.select_slider("Select Deck Level:", options=[5, 8, 16], value=5)

if selected_deck == 5:
    deck_plan_path = deck_dir / "deck5_plan.png"

    if deck_plan_path.exists():
        img = Image.open(deck_plan_path)
        img_w, img_h = img.size

        # -----------------------------------------------------------------
        # CAMERA ICON PLACEMENT: Set exact Y and X on the map image
        # Y is from bottom (0) to top (img_h), X is from left (0) to right (img_w)
        # -----------------------------------------------------------------
        camera_hotspots = [
            {"y": img_h * 0.75, "x": img_w * 0.50, "photo": "sorrentos.jpg"},
            {"y": img_h * 0.50, "x": img_w * 0.50, "photo": "the_pearl.jpg"},
            {"y": img_h * 0.25, "x": img_w * 0.50, "photo": "karaoke.jpg"},
        ]

        # FIXED LINE: crs="Simple" string format
        m = folium.Map(
            crs="Simple",
            bounds=[[0, 0], [img_h, img_w]],
            max_bounds=True,
            zoom_start=-1,
            attributionControl=False,
            zoomControl=False
        )

        # Add Deck Plan image overlay
        folium.RasterLayers.ImageOverlay(
            image=str(deck_plan_path),
            bounds=[[0, 0], [img_h, img_w]]
        ).add_to(m)

        # Custom Camera Icon HTML Pin
        camera_icon_html = """
        <div style="
            background: #00E5FF;
            color: #000;
            border: 2px solid #FFFFFF;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            box-shadow: 0 0 12px rgba(0,229,255,0.9);
            cursor: pointer;">
            📷
        </div>
        """

        # Add camera pins with clean photo-only popup
        for spot in camera_hotspots:
            photo_b64 = get_b64(deck_dir / spot["photo"])
            if not photo_b64:
                continue

            popup_html = f"""
            <div style="text-align:center; margin:-10px;">
                <img src="data:image/jpeg;base64,{photo_b64}" 
                     style="max-width:85vw; max-height:75vh; border-radius:8px; object-fit:contain;" />
            </div>
            """

            icon = folium.DivIcon(html=camera_icon_html, icon_size=(32, 32), icon_anchor=(16, 16))
            popup = folium.Popup(popup_html, max_width=350)
            
            folium.Marker(
                location=[spot["y"], spot["x"]],
                icon=icon,
                popup=popup
            ).add_to(m)

        m.fit_bounds([[0, 0], [img_h, img_w]])

        st_folium(m, width=400, height=700, returned_objects=[])
    else:
        st.warning("Please upload `deck5_plan.png` inside `images/decks/` on GitHub.")
