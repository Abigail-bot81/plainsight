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

# Soft background and matching text color mapping for categories
category_styles = {
    "Casual / Everyday": {"bg": "#DCFCE7", "text": "#166534", "border": "#BBF7D0"},       # Soft Green
    "Work / Professional": {"bg": "#DBEAFE", "text": "#1D4ED8", "border": "#BFDBFE"},     # Soft Blue
    "Formal / Evening": {"bg": "#F3E8FF", "text": "#7E22CE", "border": "#E9D5FF"},      # Soft Purple
    "Active / Athleisure": {"bg": "#CCFBF1", "text": "#0F766E", "border": "#99F6E4"},   # Soft Teal
    "Creative / Statement": {"bg": "#FFEDD5", "text": "#C2410C", "border": "#FED7AA"}   # Soft Orange
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
    
    # Get the style dictionary for the selected category
    style = category_styles.get(category, {"bg": "#F1F5F9", "text": "#334155", "border": "#E2E8F0"})
    
    # Render a beautiful pill/badge with the dynamic background color
    st.markdown(f"""
        <div style="background-color: {style['bg']}; color: {style['text']}; border: 1px solid {style['border']}; 
                    padding: 8px 14px; border-radius: 6px; font-weight: 600; font-size: 0.9rem; 
                    margin-bottom: 15px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            Active Tag: {category}
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose an outfit image", type=["jpg", "jpeg", "png"])
    
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

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
                        
                        response = generate_with_retry('gemini-2.5-flash', [image, prompt])
                        
                        st.markdown("---")
                        # Results header styled with the matching background and text color card style
                        st.markdown(f"""
                            <div style="background-color: {style['bg']}; color: {style['text']}; border-left: 4px solid {style['text']}; 
                                        padding: 10px 15px; border-radius: 4px; font-weight: 600; font-size: 1.1rem; margin-bottom: 15px;">
                                Findings ({category})
                            </div>
                        """, unsafe_allow_html=True)
                        st.write(response.text)
                        
                        st.success("Analysis complete.")
                                
                    except Exception as e:
                        st.error(f"The server is resting momentarily under high volume. Please wait a moment and try again. Details: {e}")
                        
            else:
                st.error("API key configuration is missing in your settings.")
    else:
        st.info("Upload an image on the left and select a category to begin your style review.")
