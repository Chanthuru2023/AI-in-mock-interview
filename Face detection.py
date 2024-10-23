#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install transformers


# In[2]:


from transformers import pipeline

# Load pre-trained emotion recognition model
emotion_model = pipeline('sentiment-analysis', model='j-hartmann/emotion-english-distilroberta-base')

def analyze_emotion(transcription):
    emotions = emotion_model(transcription)
    return emotions


# In[3]:


pip install opencv-python


# In[4]:


'''import cv2

def detect_face_and_eyes():
    # Load the cascade classifiers for face and eye detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read each frame
        ret, frame = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangle around the faces and detect eyes
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        # Display the video frame
        cv2.imshow('Face and Eye Detection', frame)

        # Stop if the escape key is pressed
        if cv2.waitKey(30) & 0xFF == 27:
            break

    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start detecting face and eye contact
detect_face_and_eyes()'''
import cv2
import tkinter as tk
from tkinter import messagebox

def show_popup():
    # Create a simple popup window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showwarning("Warning", "You are too far from the camera!")

def detect_face_and_eyes():
    # Load the cascade classifiers for face and eye detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read each frame
        ret, frame = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Check if a face is detected
        if len(faces) == 0:
            # No face detected, skip to the next frame
            continue

        # Draw rectangle around the faces and detect eyes
        for (x, y, w, h) in faces:
            # If face size is smaller than a threshold, trigger a pop-up
            if w < 100 or h < 100:  # Adjust threshold based on your testing
                show_popup()

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # Detect eyes
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        # Display the video frame
        cv2.imshow('Face and Eye Detection', frame)

        # Stop if the escape key is pressed
        if cv2.waitKey(30) & 0xFF == 27:
            break

    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start detecting face and eye contact
detect_face_and_eyes()



# In[ ]:


from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_interview():
    data = request.json
    transcription = data['transcription']

    # Example NLP emotion analysis (call previously defined function)
    emotions = analyze_emotion(transcription)
    
    # Sample response
    return jsonify({
        "status": "success",
        "transcription": transcription,
        "emotion_analysis": emotions
    })

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:


def generate_feedback(emotion_analysis, filler_words_count, eye_contact):
    feedback = []
    
    if eye_contact < 50:
        feedback.append("You need to improve your eye contact during the interview.")
    
    if filler_words_count > 10:
        feedback.append("Try to minimize the use of filler words like 'um', 'uh', and 'like'.")
    
    if any(emotion['label'] == 'sadness' for emotion in emotion_analysis):
        feedback.append("Try to project more confidence in your tone.")

    return feedback


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




