# Step 1: Use the official Python image from Docker Hub
FROM python:3.8-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the local directory contents into the container at /app
COPY . /app

# Step 4: Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port Streamlit will run on (default 8501)
EXPOSE 8501

# Step 6: Define the command to run your app
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false"]
