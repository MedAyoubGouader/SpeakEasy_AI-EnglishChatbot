"""
SpeakEasy AI - English Learning Voice Assistant
Professional chatbot with real-time voice input/output
Modern Light Mode Design inspired by PartyRock
With Authentication & Database Integration
"""

import streamlit as st
import os
import tempfile
import base64
from datetime import datetime
from groq import Groq
import edge_tts
import asyncio
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from modules import database as db
import streamlit.components.v1 as components

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="SpeakEasy AI - Learn English",
    page_icon="assets/favicon.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
db.init_db()

# ═══════════════════════════════════════════════════════════════
# LOAD SVG ASSETS AS BASE64
# ═══════════════════════════════════════════════════════════════

def load_svg_as_base64(filepath):
    """Load SVG file and convert to base64 for embedding in HTML."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            svg_content = f.read()
        return base64.b64encode(svg_content.encode()).decode()
    except:
        return None

def get_svg_img_tag(filepath, width="auto", height="auto", style=""):
    """Get an img tag for an SVG file."""
    b64 = load_svg_as_base64(filepath)
    if b64:
        return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}" height="{height}" style="{style}"/>'
    return ""

# Load assets
LOGO_SVG = get_svg_img_tag("assets/logo_animated.svg", width="200", height="50")
BOT_AVATAR = get_svg_img_tag("assets/bot_avatar.svg", width="40", height="40")
USER_AVATAR = get_svg_img_tag("assets/user_avatar.svg", width="40", height="40")
HERO_IMG = get_svg_img_tag("assets/hero_illustration.svg", width="100%", height="auto")

# Animated feature icons
ICON_GRAMMAR = get_svg_img_tag("assets/icon_grammar_animated.svg", width="48", height="48")
ICON_SPEAKING = get_svg_img_tag("assets/icon_speaking_animated.svg", width="48", height="48")
ICON_VOCABULARY = get_svg_img_tag("assets/icon_vocabulary_animated.svg", width="48", height="48")
ICON_LISTENING = get_svg_img_tag("assets/icon_listening_animated.svg", width="48", height="48")

# New animated assets
ROBOT_ANIMATED = get_svg_img_tag("assets/robot_animated.svg", width="100", height="100")
HERO_ANIMATED = get_svg_img_tag("assets/hero_animated.svg", width="350", height="220")
CHAT_ANIMATION = get_svg_img_tag("assets/chat_animation.svg", width="150", height="150")
MIC_ANIMATED = get_svg_img_tag("assets/mic_animated.svg", width="50", height="50")
ROBOT_SPEAKING = get_svg_img_tag("assets/robot_speaking.svg", width="80", height="80")

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS - OCEAN BLUE LIGHT MODE (PARTYROCK STYLE)
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* ═══════════════════════════════════════════════════════════════
       FORCE LIGHT MODE - OVERRIDE STREAMLIT DARK THEME
       ═══════════════════════════════════════════════════════════════ */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    .stApp > header {
        background-color: transparent !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #FFFFFF !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       CSS VARIABLES - OCEAN BLUE PALETTE
       ═══════════════════════════════════════════════════════════════ */
    :root {
        --primary-blue: #2563EB;
        --primary-blue-hover: #1D4ED8;
        --primary-blue-light: #DBEAFE;
        --primary-blue-lighter: #EFF6FF;
        --accent-green: #10B981;
        --accent-green-light: #D1FAE5;
        --accent-orange: #F59E0B;
        --accent-orange-light: #FEF3C7;
        --bg-white: #FFFFFF;
        --bg-cream: #F8FAFC;
        --bg-gray: #F1F5F9;
        --text-dark: #1E293B;
        --text-medium: #334155;
        --text-light: #64748B;
        --text-muted: #94A3B8;
        --border-light: #E2E8F0;
        --border-medium: #CBD5E1;
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-blue: 0 4px 14px rgba(37, 99, 235, 0.25);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
    }

    /* ═══════════════════════════════════════════════════════════════
       GLOBAL STYLES - FORCE LIGHT MODE
       ═══════════════════════════════════════════════════════════════ */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main, .main .block-container, [data-testid="stAppViewContainer"] {
        background: #F8FAFC !important;
        color: #1E293B !important;
    }
    
    /* Force all text to be dark */
    p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: #1E293B !important;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        max-width: 1400px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide Streamlit Multi-Page Navigation - CRITICAL */
    [data-testid="stSidebarNav"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       SIDEBAR - CLEAN WHITE DESIGN WITH DARK TEXT
       ═══════════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: #FFFFFF !important;
        padding-top: 1.5rem;
    }
    
    /* IMPORTANT: All text in sidebar must be dark */
    [data-testid="stSidebar"] * {
        color: var(--text-dark) !important;
    }
    
    [data-testid="stSidebar"] label {
        color: var(--text-medium) !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: var(--text-dark) !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--text-medium) !important;
    }
    
    /* Sidebar select and slider styles */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] label {
        color: var(--text-dark) !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: var(--bg-gray) !important;
        border: 1px solid var(--border-medium) !important;
        color: var(--text-dark) !important;
    }
    
    [data-testid="stSidebar"] .stCheckbox label span {
        color: var(--text-dark) !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stSlider"] label {
        color: var(--text-dark) !important;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: var(--bg-gray) !important;
        color: var(--text-dark) !important;
        border: 1px solid var(--border-medium) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: var(--primary-blue-light) !important;
        border-color: var(--primary-blue) !important;
        color: var(--primary-blue) !important;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 0 1rem 1.5rem 1rem;
        border-bottom: 1px solid var(--border-light);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-section {
        background: var(--bg-gray);
        border-radius: var(--radius-md);
        padding: 1rem;
        margin: 0 0.5rem 1rem 0.5rem;
    }
    
    .sidebar-section-title {
        font-size: 0.75rem;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--primary-blue) !important;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sidebar-section-title svg {
        width: 16px;
        height: 16px;
        stroke: var(--primary-blue) !important;
    }
    
    /* Stat cards in sidebar */
    .stat-card {
        background: var(--bg-gray) !important;
        border: 1px solid var(--border-light);
    }
    
    .stat-card .stat-value {
        color: var(--primary-blue) !important;
        font-weight: 700 !important;
    }
    
    .stat-card .stat-label {
        color: var(--text-medium) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       HEADER SECTION
       ═══════════════════════════════════════════════════════════════ */
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, #3B82F6 100%);
        border-radius: var(--radius-xl);
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: var(--shadow-blue);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: 10%;
        width: 150px;
        height: 150px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }
    
    .header-title {
        color: white;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
    }
    
    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 0.375rem 0.75rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.75rem;
        backdrop-filter: blur(10px);
    }
    
    .header-illustration {
        position: relative;
        z-index: 1;
        max-width: 200px;
    }

    /* ═══════════════════════════════════════════════════════════════
       FEATURE CARDS (Quick Actions)
       ═══════════════════════════════════════════════════════════════ */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .feature-card {
        background: var(--bg-white);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .feature-card:hover {
        border-color: var(--primary-blue);
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    .feature-card-icon {
        margin-bottom: 0.75rem;
    }
    
    .feature-card-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-dark);
        margin: 0;
    }
    
    .feature-card-desc {
        font-size: 0.75rem;
        color: var(--text-light);
        margin: 0.25rem 0 0 0;
    }

    /* ═══════════════════════════════════════════════════════════════
       CHAT CONTAINER
       ═══════════════════════════════════════════════════════════════ */
    .chat-container {
        background: var(--bg-white);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: var(--bg-gray);
        border-radius: 3px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: var(--border-medium);
        border-radius: 3px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }

    /* ═══════════════════════════════════════════════════════════════
       MESSAGE BUBBLES
       ═══════════════════════════════════════════════════════════════ */
    .message-row {
        display: flex;
        margin-bottom: 1rem;
        animation: fadeInUp 0.3s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message-row.user {
        flex-direction: row-reverse;
    }
    
    .message-row.assistant {
        flex-direction: row;
    }
    
    .message-avatar {
        flex-shrink: 0;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    
    .message-row.user .message-avatar {
        margin-left: 0.75rem;
    }
    
    .message-row.assistant .message-avatar {
        margin-right: 0.75rem;
    }
    
    .message-content {
        max-width: 70%;
    }
    
    .message-bubble {
        padding: 0.875rem 1.125rem;
        border-radius: var(--radius-lg);
        line-height: 1.5;
        font-size: 0.9375rem;
    }
    
    .message-row.user .message-bubble {
        background: linear-gradient(135deg, var(--primary-blue) 0%, #3B82F6 100%);
        color: white;
        border-bottom-right-radius: 4px;
        box-shadow: var(--shadow-blue);
    }
    
    .message-row.assistant .message-bubble {
        background: var(--bg-gray);
        color: var(--text-dark);
        border-bottom-left-radius: 4px;
        border: 1px solid var(--border-light);
    }
    
    .message-meta {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.375rem;
        font-size: 0.6875rem;
        color: var(--text-muted);
    }
    
    .message-row.user .message-meta {
        justify-content: flex-end;
    }
    
    .voice-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        background: var(--accent-green-light);
        color: var(--accent-green);
        padding: 0.125rem 0.5rem;
        border-radius: 50px;
        font-size: 0.625rem;
        font-weight: 500;
    }

    /* ═══════════════════════════════════════════════════════════════
       WELCOME STATE
       ═══════════════════════════════════════════════════════════════ */
    .welcome-container {
        text-align: center;
        padding: 3rem 2rem;
    }
    
    .welcome-illustration {
        max-width: 280px;
        margin: 0 auto 1.5rem auto;
    }
    
    .welcome-title {
        font-size: 1.375rem;
        font-weight: 700;
        color: var(--text-dark);
        margin: 0 0 0.5rem 0;
    }
    
    .welcome-subtitle {
        font-size: 0.9375rem;
        color: var(--text-light);
        margin: 0 0 1.5rem 0;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .welcome-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1.5rem;
    }
    
    .welcome-feature {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    
    .welcome-feature-icon {
        width: 48px;
        height: 48px;
        background: var(--primary-blue-light);
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .welcome-feature-text {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-medium);
    }

    /* ═══════════════════════════════════════════════════════════════
       INPUT AREA
       ═══════════════════════════════════════════════════════════════ */
    .input-container {
        background: var(--bg-white);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Streamlit input overrides */
    .stTextInput > div > div > input {
        background: var(--bg-gray) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-dark) !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9375rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 3px var(--primary-blue-light) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       BUTTONS
       ═══════════════════════════════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-blue) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary button style */
    .secondary-btn button {
        background: var(--bg-white) !important;
        color: var(--text-dark) !important;
        border: 1px solid var(--border-light) !important;
    }
    
    .secondary-btn button:hover {
        border-color: var(--primary-blue) !important;
        color: var(--primary-blue) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Success button */
    .success-btn button {
        background: linear-gradient(135deg, var(--accent-green) 0%, #059669 100%) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       QUICK ACTION BUTTONS
       ═══════════════════════════════════════════════════════════════ */
    .quick-actions {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }
    
    .quick-btn {
        background: var(--bg-white);
        border: 1px solid var(--border-light);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        font-size: 0.8125rem;
        font-weight: 500;
        color: var(--text-medium);
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
    }
    
    .quick-btn:hover {
        border-color: var(--primary-blue);
        color: var(--primary-blue);
        background: var(--primary-blue-lighter);
    }

    /* ═══════════════════════════════════════════════════════════════
       STATS CARDS
       ═══════════════════════════════════════════════════════════════ */
    .stats-row {
        display: flex;
        gap: 0.75rem;
        margin-top: 1rem;
    }
    
    .stat-card {
        flex: 1;
        background: var(--bg-gray);
        border-radius: var(--radius-md);
        padding: 0.875rem;
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--primary-blue);
    }
    
    .stat-label {
        font-size: 0.6875rem;
        font-weight: 500;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-top: 0.125rem;
    }

    /* ═══════════════════════════════════════════════════════════════
       LEVEL BADGE
       ═══════════════════════════════════════════════════════════════ */
    .level-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .level-beginner {
        background: var(--accent-green-light);
        color: var(--accent-green);
    }
    
    .level-intermediate {
        background: var(--primary-blue-light);
        color: var(--primary-blue);
    }
    
    .level-advanced {
        background: var(--accent-orange-light);
        color: var(--accent-orange);
    }

    /* ═══════════════════════════════════════════════════════════════
       PLAY BUTTON
       ═══════════════════════════════════════════════════════════════ */
    .play-btn {
        background: var(--accent-green-light);
        color: var(--accent-green);
        border: none;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.75rem;
    }
    
    .play-btn:hover {
        background: var(--accent-green);
        color: white;
    }

    /* ═══════════════════════════════════════════════════════════════
       SELECT & SLIDER OVERRIDES
       ═══════════════════════════════════════════════════════════════ */
    .stSelectbox > div > div {
        background: var(--bg-white) !important;
        border-color: var(--border-light) !important;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-blue), var(--accent-green)) !important;
    }
    
    .stCheckbox > label {
        color: var(--text-medium) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--primary-blue) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       DIVIDERS
       ═══════════════════════════════════════════════════════════════ */
    hr {
        border: none;
        border-top: 1px solid var(--border-light);
        margin: 1.5rem 0;
    }

    /* ═══════════════════════════════════════════════════════════════
       CHAT MESSAGE STREAMLIT OVERRIDE
       ═══════════════════════════════════════════════════════════════ */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       CORRECTION BOX
       ═══════════════════════════════════════════════════════════════ */
    .correction-box {
        background: var(--primary-blue-lighter);
        border-left: 3px solid var(--primary-blue);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        padding: 0.875rem 1rem;
        margin: 0.75rem 0;
        font-size: 0.875rem;
    }
    
    .correction-title {
        font-weight: 600;
        color: var(--primary-blue);
        margin-bottom: 0.375rem;
        display: flex;
        align-items: center;
        gap: 0.375rem;
    }

    /* ═══════════════════════════════════════════════════════════════
       AUTH FORMS
       ═══════════════════════════════════════════════════════════════ */
    div[data-testid="stForm"] {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }
    
    div[data-testid="stForm"] label,
    div[data-testid="stForm"] p,
    div[data-testid="stForm"] h3,
    div[data-testid="stForm"] span {
        color: #1E293B !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       LANDING PAGE STYLES
       ═══════════════════════════════════════════════════════════════ */
    .landing-hero {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 3rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .landing-hero-text {
        flex: 1;
        padding-right: 2rem;
    }

    .landing-hero-text h1 {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        color: #1E293B !important;
        margin-bottom: 1.5rem;
    }

    .landing-hero-text h1 span {
        color: #2563EB !important;
    }

    .landing-hero-text p {
        font-size: 1.25rem;
        color: #64748B !important;
        line-height: 1.6;
        margin-bottom: 2rem;
        max-width: 500px;
    }

    .landing-hero-image {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .features-section {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .features-section h2 {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1E293B !important;
        margin-bottom: 2rem;
    }

    .feature-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-color: #BFDBFE;
    }

    .feature-card h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #1E293B !important;
        margin-top: 1rem;
    }

    /* ═══════════════════════════════════════════════════════════════
       RESPONSIVE - MOBILE FIRST
       ═══════════════════════════════════════════════════════════════ */
    @media (max-width: 992px) {
        .landing-hero {
            flex-direction: column;
            text-align: center;
            padding: 2rem 1rem;
        }

        .landing-hero-text {
            padding-right: 0;
            margin-bottom: 2rem;
        }

        .landing-hero-text h1 {
            font-size: 2.5rem;
        }

        .landing-hero-text p {
            margin-left: auto;
            margin-right: auto;
        }
    }

    @media (max-width: 768px) {
        .features-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .main-header {
            flex-direction: column;
            text-align: center;
            padding: 1.5rem;
        }
        
        .header-title {
            font-size: 1.5rem;
        }
        
        .header-illustration {
            margin-top: 1.5rem;
        }
        
        .welcome-features {
            flex-direction: column;
            gap: 1rem;
        }
        
        .message-content {
            max-width: 85%;
        }

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .landing-hero-text h1 {
            font-size: 2rem;
        }

        .landing-hero-text p {
            font-size: 1rem;
        }
    }

    @media (max-width: 480px) {
        .features-grid {
            grid-template-columns: 1fr;
        }

        .landing-hero-text h1 {
            font-size: 1.75rem;
        }

        .stButton > button {
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for audio control
components.html("""
<script>
    function stopAllAudio() {
        const parentDoc = window.parent.document;
        parentDoc.querySelectorAll('audio').forEach(function(audio) {
            audio.pause();
            audio.currentTime = 0;
        });
    }
    
    setTimeout(function() {
        const parentDoc = window.parent.document;
        parentDoc.addEventListener('click', function(e) {
            const target = e.target;
            const path = e.composedPath();
            for (let el of path) {
                if (el.tagName) {
                    if (el.tagName === 'BUTTON' || 
                        el.tagName === 'SVG' || 
                        el.tagName === 'svg' ||
                        el.tagName === 'path' ||
                        (el.className && el.className.toString().includes('audio'))) {
                        stopAllAudio();
                        break;
                    }
                }
            }
        }, true);
    }, 2000);
