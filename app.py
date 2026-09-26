import streamlit as st
from google import genai
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image
from io import BytesIO

# 1. Page Configuration & Brand Aesthetic Styling
st.set_page_config(
    page_title="PlainSight",
    page_icon="👁️",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #F7F5F0;
        color: #222222;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    h1, h2, h3 {
        color: #1A1A1A;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    .stButton > button {
        background-color: #6B705C !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border-radius: 4px;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #555A48 !important;
    }
    div[data-testid="stFileUploader"] {
        background-color: #FFFFFF;
        border: 1px dashed #D0CBC3;
        padding: 1.5rem;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. App Header
st.title("PlainSight")
st.markdown("*Absolute clarity. Zero flattery.*")
st.write("Upload a photo of an outfit to receive an unvarnished breakdown and professional style fix.")

st.markdown("---")

uploaded_file = st.file_uploader("Upload an outfit or style photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Target Image for Analysis", use_container_width=True)
    
    if st.button("Reveal the Truth"):
        if "GEMINI_API_KEY" in st.secrets:
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            # Step 1: Expert Text Review
            with st.spinner("Analyzing structural mechanics, facial contrast, and tones..."):
                try:
                    prompt = """
                    You are PlainSight, an objective, highly observant, and straight-talking style analyst. 
                    You do not flatter people falsely. Your job is to strip away polite illusions and tell the unvarnished truth about how this outfit works.
                    
                    Analyze the image based on these strict guidelines:
                    1. Facial Harmony & Undertones: Evaluate facial features and skin undertones.
                    2. Mechanics & Proportions: Review color harmony, silhouette, scale, and cuts.
                    3. Practical Fix: Provide a concrete, actionable correction tailored precisely to this subject.
                    
                    Format your response precisely into these three sections using clear bold headings:
                    - **The Verdict**
                    - **The Reality Check**
                    - **The Fix**
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=[image, prompt]
                    )
                    
                    st.markdown("---")
                    st.markdown("### PlainSight Review")
                    st.write(response.text)
                            
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")

            # Step 2: Visual Correction Generation (Same Subject & Likeness)
            st.markdown("---")
            st.markdown("### Suggested Style Correction (Same Subject)")
            with st.spinner("Generating corrected outfit keeping the same person and likeness..."):
                try:
                    edit_prompt = (
                        "Generate a revised version of this exact photo. Keep the same person's face, skin tone, hair, and likeness completely identical. "
                        "Modify their clothing based on professional style advice: tuck the shirt in cleanly, add a defined waist, "
                        "and update the trousers to well-fitted, dark-toned structured pants to fix the proportions while keeping the background intact."
                    )
                    
                    # Requesting image generation output explicitly using the preview endpoint configuration
                    img_result = client.models.generate_content(
                        model='gemini-3.1-flash-image-preview',
                        contents=[image, edit_prompt],
                        config=GenerateContentConfig(
                            response_modalities=[Modality.TEXT, Modality.IMAGE]
                        )
                    )
                    
                    has_image = False
                    if img_result.candidates and img_result.candidates[0].content.parts:
                        for part in img_result.candidates[0].content.parts:
                            if part.inline_data:
                                corrected_img = Image.open(BytesIO(part.inline_data.data))
                                st.image(corrected_img, caption="PlainSight Corrected Look (Same Person)", use_container_width=True)
                                has_image = True
                                break
                    
                    if not has_image:
                        st.info("The model provided text adjustments. Please check your prompt configuration.")
                        
                except Exception as img_err:
                    st.error(f"Could not render corrected image: {img_err}")
                    
        else:
            st.error("Gemini API key is missing. Please configure 'GEMINI_API_KEY' in your Streamlit secrets settings.")
