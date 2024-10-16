import streamlit as st
from pydub import AudioSegment
import speech_recognition as sr
import os

# Title of the Streamlit App
st.title("Filler Words Detection App")

# Upload the MP3 file
uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

if uploaded_file is not None:
    # Save the uploaded file
    audio_file_path = "temp_audio.mp3"
    with open(audio_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(audio_file_path)
    wav_file_path = "temp_audio.wav"
    audio.export(wav_file_path, format="wav")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Recognize speech from the WAV file
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)

    # Perform speech recognition and filler word removal
    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio_data)
        st.write("### Original Recognized Text:")
        st.write(text)
        
        # Define filler words
        filler_words = ["um", "uh", "like", "you know", "basically"]
        
        # Split the text into words
        words = text.split()
        
        # Remove filler words from the recognized text
        cleaned_text = " ".join([word for word in words if word.lower() not in filler_words])
        
        # Output cleaned text
        st.write("### Cleaned Text Without Filler Words:")
        st.write(cleaned_text)

    except sr.UnknownValueError:
        st.error("Speech recognition could not understand the audio")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")

    # Clean up temporary files
    os.remove(audio_file_path)
    os.remove(wav_file_path)
