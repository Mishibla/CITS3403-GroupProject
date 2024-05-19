import os
import multiprocessing
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from unittest import TestCase

from app import create_app, db
from app.config import TestConfig

localHost = "http://localhost:5000/"

class SeleniumTestCase(TestCase):

    def setUp(self):
        print("Setting up the test environment...")

        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        print("Starting the Flask server...")
        self.server_process = multiprocessing.Process(target=self.testApp.run)
        self.server_process.start()

        time.sleep(5)  # Wait for the server to start
        print("Flask server started.")

        # Path to the chromedriver
        chromedriver_path = os.path.join(os.path.dirname(__file__), 'webdriver', 'chromedriver')
        print(f"ChromeDriver Path: {chromedriver_path}")

        if not os.path.isfile(chromedriver_path):
            raise FileNotFoundError(f"ChromeDriver not found or is not a file at {chromedriver_path}")

        # Ensure chromedriver has executable permissions
        os.chmod(chromedriver_path, 0o755)
        print("ChromeDriver is executable.")

        # Path to the Chromium binary
        chromium_binary_path = '/mnt/c/Users/mattl/Documents/CITS3403/CITS3403-GroupProject/tests/chrome-linux/chrome-linux/chrome'
        print(f"Chromium Binary Path: {chromium_binary_path}")

        if not os.path.isfile(chromium_binary_path):
            raise FileNotFoundError(f"Chromium not found or is not a file at {chromium_binary_path}")

        # Initialize the Chrome driver with options
        chrome_options = ChromeOptions()
        chrome_options.binary_location = chromium_binary_path
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')  # Disable GPU
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--metrics-recording-only')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--disable-client-side-phishing-detection')
        chrome_options.add_argument('--disable-hang-monitor')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-prompt-on-repost')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-device-discovery-notifications')
        print("Chromium options set.")

        try:
            service = ChromeService(executable_path=chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.get(localHost)
            print("WebDriver initialized and navigated to localhost.")
        except Exception as e:
            print(f"Failed to start WebDriver: {e}")
            self.driver = None

    def tearDown(self):
        print("Tearing down the test environment...")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        if self.driver:
            self.driver.quit()
        print("Test environment torn down.")

    def test_login_page(self):
        if not self.driver:
            self.fail("WebDriver not initialized.")

        print("Starting test_login_page...")
        login_button = self.driver.find_element(By.ID, "sign_in")  # Replace with the actual ID of the login button
        login_button.click()

        time.sleep(2)

        loginElement = self.driver.find_element(By.ID, "log_username")
        loginElement.send_keys("matt")

        loginElement = self.driver.find_element(By.ID, "log_password")
        loginElement.send_keys("fish")
        time.sleep(10)
        print("Test completed.")
