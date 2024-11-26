FROM python:3.10-slim

WORKDIR /app

# Install necessary tools
RUN apt-get update && apt-get install -y curl

# Download the specific file from the GitHub repository
RUN curl -o filler_words.py https://raw.githubusercontent.com/Chanthuru2023/AI-in-mock-interview/Dilpreet/filler_words.py

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Run the Streamlit app
CMD ["streamlit", "run", "filler_words.py", "--server.port=8502", "--server.address=0.0.0.0"]
