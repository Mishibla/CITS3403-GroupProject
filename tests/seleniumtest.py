selenium_test.py

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

class SimpleSeleniumTest(unittest.TestCase):

    def setUp(self):
        # Path to the chromedriver
        chromedriver_path = r'C:\webdrivers\chromedriver.exe'

        # Path to the Chromium binary
        chromium_binary_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        # Initialize the Chrome driver with options
        chrome_options = ChromeOptions()
        chrome_options.binary_location = chromium_binary_path
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
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--v=1')
        
        try:
            service = ChromeService(executable_path=chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.get("http://www.google.com")
            print("WebDriver initialized and navigated to Google.")
        except Exception as e:
            print(f"Failed to start WebDriver: {e}")
            self.driver = None

    def tearDown(self):
        if self.driver:
            self.driver.quit()
        print("Test environment torn down.")

    def test_page_load(self):
        if not self.driver:
            self.fail("WebDriver not initialized.")
        print("Page loaded successfully.")

if __name__ == "__main__":
    print("Starting simplified Selenium test...")
    unittest.main()
    print("Selenium test completed.")