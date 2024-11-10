from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/check_stories', methods=['GET'])
def check_stories():
    try:
        # Run instaLoader.py to download stories
        subprocess.run(["python", "instaLoader.py"])

        # Run StoriesChannel.py to post downloaded stories
        subprocess.run(["python", "StoriesChannel.py"])

        return "Stories checked and posted if any updates found.", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    # Run the Flask app on port 8080 (Fly.io default)
    app.run(host='0.0.0.0', port=8080)
