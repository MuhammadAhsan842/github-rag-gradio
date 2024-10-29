# Use an official Python image as the base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code and the .env file
COPY . /app
COPY .env /app/.env

# Expose the port that Gradio and Flask will run on
EXPOSE 7860

# Run the Gradio app
CMD ["python", "github_rag_gradio.py"]

