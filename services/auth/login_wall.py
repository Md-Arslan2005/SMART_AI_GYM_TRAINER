import streamlit as st
import re
from services.persistence.exercise_repository import get_or_create_user

def render_login_wall():
    # 1. Quick Auth Check
    if st.session_state.get("user_id") is not None:
        return True
    
    # 2. UI Styling Injection
    st.markdown("""
        <style>
            /* App-wide background override */
            .stApp {
                background: linear-gradient(135deg, #090d16 0%, #151f32 100%) !important;
                color: #f8fafc !important;
                font-family: 'AdobeClean', sans-serif !important;
            }

            /* Main Login Card Transformation */
            div[data-testid="stForm"] {
                max-width: 460px;
                margin: 10vh auto 20px auto;
                padding: 2.5rem !important;
                border-radius: 24px !important;
                background: rgba(30, 41, 59, 0.4) !important;
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4) !important;
            }

            /* Custom Typography & Spacing */
            .login-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            .login-title {
                font-size: 1.8rem;
                font-weight: 800;
                letter-spacing: -0.025em;
                background: linear-gradient(90deg, #38bdf8, #34d399);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            }
            .login-subtitle {
                font-size: 0.95rem;
                color: #94a3b8;
            }

            /* Form Input Enhancements */
            div[data-testid="stTextInput"] label {
                color: #cbd5e1 !important;
                font-weight: 500 !important;
                margin-bottom: 0.5rem;
            }
            div[data-testid="stTextInput"] input {
                border-radius: 12px !important;
                padding: 0.75rem 1rem !important;
                background-color: rgba(15, 23, 42, 0.6) !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                transition: all 0.2s ease;
            }
            div[data-testid="stTextInput"] input:focus {
                border-color: #34d399 !important;
                box-shadow: 0 0 0 2px rgba(52, 211, 153, 0.2) !important;
            }

            /* High-Performance Submit Button */
            div[data-testid="stFormSubmitButton"] > button {
                width: 100%;
                border-radius: 12px !important;
                background: linear-gradient(90deg, #10b981, #059669) !important;
                color: #ffffff !important;
                font-weight: 700 !important;
                letter-spacing: 0.025em;
                border: none !important;
                padding: 0.8rem 1.5rem !important;
                margin-top: 0.5rem;
                transition: all 0.2s ease-in-out !important;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
            }
            div[data-testid="stFormSubmitButton"] > button:hover {
                background: linear-gradient(90deg, #059669, #047857) !important;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
            }

            /* Theme-matching Glassmorphic Error Container */
            div[data-testid="stNotification"] {
                background: rgba(239, 68, 68, 0.15) !important;
                border: 1px solid rgba(239, 68, 68, 0.25) !important;
                color: #fca5a5 !important;
                border-radius: 12px !important;
                padding: 0.75rem !important;
            }
            div[data-testid="stNotification"] svg {
                color: #ef4444 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # 3. Form Setup Layout
    with st.form("login_form", clear_on_submit=False):
        st.markdown(
            """
            <div class="login-header">
                <div class="login-title">🏋️‍♂️ SMART AI GYM TRAINER</div>
                <div class="login-subtitle">Enter your details to synchronize your training dashboard.</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        username_input = st.text_input("Username", placeholder="e.g., Arslan2005")
        
        # Dedicated container so alert states render *inside* the card structure
        error_placeholder = st.empty()
        
        submit_button = st.form_submit_button("Launch Workspace")

    # 4. Input Validation & Action Handling
    if submit_button:
        username = username_input.strip()
        
        # Guardrail A: Empty Validation
        if not username:
            error_placeholder.error("Username cannot be empty.")
            return False
            
        # Guardrail B: Length Limitations (Prevents DB text overflow execution errors)
        if len(username) < 3 or len(username) > 18:
            error_placeholder.error("Username must be between 3 and 18 characters.")
            return False
            
        # Guardrail C: Character Sanitization (Prevents corrupt database string injections)
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            error_placeholder.error("Characters allowed: Letters, numbers, hyphens, and underscores.")
            return False
        
        try:
            user = get_or_create_user(username)
            st.session_state["user_id"] = user["id"]
            st.session_state["username"] = user["username"]
            st.rerun()
        except Exception as e:
            error_placeholder.error(f"Database connection offline. Try again shortly.")
            return False

    return False