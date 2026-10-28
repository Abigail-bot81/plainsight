from io import BytesIO
from PIL import Image
import time
from google import genai
from google.genai import types
import streamlit as st

# Page Configuration
st.set_page_config(page_title="PlainSight", page_icon="🔍", layout="centered")

# Custom CSS styling with dark blue gradient background and light text
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
    background-attachment: fixed;
}
.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
    background-attachment: fixed;
}
/* Style the sidebar background to match and force bright white text */
[data-testid="stSidebar"] {
    background-color: #0F172A;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, 
[data-testid="stSidebar"] div, [data-testid="stSidebar"] .stMarkdown {
    color: #F8FAFC !important;
}
/* General app text styling for high contrast on dark blue */
h1, h2, h3, h4, h5, h6, p, span, label {
    color: #F8FAFC !important;
}
/* Style text inputs and selectboxes */
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border-color: #3B82F6 !important;
}
/* Metric styling */
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
    color: #F8FAFC !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Credits and History
if "credits" not in st.session_state:
    st.session_state.credits = 3

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar for Outfit History Log & Credits
with st.sidebar:
    st.header("📂 Outfit History Log")
    st.write("Review previous analyses from this session.")
    st.metric("Remaining Credits", f"🔑 {st.session_state.credits} analyses left")
    
    if st.session_state.history:
        for idx, item in enumerate(st.session_state.history):
            with st.expander(f"Look {idx+1}: {item['category']}"):
                st.image(item["image"], use_container_width=True)
                st.write(item["summary"])
    else:
        st.write("No past analyses yet. Upload an outfit to start your log!")

# Main Application Title and Description
st.title("🔍 PlainSight")
st.markdown("*Upload an outfit photograph to receive a structured styling breakdown.*")

# Category Selection
category = st.selectbox(
    "Select Outfit Category",
    ["Business / Formal", "Casual / Streetwear", "Smart Casual", "Evening / Party", "Athletic / Gym"]
)
st.write(f"💼 **Active Category:** {category}")

# Image Uploader
uploaded_file = st.file_uploader("Choose an outfit image", type=["jpg", "jpeg", "png"])

target_image = None
if uploaded_file is not None:
    target_image = Image.open(uploaded_file)
    st.image(target_image, caption="Selected Outfit", use_container_width=True)

# Analysis Trigger Button
if st.button("Unlock Style Insights"):
    if target_image is not None:
        if st.session_state.credits > 0:
            st.session_state.credits -= 1
            
            with st.spinner("Analyzing outfit structure, color coordination, and styling elements..."):
                try:
                    # Initialize GenAI Client (using standard environment key resolution)
                    client = genai.Client()
                    
                    # Prepare image for Gemini API
                    buffered = BytesIO()
                    target_image.save(buffered, format="JPEG")
                    image_bytes = buffered.getvalue()
                    
                    prompt = f"""
                    You are an elite, high-end fashion stylist and wardrobe consultant. 
                    Analyze the uploaded outfit within the context category: '{category}'.
                    
                    Provide a sharp, constructive, and structured critique covering:
                    1. **Overall Aesthetic & First Impression**: The vibe and immediate impact of the look.
                    2. **Color Palette & Coordination**: How well the colors interact with each other and skin tones.
                    3. **Fit & Proportions**: Silhouette balance, tailoring, and fit.
                    4. **Accessory & Detail Pairing**: Shoes, bags, jewelry, or layering elements.
                    5. **Actionable Recommendations**: 2-3 specific tweaks to elevate or polish the look.
                    
                    Keep the tone professional, chic, and inspiring. Use clear markdown formatting.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[
                            types.Part.from_bytes(
                                data=image_bytes,
                                mime_type='image/jpeg',
                            ),
                            prompt
                        ]
                    )
                    
                    analysis_result = response.text
                    
                    # Display Results
                    st.success("Analysis complete!")
                    st.markdown("### 🎨 Styling Breakdown")
                    st.markdown(analysis_result)
                    
                    # Save to History Log
                    st.session_state.history.append({
                        "category": category,
                        "image": target_image,
                        "summary": analysis_result[:150] + "..."
                    })
                    
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
        else:
            st.error("⚠️ You have run out of free analysis credits for this session.")
    else:
        st.warning("⚠️ Please upload an outfit image before clicking Unlock Style Insights.")
