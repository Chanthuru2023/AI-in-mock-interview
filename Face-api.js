import React, { useRef, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import * as faceapi from 'face-api.js'; // Import Face-api.js

function EmotionDetection() {
  const webcamRef = useRef(null);
  const [emotion, setEmotion] = useState(''); // State to store detected emotion

  // Load Face-api.js models
  useEffect(() => {
    const loadModels = async () => {
      const MODEL_URL = '/public/models/'; // Path to your models (download from Face-api.js)
      await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
      await faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL);
    };

    loadModels();
  }, []);

  // Detect emotions on the video feed
  const detectEmotion = async () => {
    if (webcamRef.current && webcamRef.current.video.readyState === 4) {
      const video = webcamRef.current.video;

      const detections = await faceapi.detectSingleFace(video, new faceapi.TinyFaceDetectorOptions()).withFaceExpressions();

      if (detections && detections.expressions) {
        const maxEmotion = Object.entries(detections.expressions).reduce((prev, curr) =>
          curr[1] > prev[1] ? curr : prev
        );
        setEmotion(maxEmotion[0]); // Set the detected emotion
      }
    }
  };

  // Detect emotions continuously at intervals
  useEffect(() => {
    const interval = setInterval(() => {
      detectEmotion();
    }, 1000); // Run every second

    return () => clearInterval(interval); // Cleanup
  }, []);

  return (
    <div className="emotion-detection">
      <h2>Real-time Emotion Detection</h2>
      <Webcam ref={webcamRef} style={{ width: 640, height: 480 }} />
      <p>Detected Emotion: {emotion}</p> {/* Display detected emotion */}
    </div>
  );
}

export default EmotionDetection;
