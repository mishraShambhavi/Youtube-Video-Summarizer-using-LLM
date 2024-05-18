import streamlit as st
from dotenv import load_dotenv

load_dotenv()  ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi ,TranscriptsDisabled

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


prompt = """You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        # Extract video ID from different possible YouTube URL formats
        video_id = None
        if "youtu.be/" in youtube_video_url:
            video_id = youtube_video_url.split("youtu.be/")[1].split("?")[0]
        elif "youtube.com/watch" in youtube_video_url:
            video_id = youtube_video_url.split("v=")[1].split("&")[0]

        if not video_id:
            raise ValueError("Invalid YouTube URL")

        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])

        return transcript

    except Exception as e:
        raise e


## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


st.title("Get Detailed Notes and Summaries From Youtube Videos")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        # Extract video ID and display the thumbnail
        video_id = None
        if "youtu.be/" in youtube_link:
            video_id = youtube_link.split("youtu.be/")[1].split("?")[0]
        elif "youtube.com/watch" in youtube_link:
            video_id = youtube_link.split("v=")[1].split("&")[0]

        if video_id:
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        else:
            st.error("Invalid YouTube URL")

    except Exception as e:
        st.error(f"Error extracting video ID: {e}")

if st.button("Get Detailed Notes"):
    try:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
    except Exception as e:
        st.error(f"Error retrieving transcript or generating summary: {e}")