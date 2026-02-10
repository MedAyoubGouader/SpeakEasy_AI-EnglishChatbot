"""
🎨 UI MODULE
Styling and UI Components for Modern Chat Interface
"""

def get_css_styles() -> str:
    """
    Returns complete CSS styling for modern chat interface
    Similar to ChatGPT / PartyRock design
    """
    return """
<style>
    /* ═══════════════════════════════════════════════════════════════
       GLOBAL STYLES
       ═══════════════════════════════════════════════════════════════ */
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a3f 100%) !important;
        color: #fff;
        min-height: 100vh;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ═══════════════════════════════════════════════════════════════
       HEADER
       ═══════════════════════════════════════════════════════════════ */
    
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .app-header h1 {
        font-size: 2.2em;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .app-header p {
        color: rgba(255,255,255,0.9);
        margin-top: 8px;
        font-size: 1.05em;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       CHAT CONTAINER
       ═══════════════════════════════════════════════════════════════ */
    
    .chat-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        min-height: 450px;
        max-height: 550px;
        overflow-y: auto;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 3px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.5);
        border-radius: 3px;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       MESSAGE BUBBLES
       ═══════════════════════════════════════════════════════════════ */
    
    .message-wrapper {
        display: flex;
        margin: 16px 0;
        animation: fadeIn 0.3s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message-wrapper.user {
        justify-content: flex-end;
    }
    
    .message-wrapper.assistant {
        justify-content: flex-start;
    }
    
    .message-bubble {
        max-width: 75%;
        padding: 14px 18px;
        border-radius: 18px;
        line-height: 1.5;
        font-size: 0.95em;
        position: relative;
    }
    
    .user .message-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant .message-bubble {
        background: rgba(255, 255, 255, 0.08);
        color: #e8e8e8;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .message-time {
        font-size: 0.7em;
        opacity: 0.6;
        margin-top: 6px;
        text-align: right;
    }
    
    .message-avatar {
        font-size: 1.4em;
        margin: 0 10px;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       INPUT AREA
       ═══════════════════════════════════════════════════════════════ */
    
    .input-container {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 16px;
        backdrop-filter: blur(10px);
    }
    
    /* Style Streamlit inputs */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 14px 16px !important;
        font-size: 1em !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       BUTTONS
       ═══════════════════════════════════════════════════════════════ */
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary buttons */
    .secondary-btn > button {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       SIDEBAR
       ═══════════════════════════════════════════════════════════════ */
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a3f 0%, #0f0f23 100%) !important;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    .sidebar-header {
        color: white;
        font-size: 1.3em;
        font-weight: 700;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .sidebar-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .sidebar-section h4 {
        color: #667eea;
        margin-bottom: 10px;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       STATS CARDS
       ═══════════════════════════════════════════════════════════════ */
    
    .stats-container {
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .stat-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    
    .stat-card .label {
        font-size: 0.8em;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-card .value {
        font-size: 1.8em;
        font-weight: 700;
        color: #667eea;
        margin-top: 5px;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       WELCOME MESSAGE
       ═══════════════════════════════════════════════════════════════ */
    
    .welcome-message {
        text-align: center;
        padding: 40px 20px;
        color: rgba(255,255,255,0.7);
    }
    
    .welcome-message .emoji {
        font-size: 3em;
        margin-bottom: 15px;
    }
    
    .welcome-message h3 {
        color: white;
        margin-bottom: 10px;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       LOADING / TYPING INDICATOR
       ═══════════════════════════════════════════════════════════════ */
    
    .typing-indicator {
        display: flex;
        gap: 5px;
        padding: 15px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { opacity: 0.3; transform: translateY(0); }
        30% { opacity: 1; transform: translateY(-8px); }
    }
    
    /* ═══════════════════════════════════════════════════════════════
       CORRECTIONS HIGHLIGHT
       ═══════════════════════════════════════════════════════════════ */
    
    .correction-box {
        background: rgba(102, 126, 234, 0.1);
        border-left: 3px solid #667eea;
        padding: 12px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    
    .correction-original {
        color: #ff6b6b;
        text-decoration: line-through;
        opacity: 0.8;
    }
    
    .correction-fixed {
        color: #51cf66;
        font-weight: 600;
    }
    
    /* ═══════════════════════════════════════════════════════════════
       VOICE BUTTON
       ═══════════════════════════════════════════════════════════════ */
    
    .voice-btn {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%) !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.3em !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
    }
    
    .voice-btn.recording {
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 107, 107, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
    }
    
    /* ═══════════════════════════════════════════════════════════════
       RESPONSIVE
       ═══════════════════════════════════════════════════════════════ */
    
    @media (max-width: 768px) {
        .message-bubble {
            max-width: 90%;
        }
        
        .stats-container {
            flex-direction: column;
        }
    }
</style>
"""


def render_message(role: str, content: str, timestamp: str = "") -> str:
    """
    Render a chat message bubble
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        timestamp: Optional timestamp
        
    Returns:
        HTML string for message
    """
    avatar = "👤" if role == "user" else "🤖"
    wrapper_class = "user" if role == "user" else "assistant"
    
    # Process content for markdown-like formatting
    content = content.replace("\n", "<br>")
    
    return f"""
    <div class="message-wrapper {wrapper_class}">
        {"" if role == "user" else f'<span class="message-avatar">{avatar}</span>'}
        <div class="message-bubble">
            {content}
            {f'<div class="message-time">{timestamp}</div>' if timestamp else ''}
        </div>
        {f'<span class="message-avatar">{avatar}</span>' if role == "user" else ""}
    </div>
    """


def render_welcome() -> str:
    """Render welcome message when chat is empty"""
    return """
    <div class="welcome-message">
        <div class="emoji">👋</div>
        <h3>Welcome to English Learning AI!</h3>
        <p>Start typing or speaking to practice your English.<br>
        I'm here to help you improve! 🎓</p>
    </div>
    """


def render_typing_indicator() -> str:
    """Render typing/loading indicator"""
    return """
    <div class="message-wrapper assistant">
        <span class="message-avatar">🤖</span>
        <div class="message-bubble">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    </div>
    """


def render_stats(messages: int, level: str, streak: int = 0) -> str:
    """
    Render stats cards
    
    Args:
        messages: Number of messages sent
        level: Current English level
        streak: Learning streak days
        
    Returns:
        HTML string for stats
    """
    return f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="label">Messages</div>
            <div class="value">{messages}</div>
        </div>
        <div class="stat-card">
            <div class="label">Level</div>
            <div class="value">{level[:3]}</div>
        </div>
        <div class="stat-card">
            <div class="label">Streak</div>
            <div class="value">🔥 {streak}</div>
        </div>
    </div>
    """
