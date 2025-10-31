import streamlit as st
from modules.speech_to_text import transcribe_audio
from modules.text_to_speech import speak_text
from modules.emotion_detection import detect_emotion
from modules.video_understanding import analyze_video
from model import generate_response
from model import summarize_text, generate_caption, image_text_similarity
from utils import clean_text

st.set_page_config(page_title="AI Conversational Multimedia Assistant", layout="wide")

st.title("🤖 AI Conversational Multimedia Assistant")
st.caption("🧠 Powered by GPT-4, Whisper, DeepFace, and Transformers")

mode = st.selectbox("Select Mode", ["Chat", "Text + Image", "Voice", "Video"])

# Chat Mode (GPT-4)
if mode == "Chat":
    user_input = st.text_area("💬 Ask me anything:")
    if st.button("Generate Response"):
        response = generate_response(user_input)
        st.success(response)
        audio_file = speak_text(response)
        st.audio(audio_file)

# Text + Image Mode
elif mode == "Text + Image":
    text = st.text_area("📝 Enter text:")
    image = st.file_uploader("🖼️ Upload an image:", type=["jpg", "png"])
    if st.button("Analyze"):
        if image:
            with open("temp.jpg", "wb") as f: f.write(image.read())
            summary = summarize_text(clean_text(text))
            caption = generate_caption("temp.jpg")
            emotion = detect_emotion("temp.jpg")
            similarity = image_text_similarity("temp.jpg", text)
            st.json({
                "Text Summary": summary,
                "Image Caption": caption,
                "Image-Text Similarity": round(similarity, 2),
                "Detected Emotion": emotion
            })

# Voice Mode
elif mode == "Voice":
    audio = st.file_uploader("🎙️ Upload an audio file (.wav, .mp3):", type=["wav", "mp3"])
    if st.button("Transcribe & Summarize"):
        if audio:
            with open("temp.wav", "wb") as f: f.write(audio.read())
            transcript = transcribe_audio("temp.wav")
            st.write("🗣️ Transcribed Text:")
            st.info(transcript)
            summary = generate_response(f"Summarize this: {transcript}")
            st.success(summary)
            audio_file = speak_text(summary)
            st.audio(audio_file)

# Video Mode
elif mode == "Video":
    video = st.file_uploader("🎞️ Upload a video file (.mp4):", type=["mp4"])
    if st.button("Analyze Video"):
        if video:
            with open("temp.mp4", "wb") as f: f.write(video.read())
            captions = analyze_video("temp.mp4")
            st.write("🎬 Scene Descriptions:")
            for cap in captions:
                st.markdown(f"• {cap}")
