import React from 'react';
import { ClerkProvider, UserButton } from "@clerk/nextjs";
import AddNewInterview from './_components/AddNewInterview';
import InterviewList from './_components/InterviewList';

function Dashboard() {
  return (
    <div className='p-10 bg-gray-100 min-h-screen'>
      {/* Header Section */}
      <h2 className='font-bold bg-gradient-to-r from-purple-500 to-indigo-600 text-white text-3xl p-4 rounded-lg shadow-md'>
        Dashboard
      </h2>
      <h2 className='font-semibold text-xl text-gray-600 mt-2'>
        Create and Start your AI Mock Interview
      </h2>

      {/* Add New Interview Section */}
      <div className='grid grid-cols-1 md:grid-cols-3 my-8'>
        <div className="bg-gradient-to-r from-green-500 to-blue-500 text-black py-4 px-6 rounded-lg shadow-lg hover:from-green-600 hover:to-blue-600 transition-all duration-300 cursor-pointer text-center">
          <AddNewInterview /> {/* Button styled to match the design */}
        </div>
      </div>

      {/* Interview List Section */}
      <div className='bg-white p-6 rounded-lg shadow-md'>
        <InterviewList />
      </div>
    </div>
  );
}

export default Dashboard;
