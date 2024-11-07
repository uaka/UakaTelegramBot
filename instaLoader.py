import instaloader
import os
from dotenv import load_dotenv

# Initialize Instaloader
L = instaloader.Instaloader()
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
L.login(USERNAME, PASSWORD)

# Download your own stories
def download_stories():
    try:
        for story in L.get_stories():
            for item in story.get_items():
                # Check if this is your story
                if item.owner_username == USERNAME:
                    L.download_storyitem(item, target=f"{USERNAME}_stories")
    except Exception as e:
        print("Error downloading stories:", e)

download_stories()
