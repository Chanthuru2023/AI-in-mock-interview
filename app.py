from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import speech_recognition as sr
from pydub import AudioSegment
import ffmpeg
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Simulating roles, questions, and predefined keywords
roles_questions = {
    'Data Scientist': {
        'questions': [
            {"text": "Explain supervised learning.", "keywords": ["supervised", "training", "label", "classification", "regression"]},
            {"text": "What is a confusion matrix?", "keywords": ["confusion", "matrix", "accuracy", "precision", "recall"]},
        ]
    },
    'Software Engineer': {
        'questions': [
            {"text": "What is object-oriented programming?", "keywords": ["object", "class", "inheritance", "polymorphism", "encapsulation"]},
            {"text": "Explain the concept of recursion.", "keywords": ["recursion", "function", "base", "case", "stack"]},
        ]
    },
    'Product Manager': {
        'questions': [
            {"text": "Describe a go-to-market strategy.", "keywords": ["go-to-market", "strategy", "launch", "customer", "market"]},
            {"text": "How do you prioritize product features?", "keywords": ["prioritize", "features", "roadmap", "impact", "effort"]},
        ]
    }
}

@app.route('/')
def index():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username

        if username == 'admin' and password == 'admin':
            return redirect(url_for('admin_panel'))

        return redirect(url_for('choose_role'))
    return render_template('login.html')

# Admin panel route
@app.route('/admin_panel')
def admin_panel():
    if 'username' in session and session['username'] == 'admin':
        return render_template('admin_panel.html')
    return redirect(url_for('login'))

@app.route('/choose_role', methods=['GET', 'POST'])
def choose_role():
    if request.method == 'POST':
        role = request.form['role']
        session['role'] = role
        session['current_question'] = 0
        return redirect(url_for('questions'))
    return render_template('choose_role.html', roles=roles_questions.keys())

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    role = session['role']
    current_question = session['current_question']
    question = roles_questions[role]['questions'][current_question]
    
    return render_template('interview.html', role=role, question=question['text'])

@app.route('/upload_video', methods=['POST'])
def upload_video():
    # Save uploaded video
    file = request.files['file']
    video_path = os.path.join("uploads", file.filename)
    file.save(video_path)

    # Convert video to audio
    audio_path = video_path.replace('.webm', '.wav')
    ffmpeg.input(video_path).output(audio_path).run()

    # Transcribe audio
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_path)
    with audio as source:
        recorded_audio = recognizer.record(source)
    transcribed_text = recognizer.recognize_google(recorded_audio)

    # Save transcribed text
    transcript_path = video_path.replace('.webm', '.txt')
    with open(transcript_path, 'w') as f:
        f.write(transcribed_text)

    # Check transcribed text against predefined keywords
    role = session['role']
    current_question = session['current_question']
    keywords = roles_questions[role]['questions'][current_question]['keywords']

    missing_keywords = [kw for kw in keywords if kw.lower() not in transcribed_text.lower()]

    # Calculate score based on matched keywords
    matched_keywords = [kw for kw in keywords if kw.lower() in transcribed_text.lower()]
    score = round(len(matched_keywords) / len(keywords) * 100, 2)

    # Move to next question if any
    session['current_question'] += 1 if session['current_question'] + 1 < len(roles_questions[role]['questions']) else 0

    return jsonify({
        'transcribed_text': transcribed_text,
        'missing_keywords': missing_keywords,
        'score': score,
        'is_answer_correct': len(missing_keywords) == 0
    })

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
