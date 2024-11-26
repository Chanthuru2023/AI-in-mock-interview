FROM python:3.10-slim

WORKDIR /app

# Install necessary tools
RUN apt-get update && apt-get install -y curl

# Download the specific file from the GitHub repository
RUN curl -o EyeDetection.ipynb https://raw.githubusercontent.com/Chanthuru2023/AI-in-mock-interview/Jaskaran/Eye%20Detection.ipynb

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Run Jupyter Notebook (you may need to adjust this depending on your setup)
CMD ["jupyter", "notebook", "EyeDetection.ipynb", "--ip=0.0.0.0", "--port=8503", "--no-browser", "--allow-root"]
