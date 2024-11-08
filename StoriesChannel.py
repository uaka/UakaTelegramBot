import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Convert to int if needed
USERNAME = os.getenv("USERNAME")
TOKEN = os.getenv("TOKEN")

# File path for tracking posted stories
TRACK_FILE = "posted_story_ids.txt"

# Initialize tracking file if it doesn't exist
if not os.path.exists(TRACK_FILE):
    open(TRACK_FILE, 'w').close()


# Helper function to load posted story IDs
def load_posted_story_ids():
    with open(TRACK_FILE, 'r') as f:
        return set(f.read().splitlines())


# Helper function to add a new story ID to the tracking file
def save_posted_story_id(story_id):
    with open(TRACK_FILE, 'a') as f:
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
                print(f"Skipping already posted story: {filename}")
                continue

            if os.path.isfile(file_path):
                # Check if the file is an image or a video and send accordingly
                if filename.endswith('.jpg'):
                    await context.bot.send_photo(chat_id=CHANNEL_ID, photo=open(file_path, 'rb'))
                elif filename.endswith('.mp4'):
                    await context.bot.send_video(chat_id=CHANNEL_ID, video=open(file_path, 'rb'))

                # Mark story as posted
                save_posted_story_id(story_id)
                print(f"Posted and saved story ID: {story_id}")

                # Optional: Delete the file after sending to avoid re-posting
                os.remove(file_path)
    else:
        print("No new stories available to post.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Schedule the post_story function to run periodically (every 10 minutes as an example)
    app.job_queue.run_repeating(post_story, interval=10)  # interval is in seconds

    app.run_polling()


if __name__ == "__main__":
    main()