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

# Custom Styling & CSS Polish for a Sleek UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    .uploadedFile {
        border-radius: 8px;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. APP HEADER & NAVIGATION
# ==========================================
st.title("✨ PlainSight")
st.write(
    "Upload an outfit photograph to receive an instant, structured styling"
    " breakdown, professional fashion assessment, and tailored wardrobe"
    " recommendations."
)

# Sidebar / Category selection & Advanced Preferences
st.sidebar.header("🎨 Styling Settings")
category = st.sidebar.selectbox(
    "Select Outfit Category",
    [
        "Casual / Everyday",
        "Work / Business Professional",
        "Formal / Evening",
        "Athleisure / Active",
        "Date Night / Social",
    ],
)

style_vibe = st.sidebar.selectbox(
    "Preferred Feedback Tone",
    ["Constructive & Direct", "Encouraging & Chic", "Editorial / High Fashion"],
)

focus_area = st.sidebar.multiselect(
    "Primary Focus Areas",
    ["Color Coordination", "Proportions & Fit", "Accessorizing", "Layering"],
    default=["Color Coordination", "Proportions & Fit"],
)

st.sidebar.divider()
st.sidebar.info(
    "💡 **Pro Tip:** Ensure your photo has clean natural lighting and shows the"
    " full silhouette for the most accurate styling breakdown."
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
  st.markdown(
      f"**Active Category:** `{category}` &nbsp;|&nbsp; **Tone:**"
      f" `{style_vibe}`"
  )

  # Main Action Button
  if st.button("Reveal the Truth", type="primary"):
    with st.spinner(
        "Analyzing fabric texture, color harmony, and silhouette proportions..."
    ):
      # --- PLACEHOLDER FOR YOUR AI/GEMINI VISION CALL ---
      # response = model.generate_content([uploaded_file, f"Analyze this outfit for {category} with a {style_vibe} tone focusing on {focus_area}."])

      # Structured Display Blocks
      st.success("Analysis complete!")

      st.markdown("### 📊 Comprehensive Style Breakdown")

      # Expander 1: Strengths
      with st.expander("✨ Core Strengths & Highlights", expanded=True):
        st.markdown("""
                - **Color Harmony:** The chosen palette complements underlying tone selections effectively without visual friction or clashing.
                - **Silhouette & Balance:** Proportions are well-managed, establishing an approachable, clean, and balanced look.
                - **Contextual Fit:** Aligns neatly with expectations and dress codes for the selected category.
                """)

      # Expander 2: Detailed Assessment
      with st.expander("⭐ Detailed Aesthetic Assessment", expanded=True):
        st.write(
            "The outfit delivers a strong foundational aesthetic. The garment"
            " pairings establish a clear visual narrative, though strategic"
            " adjustments in layering, tailoring, or accessory placement can"
            " elevate the overall impact from standard to statement-level."
        )

      # Expander 3: Actionable Refinements
      with st.expander("🎯 Actionable Refinements", expanded=True):
        st.markdown("""
                - **Anchor the Proportions:** Consider a subtle tuck or structured belt line to accentuate height and define the waist.
                - **Introduce Textural Contrast:** Pairing smooth fabrics with a textured layer (like knitwear, leather, or tailored outerwear) adds immediate depth.
                - **Accessory Focus:** Keep metal accents unified (all gold or all silver) to maintain a cohesive, high-end finish.
                """)

      # Expander 4: Suggested Shopping / Pairings
      with st.expander("🛍️ Recommended Complementary Pieces"):
        st.markdown("""
                - **Footwear:** Structured loafers or clean minimalist leather sneakers.
                - **Outerwear:** Tailored single-breasted blazer or a classic trench coat.
                - **Accents:** Minimalist pendant necklace or structured structured crossbody bag.
                """)

      st.divider()

      # Download Report Section
      report_text = f"""========================================
PLAIN-SIGHT STYLE REPORT
========================================
Category: {category}
Feedback Tone: {style_vibe}
Focus Areas: {', '.join(focus_area)}

[ CORE STRENGTHS ]
- Color Harmony: Solid palette coordination.
- Silhouette & Balance: Well-managed proportions.
- Contextual Fit: Aligns with category expectations.

[ DETAILED ASSESSMENT ]
The outfit delivers a strong foundational aesthetic with clear visual narratives.

[ ACTIONABLE REFINEMENTS ]
- Anchor proportions with a subtle tuck or belt.
- Introduce textural contrast via layering.
- Keep metal accents unified.

Status: Complete and Analyzed.
========================================
"""
      st.download_button(
          label="📥 Download Full Styling Report",
          data=report_text,
          file_name="plainsight_styling_report.txt",
          mime="text/plain",
      )
else:
  # Empty state banner & onboarding guide
  st.info(
      "👆 Please upload an outfit image above to start your instant styling"
      " analysis."
  )

  col_a, col_b = st.columns(2)
  with col_a:
    with st.container():
      st.markdown("### 🚀 What PlainSight Does")
      st.write(
          "PlainSight acts as your personal AI stylist, giving you instant,"
          " constructive feedback on color theory, fit, and wardrobe"
          " enhancements."
      )

  with col_b:
    with st.expander("📖 How It Works", expanded=True):
      st.markdown("""
            1. **Upload:** Drop your outfit picture above (JPEG or PNG).
            2. **Configure:** Pick your category and preferred feedback tone in the sidebar.
            3. **Reveal:** Hit **Reveal the Truth** to instantly unlock professional fashion insights.
            """)
