import streamlit as st
import time
from google import genai
from PIL import Image

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
st.markdown("*Honest style guidance. Zero pretense.*")
st.write("Upload a photo of an outfit to receive a balanced, discerning review and supportive style advice.")

st.markdown("---")

uploaded_file = st.file_uploader("Upload an outfit or style photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Target Image for Analysis", use_container_width=True)
    
    if st.button("Reveal the Truth"):
        if "GEMINI_API_KEY" in st.secrets:
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            # Helper function with automatic retry for traffic spikes
            def generate_with_retry(model_name, contents, max_retries=3):
                for attempt in range(max_retries):
                    try:
                        return client.models.generate_content(model=model_name, contents=contents)
                    except Exception as err:
                        if "503" in str(err) and attempt < max_retries - 1:
                            time.sleep(2 * (attempt + 1))
                            continue
                        raise err

            # Balanced Fashion Mentor Review
            with st.spinner("Analyzing the look, vibe, and proportions..."):
                try:
                    prompt = """
                    You are PlainSight, an expert, sophisticated, and discerning fashion stylist. 
                    Your philosophy is simple: celebrate great style warmly when it is earned, be completely honest when an outfit fails, but always offer guidance with empathy, kindness, and respect. Never make cynical assumptions (like calling fresh streetwear or modern youth style "hand-me-downs").
                    
                    Analyze the image based on these guidelines:
                    1. The Vibe & Strengths: Highlight what works. If the outfit has a cool energy, intentional proportions, or modern flair, give it genuine, well-deserved compliments.
                    2. The Honest Assessment: Evaluate silhouette, color coordination, and fit with fairness and clarity.
                    3. The Guidance: If the look is stellar, explain how to accessorize it further. If it needs help, offer gentle, constructive, and practical adjustments.
                    
                    Format your response precisely into these three sections using clear bold headings:
                    - **The Vibe & Highlights**
                    - **The Honest Breakdown**
                    - **Style Suggestions**
                    """
                    
                    response = generate_with_retry('gemini-3.8-flash', [image, prompt])
                    
                    st.markdown("---")
                    st.markdown("### PlainSight Review")
                    st.write(response.text)
                    
                    st.success("Style analysis complete!")
                            
                except Exception as e:
                    st.error(f"The server is experiencing high demand right now. Please wait a moment and click 'Reveal The Truth' again. Details: {e}")
                    
        else:
            st.error("Gemini API key is missing. Please configure 'GEMINI_API_KEY' in your Streamlit secrets settings.")
