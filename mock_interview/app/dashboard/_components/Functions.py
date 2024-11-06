import requests
import json

def send_prompt_to_ai(prompt):
    # Simulating an AI API call that returns interview questions in JSON format
    api_url = "https://api.example.com/generate-questions"
    response = requests.post(api_url, json={"prompt": prompt})
    
    if response.status_code == 200:
        try:
            # Parse and return the response as JSON
            return response.json()
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON received from AI")
    else:
        raise ConnectionError("Failed to connect to AI service")

def save_to_db(data, job_position, job_description, job_experience):
    # Simulating saving data to a database
    if not data:
        raise ValueError("No data to save")

    # Simulate database save logic
    saved_id = "mock_id_12345"
    return saved_id
