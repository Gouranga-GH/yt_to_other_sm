# youtube_tools.py - YouTube Video Analysis and Transcript Extraction
# ---------------------------------------------------------------
# This module provides the YouTubeVideoAnalyzer class, which extracts
# video metadata and transcript from a YouTube URL using yt_dlp.
# Logging is used for traceability and debugging.

import yt_dlp
import requests
from urllib.parse import urlparse, parse_qs
import logging

logger = logging.getLogger(__name__)

class YouTubeVideoAnalyzer:
    """
    Tool to analyze specific YouTube videos and extract their content.
    Extracts title, description, duration, and transcript (if available).
    """
    def __init__(self):
        pass

    def analyze_video(self, video_url):
        """
        Analyze a specific YouTube video and extract its information and transcript.
        Args:
            video_url (str): The YouTube video URL to analyze
        Returns:
            dict: Video information including title, description, transcript, and metadata
        """
        try:
            # Extract the video ID from the URL
            video_id = self._extract_video_id(video_url)
            if not video_id:
                logger.error(f"Could not extract video ID from URL: {video_url}")
                return {"error": "Could not extract video ID from URL"}
            # yt_dlp options to get subtitles and metadata without downloading video
            ydl_opts = {
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'skip_download': True,
                'quiet': True,
                'outtmpl': '%(id)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                if info is None:
                    logger.error(f"Could not extract video information for: {video_url}")
                    return {"error": "Could not extract video information"}
                # Extract metadata
                title = info.get('title', 'Unknown Title')
                description = info.get('description', '')
                duration = info.get('duration', 0)
                transcript = ""
                try:
                    # Try to get transcript from subtitles or automatic captions
                    subtitles = info.get('subtitles', {})
                    auto_subs = info.get('automatic_captions', {})
                    transcript_url = None
                    if subtitles and 'en' in subtitles:
                        transcript_url = subtitles['en'][0].get('url')
                    elif auto_subs and 'en' in auto_subs:
                        transcript_url = auto_subs['en'][0].get('url')
                    if transcript_url:
                        # Download and parse the transcript (VTT/SRT)
                        resp = requests.get(transcript_url)
                        if resp.status_code == 200:
                            text = resp.text
                            # Simple VTT/SRT to plain text conversion
                            transcript = '\n'.join([
                                line for line in text.splitlines()
                                if line and not line.replace('.', '').replace(':', '').isdigit() and '-->' not in line and not line.startswith('WEBVTT')
                            ]).strip()
                    # Fallback to description if no transcript
                    if not transcript:
                        transcript = description[:1000] if description else "No transcript available"
                except Exception as e:
                    logger.warning(f"Transcript extraction failed: {e}")
                    transcript = description[:1000] if description else "No transcript available"
                video_info = {
                    "video_id": video_id,
                    "url": video_url,
                    "title": title,
                    "description": description[:500] if description else "No description available",
                    "duration": duration,
                    "transcript": transcript,
                }
                logger.info(f"Extracted video info for {video_url}: {title}")
                return video_info
        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
            return {"error": f"Error analyzing video: {str(e)}"}

    def _extract_video_id(self, url):
        """
        Extract the video ID from a YouTube URL.
        Supports standard, short, and embed URLs.
        Args:
            url (str): YouTube URL
        Returns:
            str: Video ID or None if not found
        """
        try:
            if 'youtube.com/watch' in url:
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                return query_params.get('v', [None])[0]
            elif 'youtu.be/' in url:
                return url.split('youtu.be/')[-1].split('?')[0]
            elif 'youtube.com/embed/' in url:
                return url.split('youtube.com/embed/')[-1].split('?')[0]
            else:
                return None
        except Exception as e:
            logger.warning(f"Failed to extract video ID: {e}")
            return None 