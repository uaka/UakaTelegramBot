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

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

# Set up Reddit API credentials
reddit = praw.Reddit(
    client_id = os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("TELEGRAM_BOT"),
    check_for_async=False
)
# Telegram bot token and channel ID
TOKEN = os.getenv("PETMEMES_TOKEN")  # Bot token
CHANNEL_ID = os.getenv("PETMEMES_CHANNEL_ID")  # Channel ID with `-100` prefix

# Initialize bot
bot = Bot(token=TOKEN)

def fetch_random_meme():
    try:
        subreddit = reddit.subreddit("AnimalMemes")
        posts = list(subreddit.hot(limit=30))  # Fetch top 30 posts
    except RedditAPIException as e:
        print(f"Reddit API error: {e}")
        time.sleep(60)  # Wait for 1 minute before retrying

    random_post = random.choice(posts)
    print("WE WILL POST THIS TO YOUR CHANNEL", random_post.title, random_post.url)
    return random_post.title, random_post.url  # Return the title and image URL

#______________________
def post_to_channel(title, meme_url):
    try:
        # Post meme to Telegram channel
        bot.send_message(chat_id=CHANNEL_ID, text=title)
        bot.send_photo(chat_id=CHANNEL_ID, photo=meme_url)
        print("Posted meme to Telegram channel.")
    except Exception as e:
        print(f"Error posting to Telegram: {e}")
#______________________
async def scheduled_post(context):
    # Fetch a random meme
    title, meme_url = fetch_random_meme()
    if title and meme_url:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=meme_url, caption=title)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Schedule the job to run every 6 hours
    app.job_queue.run_repeating(scheduled_post, interval=21600)  # 21600 seconds = 6 hours

    app.run_polling()

if __name__ == "__main__":
    main()
