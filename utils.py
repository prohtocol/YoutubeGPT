"""
FILE NAME   : utils.py
PURPOSE     : Utility funcions module
              Contains utility function for youtube and chatGPT APIs
PROGRAMMER  : Aleksei Seliverstov.
NOTE        : None.

Copyright (c) 2023 Aleksei Seliverstov
"""

from youtube_transcript_api import YouTubeTranscriptApi
import config
import openai
from openai import OpenAI
import time
import datetime


def get_video_transcript(video_id):
    """
    Retrieves the transcript of a YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.

    Returns:
        list: A list of dictionaries representing the transcript.
        Each dictionary contains the following keys:
            - 'text': The text of the transcript.
            - 'start': The start time of the transcript segment in seconds.
            - 'duration': The duration of the transcript segment in seconds.
    """
    transcript = YouTubeTranscriptApi.get_transcript(
        video_id, languages=config.languages
    )
    return transcript


def get_video_id(youtube_link):
    """
    Extracts the video ID from a YouTube link.

    Args:
        youtube_link (str): The YouTube link.

    Returns:
        str: The video ID extracted from the link.

    Raises:
        ValueError: If the video ID cannot be found in the link.
    """
    video_id = youtube_link.split("v=")
    if len(video_id) > 1:
        return video_id[1]
    video_id = youtube_link.split("youtu.be/")
    if len(video_id) > 1:
        return video_id[1]
    raise ValueError(f"Unable to find video id for url: [{youtube_link}]")


client = OpenAI(api_key=config.open_ai_key)


def use_chatgpt(prompt):
    """
    Generates a response using the ChatGPT model.

    Args:
        prompt (str): The user's prompt.

    Returns:
        str: The generated response from the ChatGPT model.
    """
    try:
        response = client.chat.completions.create(
            model=config.open_ai_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except openai.RateLimitError:
        print("RateLimitError occurred. Retrying in 1 minute...")
        time.sleep(60)
        return use_chatgpt(prompt)


def convert_seconds_to_time(seconds):
    """
    Converts seconds to a formatted time string.

    Args:
        seconds (float): The number of seconds.

    Returns:
        str: The formatted time string in the format "HH:MM:SS.SSS".
    """
    time_parts = str(datetime.timedelta(seconds=seconds)).split(":")
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(float(time_parts[2]))
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
