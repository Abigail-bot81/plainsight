from PIL import Image
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PlainSight", page_icon="✨", layout="centered"
)

# ==========================================
# 2. IMAGE OPTIMIZATION FOR SPEED
# ==========================================


def optimize_uploaded_image(uploaded_file):
  """Opens an uploaded image, resizes it if it's too large,

  and returns it optimized for fast AI processing.
  """
  img = Image.open(uploaded_file)

  # Convert to RGB if it's in RGBA (PNG transparency) to avoid color errors
  if img.mode in ("RGBA", "P"):
    img = img.convert("RGB")

  # Set a max width/height to keep processing lightning fast (800px)
  max_size = (800, 800)
  img.thumbnail(max_size, Image.Resampling.LANCZOS)

  return img


# ==========================================
# 3. APP HEADER & LAYOUT
# ==========================================
st.title("✨ PlainSight")
st.write(
    "Upload an outfit photograph to receive a structured styling breakdown"
    " instantly."
)

# Sidebar / Category selection
st.sidebar.header("Settings")
category = st.sidebar.selectbox(
    "Select Outfit Category", ["Casual / Everyday", "Work / Business", "Formal"]
)

st.divider()

# ==========================================
# 4. FILE UPLOAD & PROCESSING
# ==========================================
uploaded_file = st.file_uploader(
    "Choose an outfit image", type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
  # Display original preview or process immediately
  st.image(
      uploaded_file, caption="Selected Outfit", use_container_width=True
  )

  # Optimize the image for speed behind the scenes
  processed_image = optimize_uploaded_image(uploaded_file)

  st.write(f"**Active Category:** {category}")

  if st.button("Reveal the Truth", type="primary"):
    with st.spinner("Analyzing outfit with lightning speed..."):
      # --- PLACEHOLDER FOR YOUR AI/GEMINI VISION CALL ---
      # Replace 'processed_image' in your API call below:
      # response = model.generate_content([processed_image, "Analyze this outfit..."])

      # Simulated rapid analysis output
      st.success("Analysis complete!")

      st.subheader(f"Findings ({category})")

      with st.expander("✨ Strengths", expanded=True):
        st.markdown("""
                - **Timeless Color Coordination:** Utilizes a clean, harmonious palette.
                - **Flattering Proportions:** Balanced silhouette that highlights ease of wear.
                - **Effortless Practicality:** Meets modern everyday functionality.
                """)

      with st.expander("⭐ Assessment", expanded=True):
        st.write(
            "The outfit successfully delivers a solid foundational aesthetic."
            " With minor tweaks, it can transition seamlessly to high-impact"
            " style."
        )

      with st.expander("🎯 Refinements", expanded=True):
        st.markdown("""
                - **Define the Waistline:** Apply a subtle tuck to anchor proportions.
                - **Add a Third Piece:** Introduce layering for added texture.
                """)

      # Download report button placeholder
      st.download_button(
          label="📥 Download Styling Report",
          data="PlainSight Style Report Content",
          file_name="plainsight_report.txt",
          mime="text/plain",
      )
else:
  st.info("Please upload an image above to start your styling analysis.")
