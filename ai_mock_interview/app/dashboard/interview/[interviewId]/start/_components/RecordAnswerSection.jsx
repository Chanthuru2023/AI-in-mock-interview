"use client"; // Ensure this is a Client Component

import React, { useRef, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { useUser } from '@clerk/nextjs';
import * as faceapi from 'face-api.js';
import moment from 'moment';

function RecordAnswerSection({ mockInterviewQuestions, activeQuestionIndex, interviewData }) {
  const webcamRef = useRef(null);
  const [modelsLoaded, setModelsLoaded] = useState(false);
  const EAR_HISTORY = useRef([]);
  const ANGLE_HISTORY = useRef([]);
  const { user } = useUser();

  // Load models on component mount
  useEffect(() => {
    const loadModels = async () => {
      try {
        await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
        console.log('FaceAPI models loaded successfully');
        setModelsLoaded(true); // Mark models as loaded
      } catch (error) {
        console.error('Error loading FaceAPI models:', error);
      }
    };
    loadModels();
  }, []);

  // Continuous detection with a safeguard for model loading and readiness
  useEffect(() => {
    const intervalId = setInterval(async () => {
      if (modelsLoaded && webcamRef.current && webcamRef.current.video.readyState === 4) {
        await detectFacesAndGaze();
      }
    }, 500); // Check every 500ms

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, [modelsLoaded]);

  const detectFacesAndGaze = async () => {
    try {
      const video = webcamRef.current.video;
      const detections = await faceapi
        .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions())
        .withFaceLandmarks();

      if (!detections || !detections.landmarks) {
        console.warn('No face or landmarks detected');
        return;
      }

      const landmarks = detections.landmarks;
      const leftEye = landmarks.getLeftEye();
      const rightEye = landmarks.getRightEye();

      if (!leftEye || !rightEye) {
        console.warn('Eye landmarks are not available');
        return;
      }

      console.log('Left Eye Coordinates:', leftEye);
      console.log('Right Eye Coordinates:', rightEye);

      const leftEAR = calculateEAR(leftEye);
      const rightEAR = calculateEAR(rightEye);
      const eyeAngle = calculateAngle(
        getMidpoint(leftEye[0], leftEye[3]),
        getMidpoint(rightEye[0], rightEye[3])
      );

      console.log('Left EAR:', leftEAR, 'Right EAR:', rightEAR, 'Eye Angle:', eyeAngle);

      EAR_HISTORY.current.push(Math.abs(leftEAR - rightEAR));
      ANGLE_HISTORY.current.push(eyeAngle);

      if (EAR_HISTORY.current.length > 10) EAR_HISTORY.current.shift();
      if (ANGLE_HISTORY.current.length > 10) ANGLE_HISTORY.current.shift();

      const isLookingForward = analyzeGaze(EAR_HISTORY.current, ANGLE_HISTORY.current);
      if (!isLookingForward) {
        toast('Please look at the screen to avoid reading from another source.');
      }
    } catch (error) {
      console.error('Error during detection:', error);
    }
  };

  const calculateEAR = (eye) => {
    const width = Math.hypot(eye[3].x - eye[0].x, eye[3].y - eye[0].y);
    const height1 = Math.hypot(eye[1].x - eye[5].x, eye[1].y - eye[5].y);
    const height2 = Math.hypot(eye[2].x - eye[4].x, eye[2].y - eye[4].y);
    return (height1 + height2) / (2.0 * width);
  };

  const calculateAngle = (pointA, pointB) => {
    const deltaY = pointB.y - pointA.y;
    const deltaX = pointB.x - pointA.x;
    return Math.atan2(deltaY, deltaX) * (180 / Math.PI);
  };

  const getMidpoint = (pointA, pointB) => ({
    x: (pointA.x + pointB.x) / 2,
    y: (pointA.y + pointB.y) / 2,
  });

  const analyzeGaze = (earHistory, angleHistory) => {
    const earDeviation = Math.max(...earHistory) - Math.min(...earHistory);
    const angleDeviation = Math.max(...angleHistory) - Math.min(...angleHistory);

    const earThreshold = 0.05;
    const angleThreshold = 10;

    return earDeviation < earThreshold && angleDeviation < angleThreshold;
  };

  return (
    <div className="flex flex-col items-center">
      <div className="relative my-4">
        <Webcam ref={webcamRef} className="border rounded-lg" audio={false} />
      </div>
      <Button onClick={detectFacesAndGaze}>Test Detection</Button>
    </div>
  );
}

export default RecordAnswerSection;
