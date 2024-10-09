"use client";
import { db } from "@/utils/db";
import { UserAnswer } from "@/utils/schema";
import React, { useState, useEffect } from "react";
import { eq } from "drizzle-orm"; // Import eq for query filtering
import { useRouter } from "next/navigation";

function Feedback({ params }) {
  const [feedbackData, setFeedbackData] = useState(null); // State for feedback data
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state
  const [overallRating, setOverallRating] = useState(0); // State for overall rating
  const [expandedQuestions, setExpandedQuestions] = useState({}); // State to track expanded questions
  const router = useRouter();

  useEffect(() => {
    GetFeedback();
  }, []); // Fetch feedback on component mount

  // Function to fetch feedback from the database
  const GetFeedback = async () => {
    try {
      const result = await db
        .select()
        .from(UserAnswer)
        .where(eq(UserAnswer.mockIdRef, params.interviewId))
        .orderBy(UserAnswer.id); // Order results by ID

      console.log("Feedback Data:", result);
      setFeedbackData(result); // Store feedback data in state

      // Calculate overall rating
      const totalRating = result.reduce((acc, curr) => {
        const rating = curr.rating.split("/")[0]; // Extracting the first part of rating (e.g., "1" from "1/5")
        return acc + parseInt(rating);
      }, 0);
      const averageRating = totalRating / result.length;
      setOverallRating(averageRating.toFixed(1)); // Set the overall rating
    } catch (error) {
      console.error("Error fetching feedback:", error);
      setError("Failed to load feedback data.");
    } finally {
      setLoading(false); // Set loading to false when the fetch is complete
    }
  };

  // Function to toggle the visibility of results
  const toggleQuestion = (index) => {
    setExpandedQuestions((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  // Function to get the color based on rating
  const getRatingColor = (rating) => {
    const value = parseInt(rating.split("/")[0]); // Get the numeric part of the rating
    const maxRating = 5; // Set the maximum rating value
    const percentage = (value / maxRating) * 100; // Calculate the percentage

    // Determine the color based on the percentage
    if (percentage <= 40) return "bg-red-200"; // Red for poor ratings (0-2)
    if (percentage <= 80) return "bg-yellow-200"; // Yellow for average ratings (2.5-4)
    return "bg-green-200"; // Green for good ratings (4.5-5)
  };

  // Function to get the color for overall rating question
  const getOverallRatingColor = (rating) => {
    const value = parseFloat(rating);
    const percentage = (value / 5) * 100; // Calculate the percentage based on a 5-point scale

    // Determine the color for the overall rating
    if (percentage <= 40) return "text-red-600"; // Red for poor ratings
    if (percentage <= 80) return "text-yellow-600"; // Yellow for average ratings
    return "text-green-600"; // Green for good ratings
  };

  // Function to aggregate feedback data to get unique questions with highest ratings
  const aggregateFeedback = (feedback) => {
    const uniqueQuestions = {};

    feedback.forEach((item) => {
      const question = item.question;
      const ratingValue = parseInt(item.rating.split("/")[0]); // Get the numeric rating

      // Check if the question is already in the uniqueQuestions object
      if (!uniqueQuestions[question] || ratingValue > uniqueQuestions[question].ratingValue) {
        // If it doesn't exist or the current rating is higher, update it
        uniqueQuestions[question] = {
          userAnswer: item.userAnswer,
          feedback: item.feedback,
          correctAnswer: item.correctAnswer,
          rating: item.rating,
          ratingValue, // Store the numeric rating for comparison
        };
      }
    });

    return Object.entries(uniqueQuestions).map(([question, data]) => ({
      question,
      ...data,
    })); // Convert back to an array
  };

  // Display loading message while data is being fetched
  if (loading) {
    return <div className="text-center text-lg font-semibold">Loading feedback...</div>;
  }

  // Display error message if there's an error
  if (error) {
    return <div className="text-center text-lg font-semibold text-red-600">{error}</div>;
  }

  // Aggregate feedback to get unique questions with the highest rating
  const aggregatedFeedbackData = aggregateFeedback(feedbackData);

  return (
    <div className="max-w-full mx-auto p-5 bg-white rounded-lg shadow-lg"> {/* Increased width */}
      <h2 className="text-3xl font-bold text-green-600 text-center">Congratulations!</h2>
      <h2 className="font-bold text-2xl text-center mt-2">Here is your interview feedback</h2>
      <h2 className={`text-lg my-3 ${getOverallRatingColor(overallRating)} text-center`}>
        Your overall interview rating: <strong>{overallRating}/5</strong> {/* Display overall rating */}
      </h2>
      <h2 className="text-sm text-gray-500 text-center mb-4">
        Below are the interview questions, your answers, and feedback for improvement.
      </h2>

      {/* Display aggregated feedback data if available */}
      {aggregatedFeedbackData && aggregatedFeedbackData.length > 0 ? (
        <div>
          {aggregatedFeedbackData.map((answer, index) => (
            <div
              key={index}
              className="my-4 border border-gray-300 rounded-md shadow-md transition-all duration-300 hover:shadow-xl p-4"
            >
              <h3
                className="font-bold text-lg cursor-pointer hover:text-blue-600"
                onClick={() => toggleQuestion(index)} // Toggle results on click
              >
                Question {index + 1}{" "}
                {expandedQuestions[index] ? "▼" : "►"} {/* Indicator for expansion */}
              </h3>
              {/* Always display the question */}
              <div className="border-b border-gray-200 mb-2 pb-2">
                <strong className="text-gray-800">Question:</strong> {answer.question} {/* Display question */}
              </div>
              {/* Display results and toggle visibility based on expanded state */}
              {expandedQuestions[index] && (
                <div className="mt-2">
                  <div className="border rounded-md p-2 mb-2 bg-blue-100"> {/* Background color for "Your Answer" */}
                    <strong>Your Answer:</strong>{" "}
                    {answer.userAnswer ? answer.userAnswer : "No answer provided"} {/* Check userAnswer */}
                  </div>
                  <div className="border rounded-md p-2 mb-2 bg-yellow-100"> {/* Background color for "Feedback" */}
                    <strong>Feedback:</strong> {answer.feedback}
                  </div>
                  <div className="border rounded-md p-2 mb-2 bg-green-100"> {/* Background color for "Correct Answer" */}
                    <strong>Correct Answer:</strong> {answer.correctAnswer || "N/A"} {/* Display correct answer */}
                  </div>
                  <div className={`border rounded-md p-2 mb-2 ${getRatingColor(answer.rating)}`}> {/* Dynamic background color for "Rating" */}
                    <strong>Rating:</strong> {answer.rating || "N/A"} {/* Display rating */}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-center text-lg font-semibold">No feedback available.</p> // Message for no feedback
      )}
      
      <button
        className="mt-4 bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 transition duration-300"
        onClick={() => router.replace('/dashboard')} // Navigate to the dashboard
      >
        Go Home
      </button>
    </div>
  );
}

export default Feedback;
