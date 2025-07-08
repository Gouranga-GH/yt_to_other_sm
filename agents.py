# agents.py - CrewAI Agent Creation
# ---------------------------------
# This module provides functions to create CrewAI agents for the modular app.
# Each agent is specialized for a role in the content creation workflow.
# Logging is used for traceability.

import logging
from crewai import Agent

logger = logging.getLogger(__name__)

def create_video_analyzer(tools=None):
    """
    Create the Video Content Analyzer agent.
    This agent extracts key insights and main points from YouTube videos.
    Args:
        tools (list): List of tools the agent can use (optional)
    Returns:
        Agent: Configured CrewAI agent
    """
    logger.info('Creating Video Content Analyzer agent.')
    return Agent(
        role='Video Content Analyzer',
        goal='Extract key insights, main points, and engaging content from YouTube videos',
        verbose=True,
        memory=True,
        backstory=(
            "You are an expert content analyst with deep understanding of video content. "
            "You excel at identifying the most compelling and shareable aspects of videos, "
            "understanding audience engagement patterns, and extracting actionable insights."
        ),
        tools=tools or [],
        allow_delegation=False
    )

def create_content_creator(tools=None):
    """
    Create the Creative Content Writer agent.
    This agent transforms video insights into engaging, platform-optimized content.
    Args:
        tools (list): List of tools the agent can use (optional)
    Returns:
        Agent: Configured CrewAI agent
    """
    logger.info('Creating Creative Content Writer agent.')
    return Agent(
        role='Creative Content Writer',
        goal='Transform video insights into engaging, platform-optimized content',
        verbose=True,
        memory=True,
        backstory=(
            "You are a creative content writer who specializes in adapting video content "
            "for different social media platforms. You understand what makes content viral "
            "and how to craft compelling narratives that resonate with different audiences."
        ),
        tools=tools or [],
        allow_delegation=False
    )

def create_platform_specialist(tools=None):
    """
    Create the Platform Optimization Specialist agent.
    This agent optimizes content for Instagram or Medium using best practices.
    Args:
        tools (list): List of tools the agent can use (optional)
    Returns:
        Agent: Configured CrewAI agent
    """
    logger.info('Creating Platform Optimization Specialist agent.')
    return Agent(
        role='Platform Optimization Specialist',
        goal='Optimize content specifically for Instagram or Medium based on platform best practices',
        verbose=True,
        memory=True,
        backstory=(
            "You are a social media expert who understands the unique requirements and "
            "best practices for different platforms. You know how to format content for "
            "maximum engagement on Instagram and Medium, including hashtags, formatting, "
            "and platform-specific features."
        ),
        tools=tools or [],
        allow_delegation=False
    ) 