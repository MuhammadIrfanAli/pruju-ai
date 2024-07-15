#!/bin/bash

# Start the FastAPI application
uvicorn api:app_fastapi --host 0.0.0.0 --port 6500 --reload  &

# Start another command, replace with your actual command
gradio app.py
