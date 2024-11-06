import pytest
from unittest.mock import patch, Mock
from functions import send_prompt_to_ai, save_to_db

# Test case for sending the prompt to the AI
@patch('functions.requests.post')
def test_send_prompt_to_ai(mock_post):
    # Simulate a successful API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "questions": [
            {"question": "What is Python?", "answer": "Python is a programming language."}
        ]
    }
    mock_post.return_value = mock_response

    # Call the function
    prompt = "Generate interview questions for a Python developer."
    result = send_prompt_to_ai(prompt)

    # Assertions
    assert result is not None
    assert "questions" in result
    assert result["questions"][0]["question"] == "What is Python?"

# Test case for handling invalid JSON from the AI
@patch('functions.requests.post')
def test_send_prompt_to_ai_invalid_json(mock_post):
    # Simulate an API response with invalid JSON
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_post.return_value = mock_response

    prompt = "Generate interview questions for a Java developer."

    # Assert that the function raises a ValueError when the JSON is invalid
    with pytest.raises(ValueError, match="Invalid JSON received from AI"):
        send_prompt_to_ai(prompt)

# Test case for saving to the database
def test_save_to_db():
    # Call the function with valid data
    data = {"questions": ["What is Python?"]}
    job_position = "Python Developer"
    job_description = "Develops Python applications"
    job_experience = "3 years"

    saved_id = save_to_db(data, job_position, job_description, job_experience)

    # Assertions
    assert saved_id == "mock_id_12345"

# Test case for saving to the database with no data
def test_save_to_db_no_data():
    with pytest.raises(ValueError, match="No data to save"):
        save_to_db(None, "Python Developer", "Develops Python apps", "3 years")
