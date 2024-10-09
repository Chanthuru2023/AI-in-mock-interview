"use client";
import React from 'react';
import { ClerkProvider, UserButton } from "@clerk/nextjs";
import AddNewInterview from './_components/AddNewInterview';
import InterviewList from './_components/InterviewList';



function Dashbord() {
  return (
    <div className='p-10'>

     <h2 className='font-bold text-2xl'>Dashboard</h2>
     <h2 className='font-semibold text-xl text-gray-500'>Create and Start your AI Mock Interview</h2>
     
     <div className='grid grid-cols-1 md:grid-cols-3 my-5'>
       <AddNewInterview/>
     </div>
     
     <InterviewList/>
      
    </div>
  )
}

export default Dashbord