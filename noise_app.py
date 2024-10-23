import streamlit as st
import noisereduce as nr
import numpy as np
import soundfile as sf
import librosa
import os

# Title of the app
st.title("Audio Noise Reduction App")

# File uploader for the audio file
uploaded_file = st.file_uploader("Upload an audio file (mp3 or wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_audio_path = "temp_audio"
    with open(temp_audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load the audio file using librosa
    audio_data, sample_rate = librosa.load(temp_audio_path, sr=None)

    # Play the original audio
    st.audio(temp_audio_path, format="audio/wav")

    # Apply noise reduction
    reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)

    # Save the output audio to a file
    output_audio_path = "output_audio.wav"
    sf.write(output_audio_path, reduced_noise, sample_rate)

    # Play the processed audio
    st.audio(output_audio_path, format="audio/wav")

    # Clean up temporary files
    os.remove(temp_audio_path)
