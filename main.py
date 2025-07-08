# main.py - Modular Streamlit App for YouTube to Content Creator
# -------------------------------------------------------------
# This is the main entry point for the modularized CrewAI app.
# It uses separate modules for logging, YouTube video analysis, agent creation, and task creation.
# The app allows users to input a YouTube video URL and generate Instagram/Medium content using AI agents.

import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

# Import the logging setup function
from logger import setup_logging
# Import the YouTube video analyzer
from youtube_tools import YouTubeVideoAnalyzer
# Import agent creation functions
from agents import create_video_analyzer, create_content_creator, create_platform_specialist
# Import task creation function
from tasks import create_tasks
from crewai import Crew, Process

# 1. Initialize logging (file + console)
setup_logging()
logger = logging.getLogger(__name__)

# 2. Load environment variables from .env (for API keys, etc.)
load_dotenv()

# 3. Streamlit UI configuration
st.set_page_config(
    page_title="YouTube to Content Creator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 4. Inject custom CSS for dark mode and card styling
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

# 5. App header
st.markdown("""
<div class="main-header">
    <h1>🎬 YouTube to Content Creator</h1>
    <p>Transform YouTube videos into Instagram/Medium content using AI agents</p>
</div>
""", unsafe_allow_html=True)

# 6. Sidebar for API key input
with st.sidebar:
    st.header("🔑 API Configuration")
    # User inputs their OpenAI API key (required for CrewAI)
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key to enable AI-powered content generation"
    )
    if not openai_api_key:
        st.warning("⚠️ OpenAI API key is required to use this application")
        st.stop()
    st.success("✅ API key configured successfully!")

# 7. Main layout: two columns (input/config on left, tips on right)
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎥 Input Configuration")
    # User inputs the YouTube video URL
    video_url = st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste the full YouTube video URL you want to convert"
    )
    # Helper function to validate YouTube URLs
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
    # Validate the URL and show error if invalid
    if video_url and not validate_youtube_url(video_url):
        st.error("❌ Please enter a valid YouTube URL")
        st.stop()
    # User selects the target platform
    platform = st.selectbox(
        "Target Platform",
        ["Instagram", "Medium"],
        help="Choose where you want to publish your content"
    )
    # User selects the content type based on platform
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
    # Main action button to generate content
    if st.button("🚀 Generate Content", type="primary", use_container_width=True):
        if not video_url:
            st.error("❌ Please enter a YouTube URL")
            st.stop()
        # Set OpenAI API key for CrewAI
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["OPENAI_MODEL_NAME"] = "gpt-4-0125-preview"
        with st.spinner("🤖 AI agents are working on your content..."):
            # 1. Analyze the YouTube video (extract transcript, description, etc.)
            analyzer = YouTubeVideoAnalyzer()
            video_info = analyzer.analyze_video(video_url)
            logger.info(f"Video info: {video_info}")
            # 2. Create the three agents
            video_analyzer = create_video_analyzer()
            content_creator = create_content_creator()
            platform_specialist = create_platform_specialist()
            # 3. Create the tasks (with transcript/description embedded)
            tasks = create_tasks(
                video_url, platform, content_type, video_info,
                video_analyzer, content_creator, platform_specialist
            )
            # 4. Create the Crew and run the workflow
            crew = Crew(
                agents=[video_analyzer, content_creator, platform_specialist],
                tasks=tasks,
                process=Process.sequential,
                memory=True,
                cache=True,
                max_rpm=100,
                share_crew=True
            )
            try:
                # Run the CrewAI workflow
                result = crew.kickoff()
                st.success("✅ Content generated successfully!")
                st.header("📝 Generated Content")
                st.markdown("---")
                st.markdown(str(result))
                # Download button for the generated content
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{platform.lower()}_{content_type.lower()}_{timestamp}.md"
                st.download_button(
                    label="📥 Download Content",
                    data=str(result),
                    file_name=filename,
                    mime="text/markdown",
                    use_container_width=True
                )
            except Exception as e:
                logger.error(f"Error generating content: {e}")
                st.error(f"Error generating content: {e}")

# 8. Tips and best practices in the right column
with col2:
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