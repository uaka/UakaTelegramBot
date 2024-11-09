import subprocess
# Run instaLoader.py to download stories
subprocess.run(["pythonProject/.venv/bin/python", "instaLoader.py"])

# Run StoriesChannel.py to post downloaded stories
subprocess.run(["pythonProject/.venv/bin/python", "StoriesChannel.py"])