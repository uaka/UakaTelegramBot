import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Convert to int if needed


# Define the function to post the latest stories to the Telegram channel
async def post_story(context: ContextTypes.DEFAULT_TYPE) -> None:
    folder = "uakaama_stories"  # Folder where stories are downloaded

    # Check if folder exists and contains files
    if os.path.exists(folder) and os.listdir(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                # Check if the file is an image or a video and send accordingly
                if filename.endswith('.jpg'):
                    await context.bot.send_photo(chat_id=CHANNEL_ID, photo=open(file_path, 'rb'))
                elif filename.endswith('.mp4'):
                    await context.bot.send_video(chat_id=CHANNEL_ID, video=open(file_path, 'rb'))

                # Optional: Delete the file after sending to avoid re-posting
                os.remove(file_path)

        # Log confirmation of posting
        print("Stories have been posted to the channel.")
    else:
        print("No new stories available to post.")


def main():
    app = ApplicationBuilder().token("7608645532:AAEiXOHsBNjhkVbgFwQU9S1CrF59TD4QHsc").build()

    # Schedule the post_story function to run periodically (every 10 minutes as an example)
    app.job_queue.run_repeating(post_story, interval=6)  # interval is in seconds

    app.run_polling()

    # app = ApplicationBuilder().token("7608645532:AAEiXOHsBNjhkVbgFwQU9S1CrF59TD4QHsc").post_init(lambda app: app.job_queue.start()).build()
    #
    # # Schedule the post_story function to run periodically (every 10 minutes as an example)
    # app.job_queue.run_repeating(post_story, interval=600)  # interval is in seconds
    #
    # app.run_polling()


if __name__ == "__main__":
    main()
