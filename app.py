import streamlit as st 
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import wikipedia
import spacy
from transformers import pipeline

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are youtube video summarizer. You will be taking the transcript text and 
summarizingthe entire video and providing the important summary in points within 250 words.Please 
provide the summary of the text given here:
"""

# Function to perform fact-checking analysis using a multi-modal AI model
def perform_fact_checking_analysis(video_url):
    # This function should implement the fact-checking analysis
    # and return a report with factual statements, fallacious statements, and unsubstantiated claims
    # Placeholder for actual fact-checking implementation
    return {
        "factualStatements": ["Fact 1", "Fact 2"],
        "fallaciousStatements": ["Fallacy 1", "Fallacy 2"],
        "unsubstantiatedClaims": ["Claim 1", "Claim 2"]
    }

## getting the transcript data from youtube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
            
        return transcript
    
    except Exception as e:
        raise e

## getting the summary based on prompt from LLM
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    summary = response.text
    # Perform fact-checking analysis
    fact_check_report = perform_fact_checking_analysis(transcript_text)
    return summary, fact_check_report

st.title("YouTube Video Summarizer and Fact Checker")
youtube_link = st.text_input("Enter Your Video link: ")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
    
if st.button("Get Detailed Notes and Fact Check Report"):
    transcript_text=extract_transcript_details(youtube_link)
    
    if transcript_text:
        summary, fact_check_report = generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes: ")
        st.write(summary)
        
        # Displaying the fact-checking report
        st.markdown("## Fact-Checking Report: ")
        st.markdown("### Factual Statements")
        for fact in fact_check_report["factualStatements"]:
            st.write(fact)
        st.markdown("### Fallacious Statements")
        for fallacy in fact_check_report["fallaciousStatements"]:
            st.write(fallacy)
        st.markdown("### Unsubstantiated Claims")
        for claim in fact_check_report["unsubstantiatedClaims"]:
            st.write(claim)
