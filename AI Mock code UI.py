#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter
print(tkinter.TkVersion)


# In[2]:


import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[3]:


class MockInterviewApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AI-Powered Mock Interview Tool")

        self.question_label = tk.Label(master, text="Interview Question:")
        self.question_label.pack(pady=10)

        self.answer_label = tk.Label(master, text="Your Answer:")
        self.answer_label.pack(pady=10)

        self.answer_text = tk.Text(master, height=5, width=50)
        self.answer_text.pack(pady=10)

        self.submit_button = tk.Button(master, text="Submit Answer", command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.next_button = tk.Button(master, text="Next Question", command=self.next_question)
        self.next_button.pack(pady=10)

        self.results_label = tk.Label(master, text="")
        self.results_label.pack(pady=10)

        self.actual_answers = {
            "What is your greatest strength?": "My greatest strength is my ability to learn quickly and adapt to new situations.",
            "Describe a challenge you faced at work.": "I faced a challenge when I had to complete a project with a tight deadline, but I prioritized tasks effectively and collaborated with my team to meet the deadline."
        }
        self.questions = list(self.actual_answers.keys())
        self.current_question_index = -1

        self.next_question()

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question)
            self.answer_text.delete(1.0, tk.END)
            self.results_label.config(text="")
        else:
            messagebox.showinfo("End of Interview", "Thank you for participating!")
            self.master.quit()

    def submit_answer(self):
        user_answer = self.answer_text.get(1.0, tk.END).strip()
        if user_answer:
            actual_answer = self.actual_answers[self.questions[self.current_question_index]]
            similarity_score = self.calculate_similarity(user_answer, actual_answer)
            self.results_label.config(text=f"Similarity Score: {similarity_score:.2f}")
            if similarity_score > 0.7:  # Adjust threshold as needed
                messagebox.showinfo("Result", "Your answer is quite similar to the expected answer.")
            else:
                messagebox.showinfo("Result", "Your answer differs from the expected answer.")
        else:
            messagebox.showwarning("Warning", "Please provide an answer.")

    def calculate_similarity(self, user_answer, actual_answer):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([user_answer, actual_answer])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]  # Return the similarity score

if __name__ == "__main__":
    root = tk.Tk()
    app = MockInterviewApp(root)
    root.mainloop()


# In[4]:


python mock_interview_gui.py