</script>
""", height=0)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════

# Check for persistent session via query params
def restore_session():
    """Restore user session from query params if available."""
    params = st.query_params
    if "user_id" in params and "username" in params:
        user_id = int(params["user_id"])
        username = params["username"]
        # Verify user still exists in DB
        convs = db.get_user_conversations(user_id)
        if convs is not None:  # User exists
            st.session_state.auth_status = True
            st.session_state.user = {"id": user_id, "username": username}
            st.session_state.page = "chat"
            if convs:
                st.session_state.current_chat_id = convs[0]['id']
                st.session_state.messages = db.get_conversation_messages(convs[0]['id'])
            else:
                chat_id = db.create_conversation(user_id, f"Chat {datetime.now().strftime('%m/%d %H:%M')}")
                st.session_state.current_chat_id = chat_id
                st.session_state.messages = []
            return True
    return False

if "page" not in st.session_state:
    st.session_state.page = "landing"
if "auth_status" not in st.session_state:
    st.session_state.auth_status = False
if "user" not in st.session_state:
    st.session_state.user = None
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_settings" not in st.session_state:
    st.session_state.voice_settings = {
        "level": "Intermediate",
        "accent": "US",
        "auto_speak": True,
        "correction_enabled": True
    }
if "voice_state" not in st.session_state:
    st.session_state.voice_state = "idle"
if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None
if "session_restored" not in st.session_state:
    st.session_state.session_restored = False

# Restore session on first load
if not st.session_state.session_restored and not st.session_state.auth_status:
    restore_session()
    st.session_state.session_restored = True

# ═══════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def transcribe_audio(audio_bytes):
    """Transcribe audio bytes to text using Google Speech Recognition."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
            f.write(audio_bytes)
            temp_path = f.name
        
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)
        
        os.unlink(temp_path)
        text = recognizer.recognize_google(audio, language='en-US')
        return True, text
        
    except sr.UnknownValueError:
        return False, "I didn't catch that. Please speak more clearly."
    except sr.RequestError as e:
        return False, f"Speech service error: {str(e)}"
    except Exception as e:
        return False, f"Audio error: {str(e)}"


