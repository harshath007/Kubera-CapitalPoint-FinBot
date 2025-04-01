# Use the official Streamlit image from Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Run Streamlit when the container starts
CMD ["streamlit", "run", "streamlit_app.py"]
