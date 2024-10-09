"use client"; // Ensure this component is client-side

import { db } from '@/utils/db';
import { MockInterview } from '@/utils/schema';
import { useUser } from '@clerk/nextjs';
import { eq, desc } from 'drizzle-orm';
import React, { useEffect, useState } from 'react';
import InterviewItemCard from './interviewItemCard';

function InterviewList() {
  const { user } = useUser();
  const [interviewList, setInterviewList] = useState([]);
  const [error, setError] = useState(null); // State for handling errors

  useEffect(() => {
    if (user) {
      console.log("User's primary email address object: ", user?.primaryEmailAddress);
      console.log("User's actual email: ", user?.primaryEmailAddress?.emailAddress); // Log the actual email
      GetInterviewList();
    }
  }, [user]);

  const GetInterviewList = async () => {
    try {
      // Use the actual email string for filtering
      const filteredResult = await db.select()
        .from(MockInterview)
        .where(eq(MockInterview.createdBy, user?.primaryEmailAddress?.emailAddress)) // Access email string
        .orderBy(desc(MockInterview.id));

      console.log("Filtered interviews: ", filteredResult);
      setInterviewList(filteredResult);
    } catch (error) {
      console.error('Error fetching interview list:', error);
      setError('Failed to fetch interview list.'); // Set error message
    }
  };

  return (
    <div>
      <h2 className='font-medium text-xl'>Previous Mock Interviews</h2>
      {error && <p className='text-red-500'>{error}</p>} {/* Show error message if there is one */}
      <div className='flex flex-wrap gap-4 mt-4'> {/* Flex container with gap between items */}
        {interviewList.map((interview, index) => (
          <InterviewItemCard key={interview.mockId} interview={interview} /> // Pass the interview prop and add a key
        ))}
      </div>
    </div>
  );
}

export default InterviewList;
