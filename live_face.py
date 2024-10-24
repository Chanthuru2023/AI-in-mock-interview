import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the pre-trained model
model = load_model('emotion_model.h5')  # Ensure this file is in your working directory
emotion_labels = ['Happy', 'Sad', 'Neutral', 'Surprise']

# Start video capture
cap = cv2.VideoCapture(0)  # Ensure your webcam is accessible

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_roi = gray_frame[y:y + h, x:x + w]
        face_roi = cv2.resize(face_roi, (48, 48))
        face_roi = face_roi.astype('float32') / 255.0
        face_roi = np.expand_dims(face_roi, axis=-1)
        face_roi = np.expand_dims(face_roi, axis=0)

        # Predict emotion
        predictions = model.predict(face_roi)
        emotion_index = np.argmax(predictions)
        emotion = emotion_labels[emotion_index]

        # Display emotion on the frame
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        print(emotion)

    # Display the resulting frame
    cv2.imshow('Live Facial Expression Recognition', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting the application...")
        break

cap.release()
cv2.destroyAllWindows()
