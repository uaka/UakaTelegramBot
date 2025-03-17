import pytest
import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

to_search = "StarCraft II"

logging.basicConfig(
    filename="test_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@pytest.fixture
def setup_browser():
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "Pixel 4"})
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver


def test_twitch_search(setup_browser, request):
    try:
        driver = setup_browser
        driver.get("https://m.twitch.tv/search?term=" + to_search.replace(' ', "%20") + "&type=channels")
        accept_cookie(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        streamer = driver.find_elements(By.CSS_SELECTOR, "[role=list] a")[0]
        streamer_link = streamer.get_attribute("href")
        driver.get(streamer_link)
        close_modal(driver)
        driver.save_screenshot("twitch_test_screenshot.png")
        assert True  # Mark test as passed if no errors occur

    except Exception as e:
        error_screenshot = f"error_{request.node.name}.png"
        driver.save_screenshot(error_screenshot)
        logging.error(f"Test failed: {e}, screenshot: {error_screenshot}")
        pytest.fail(f"Error: {e}")


def close_modal(driver):
    try:
        close_button = driver.find_element(By.XPATH, "//button[contains(text(),'Close')]")
        close_button.click()
        logging.info("Modal closed")
    except:
        logging.info("No modal appeared")


def accept_cookie(driver):
    try:
        cookie_button = driver.find_element(By.XPATH,
                                            "//button[@data-a-target='consent-banner-accept']")
        cookie_button.click()
    except:
        logging.info("Cookie Notice not found")
