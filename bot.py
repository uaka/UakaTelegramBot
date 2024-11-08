import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
USERNAME = os.getenv("USERNAME")
TOKEN = os.getenv("TOKEN")
# Define the function to post the latest stories to a Telegram channel
async def post_story(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    folder = f"{USERNAME}_stories" # Make sure this matches your actual download folder name

    # Check if folder exists and contains files
    if os.path.exists(folder) and os.listdir(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                # Check if the file is an image or a video and send accordingly
                if filename.endswith('.jpg'):
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(file_path, 'rb'))
                elif filename.endswith('.mp4'):
                    await context.bot.send_video(chat_id=update.effective_chat.id, video=open(file_path, 'rb'))

                # Optional: Delete the file after sending to avoid re-posting
                os.remove(file_path)

        await update.message.reply_text("Stories have been posted to Telegram.")
    else:
        await update.message.reply_text("No new stories available to post.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("poststory", post_story))

    app.run_polling()


if __name__ == "__main__":
    main()
