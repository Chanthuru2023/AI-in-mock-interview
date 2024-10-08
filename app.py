import streamlit as st
from gtts import gTTS
import os
import pyaudio
import wave
import threading
import time

# Function to convert text to audio
def text_to_audio(text, filename):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)

# Function to record audio
def record_audio(filename, duration):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    frames = []
    for _ in range(int(44100 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

# Streamlit app
st.title("Mock Interview AI Tool")

interview_question = st.text_input("Enter your interview question:")
mic_status = st.empty()  # Placeholder for microphone status

if st.button("Start Interview"):
    if interview_question:
        audio_filename = "question.mp3"
        answer_audio_filename = "answer.wav"
        recording_duration = 10

        # Convert text to audio and play it
        text_to_audio(interview_question, audio_filename)
        st.audio(audio_filename)  # Play the audio file

        # Update microphone status
        mic_status.markdown("<h3 style='color: red;'>Microphone Muted.</h3>", unsafe_allow_html=True)

        # Start recording
        st.write("Recording your answer...")
        threading.Thread(target=lambda: record_audio(answer_audio_filename, recording_duration)).start()
        
        # Simulate the waiting period while recording
        for _ in range(recording_duration):
            time.sleep(1)  # Simulate waiting while recording
            mic_status.markdown("<h3 style='color: green;'>Microphone Active - Recording...</h3>", unsafe_allow_html=True)

        st.write("Finished recording your answer.")
        mic_status.markdown("<h3 style='color: red;'>Microphone Muted.</h3>", unsafe_allow_html=True)
    else:
        st.error("Please enter a question.")
