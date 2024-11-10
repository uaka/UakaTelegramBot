import subprocess
# Run instaLoader.py to download stories
subprocess.run(["python", "instaLoader.py"])

# Run StoriesChannel.py to post downloaded stories
subprocess.run(["python", "StoriesChannel.py"])