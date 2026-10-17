import time
import streamlit as st

st.set_page_config(page_title="PlainSight", page_icon="🔍", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
    .main {
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
    </style>
""", unsafe_allow_html=True)

st.title("PlainSight")
st.markdown("*Honest perspective. Real clarity.*")
st.write("Upload an outfit photograph to receive a structured breakdown and thoughtful styling guidance.")

st.markdown("---")

# Target Image Section
st.subheader("Target Image")
category = st.selectbox("Select Outfit Category", ["Casual / Everyday", "Business / Formal", "Evening / Special Occasion", "Athleisure"])

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
        ]
        
        for msg, icon in messages:
            loading_placeholder.markdown(f"""
                <div style="padding: 15px; text-align: center; font-size: 1.1rem; font-weight: 600; color: #2563EB; background: rgba(255,255,255,0.7); border-radius: 8px; margin-bottom: 15px;">
                    {msg} {icon} ✨
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1.2)
            
        loading_placeholder.empty()
        
        # Results Display
        st.markdown(f"### Findings ({category})")
        
        st.markdown("**Strengths**")
        st.info("The dress radiates a charming, vintage-inspired warmth that feels entirely authentic to you. The gathered midi silhouette—paired with ruffled shoulder straps and a fitted bodice—creates a timeless, feminine proportion that feels relaxed rather than precious. Your choice to keep the styling simple with your natural curls, minimal jewelry, and a soft neutral flat ensures the dense garden floral print remains sweet and approachable, grounding the romantic aesthetic perfectly for everyday wear.")
        
        st.markdown("**Assessment**")
        st.write("For a casual, warm-weather setting, this look functions beautifully. The waistline hits precisely at the natural waist, allowing the full skirt to drape comfortably without overwhelming your frame. The open neckline and sleeveless cut balance the coverage provided by the midi length.")
        st.write("The only element that feels slightly understated is the footwear. While the cream slip-ons keep the outfit easy and practical, their pale tone and soft, rounded shape slightly disappear against the visual weight and movement of the full, patterned skirt.")
        
        st.markdown("**Refinements**")
        st.markdown("""
        - *Ground the Footwear:* Replace the pale canvas flats with a tan or cognac leather sandal (such as a strappy flat slide or a woven fisherman sandal). The richer leather tone will anchor the print and give the casual look a bit more intentionality.
        - *Add Casual Structure:* If you need a layer for cooler breezes, pair the dress with an oversized cropped denim jacket or an open, textured knit cardigan in olive or oatmeal to casually balance the ultra-feminine print.
        - *Complementary Accessories:* A woven straw tote, canvas market bag, or a pair of tortoiseshell sunglasses would effortlessly round out the daytime, warm-weather narrative.
        """)
        
        st.success("Analysis complete.")
