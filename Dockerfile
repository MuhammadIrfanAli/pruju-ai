# Use an official Python runtime as the base image
FROM python:3.10.6

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 7860

# Run app.py when the container launches
CMD ["gradio", "app.py"]