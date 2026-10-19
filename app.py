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
    
    /* Global text color adjustment for readability on dark background */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #F8FAFC !important;
    }

    /* Force all sidebar text and content to be bright white */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"], [data-testid="stSidebarContent"] * {
        color: #F8FAFC !important;
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
""", unsafe_allow_html=True)