def text_to_speech(text, accent="US"):
    """Convert text to speech using Edge-TTS (Microsoft Natural Voices)."""
    text = text.replace("/", " or ").replace("\\", " or ")
    text = text.replace("**", "").replace("##", "").replace("*", "").replace("#", "")
    text = text.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
    text = text.replace("(", ", ").replace(")", ", ")
    text = text.replace("<", "").replace(">", "").replace("|", " or ")
    text = text.replace("&", " and ").replace("@", " at ").replace("_", " ")
    text = text.replace("~", "").replace("`", "").replace("^", "")
    text = text.replace("+", " plus ").replace("=", " equals ")
    text = text.replace("->", " becomes ").replace("=>", " becomes ")
    text = text.replace("...", ", ").replace("--", ", ").replace("---", ", ")
    
    while "  " in text:
        text = text.replace("  ", " ")
    text = text.strip()
    
    voice_map = {
        "US": "en-US-AriaNeural",
        "UK": "en-GB-SoniaNeural",
        "Australian": "en-AU-NatashaNeural"
    }
    
    voice = voice_map.get(accent, "en-US-AriaNeural")
    
    try:
        async def generate_speech():
            communicate = edge_tts.Communicate(text, voice)
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            await communicate.save(audio_file.name)
            return audio_file.name
        
        audio_path = asyncio.run(generate_speech())
        return audio_path
        
    except Exception as e:
        return None


