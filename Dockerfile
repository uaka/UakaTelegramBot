# Use the official Python 3.9 slim image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Make sure the session file is included if you're using one with instaloader
# COPY your_instagram_username.session .

# Run the main script, which triggers both instaLoader.py and StoriesChannel.py
CMD ["python", "run_all.py"]


