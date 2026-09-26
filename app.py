import streamlit as st
import time
from google import genai
from PIL import Image

# 1. Page Configuration & Natural Aesthetic Styling
st.set_page_config(
    page_title="PlainSight",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
    <style>
    /* Grounded, natural stone and sand tones */
    .stApp {
        background-color: #F5F4F0;
        color: #2F3530;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    h1, h2, h3 {
        color: #384039;
        font-weight: 500;
        letter-spacing: -0.4px;
    }
    /* Muted forest button */
    .stButton > button {
        background-color: #798678 !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 0.6rem 1.4rem;
        font-weight: 400;
        border-radius: 6px;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #637062 !important;
    }
    /* Soft stone container */
    div[data-testid="stFileUploader"] {
        background-color: #FAF9F6;
        border: 1px solid #D9D5CD;
        padding: 1.5rem;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. App Header
st.title("PlainSight")
st.markdown("*Honest perspective. Real clarity.*")
st.write("Upload an outfit photograph to receive a structured breakdown and thoughtful styling guidance.")

st.markdown("---")

# Create side-by-side columns (Left: Upload/Image, Right: Analysis)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Target Image")
    uploaded_file = st.file_uploader("Choose an outfit image", type=["jpg", "jpeg", "png"])
    
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Selected Image", use_container_width=True)

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
                        prompt = """
                        You are PlainSight, an expert, observant, and discerning style mentor. 
                        Your approach is grounded and completely honest. Celebrate genuine style with appreciation when it works well, and offer constructive guidance when an outfit needs refinement. Never make cynical assumptions.
                        
                        Analyze the image based on these principles:
                        1. The Strengths: Notice what feels natural, balanced, or expressive about the look.
                        2. The Assessment: Evaluate proportions, color flow, and silhouette with clarity.
                        3. Guidance: Provide practical, thoughtful suggestions to elevate or harmonize the outfit.
                        
                        Format your response precisely into these three sections using clear bold headings:
                        - **Strengths**
                        - **Assessment**
                        - **Refinements**
                        """
                        
                        response = generate_with_retry('gemini-3.8-flash', [image, prompt])
                        
                        st.markdown("---")
                        st.markdown("### Findings")
                        st.write(response.text)
                        
                        st.success("Analysis complete.")
                                
                    except Exception as e:
                        st.error(f"The server is resting momentarily under high volume. Please wait a moment and try again. Details: {e}")
                        
            else:
                st.error("API key configuration is missing in your settings.")
    else:
        st.info("Upload an image on the left to begin your style review.")
