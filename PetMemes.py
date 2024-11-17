import os
from datetime import time
from praw.exceptions import RedditAPIException
from telegram import Bot
from telegram.ext import ApplicationBuilder
import praw
import random
# Load environment variables
from dotenv import load_dotenv
import logging
import requests

# Initialize logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

# Set up Reddit API credentials
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("TELEGRAM_BOT"),
    check_for_async=False
)
# Telegram bot token and channel ID
TOKEN = os.getenv("PETMEMES_TOKEN")  # Bot token
CHANNEL_ID = os.getenv("PETMEMES_CHANNEL_ID")  # Channel ID with `-100` prefix

# Initialize bot
bot = Bot(token=TOKEN)

# List of subreddits to choose from
subreddits = ["AnimalMemes", "aww", "funnyanimals", "AnimalsBeingDerps"]
current_subreddit_index = 0


def fetch_random_meme(subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        posts = list(subreddit.hot(limit=30))  # Fetch top 30 posts
    except RedditAPIException as e:
        logging.error(f"Reddit API error: {e}")
        time.sleep(60)  # Wait for 1 minute before retrying

    random_post = random.choice(posts)
    logging.info(f"WE WILL POST THIS TO YOUR CHANNEL:  {random_post.title}, {random_post.url}")
    return random_post.title, random_post.url  # Return the title and image URL

# ______________________
async def scheduled_post(context):
    """Post a meme to Telegram and switch subreddit if no updates."""
    global current_subreddit_index
    try:
        # Get the current subreddit
        subreddit_name = subreddits[current_subreddit_index]
        logging.info(f"Fetching meme from subreddit: {subreddit_name}")

        # Fetch a meme
        title, meme_url = fetch_random_meme(subreddit_name)

        if title and meme_url:
            # Post to Telegram
            # await context.bot.send_photo(chat_id=CHANNEL_ID, photo=meme_url, caption=title)
            try:
                response = requests.head(meme_url)
                content_type = response.headers['Content-Type']
                if 'image' in content_type:
                    await context.bot.send_photo(chat_id=CHANNEL_ID, photo=meme_url, caption=title)
                elif 'video' in content_type:
                    await context.bot.send_video(chat_id=CHANNEL_ID, video=meme_url, caption=title)
            except Exception as e:
                logging.warning(f"ERROR SENDING MEDIA TO THE CHANNEL!!! {str(e)}")

            logging.info(f"Posted meme from {subreddit_name} to Telegram.")
        else:
            logging.warning(f"No memes found in subreddit: {subreddit_name}. Switching subreddit.")

            # Switch to the next subreddit
            current_subreddit_index = (current_subreddit_index + 1) % len(subreddits)

    except Exception as e:
        logging.error(f"Error fetching or posting meme: {e}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Schedule the job to run every 6 hours
    app.job_queue.run_repeating(scheduled_post, interval=600)  # 21600 seconds = 6 hours

    app.run_polling(poll_interval=15)  # Poll every 15 seconds


if __name__ == "__main__":
    main()
