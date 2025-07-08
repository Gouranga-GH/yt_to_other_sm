# ui.py - Streamlit UI Components
# ------------------------------
# This module provides all Streamlit UI rendering functions for the modular app.
# It separates UI logic from the main workflow logic for clarity and maintainability.

import streamlit as st
from datetime import datetime

def render_page_config():
    """Set Streamlit page configuration and inject custom CSS."""
    st.set_page_config(
        page_title="YouTube to Content Creator",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown("""
    <style>
    body, .main, .stApp {
        background: #181a20 !important;
        color: #f8f9fa !important;
    }
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #23272f;
        color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the app header."""
    st.markdown("""
    <div class="main-header">
        <h1>🎬 YouTube to Content Creator</h1>
        <p>Transform YouTube videos into Instagram/Medium content using AI agents</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar for API key input. Returns the OpenAI API key."""
    with st.sidebar:
        st.header("🔑 API Configuration")
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to enable AI-powered content generation"
        )
        if not openai_api_key:
            st.warning("⚠️ OpenAI API key is required to use this application")
            st.stop()
        st.success("✅ API key configured successfully!")
    return openai_api_key

def render_input_form():
    """Render the main input form and return user selections."""
    st.header("🎥 Input Configuration")
    video_url = st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste the full YouTube video URL you want to convert"
    )
    def validate_youtube_url(url):
        import re
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+'
        ]
        for pattern in youtube_patterns:
            if re.match(pattern, url):
                return True
        return False
    if video_url and not validate_youtube_url(video_url):
        st.error("❌ Please enter a valid YouTube URL")
        st.stop()
    platform = st.selectbox(
        "Target Platform",
        ["Instagram", "Medium"],
        help="Choose where you want to publish your content"
    )
    if platform == "Instagram":
        content_type = st.selectbox(
            "Content Type",
            ["Post", "Story", "Carousel"],
            help="Choose the type of Instagram content"
        )
    else:
        content_type = st.selectbox(
            "Content Type",
            ["Article", "Story", "Tutorial"],
            help="Choose the type of Medium content"
        )
    generate = st.button("🚀 Generate Content", type="primary", use_container_width=True)
    return video_url, platform, content_type, generate

def render_output(result, platform, content_type):
    """Render the generated content and download button."""
    st.success("✅ Content generated successfully!")
    st.header("📝 Generated Content")
    st.markdown("---")
    st.markdown(str(result))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{platform.lower()}_{content_type.lower()}_{timestamp}.md"
    st.download_button(
        label="📥 Download Content",
        data=str(result),
        file_name=filename,
        mime="text/markdown",
        use_container_width=True
    )

def render_tips():
    """Render the tips and best practices section."""
    st.header("💡 Tips")
    st.markdown("""
    <div class="feature-card">
        <h4>🎯 Best Practices</h4>
        <ul>
            <li>Use high-quality YouTube videos</li>
            <li>Videos with clear audio work best</li>
            <li>Longer videos provide more content</li>
            <li>Educational content performs well</li>
        </ul>
    </div>
    <div class="feature-card">
        <h4>⚡ Quick Tips</h4>
        <ul>
            <li>Instagram: Use relevant hashtags</li>
            <li>Medium: Focus on storytelling</li>
            <li>Add call-to-actions</li>
            <li>Engage with your audience</li>
        </ul>
    </div>
    <div class="feature-card">
        <h4>📱 Instagram Tips</h4>
        <ul>
            <li>Use 5-15 hashtags</li>
            <li>Keep captions engaging</li>
            <li>Add emojis for visual appeal</li>
            <li>Include call-to-actions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True) 