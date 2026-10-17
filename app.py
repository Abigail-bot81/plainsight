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

# Custom CSS styling including individual section card themes and centered completion message
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
    
    /* Custom Category Box Themes */
    .cat-casual {
        background-color: #EEF2FF;
        color: #4F46E5;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 10px;
        border: 1px solid #C7D2FE;
    }
    .cat-business {
        background-color: #E0F2FE;
        color: #1E3A8A;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 10px;
        border: 1px solid #BFDBFE;
    }
    .cat-evening {
        background-color: #FEF3C7;
        color: #581C87;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 10px;
        border: 1px solid #FDE68A;
    }
    .cat-athleisure {
        background-color: #FFEDD5;
        color: #14532D;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 10px;
        border: 1px solid #FED7AA;
    }

    /* Strengths Card Theme (Blue) */
    .card-strengths {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    .header-strengths {
        color: #1E40AF;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 12px;
        border-bottom: 2px solid #DBEAFE;
        padding-bottom: 6px;
    }

    /* Assessment Card Theme (Gold) */
    .card-assessment {
        background-color: #FEFCE8;
        border: 1px solid #FEF08A;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    .header-assessment {
        color: #854D0E;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 12px;
        border-bottom: 2px solid #FEF9C3;
        padding-bottom: 6px;
    }

    /* Refinements Card Theme (Green) */
    .card-refinements {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    .header-refinements {
        color: #166534;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 12px;
        border-bottom: 2px solid #DCFCE7;
        padding-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header Section
st.title("PlainSight")
st.markdown("*Honest perspective. Real clarity.*")
st.write("Upload an outfit photograph to receive a structured styling breakdown.")

st.markdown("---")

# Target Image Section
st.subheader("Target Image")

# Category selection mapped to your custom styled themes
category = st.selectbox(
    "Select Outfit Category", 
    ["Casual / Everyday", "Business / Formal", "Evening / Special Occasion", "Athleisure"]
)

# Render the active category box with your exact custom colors
if category == "Casual / Everyday":
    st.markdown('<div class="cat-casual">✨ Active Category: Casual / Everyday</div>', unsafe_allow_html=True)
elif category == "Business / Formal":
    st.markdown('<div class="cat-business">💼 Active Category: Business / Formal</div>', unsafe_allow_html=True)
elif category == "Evening / Special Occasion":
    st.markdown('<div class="cat-evening">🌙 Active Category: Evening / Special Occasion</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="cat-athleisure">⚡ Active Category: Athleisure</div>', unsafe_allow_html=True)

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
        
        # Live Gemini AI Analysis
        response = None
        error_message = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                client = genai.Client()
                
                prompt = f"""
                Analyze this outfit photo for the category '{category}'. Return your analysis using these exact section headers:
                ### Strengths
                ### Assessment
                ### Refinements
                
                Keep the content fully detailed, insightful, and professional.
                """
                
                image_part = types.Part.from_bytes(
                    data=uploaded_file.getvalue(),
                    mime_type=uploaded_file.type
                )
                
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=[prompt, image_part]
                )
                break
            except Exception as e:
                error_message = str(e)
                if "503" in error_message or "Unavailable" in error_message:
                    time.sleep(2)
                    continue
                else:
                    break

        if response and hasattr(response, 'text'):
            analysis_text = response.text
            
            st.markdown(f"### Findings ({category})")
            
            # Splitting and rendering the output into distinct color-coded cards
            chunks = analysis_text.split("###")
            
            for chunk in chunks:
                if chunk.strip():
                    lines = chunk.strip().split("\n", 1)
                    title = lines[0].strip().replace("#", "").strip()
                    body = lines[1].strip() if len(lines) > 1 else ""
                    
                    if title == "Strengths":
                        st.markdown(f"""
                            <div class="card-strengths">
                                <div class="header-strengths">{title}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown(body)
                    elif title == "Assessment":
                        st.markdown(f"""
                            <div class="card-assessment">
                                <div class="header-assessment">{title}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown(body)
                    elif title == "Refinements":
                        st.markdown(f"""
                            <div class="card-refinements">
                                <div class="header-refinements">{title}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown(body)
            
            # Centered, grey analysis complete message
            st.markdown("""
                <div style="text-align: center; color: #64748B; font-weight: 500; padding: 20px 0;">
                    Analysis complete.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"The server is experiencing high traffic right now. Please try clicking 'Reveal the Truth' again in a moment. (Details: {error_message})")
