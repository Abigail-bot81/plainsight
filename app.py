import streamlit as st
import time
from google import genai
from PIL import Image

# 1. Page Configuration & Soft Wavy Blue Styling
st.set_page_config(
    page_title="PlainSight",
    page_icon="👁️",
    layout="wide"
)

st.markdown("""
    <style>
    /* Soft organic wavy gradient with gentle blue tones */
    .stApp {
        background: linear-gradient(135deg, #EBF1F5 0%, #D8E3ED 50%, #E6EDF5 100%);
        background-attachment: fixed;
        color: #1E252B;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    h1, h2, h3 {
        color: #12181E;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    /* Royal blue accent button */
    .stButton > button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 0.6rem 1.4rem;
        font-weight: 500;
        border-radius: 6px;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1D4ED8 !important;
    }
    /* Crisp clean cards to layer over the soft background */
    div[data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(203, 213, 225, 0.8);
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
    </style>
""", unsafe_allow_html=True)

# Color mapping dictionary for dynamic styling
category_colors = {
    "Casual / Everyday": "#166534",        # Forest Green
    "Work / Professional": "#1D4ED8",      # Royal Blue
    "Formal / Evening": "#7E22CE",       # Deep Plum / Purple
    "Active / Athleisure": "#0D9488",    # Teal
    "Creative / Statement": "#C2410C"    # Burnt Orange
}

# 2. App Header
st.title("PlainSight")
st.markdown("*Honest perspective. Real clarity.*")
st.write("Upload an outfit photograph to receive a structured breakdown and thoughtful styling guidance.")

st.markdown("---")

# Side-by-side columns (Left: Upload/Image, Right: Analysis)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Target Image")
    
    # Category Tags Selection
    category = st.selectbox(
        "Select Outfit Category",
        ["Casual / Everyday", "Work / Professional", "Formal / Evening", "Active / Athleisure", "Creative / Statement"]
    )
    
    uploaded_file = st.file_uploader("Choose an outfit image", type=["jpg", "jpeg", "png"])
    
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Selected Image ({category})", use_container_width=True)

with col2:
    st.subheader("Analysis & Guidance")
    
    if image is not None:
        if st.button("Reveal the Truth"):
            if "GEMINI_API_KEY" in st.secrets:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                def generate_with_retry(model_name, contents, max_retries=3):
                    for attempt in range(max_retries):
                        try:
                            return client.models.generate_content(model=model_name, contents=contents)
                        except Exception as err:
                            if "503" in str(err) and attempt < max_retries - 1:
                                time.sleep(2 * (attempt + 1))
                                continue
                            raise err

                with st.spinner("Reviewing proportions and styling..."):
                    try:
                        prompt = f"""
                        You are PlainSight, an expert, observant, and discerning style mentor. 
                        Your approach is grounded and completely honest. Celebrate genuine style with appreciation when it works well, and offer constructive guidance when an outfit needs refinement. Never make cynical assumptions.
                        
                        This outfit has been tagged as: {category}. Keep this context in mind when evaluating its purpose and appropriateness.
                        
                        Analyze the image based on these principles:
                        1. The Strengths: Notice what feels natural, balanced, or expressive about the look.
                        2. The Assessment: Evaluate proportions, color flow, and silhouette with clarity in relation to the {category} context.
                        3. Guidance: Provide practical, thoughtful suggestions to elevate or harmonize the outfit.
                        
                        Format your response precisely into these three sections using clear bold headings:
                        - **Strengths**
                        - **Assessment**
                        - **Refinements**
                        """
                        
                        # Updated to use the active model name
                        response = generate_with_retry('gemini-2.5-flash', [image, prompt])
                        
                        accent_color = category_colors.get(category, "#2563EB")
                        
                        st.markdown("---")
                        # Dynamically style the header line color using HTML/CSS inline styling
                        st.markdown(f"<h3 style='color: {accent_color}; border-bottom: 2px solid {accent_color}; padding-bottom: 5px;'>Findings ({category})</h3>", unsafe_allow_html=True)
                        st.write(response.text)
                        
                        st.success("Analysis complete.")
                                
                    except Exception as e:
                        st.error(f"The server is resting momentarily under high volume. Please wait a moment and try again. Details: {e}")
                        
            else:
                st.error("API key configuration is missing in your settings.")
    else:
        st.info("Upload an image on the left and select a category to begin your style review.")
