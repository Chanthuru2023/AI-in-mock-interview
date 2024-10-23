#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install opencv-python mediapipe


# In[2]:


pip install protobuf==3.20.3


# In[ ]:


import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe segmentation solution
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Set the desired frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from webcam. Exiting...")
        break

    # Convert the image from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get segmentation results
    results = selfie_segmentation.process(rgb_frame)

    # Create a mask from the segmentation results
    mask = results.segmentation_mask

    # Resize the mask to match the frame size
    mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

    # Convert the mask to binary format with a threshold
    _, binary_mask = cv2.threshold(mask, 0.5, 1, cv2.THRESH_BINARY)
    binary_mask = binary_mask.astype(np.uint8)

    # Refine the mask using a dilation operation to smooth the edges
    kernel = np.ones((15, 15), np.uint8)
    dilated_mask = cv2.dilate(binary_mask, kernel, iterations=1)

    # Invert the mask for background
    inverse_mask = cv2.bitwise_not(dilated_mask)

    # Apply a strong blur effect to the entire frame
    blurred_background = cv2.GaussianBlur(frame, (45, 45), 0)

    # Extract the foreground (user) from the original frame using the mask
    foreground = cv2.bitwise_and(frame, frame, mask=dilated_mask)

    # Extract the background from the blurred frame using the inverse mask
    background = cv2.bitwise_and(blurred_background, blurred_background, mask=inverse_mask)

    # Combine the foreground and blurred background
    output_frame = cv2.add(foreground, background)

    # Display the result
    cv2.imshow('Enhanced Background Blur', output_frame)

    # Exit when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()

