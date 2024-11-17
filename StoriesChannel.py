import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables from the .env file
load_dotenv()

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Convert to int if needed
USERNAME = os.getenv("USERNAME")
TOKEN = os.getenv("TOKEN")

# File path for tracking posted stories
TRACK_POSTED_STORIES_FILE = "posted_story_ids.txt"

# Initialize tracking file if it doesn't exist
if not os.path.exists(TRACK_POSTED_STORIES_FILE):
    open(TRACK_POSTED_STORIES_FILE, 'w').close()

# Helper function to load posted story IDs
def load_posted_story_ids():
    with open(TRACK_POSTED_STORIES_FILE, 'r') as f:
        return set(f.read().splitlines())

# Helper function to add a new story ID to the tracking file
def save_posted_story_id(story_id):
    with open(TRACK_POSTED_STORIES_FILE, 'a') as f:
        f.write(f"{story_id}\n")

# Define the function to post the latest stories to the Telegram channel
async def post_story(context: ContextTypes.DEFAULT_TYPE) -> None:
    folder = f"{USERNAME}_stories"  # Folder where stories are downloaded
    posted_story_ids = load_posted_story_ids()

    # Check if folder exists and contains files
    if os.path.exists(folder) and os.listdir(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            story_id = os.path.splitext(filename)[0]  # Use filename (without extension) as story ID

            # Skip if this story was already posted
            if story_id in posted_story_ids:
                logging.info(f"Skipping already posted story: {filename}")
                continue

            if os.path.isfile(file_path):
                try:
                    # Send the file based on type
                    with open(file_path, 'rb') as file:
                        if filename.endswith('.jpg'):
                            await context.bot.send_photo(chat_id=CHANNEL_ID, photo=file)
                        elif filename.endswith('.mp4'):
                            await context.bot.send_video(chat_id=CHANNEL_ID, video=file)

                    # Mark story as posted
                    save_posted_story_id(story_id)
                    logging.info(f"Posted and saved story ID: {story_id}")

                    # Optional: Delete the file after sending to avoid re-posting
                    os.remove(file_path)
                    logging.info(f"Deleted file after posting: {filename}")

                except Exception as e:
                    logging.error(f"Failed to post {filename}: {e}")
    else:
        logging.info("No new stories available to post.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Schedule the post_story function to run periodically (e.g., every 10 minutes)
    app.job_queue.run_repeating(post_story, interval=60)  # interval is in seconds (600s = 10 min)

    app.run_polling()

if __name__ == "__main__":
    main()
