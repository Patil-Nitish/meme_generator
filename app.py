import os
import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from google import genai
from google.genai import types

# Load Gemini API key securely from Streamlit Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Missing Gemini API key in .streamlit/secrets.toml or Streamlit Cloud settings.")
    st.stop()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Initialize Gemini client
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Gemini client: {e}")
    st.stop()

st.set_page_config(page_title="Gemini Meme Creator", layout="centered")
st.title("🪄 Gemini-powered Meme Creator — Gemini Only (Fixed)")

st.markdown(
    """
Upload an image, and Gemini will describe it in one short caption suitable for a meme.  
This version has no fallback, always uses Gemini, and prevents text from going out of bounds.
"""
)

# ---------------- Options ----------------
model_choice = st.sidebar.selectbox(
    "Model",
    options=["gemini-2.5-flash", "gemini-2.0", "gemini-1.5-pro", "gemini-1.5-mini"],
    index=0,
)
cover_old_text = st.sidebar.checkbox("Cover old text (semi-opaque background)", value=True)

# ---------------- Meme Drawing Utilities ----------------
FONT_PATHS = [
    "Impact.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

def load_font(preferred_paths, size):
    for p in preferred_paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

def _text_size(draw, text, font):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2]-bbox[0], bbox[3]-bbox[1]
    except Exception:
        return font.getsize(text)

def wrap_text_to_width(draw, text, font, max_width):
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for w in words[1:]:
        test = current + " " + w
        tw, _ = _text_size(draw, test, font)
        if tw <= max_width:
            current = test
        else:
            lines.append(current)
            current = w
    lines.append(current)
    return lines

def fit_font_and_wrap(draw, text, preferred_paths, max_width, max_height_fraction, image_height):
    if not text:
        return load_font(preferred_paths, int(image_height*0.06)), []
    for size in range(int(image_height*0.11), 12, -2):
        font = load_font(preferred_paths, size)
        lines = wrap_text_to_width(draw, text, font, max_width)
        total_h = sum(_text_size(draw, ln, font)[1] for ln in lines)
        if total_h <= max_height_fraction * image_height:
            return font, lines
    return load_font(preferred_paths, 12), [text]

def draw_text_on_image_fixed(image, top_text, bottom_text, cover_old=True):
    base = image.convert("RGBA")
    W, H = base.size
    draw = ImageDraw.Draw(base)

    margin = int(W * 0.04)
    max_width = W - 2*margin

    top_font, top_lines = fit_font_and_wrap(draw, top_text.upper(), FONT_PATHS, max_width, 0.28, H)
    bottom_font, bottom_lines = fit_font_and_wrap(draw, bottom_text.upper(), FONT_PATHS, max_width, 0.28, H)

    overlay = Image.new("RGBA", base.size, (255,255,255,0))
    overlay_draw = ImageDraw.Draw(overlay)

    def draw_block(lines, font, top=True):
        total_h = sum(_text_size(draw, ln, font)[1] for ln in lines)
        block_h = total_h + int(font.size*0.4)
        block_w = min(max(_text_size(draw, ln, font)[0] for ln in lines) + int(font.size*0.6), W - 2*margin)
        y = margin if top else H - block_h - margin
        if cover_old:
            overlay_draw.rectangle([(W-block_w)//2, y, (W+block_w)//2, y+block_h], fill=(0,0,0,180))
        y_text = y + int(font.size*0.2)
        for ln in lines:
            w, h = _text_size(draw, ln, font)
            x = (W - w) / 2
            stroke = max(1, int(font.size * 0.06))
            for ox in range(-stroke, stroke+1):
                for oy in range(-stroke, stroke+1):
                    if ox == 0 and oy == 0: continue
                    draw.text((x+ox, y_text+oy), ln, font=font, fill="black")
            draw.text((x, y_text), ln, font=font, fill="white")
            y_text += h + int(font.size*0.05)

    if top_lines:
        draw_block(top_lines, top_font, top=True)
    if bottom_lines:
        draw_block(bottom_lines, bottom_font, top=False)

    composed = Image.alpha_composite(base, overlay)
    return composed.convert("RGB")

# ---------------- Main Logic ----------------
uploaded = st.file_uploader("Upload an image (jpg/png)", type=["jpg", "jpeg", "png"])
user_bottom = st.text_input("Bottom text (optional)")

if st.button("✨ Generate Meme with Gemini"):
    if not uploaded:
        st.warning("Please upload an image first.")
    else:
        raw = uploaded.read()
        pil = Image.open(io.BytesIO(raw)).convert("RGB")

        with st.spinner("Generating caption with Gemini..."):
            mime = uploaded.type if hasattr(uploaded, "type") else "image/jpeg"
            image_part = types.Part.from_bytes(data=raw, mime_type=mime)
            prompt = "Describe this image in one short, funny meme-style caption."
            resp = client.models.generate_content(model=model_choice, contents=[prompt, image_part])
            caption = resp.text.strip() if hasattr(resp, "text") else str(resp)

        meme = draw_text_on_image_fixed(pil, caption, user_bottom, cover_old=cover_old_text)

        st.image(meme, caption="Generated Meme", use_container_width=True)

        buf = io.BytesIO()
        meme.save(buf, format="JPEG")
        st.download_button("📥 Download Meme", buf.getvalue(), "meme.jpg", "image/jpeg")

        st.markdown("---")
        st.markdown(f"**Auto-caption:** {caption}")
