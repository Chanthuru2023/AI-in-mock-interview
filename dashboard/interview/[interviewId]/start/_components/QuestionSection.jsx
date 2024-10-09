import { Lightbulb, Volume2 } from 'lucide-react';
import React from 'react';

function QuestionSection({ mockInterviewQuestions, activeQuestionIndex }) {
  const textToSpeech=(text)=>{
    if('speechSynthesis' in window){

        const speech=new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(speech)
    }
    else{
        alert('Sorry, Your browser does not support speech to text')
    }

  }
    return (
    <div className='p-5 border rounded-lg my-5'>
      <div className='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5'>
        {mockInterviewQuestions && mockInterviewQuestions.length > 0 ? (
          mockInterviewQuestions.map((questionObj, index) => (
            <div key={index} className="mb-4">
              {/* Use a predefined Tailwind color or your custom class */}
              <h2 
                className={`p-2 rounded-full font-bold text-center cursor-pointer ${activeQuestionIndex === index ? 'bg-blue-500 text-white' : 'bg-secondary'}`}
              >
                Question #{index + 1}
              </h2>

     
            </div>
            
          ))
        ) : (
          <p>No questions available.</p>
        )}
      </div>
      <h2 className='my-5 text-md md:text-lg'>{mockInterviewQuestions[activeQuestionIndex]?.question} </h2>
      <Volume2 className='cursor-pointer' onClick={()=>(textToSpeech(mockInterviewQuestions[activeQuestionIndex]?.question))}/>
      <div>
        
      </div>
    </div>
    
  );
}

export default QuestionSection;
