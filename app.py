import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PlainSight",
    page_icon="✨",
    layout="centered"
)

# ==========================================
# APP HEADER & LAYOUT
# ==========================================
st.title("✨ PlainSight")
st.write("Upload an outfit photograph to receive a structured styling breakdown instantly.")

# Sidebar / Category selection
st.sidebar.header("Settings")
category = st.sidebar.selectbox(
    "Select Outfit Category",
    ["Casual / Everyday", "Work / Business", "Formal"]
)

st.divider()

# ==========================================
# FILE UPLOAD & PROCESSING
# ==========================================
uploaded_file = st.file_uploader("Choose an outfit image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display original preview
    st.image(uploaded_file, caption="Selected Outfit", use_container_width=True)
    
    st.write(f"**Active Category:** {category}")
    
    if st.button("Reveal the Truth", type="primary"):
        with st.spinner("Analyzing outfit..."):
            
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
                st.write("The outfit successfully delivers a solid foundational aesthetic. With minor tweaks, it can transition seamlessly to high-impact style.")
                
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
                mime="text/plain"
            )
else:
    st.info("Please upload an image above to start your styling analysis.")
