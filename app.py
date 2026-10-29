import base64
from io import BytesIO
from PIL import Image
import time
import requests
import streamlit as st

# Page Configuration
st.set_page_config(page_title="PlainSight", page_icon="🔍", layout="centered")

# Custom CSS styling with dark blue gradient background and light text
st.markdown(
    """
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

    /* Global text color adjustment for main app */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #F8FAFC !important;
    }

    /* Force file uploader text and instructions to be dark and high-contrast */
    [data-testid="stFileUploader"] *, [data-testid="stFileUploader"] span, 
    [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] div, 
    [data-testid="stFileUploader"] label {
        color: #0F172A !important;
        font-weight: 600 !important;
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

    /* Assessment Card Theme (Gold) */
    .card-assessment {
        background-color: #FEF08A;
        border: 1px solid #FDE047;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: #713F12 !important;
    }
    .header-assessment {
        color: #713F12 !important;
        font-weight: 700;
        font-size: 1.1rem;
        margin-top: 0px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State for History Log
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar for Outfit History Log & Session Export
with st.sidebar:
    st.header("📂 Outfit History Log")
    st.write("Review previous analyses from this session.")

    if not st.session_state.history:
        st.info("No past analyses yet. Upload an outfit to start your log!")
    else:
        session_export_markdown = "# PlainSight - Complete Session Styling Report\n\n"
        for item in st.session_state.history:
            session_export_markdown += (
                f"## Category: {item['category']} (Time: {item['time']})\n\n"
                f"{item['text']}\n\n---\n\n"
            )

        st.download_button(
            label="📥 Download Session Report",
            data=session_export_markdown,
            file_name="plainsight_complete_session_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
        st.markdown("---")

        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{item['category']} ({item['time']})"):
                st.image(item["image"], use_container_width=True)
                st.markdown(item["text"])
                
    st.markdown("---")
    st.header("ℹ️ About PlainSight")
    st.markdown(
        """
        **PlainSight** is an AI-powered styling companion designed to evaluate outfit photos and provide instant, objective analysis.
        
        ### How it works:
        1. **Select** your target dress category.
        2. **Upload** a clear, full-length photo.
        3. **Analyze** to review visual color matching, fit proportions, and style accents.
        
        *Your uploads are processed privately and are never stored permanently.*
        """
    )

# Display Logo
try:
    st.image("PlainSight logo.png", width=200)
except Exception:
    st.title("🔍 PlainSight")

st.markdown(
    "<p style='color: #F8FAFC; font-weight: 600;'>Upload an outfit photograph to receive a structured styling breakdown.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Target Image Section
st.subheader("Target Image")

category = st.selectbox(
    "Select Outfit Category",
    ["Casual / Everyday", "Business / Formal", "Evening / Special Occasion", "Athleisure"],
)

st.markdown(
    '<p style="color: #F8FAFC; font-weight: 600; margin-bottom: 0.5rem;">Choose an outfit image</p>',
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file is not None:
    st.image(uploaded_file, caption="Selected Outfit", use_container_width=True)
    st.markdown("---")

    if st.button("Analyze Outfit"):
        with st.spinner("Analyzing your style details... Please hold."):
            api_key = st.secrets.get("OPENROUTER_API_KEY", None)
            
            if not api_key:
                st.error("⚠️ OPENROUTER_API_KEY not found in Streamlit Secrets.")
            else:
                try:
                    # Compress image to save bandwidth
                    img = Image.open(uploaded_file)
                    img.thumbnail((800, 800))
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    img_byte_arr = BytesIO()
                    img.save(img_byte_arr, format="JPEG")
                    base64_image = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

                    # Fast, free vision model route via OpenRouter
                    model_name = "google/gemini-flash-1.5-8b:free"
                    
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model": model_name,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"Analyze this outfit photo for the category '{category}'. Provide detailed feedback on what works well and what could be improved. Break your answer down with clean, bulleted summaries."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }
                        ]
                    }

                    response = requests.post("https://openrouter.ai", headers=headers, json=payload, timeout=45)
                    
                    if response.status_code == 200:
                        result_json = response.json()
                        raw_text = result_json["choices"]["message"]["content"]
                        
                        st.subheader("Analysis Results")
                        st.markdown(
                            f'<div class="card-assessment">'
                            f'<div class="header-assessment">🔍 Style Breakdown</div>'
                            f'{raw_text}'
                            f'</div>', 
                            unsafe_allow_html=True
                        )

                        timestamp = time.strftime("%H:%M")
                        st.session_state.history.append({
                            "category": category,
                            "time": timestamp,
                            "image": uploaded_file,
                            "text": raw_text
                        })
                        st.rerun()
                    else:
                        st.error(f"API Error (Status {response.status_code}): {response.text}")

                except Exception as e:
                    st.error(f"Execution Error: {e}")
