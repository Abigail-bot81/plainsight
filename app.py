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
    }
    .header-strengths {
        color: #1E40AF !important;
        font-weight: 700;
        font-size: 1.1rem;
    }

    /* Assessment Card Theme (Gold) */
    .card-assessment {
        background-color: #FEF08A;
        border: 1px solid #FDE047;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .header-assessment {
        color: #713F12 !important;
        font-weight: 700;
        font-size: 1.1rem;
    }

    /* Refinements Card Theme (Green) */
    .card-refinements {
        background-color: #BBF7D0;
        border: 1px solid #86EFAC;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .header-refinements {
        color: #14532D !important;
        font-weight: 700;
        font-size: 1.1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Helper function to optimize image for lightning-fast AI processing
def optimize_uploaded_image(uploaded_file):
  img = Image.open(uploaded_file)
  if img.mode in ("RGBA", "P"):
    img = img.convert("RGB")
  max_size = (600, 600)
  img.thumbnail(max_size, Image.Resampling.LANCZOS)
  buffered = BytesIO()
  img.save(buffered, format="JPEG", quality=80)
  return buffered.getvalue()


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

# Display the custom PNG Logo Lockup
st.image("PlainSight logo.png", width=200)

st.markdown(
    "<p style='color: #F8FAFC; font-weight: 600;'>Upload an outfit photograph"
    " to receive a structured styling breakdown.</p>",
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
      '<div class="cat-evening">🌙 Active Category: Evening / Special'
      " Occasion</div>",
      unsafe_allow_html=True,
  )
else:
  st.markdown(
      '<div class="cat-athleisure">⚡ Active Category: Athleisure</div>',
      unsafe_allow_html=True,
  )

st.markdown(
    '<p style="color: #F8FAFC; font-weight: 600; margin-bottom: 0.5rem;">Choose'
    " an outfit image</p>",
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader(
    "", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
)

if uploaded_file is not None:
  st.image(uploaded_file, caption="Selected Outfit", use_container_width=True)
  st.markdown("---")

  st.subheader("Analysis & Guidance")

  if st.button("Reveal the Truth"):
    if uploaded_file is None:
      st.warning("Please upload an outfit image first.")
    else:
      # Quick spinner for instant feedback
      with st.spinner("Analyzing outfit..."):
        client = genai.Client()
        prompt = f"""
                Analyze this outfit photo for the category '{category}'. Return your analysis using these exact section headers:
                ### Strengths
                ### Assessment
                ### Refinements
                Keep the content fully detailed, insightful, and professional.
                """

        optimized_image_bytes = optimize_uploaded_image(uploaded_file)
        image_part = types.Part.from_bytes(
            data=optimized_image_bytes, mime_type="image/jpeg"
        )

        try:
          response = client.models.generate_content(
              model="gemini-2.5-flash", contents=[prompt, image_part]
          )
        except Exception as e:
          response = None
          error_message = str(e)

      if response and hasattr(response, "text"):
        analysis_text = response.text

        current_time = time.strftime("%H:%M:%S")
        st.session_state.history.append({
            "category": category,
            "time": current_time,
            "image": uploaded_file.getvalue(),
            "text": analysis_text,
        })

        st.markdown(f"### Findings ({category})")

        chunks = analysis_text.split("###")
        for chunk in chunks:
          if chunk.strip():
            lines = chunk.strip().split("\n", 1)
            title = lines[0].strip().replace("#", "").strip()
            body = lines[1].strip() if len(lines) > 1 else ""

            if title == "Strengths":
              with st.expander(
                  f"✨ {title} (Click to expand/collapse)", expanded=True
              ):
                st.markdown(
                    f"""
                                    <div class="card-strengths">
                                        <div class="header-strengths">{title}</div>
                                    </div>
                                """,
                    unsafe_allow_html=True,
                )
                st.markdown(body)
            elif title == "Assessment":
              with st.expander(
                  f"⭐ {title} (Click to expand/collapse)", expanded=True
              ):
                st.markdown(
                    f"""
                                    <div class="card-assessment">
                                        <div class="header-assessment">{title}</div>
                                    </div>
                                """,
                    unsafe_allow_html=True,
                )
                st.markdown(body)
            elif title == "Refinements":
              with st.expander(
                  f"🎯 {title} (Click to expand/collapse)", expanded=True
              ):
                st.markdown(
                    f"""
                                    <div class="card-refinements">
                                        <div class="header-refinements">{title}</div>
                                    </div>
                                """,
                    unsafe_allow_html=True,
                )
                st.markdown(body)

        st.markdown(
            """
                <div style="display: flex; justify-content: center; margin-top: 30px; margin-bottom: 20px;">
                    <div style="background-color: rgba(226, 232, 240, 0.9); color: #1E293B; font-weight: 600; padding: 10px 24px; border-radius: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                        Analysis complete.
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        report_markdown = (
            f"# PlainSight Styling Report\n\n**Category:**"
            f" {category}\n\n{analysis_text}"
        )
        st.download_button(
            label="📥 Download Styling Report",
            data=report_markdown,
            file_name=(
                "plainsight_report_"
                f"{category.lower().replace('/', '_').strip()}.md"
            ),
            mime="text/markdown",
        )
      else:
        st.error(
            "Unable to connect to the model endpoint. (Details:"
            f" {error_message})"
        )
