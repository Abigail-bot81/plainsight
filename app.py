import time
import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="PlainSight", 
    page_icon="🔍", 
    layout="centered"
)

# Custom CSS styling with your original dropdown styling and color themes
st.markdown("""
    <style>
    .main {
        background-color: #F8FAFC;
    }
    .stApp {
        background-color: #F8FAFC;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    /* Custom styling for selectbox box and dropdown options */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        color: #1E293B;
    }
    </style>
""", unsafe_allow_html=True)

# App Header Section
st.title("PlainSight")
st.markdown("*Honest perspective. Real clarity.*")
st.write("Upload an outfit photograph to receive a structured breakdown and thoughtful styling guidance.")

st.markdown("---")

# Target Image Section
st.subheader("Target Image")

# Your original dropdown component
category = st.selectbox(
    "Select Outfit Category", 
    ["Casual / Everyday", "Business / Formal", "Evening / Special Occasion", "Athleisure"]
)

uploaded_file = st.file_uploader("Choose an outfit image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Selected Outfit", use_container_width=True)

st.markdown("---")

# Analysis Section
st.subheader("Analysis & Guidance")

if st.button("Reveal the Truth"):
    if uploaded_file is None:
        st.warning("Please upload an outfit image first.")
    else:
        loading_placeholder = st.empty()
        
        # Rotating loading messages
        messages = [
            ("Looking and analysing...", "👔"),
            ("Checking the vibe...", "✨"),
            ("Putting it all together...", "🔍"),
        ]
        
        for msg, icon in messages:
            loading_placeholder.markdown(f"""
                <div style="padding: 15px; text-align: center; font-size: 1.1rem; font-weight: 600; color: #2563EB; background: rgba(255,255,255,0.7); border-radius: 8px; margin-bottom: 15px;">
                    {msg} {icon}
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1.2)
            
        loading_placeholder.empty()
        
        # Live Gemini AI Analysis for the uploaded photo
        try:
            client = genai.Client()
            
            prompt = f"""
            Analyze this outfit photo for the category '{category}'. Provide a structured breakdown with:
            1. **Strengths** (What works well)
            2. **Assessment** (Overall fit, proportions, and styling critique)
            3. **Refinements** (Actionable suggestions for improvement)
            Keep the tone honest, insightful, and stylish.
            """
            
            image_part = types.Part.from_bytes(
                data=uploaded_file.getvalue(),
                mime_type=uploaded_file.type
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[prompt, image_part]
            )
            
            # Results Display Area
            st.markdown(f"### Findings ({category})")
            st.markdown(response.text)
            st.success("Analysis complete.")
            
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
