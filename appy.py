import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import tempfile
import time

st.set_page_config(page_title="Text to Slides", layout="centered")
st.title("📝 Text-to-Image Slideshow")

# Helper to load a font
def get_font(size=48):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

# Create image from text
def render_text_to_image(text, size=(1280, 720), font_size=48):
    img = Image.new("RGB", size, color="black")
    draw = ImageDraw.Draw(img)
    font = get_font(font_size)

    lines = []
    words = text.split()
    line = ""
    for word in words:
        test_line = line + word + " "
        if draw.textlength(test_line, font=font) > size[0] - 100:
            lines.append(line)
            line = word + " "
        else:
            line = test_line
    lines.append(line)

    y_text = (size[1] - (len(lines) * font_size)) // 2
    for l in lines:
        text_width = draw.textlength(l, font=font)
        x = (size[0] - text_width) // 2
        draw.text((x, y_text), l.strip(), font=font, fill="white")
        y_text += font_size + 10

    return img

# UI
input_text = st.text_area("Enter your story (each line = one slide):", height=300)

if st.button("Generate Slideshow"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        st.info("Generating images...")
        lines = input_text.strip().split('\n')
        for i, line in enumerate(lines):
            if line.strip():
                img = render_text_to_image(line.strip())
                st.image(img, caption=f"Slide {i+1}", use_column_width=True)
                time.sleep(0.5)