def get_ai_response(messages, level, correction_enabled, is_voice=False):
    """Get response from Groq AI with strict English-only policy."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    strict_policy = """
CRITICAL RULES - YOU MUST FOLLOW THESE WITHOUT EXCEPTION:
1. ENGLISH ONLY - You ONLY communicate in English
2. TOPIC RESTRICTION - You ONLY discuss English learning topics
3. Be encouraging, helpful, and educational
4. If user speaks another language, respond in English asking them to use English
"""
    
    correction_text = ""
    if correction_enabled:
        correction_text = "If there's a grammar mistake, gently correct it after responding."
    
    level_instructions = {
        "Beginner": "Use SIMPLE vocabulary and short sentences. Be extra encouraging.",
        "Intermediate": "Use moderate vocabulary with some idioms. Include phrasal verbs.",
        "Advanced": "Use rich, sophisticated vocabulary. Include idioms and nuanced expressions."
    }
    
    level_guide = level_instructions.get(level, level_instructions["Intermediate"])

    system_prompt = f"""{strict_policy}

You are SpeakEasy AI, a friendly English tutor.
STUDENT LEVEL: {level}
{level_guide}
{correction_text}
{"VOICE MODE: Be conversational and concise (3-4 sentences)." if is_voice else "TEXT MODE: Be detailed and educational (4-6 sentences)."}
"""

    try:
        # Clean messages for API (only role and content)
        api_messages = [{"role": "system", "content": system_prompt}]
        for m in messages[-10:]:
            api_messages.append({
                "role": m["role"],
                "content": m["content"]
            })
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=api_messages,
            max_tokens=400 if is_voice else 1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


def autoplay_audio(file_path):
    """Create autoplay audio HTML."""
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        st.markdown(
            f'''<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>''',
            unsafe_allow_html=True
        )
        os.unlink(file_path)
    except Exception:
        pass


def get_level_badge_class(level):
    """Return CSS class for level badge."""
    level_classes = {
        "Beginner": "level-beginner",
        "Intermediate": "level-intermediate", 
        "Advanced": "level-advanced"
    }
    return level_classes.get(level, "level-intermediate")


# ═══════════════════════════════════════════════════════════════
# NAVIGATION & AUTH FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def go_to(page):
    st.session_state.page = page
    st.rerun()

def login_user(username, password):
    user_data = db.verify_user(username, password)
    if user_data:
        # Handle tuple from SQLite: (id, username)
        user = {"id": user_data[0], "username": user_data[1]}
        st.session_state.auth_status = True
        st.session_state.user = user
        st.session_state.page = "chat"
        
        # Save session to query params for persistence
        st.query_params["user_id"] = str(user['id'])
        st.query_params["username"] = user['username']
        
        convs = db.get_user_conversations(user['id'])
        if convs:
            st.session_state.current_chat_id = convs[0]['id']
            st.session_state.messages = db.get_conversation_messages(convs[0]['id'])
        else:
            chat_id = db.create_conversation(user['id'], f"Chat {datetime.now().strftime('%m/%d %H:%M')}")
            st.session_state.current_chat_id = chat_id
            st.session_state.messages = []
        st.rerun()
    else:
        st.error("Invalid username or password")

def signup_user(username, password, email):
    try:
        success, msg = db.create_user(username, password, email)
        if success:
            st.success("Account created! Please log in.")
            import time
            time.sleep(1)
            go_to("login")
        else:
            st.error(msg)
    except Exception as e:
        st.error(f"Error: {e}")

def logout():
    st.session_state.auth_status = False
    st.session_state.user = None
    st.session_state.page = "landing"
    st.session_state.messages = []
    st.session_state.current_chat_id = None
    # Clear session params
    st.query_params.clear()
    st.rerun()

def new_chat():
    chat_id = db.create_conversation(st.session_state.user['id'], f"Chat {datetime.now().strftime('%m/%d %H:%M')}")
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = []
    st.rerun()

def load_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = db.get_conversation_messages(chat_id)
    st.rerun()


# ═══════════════════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════════════════

def show_landing_page():
    # Full-width Navbar
    st.markdown(f'''
    <div style="display:flex; justify-content:space-between; align-items:center; padding:1rem 0; margin-bottom:2rem;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
            {LOGO_SVG}
        </div>
        <div id="nav-actions"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([6, 1, 1, 1])
    with nav_col3:
        if st.button("Sign In", key="nav_signin", use_container_width=True):
            go_to("login")
    with nav_col4:
        if st.button("Sign Up", key="nav_signup_btn", use_container_width=True):
            go_to("signup")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hero Section - Full Width
    hero_col1, hero_col2 = st.columns([1.5, 1])
    
    with hero_col1:
        st.markdown(f"""
        <div style="padding-right: 2rem;">
            <h1 style="font-size: 3.5rem; font-weight: 800; color: #1E293B; line-height: 1.1; margin-bottom: 1.5rem;">
                Master English<br><span style="color: #2563EB;">Fluency Today</span>
            </h1>
            <p style="font-size: 1.3rem; color: #64748B; margin-bottom: 2rem; line-height: 1.7; max-width: 600px;">
                Your personal AI tutor for 24/7 conversation practice, grammar correction, and vocabulary building. Start speaking confidently with real-time feedback and adaptive lessons.
            </p>
            <div style="display:flex; gap:1rem; margin-bottom:2rem;">
                <div style="display:flex; align-items:center; gap:0.5rem; color:#10B981; font-size:0.95rem;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                    24/7 Availability
                </div>
                <div style="display:flex; align-items:center; gap:0.5rem; color:#10B981; font-size:0.95rem;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                    Real-time Feedback
                </div>
                <div style="display:flex; align-items:center; gap:0.5rem; color:#10B981; font-size:0.95rem;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                    Voice Enabled
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        cta_col1, cta_col2, _ = st.columns([1, 1, 2])
        with cta_col1:
            if st.button("Get Started Free", key="hero_cta", use_container_width=True):
                go_to("signup")
        with cta_col2:
            if st.button("Learn More", key="hero_learn", use_container_width=True):
                pass
    
    with hero_col2:
        st.markdown(f'''
        <div style="display:flex; justify-content:center; align-items:center; min-height:350px;">
            <div style="transform: scale(1.2);">{HERO_ANIMATED}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown('''
    <div style="background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%); border-radius: 20px; padding: 2.5rem; margin: 2rem 0;">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; text-align: center;">
            <div>
                <div style="font-size: 2.5rem; font-weight: 800; color: white;">10K+</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.95rem;">Active Learners</div>
            </div>
            <div>
                <div style="font-size: 2.5rem; font-weight: 800; color: white;">50+</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.95rem;">Grammar Topics</div>
            </div>
            <div>
                <div style="font-size: 2.5rem; font-weight: 800; color: white;">5000+</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.95rem;">Vocabulary Words</div>
            </div>
            <div>
                <div style="font-size: 2.5rem; font-weight: 800; color: white;">98%</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.95rem;">Satisfaction Rate</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Features Section - Full Width Cards
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; margin-bottom:0.5rem;'>Why Choose SpeakEasy?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748B; margin-bottom:2rem;'>Everything you need to master English fluency</p>", unsafe_allow_html=True)
    
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(f'''
        <div style="text-align:center; padding:2rem 1.5rem; background:white; border-radius:16px; border:1px solid #E2E8F0; min-height:220px; transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="width:60px; height:60px; margin:0 auto 1rem; background:#EFF6FF; border-radius:12px; display:flex; align-items:center; justify-content:center;">
                {ICON_GRAMMAR}
            </div>
            <div style="font-weight:700; font-size:1.1rem; color:#1E293B; margin-bottom:0.5rem;">Grammar Mastery</div>
            <div style="color:#64748B; font-size:0.9rem; line-height:1.5;">Learn rules with context and get instant corrections</div>
        </div>
        ''', unsafe_allow_html=True)
    with f2:
        st.markdown(f'''
        <div style="text-align:center; padding:2rem 1.5rem; background:white; border-radius:16px; border:1px solid #E2E8F0; min-height:220px; transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="width:60px; height:60px; margin:0 auto 1rem; background:#DBEAFE; border-radius:12px; display:flex; align-items:center; justify-content:center;">
                {ICON_SPEAKING}
            </div>
            <div style="font-weight:700; font-size:1.1rem; color:#1E293B; margin-bottom:0.5rem;">Speaking Practice</div>
            <div style="color:#64748B; font-size:0.9rem; line-height:1.5;">Voice conversations with AI-powered feedback</div>
        </div>
        ''', unsafe_allow_html=True)
    with f3:
        st.markdown(f'''
        <div style="text-align:center; padding:2rem 1.5rem; background:white; border-radius:16px; border:1px solid #E2E8F0; min-height:220px; transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="width:60px; height:60px; margin:0 auto 1rem; background:#D1FAE5; border-radius:12px; display:flex; align-items:center; justify-content:center;">
                {ICON_VOCABULARY}
            </div>
            <div style="font-weight:700; font-size:1.1rem; color:#1E293B; margin-bottom:0.5rem;">Vocabulary Builder</div>
            <div style="color:#64748B; font-size:0.9rem; line-height:1.5;">5000+ words organized by CEFR levels</div>
        </div>
        ''', unsafe_allow_html=True)
    with f4:
        st.markdown(f'''
        <div style="text-align:center; padding:2rem 1.5rem; background:white; border-radius:16px; border:1px solid #E2E8F0; min-height:220px; transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="width:60px; height:60px; margin:0 auto 1rem; background:#FEF3C7; border-radius:12px; display:flex; align-items:center; justify-content:center;">
                {ICON_LISTENING}
            </div>
            <div style="font-weight:700; font-size:1.1rem; color:#1E293B; margin-bottom:0.5rem;">Listening Skills</div>
            <div style="color:#64748B; font-size:0.9rem; line-height:1.5;">Train your ear with native accents</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # CTA Section
    st.markdown('''
    <div style="text-align:center; padding:4rem 2rem; margin-top:3rem; background:#F8FAFC; border-radius:20px; border:1px solid #E2E8F0;">
        <h2 style="margin-bottom:1rem;">Ready to Start Your Journey?</h2>
        <p style="color:#64748B; margin-bottom:2rem; max-width:500px; margin-left:auto; margin-right:auto;">
            Join thousands of learners improving their English every day with SpeakEasy AI.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    _, cta_center, _ = st.columns([1.5, 1, 1.5])
    with cta_center:
        if st.button("Create Free Account", key="bottom_cta", use_container_width=True):
            go_to("signup")
    
    # Footer
    st.markdown('''
    <div style="text-align:center; padding:2rem 0; margin-top:3rem; border-top:1px solid #E2E8F0; color:#94A3B8; font-size:0.85rem;">
        SpeakEasy AI - Your English Learning Companion<br>
        <span style="font-size:0.75rem;">Powered by Advanced AI Technology</span>
    </div>
    ''', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════════════════════

def show_login_page():
    # Two column layout: illustration + form
    ill_col, form_col = st.columns([1.2, 1])
    
    with ill_col:
        st.markdown(f'''
        <div style="display:flex; flex-direction:column; justify-content:center; height:100%; padding:2rem;">
            <div style="max-width:350px; margin:0 auto;">
                {HERO_ANIMATED}
            </div>
            <div style="text-align:center; margin-top:2rem;">
                <h3 style="color:#1E293B; margin-bottom:0.5rem;">Welcome to SpeakEasy AI</h3>
                <p style="color:#64748B;">Your journey to English fluency starts here</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with form_col:
        st.markdown(f'''
        <div style="background:white; border-radius:20px; border:1px solid #E2E8F0; padding:2.5rem; box-shadow:0 4px 20px rgba(0,0,0,0.05);">
            <div style="text-align:center; margin-bottom:1.5rem;">
                {LOGO_SVG}
            </div>
            <h3 style="text-align:center; color:#1E293B; margin-bottom:0.25rem;">Welcome Back</h3>
            <p style="text-align:center; color:#64748B; font-size:0.9rem; margin-bottom:1.5rem;">Sign in to continue learning</p>
        </div>
        ''', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            
            if submitted and username and password:
                login_user(username, password)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align:center; color:#64748B; font-size:0.9rem;'>Don't have an account?</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Create Account", use_container_width=True, key="login_create"):
                go_to("signup")
        with c2:
            if st.button("Back Home", use_container_width=True, key="login_home"):
                go_to("landing")


# ═══════════════════════════════════════════════════════════════
# SIGNUP PAGE
# ═══════════════════════════════════════════════════════════════

def show_signup_page():
    # Two column layout: illustration + form
    ill_col, form_col = st.columns([1.2, 1])
    
    with ill_col:
        st.markdown(f'''
        <div style="display:flex; flex-direction:column; justify-content:center; height:100%; padding:2rem;">
            <div style="max-width:350px; margin:0 auto;">
                {ROBOT_ANIMATED}
            </div>
            <div style="text-align:center; margin-top:2rem;">
                <h3 style="color:#1E293B; margin-bottom:0.5rem;">Join SpeakEasy AI</h3>
                <p style="color:#64748B;">Create your free account and start learning today</p>
            </div>
            <div style="display:flex; justify-content:center; gap:1.5rem; margin-top:1.5rem;">
                <div style="text-align:center;">
                    <div style="font-size:1.5rem; font-weight:700; color:#2563EB;">10K+</div>
                    <div style="font-size:0.8rem; color:#64748B;">Learners</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.5rem; font-weight:700; color:#10B981;">24/7</div>
                    <div style="font-size:0.8rem; color:#64748B;">Available</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.5rem; font-weight:700; color:#F59E0B;">Free</div>
                    <div style="font-size:0.8rem; color:#64748B;">To Start</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with form_col:
        st.markdown(f'''
        <div style="background:white; border-radius:20px; border:1px solid #E2E8F0; padding:2.5rem; box-shadow:0 4px 20px rgba(0,0,0,0.05);">
            <div style="text-align:center; margin-bottom:1.5rem;">
                {LOGO_SVG}
            </div>
            <h3 style="text-align:center; color:#1E293B; margin-bottom:0.25rem;">Create Account</h3>
            <p style="text-align:center; color:#64748B; font-size:0.9rem; margin-bottom:1.5rem;">Start your English learning journey</p>
        </div>
        ''', unsafe_allow_html=True)
        
        with st.form("signup_form"):
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="Min 6 characters")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted:
                if username and email and password:
                    if "@" not in email:
                        st.error("Enter a valid email")
                    elif len(password) < 6:
                        st.error("Password must be 6+ characters")
                    elif password != confirm:
                        st.error("Passwords don't match")
                    else:
                        signup_user(username, password, email)
                else:
                    st.error("Fill all fields")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align:center; color:#64748B; font-size:0.9rem;'>Already have an account?</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Sign In", use_container_width=True, key="signup_signin"):
                go_to("login")
        with c2:
            if st.button("Back Home", use_container_width=True, key="signup_home"):
                go_to("landing")


# ═══════════════════════════════════════════════════════════════
# CHAT INTERFACE (THE ORIGINAL BEAUTIFUL ONE)
# ═══════════════════════════════════════════════════════════════

def show_chat_interface():
    # ═══════════════════════════════════════════════════════════════
    # SIDEBAR - PROFESSIONAL DESIGN
    # ═══════════════════════════════════════════════════════════════
    with st.sidebar:
        # Logo Section with gradient background
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%); padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem; text-align: center;">
            <div style="filter: brightness(0) invert(1); margin-bottom: 0.5rem;">
                {LOGO_SVG}
            </div>
            <div style="max-width: 80px; margin: 0 auto;">
                {ROBOT_ANIMATED}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # User Card with avatar
        if st.session_state.user:
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); padding: 1.25rem; border-radius: 16px; margin-bottom: 1.5rem; border: 1px solid #BFDBFE;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1.2rem;">
                        {st.session_state.user['username'][0].upper()}
                    </div>
                    <div>
                        <div style="font-weight: 700; color: #1E293B; font-size: 1rem;">{st.session_state.user['username']}</div>
                        <div style="font-size: 0.8rem; color: #64748B; display: flex; align-items: center; gap: 0.25rem;">
                            <span style="width: 8px; height: 8px; background: #10B981; border-radius: 50%; display: inline-block;"></span>
                            Active now
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # New Chat Button with icon
        st.markdown('''
        <style>
            [data-testid="stSidebar"] [data-testid="baseButton-secondary"][key="new_chat_btn"] {
                background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
                color: white !important;
                border: none !important;
            }
        </style>
        ''', unsafe_allow_html=True)
        
        if st.button("+ New Conversation", use_container_width=True, key="new_chat_btn"):
            new_chat()
        
        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
        
        # Conversation History Section
        st.markdown('''
        <div style="background: #F1F5F9; padding: 0.75rem 1rem; border-radius: 10px; margin-bottom: 0.75rem;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 0.5rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
                Conversations
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        convs = db.get_user_conversations(st.session_state.user['id'])
        if convs:
            for conv in convs[:8]:
                active = st.session_state.current_chat_id == conv['id']
                btn_style = "background: #DBEAFE; border-color: #2563EB;" if active else ""
                if st.button(f"{'▸ ' if active else ''}{conv['title'][:25]}{'...' if len(conv['title']) > 25 else ''}", key=f"conv_{conv['id']}", use_container_width=True):
                    load_chat(conv['id'])
        else:
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; text-align: center; padding: 1rem;'>No conversations yet</p>", unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 1.5rem 0; border-top: 1px solid #E2E8F0;'></div>", unsafe_allow_html=True)
        
        # Settings Sections
        st.markdown('''
        <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #E2E8F0;">
            <div style="font-size: 0.7rem; font-weight: 700; color: #2563EB; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 20V10M18 20V4M6 20v-4"/>
                </svg>
                Proficiency Level
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.session_state.voice_settings["level"] = st.select_slider(
            "Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value=st.session_state.voice_settings["level"],
            label_visibility="collapsed"
        )
        
        level = st.session_state.voice_settings["level"]
        badge_class = get_level_badge_class(level)
        st.markdown(f'<div style="text-align: center; margin: 0.5rem 0 1rem;"><span class="level-badge {badge_class}">{level}</span></div>', unsafe_allow_html=True)
        
        # Voice Settings
        st.markdown('''
        <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #E2E8F0;">
            <div style="font-size: 0.7rem; font-weight: 700; color: #2563EB; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8"/>
                </svg>
                Voice Settings
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.session_state.voice_settings["accent"] = st.selectbox(
            "Accent",
            options=["US", "UK", "Australian"],
            index=["US", "UK", "Australian"].index(st.session_state.voice_settings["accent"]),
            label_visibility="collapsed"
        )
        
        st.session_state.voice_settings["auto_speak"] = st.checkbox(
            "Auto-play responses",
            value=st.session_state.voice_settings["auto_speak"]
        )
        
        st.session_state.voice_settings["correction_enabled"] = st.checkbox(
            "Grammar correction",
            value=st.session_state.voice_settings["correction_enabled"]
        )
        
        st.markdown("<div style='margin: 1.5rem 0; border-top: 1px solid #E2E8F0;'></div>", unsafe_allow_html=True)
        
        # Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear", use_container_width=True, key="clear_btn"):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("Stop", use_container_width=True, key="stop_btn"):
                st.session_state.stop_audio = True
                st.rerun()
        
        st.markdown("<div style='margin: 0.75rem 0;'></div>", unsafe_allow_html=True)
        
        # Logout Button
        if st.button("Log Out", use_container_width=True, key="logout_btn"):
            logout()
        
        # Statistics Cards
        total_msgs = len(st.session_state.messages)
        voice_msgs = sum(1 for m in st.session_state.messages if m.get("voice", False))
        voice_msgs = sum(1 for m in st.session_state.messages if m.get("voice", False))
        
        st.markdown(f'''
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-value">{total_msgs}</div>
                <div class="stat-label">Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{voice_msgs}</div>
                <div class="stat-label">Voice</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # Stop audio if requested
    if st.session_state.get("stop_audio"):
        st.session_state.stop_audio = False
        st.session_state.pending_audio = None
        components.html("""
        <script>
            window.parent.document.querySelectorAll('audio').forEach(a => { a.pause(); a.currentTime = 0; });
        </script>
        """, height=0)

    # ═══════════════════════════════════════════════════════════════
    # MAIN CONTENT
    # ═══════════════════════════════════════════════════════════════

    # Header with animated robot
    st.markdown(f'''
    <div class="main-header">
        <div class="header-content">
            <h1 class="header-title">Welcome to SpeakEasy AI</h1>
            <p class="header-subtitle">Your personal English learning assistant</p>
            <div class="header-badge">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                </svg>
                Voice Enabled
            </div>
        </div>
        <div class="header-illustration">
            {ROBOT_ANIMATED}
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════
    # CHAT AREA
    # ═══════════════════════════════════════════════════════════════

    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            is_user = msg["role"] == "user"
            avatar_icon = "🧑‍🎓" if is_user else "🤖"
            
            with st.chat_message(msg["role"], avatar=avatar_icon):
                if msg.get("voice", False):
                    st.caption(f"🎤 Voice message • {msg.get('timestamp', '')}")
                else:
                    st.caption(msg.get('timestamp', ''))
                
                st.markdown(msg["content"])
                
                if not is_user:
                    if st.button("🔊 Play", key=f"play_{i}"):
                        audio_path = text_to_speech(msg["content"], st.session_state.voice_settings["accent"])
                        if audio_path:
                            with open(audio_path, "rb") as audio_file:
                                audio_bytes = audio_file.read()
                            audio_base64 = base64.b64encode(audio_bytes).decode()
                            st.markdown(f'''<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>''', unsafe_allow_html=True)

    else:
        # Welcome state with animated hero
        st.markdown(f'''
        <div class="welcome-container">
            <div class="welcome-illustration">{HERO_ANIMATED}</div>
            <h2 class="welcome-title">Start practicing your English!</h2>
            <p class="welcome-subtitle">Type a message or use voice input to begin your conversation with SpeakEasy AI.</p>
            <div class="welcome-features">
                <div class="welcome-feature">
                    <div class="welcome-feature-icon">{ICON_GRAMMAR}</div>
                    <span class="welcome-feature-text">Grammar</span>
                </div>
                <div class="welcome-feature">
                    <div class="welcome-feature-icon">{ICON_SPEAKING}</div>
                    <span class="welcome-feature-text">Speaking</span>
                </div>
                <div class="welcome-feature">
                    <div class="welcome-feature-icon">{ICON_VOCABULARY}</div>
                    <span class="welcome-feature-text">Vocabulary</span>
                </div>
                <div class="welcome-feature">
                    <div class="welcome-feature-icon">{ICON_LISTENING}</div>
                    <span class="welcome-feature-text">Listening</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Quick action buttons
        st.markdown("---")
        st.markdown("**Quick Start**")
        
        qcol1, qcol2, qcol3, qcol4 = st.columns(4)
        
        quick_phrases = [
            ("Say Hello", "Hello! I want to practice my English."),
            ("Practice Grammar", "Can you help me with English grammar?"),
            ("Learn Vocabulary", "Teach me some new English words."),
            ("Conversation", "Let's have a conversation in English.")
        ]
        
        for (label, phrase), col in zip(quick_phrases, [qcol1, qcol2, qcol3, qcol4]):
            with col:
                if st.button(label, use_container_width=True, key=f"quick_{label}"):
                    st.session_state.messages.append({
                        "role": "user",
                        "content": phrase,
                        "timestamp": datetime.now().strftime("%H:%M"),
                        "voice": False
                    })
                    
                    ai_response = get_ai_response(
                        st.session_state.messages,
                        st.session_state.voice_settings["level"],
                        st.session_state.voice_settings["correction_enabled"],
                        is_voice=False
                    )
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_response,
                        "timestamp": datetime.now().strftime("%H:%M"),
                        "voice": False
                    })
                    
                    # Save to DB
                    if st.session_state.current_chat_id:
                        db.save_message(st.session_state.current_chat_id, "user", phrase)
                        db.save_message(st.session_state.current_chat_id, "assistant", ai_response)
                    
                    st.rerun()

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════════
    # INPUT ROW
    # ═══════════════════════════════════════════════════════════════

    def process_text_input():
        user_input = st.session_state.get("user_text_input", "").strip()
        if user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%H:%M"),
                "voice": False
            })
            
            ai_response = get_ai_response(
                st.session_state.messages,
                st.session_state.voice_settings["level"],
                st.session_state.voice_settings["correction_enabled"],
                is_voice=False
            )
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().strftime("%H:%M"),
                "voice": False
            })
            
            # Save to DB
            if st.session_state.current_chat_id:
                db.save_message(st.session_state.current_chat_id, "user", user_input)
                db.save_message(st.session_state.current_chat_id, "assistant", ai_response)
            
            st.session_state.user_text_input = ""

    # ═══════════════════════════════════════════════════════════════
    # INPUT ROW - Clean Aligned Design
    # ═══════════════════════════════════════════════════════════════
    
    st.markdown('''
    <style>
        /* Better alignment for input row */
        div[data-testid="column"]:has(iframe[title="audiorecorder"]) {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding-top: 0 !important;
        }
        div[data-testid="column"]:has(iframe[title="audiorecorder"]) > div {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            height: 100% !important;
        }
        /* Audio recorder styling */
        iframe[title="audiorecorder"] {
            transform: scale(1.1);
            margin-top: -5px;
        }
    </style>
    ''', unsafe_allow_html=True)
    
    input_col, mic_col = st.columns([12, 1])

    with input_col:
        st.text_input("", placeholder="Type your message here...", key="user_text_input", on_change=process_text_input, label_visibility="collapsed")

    with mic_col:
        audio_bytes = audio_recorder(
            text="",
            recording_color="#EF4444",
            neutral_color="#2563EB",
            icon_name="microphone",
            icon_size="2x",
            sample_rate=16000,
            key="voice_recorder"
        )

    # Process voice input
    if audio_bytes and st.session_state.get("last_audio") != audio_bytes:
        st.session_state.last_audio = audio_bytes
        
        with st.spinner("Processing voice..."):
            success, result = transcribe_audio(audio_bytes)
            
            if success:
                st.session_state.messages.append({
                    "role": "user",
                    "content": result,
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "voice": True
                })
                
                ai_response = get_ai_response(
                    st.session_state.messages,
                    st.session_state.voice_settings["level"],
                    st.session_state.voice_settings["correction_enabled"],
                    is_voice=True
                )
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "voice": True
                })
                
                # Save to DB
                if st.session_state.current_chat_id:
                    db.save_message(st.session_state.current_chat_id, "user", result)
                    db.save_message(st.session_state.current_chat_id, "assistant", ai_response)
                
                if st.session_state.voice_settings["auto_speak"]:
                    audio_path = text_to_speech(ai_response, st.session_state.voice_settings["accent"])
                    if audio_path:
                        st.session_state.pending_audio = audio_path
                
                st.rerun()
            else:
                st.error(f"Error: {result}")

    # Play pending audio
    if st.session_state.pending_audio:
        autoplay_audio(st.session_state.pending_audio)
        st.session_state.pending_audio = None

    # Footer
    st.markdown('''
    <div style="text-align: center; padding: 2rem 0 1rem 0; color: var(--text-muted); font-size: 0.75rem;">
        SpeakEasy AI - Your English Learning Companion<br>
        Powered by Advanced AI Technology
    </div>
    ''', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# MAIN ROUTER
# ═══════════════════════════════════════════════════════════════

if st.session_state.page == "landing":
    show_landing_page()
elif st.session_state.page == "login":
    show_login_page()
elif st.session_state.page == "signup":
    show_signup_page()
elif st.session_state.page == "chat":
    if st.session_state.auth_status:
        show_chat_interface()
    else:
        go_to("login")
