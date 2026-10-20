import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & SETUP
# ==========================================
st.set_page_config(
    page_title="PlainSight - AI Styling Assistant",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom Styling & CSS Polish
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .uploadedFile {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. APP HEADER & NAVIGATION
# ==========================================
st.title("✨ PlainSight")
st.write(
    "Upload an outfit photograph to receive an instant, structured styling"
    " breakdown and professional fashion assessment."
)

# Sidebar / Category selection & Preferences
st.sidebar.header("Styling Settings")
category = st.sidebar.selectbox(
    "Select Outfit Category",
    [
        "Casual / Everyday",
        "Work / Business Professional",
        "Formal / Evening",
        "Athleisure / Active",
    ],
)

style_vibe = st.sidebar.selectbox(
    "Preferred Tone", ["Constructive & Direct", "Encouraging & Chic", "Editorial"]
)

st.sidebar.divider()
st.sidebar.info(
    "💡 **Tip:** Ensure your photo has good natural lighting for the most"
    " accurate color and fit breakdown."
)

st.divider()

# ==========================================
# 3. FILE UPLOAD & PROCESSING ENGINE
# ==========================================
uploaded_file = st.file_uploader(
    "Choose an outfit image", type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
  # Container for visual preview
  col1, col2, col3 = st.columns([1, 6, 1])
  with col2:
    st.image(
        uploaded_file, caption="Selected Outfit Preview", use_container_width=True
    )

  st.write("")
  st.write(
      f"**Active Category:** `{category}` | **Analysis Mode:** `{style_vibe}`"
  )

  # Main Action Button
  if st.button("Reveal the Truth", type="primary"):
    with st.spinner("Analyzing outfit..."):
      # --- PLACEHOLDER FOR YOUR AI/GEMINI VISION CALL ---
      # response = model.generate_content([uploaded_file, f"Analyze this outfit for {category} with a {style_vibe} tone."])

      # Structured Display Blocks
      st.success("Analysis complete!")

      st.markdown("### 📊 Comprehensive Style Breakdown")

      # Expander 1: Strengths
      with st.expander("✨ Core Strengths & Highlights", expanded=True):
        st.markdown("""
                - **Color Harmony:** The palette complements underlying tone selections effectively without visual friction.
                - **Silhouette & Balance:** Proportions are well-managed, creating an approachable and structured look.
                - **Contextual Fit:** Aligns neatly with expectations for the selected category.
                """)

      # Expander 2: Detailed Assessment
      with st.expander("⭐ Detailed Aesthetic Assessment", expanded=True):
        st.write(
            "The outfit delivers a strong foundational aesthetic. The garment"
            " pairings establish a clear visual narrative, though minor"
            " adjustments in layering or accessory placement can elevate the"
            " overall impact from standard to statement-level."
        )

      # Expander 3: Actionable Refinements
      with st.expander("🎯 Actionable Refinements", expanded=True):
        st.markdown("""
                - **Anchor the Proportions:** Consider a subtle tuck or structured belt line to accentuate height.
                - **Introduce Textural Contrast:** Pairing smooth fabrics with a textured layer (like knitwear or tailored outerwear) adds depth.
                - **Accessory Focus:** Keep metal accents unified (all gold or all silver) to maintain a cohesive finish.
                """)

      st.divider()

      # Download Report Section
      report_text = (
          f"PLAIN-SIGHT STYLE REPORT\nCategory: {category}\nTone:"
          f" {style_vibe}\n\nStatus: Complete and Analyzed."
      )
      st.download_button(
          label="📥 Download Full Styling Report",
          data=report_text,
          file_name="plainsight_styling_report.txt",
          mime="text/plain",
      )
else:
  # Empty state banner
  st.info(
      "👆 Please upload an image above to start your instant styling analysis."
  )

  # Quick feature breakdown for first-time visitors
  with st.expander("How PlainSight Works"):
    st.markdown("""
        1. **Upload:** Drop your outfit picture above (JPEG or PNG).
        2. **Configure:** Pick your category and preferred feedback tone in the sidebar.
        3. **Reveal:** Hit **Reveal the Truth** to instantly get structured feedback on strengths, assessments, and actionable refinements.
        """)
