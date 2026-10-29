from io import BytesIO
from PIL import Image
import time
from google import genai
from google.genai import types
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
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .stMarkdown {
        color: #F8FAFC !important;
    }

    /* Global text color adjustment for main app */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #F8FAFC !important;
    }

    /* Force file uploader text and instructions to be dark and high-contrast */
    [data-testid="stFileUploader"] *, 
    [data-testid="stFileUploader"] span, 
    [data-testid="stFileUploader"] small, 
    [data-testid="stFileUploader"] div, 
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

    /* Custom Category Box Themes */
    .cat-casual {
        background-color: rgba(238, 242, 255, 0.9);
        color: #4F46E5 !important;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 10px;
        border: 1px solid #C7D2FE;
    }
    .cat-business {
        background-color: rgba(224, 242, 254, 0.9);
        color: #1E3A8A !important;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 10px;
        border: 1px solid #BFDBFE;
    }
    .cat-evening {
        background-color: rgba(254, 243, 199, 0.9);
        color: #581C87 !important;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 10px;
        border: 1px solid #FDE68A;
    }
    .cat-athleisure {
        background-color: rgba(255, 237, 213, 0.9);
        color: #14532D !important;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 10px;
        border: 1px solid #FED7AA;
    }

    /* Strengths Card Theme (Blue) */
    .card-strengths {
        background-color: #DBEAFE;
        border: 1px solid #93C5FD;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: #1E40AF !important;
    }
    .header-strengths {
        color: #1E40AF !important;
        font-weight: 700;
        font-size: 1.1rem;
        margin-top: 0px;
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

    /* Refinements Card Theme (Green) */
    .card-refinements {
        background-color: #BBF7D0;
        border: 1px solid #86EFAC;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: #14532D !important;
    }
    .header-refinements {
        color: #14532D !important;
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
    # Added "About" section matching your design aesthetic
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

# Display Logo (Gracefully handles case where file is missing locally)
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
    [
        "Casual / Everyday",
        "Business / Formal",
        "Evening / Special Occasion",
        "Athleisure",
    ],
)

if category == "Casual / Everyday":
    st.markdown(
        '<div class="cat-casual">✨ Active Category: Casual / Everyday</div>',
        unsafe_allow_html=True,
    )
elif category == "Business / Formal":
    st.markdown(
        '<div class="cat-business">💼 Active Category: Business / Formal</div>',
        unsafe_allow_html=True,
    )
elif category == "Evening / Special Occasion":
    st.markdown(
        '<div class="cat-evening">🌙 Active Category: Evening / Special Occasion</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="cat-athleisure">⚡ Active Category: Athleisure</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<p style="color: #F8FAFC; font-weight: 600; margin-bottom: 0.5rem;">Choose an outfit image</p>',
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader(
    "", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Selected Outfit", use_container_width=True)
    st.markdown("---")

    if st.button("Analyze Outfit"):
        with st.spinner("Analyzing your style... Please hold."):
            # Note: "gemini-2.5-flash" is Google's core, highly efficient multimodal model for production
            target_model = "gemini-2.5-flash"

            api_key = st.secrets.get("GEMINI_API_KEY", None)
            if not api_key:
                st.error("⚠️ GEMINI_API_KEY not found in Streamlit Secrets. Please check your dashboard setup.")
            else:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                Analyze this outfit photo for the category '{category}'. Return your analysis using these exact section headers:
                ### Strengths
                ### Assessment
                ### Refinements
                Keep the content fully detailed, insightful, and professional. Do not include markdown headers other than the requested sections.
                """

                try:
                    # Open image with PIL, resize it to max 800px wide for lightning-fast processing
                    img = Image.open(uploaded_file)
                    img.thumbnail((800, 800))

                    # Save compressed image into bytes buffer
                    img_byte_arr = BytesIO()
                    
                    # Convert to RGB if image is RGBA (PNG with transparency) to avoid JPEG saving issues
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                        
                    img.save(img_byte_arr, format="JPEG")
                    compressed_image_bytes = img_byte_arr.getvalue()

                    image_part = types.Part.from_bytes(
                        data=compressed_image_bytes, mime_type="image/jpeg"
                    )

                    # Execute the model call to process the image and text prompt
                    response = client.models.generate_content(
                        model=target_model,
contents=[image_part, prompt]
)
if response and response.text:
raw_text = response.text
# Parse out individual sections to map them nicely to your custom CSS classes
sections = {"### Strengths": "", "### Assessment": "", "### Refinements": ""}
current_key = None
for line in raw_text.split("\n"):
if line.strip() in sections:
current_key = line.strip()
elif current_key:
sections[current_key] += line + "\n"
# Display styled output cards matching your color design parameters
st.subheader("Analysis Results")
if sections["### Strengths"].strip():
st.markdown(f'✨ Strengths{sections["### Strengths"]}', unsafe_allow_html=True)
if sections["### Assessment"].strip():
st.markdown(f'🔍 Assessment{sections["### Assessment"]}', unsafe_allow_html=True)
if sections["### Refinements"].strip():
st.markdown(f'💡 Refinements{sections["### Refinements"]}', unsafe_allow_html=True)
# Save to session history log
timestamp = time.strftime("%H:%M")
st.session_state.history.append({
"category": category,
"time": timestamp,
"image": uploaded_file,
"text": raw_text
})
st.rerun()
else:
st.error("Could not obtain text back from the analysis engine.")
except Exception as e:
st.error(f"An unexpected error occurred during execution: {e}")
