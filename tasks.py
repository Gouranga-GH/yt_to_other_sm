# tasks.py - CrewAI Task Creation
# ------------------------------
# This module provides a function to create CrewAI tasks for the modular app.
# Each task embeds the transcript and description for context.
# Logging is used for traceability.

import logging
from crewai import Task

logger = logging.getLogger(__name__)

def create_tasks(video_url, platform, content_type, video_info, video_analyzer, content_creator, platform_specialist):
    """
    Create the sequence of CrewAI tasks for the content creation workflow.
    Each task embeds the transcript and description for the agents to use.
    Args:
        video_url (str): The YouTube video URL
        platform (str): Target platform (Instagram or Medium)
        content_type (str): Type of content to create
        video_info (dict): Extracted video metadata and transcript
        video_analyzer, content_creator, platform_specialist: CrewAI agents
    Returns:
        list: List of Task objects (analysis, creation, optimization)
    """
    transcript = video_info.get('transcript', 'No transcript available')
    description = video_info.get('description', 'No description available')
    title = video_info.get('title', 'Unknown')
    duration = video_info.get('duration', 0)
    logger.info(f'Creating tasks for video: {title}')
    # Task 1: Analysis - Agent analyzes the transcript and description
    analyze_task = Task(
        description=(
            f"You are analyzing a YouTube video.\n"
            f"Title: {title}\nDuration: {duration} seconds\n"
            f"Description: {description}\n"
            f"Transcript below:\n{transcript}\n"
            "Extract the main topic, 5-7 key points, interesting facts, and compelling quotes from the transcript above. "
            "Focus on elements that would resonate with a {platform} audience. Do NOT use general knowledge."
        ),
        expected_output=(
            "A comprehensive analysis of the specific video including: main topic, 5-7 key points, "
            "interesting facts, compelling quotes, and audience insights from this video only."
        ),
        agent=video_analyzer
    )
    # Task 2: Content Creation - Agent creates content using the analysis and transcript
    create_task = Task(
        description=(
            f"Based on the analysis, create engaging content for {platform}. "
            f"The content should be optimized for {content_type} format. "
            "Make it compelling, informative, and shareable. "
            "Include relevant hashtags and call-to-actions where appropriate.\n"
            f"REFERENCE: Transcript below:\n{transcript}\n"
            f"REFERENCE: Description: {description}\n"
            "IMPORTANT: Use ONLY the transcript and description above."
        ),
        expected_output=(
            f"A well-crafted {content_type} piece that captures the essence "
            "of the video while being optimized for the target platform."
        ),
        agent=content_creator,
        context=[analyze_task]
    )
    # Task 3: Platform Optimization - Agent optimizes content for the chosen platform
    optimize_task = Task(
        description=(
            f"Take the created content and optimize it specifically for {platform} {content_type}. "
            f"Apply platform-specific best practices, formatting, hashtag strategies, "
            f"and engagement techniques. Ensure it follows {platform} guidelines and trends.\n"
            f"REFERENCE: Transcript below:\n{transcript}\n"
            f"REFERENCE: Description: {description}\n"
            "IMPORTANT: Use ONLY the transcript and description above."
        ),
        expected_output=(
            f"Final optimized content ready for {platform} {content_type} with "
            "proper formatting, hashtags, and platform-specific optimizations."
        ),
        agent=platform_specialist,
        context=[create_task]
    )
    logger.info('Tasks created successfully.')
    return [analyze_task, create_task, optimize_task] 