import instaloader
import os
import logging
from dotenv import load_dotenv

# Configure logging to output to console
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Instaloader and load environment variables
L = instaloader.Instaloader()
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Login to Instagram
L.login(USERNAME, PASSWORD)

# Define the target download folder
TARGET_FOLDER = f"{USERNAME}_stories"

# Ensure the folder exists
if not os.path.exists(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)

# Download only unique videos from your own stories
def download_stories():
    try:
        for story in L.get_stories():
            for item in story.get_items():
                # Check if this is your story
                if item.owner_username == USERNAME:
                    # Create a unique story ID based on the filename without the extension
                    story_id = item.mediaid  # or use item.mediaid for a unique ID

                    # Construct the file path to check if the video is already downloaded
                    video_path = os.path.join(TARGET_FOLDER, f"{story_id}.mp4")
                    image_path = os.path.join(TARGET_FOLDER, f"{story_id}.jpg")

                    # If the video file exists, skip downloading any additional files with the same ID
                    if os.path.exists(video_path):
                        logging.info(f"Video for story ID {story_id} already exists. Skipping download of other formats.")
                        continue

                    # If an image with the same story ID exists, remove it and download only the video
                    if os.path.exists(image_path) and item.is_video:
                        os.remove(image_path)
                        logging.info(f"Removed image for story ID {story_id} to download video instead.")

                    # Download only if it's a video or if no other file with the same ID exists
                    if item.is_video:
                        L.download_storyitem(item, target=TARGET_FOLDER)
                        logging.info(f"Downloaded video for story ID {story_id}.")
                    else:
                        logging.info(f"Skipping image for story ID {story_id} as a video will be prioritized.")

    except Exception as e:
        logging.error(f"Error downloading stories: {e}")

# Run the download function
download_stories()
