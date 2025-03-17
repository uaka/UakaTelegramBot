📌 Twitch Automated Test (WAP Testing)
This project automates Twitch mobile testing using Selenium and pytest. It searches for "StarCraft II" on Twitch, scrolls down, selects a streamer, handles pop-ups, and takes a screenshot when the page is fully loaded.

🚀 Test Scenario 

1. Open Twitch Mobile (https://m.twitch.tv/) with the search endpoint "StarCraft II" 
2. Scroll down twice.
3. Click on the first streamer in the list.
4. Handle any pop-ups or modals that appear.
5. Wait for the streamer’s page to load fully.
6. Take a screenshot (twitch_test_screenshot.png).
7. Close the browser.

📂 Project Structure

📦 testTaskSporty
 ┣ 📜 test_twitch.py      # Selenium test script
 ┣ 📜 requirements.txt     # List of dependencies
 ┣ 📜 README.md           # Project documentation
 ┣ 📜 twitch_test_screenshot.png     # PNG showing test execution

⚙️ Setup & Installation

1️⃣ Install Dependencies
Make sure you have Python 3 installed, then run:

`pip install -r requirements.txt`

2️⃣ Run the Test
Run the test using:


`pytest test_twitch.py`


🛠️ Technologies Used
Python (3.x)
Selenium (for browser automation)
pytest (for test execution)
WebDriver Manager (automatically installs the correct ChromeDriver)
