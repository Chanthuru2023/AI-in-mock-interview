import streamlit as st
from gtts import gTTS
import pandas as pd
import os

# Function to convert text to audio
def text_to_audio(text, filename):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)

# Streamlit Web App
def main():
    st.title("AI Mock Interview Tool")

    # Step 1: Upload multiple CSV files
    uploaded_files = st.file_uploader("Upload Job Role Question Files", type=["csv"], accept_multiple_files=True)

    questions_dict = {}
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save the uploaded file to a temporary directory
            with open(os.path.join("temp", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            job_role = uploaded_file.name.split('_')[0]  # Assuming files are named like 'developer_questions.csv'
            questions_dict[job_role] = df['Questions'].tolist()  # Assuming the column with questions is named 'Questions'

        # Store questions dictionary in session state
        st.session_state.questions_dict = questions_dict
        st.session_state.question_index = 0  # Reset question index

    # Step 2: Select job role
    if 'questions_dict' in st.session_state:
        job_role = st.selectbox("Select Job Role", list(st.session_state.questions_dict.keys()))

        if st.button("Start Interview"):
            # Set the questions for the selected job role
            st.session_state.questions = st.session_state.questions_dict[job_role]
            st.session_state.question_index = 0  # Reset index for new interview
            st.session_state.total_questions = len(st.session_state.questions)

    # Track current index to know which question is being asked
    current_index = st.session_state.get('question_index', 0)

    # Step 3: Ask questions
    if 'questions' in st.session_state and st.session_state.questions:
        if current_index < st.session_state.total_questions:
            # Display current question
            current_question = st.session_state.questions[current_index]
            st.write(f"Interview Question {current_index + 1}: {current_question}")

            # Convert current question to audio
            filename = f"question_{current_index + 1}.mp3"
            text_to_audio(current_question, filename)

            # Display the audio file
            audio_file = open(filename, "rb").read()
            st.audio(audio_file, format='audio/mp3')

            # Next button to move to the next question
            if st.button("Next"):
                st.session_state.question_index += 1  # Move to the next question
        else:
            st.write("You have completed all the questions.")
            st.write("Interview completed! Please wait for the feedback.")
            st.session_state.question_index = 0  # Reset to allow new input

if __name__ == '__main__':
    # Create a temporary folder if it doesn't exist
    os.makedirs("temp", exist_ok=True)
    main()
