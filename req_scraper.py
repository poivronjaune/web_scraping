# Search the "Registraire des entreprises" web site
#
import os
import sys
import logging
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

class req:
    def __init__(self, log=logging.INFO) -> None:
        self.driver = None                  # Holder for Chrome Browser driver

        self.setup_logging(log)
        self.setup_browser_controller()
        logging.info(f"Init message to test debug logging format")

    def setup_logging(self, log):
        logging.basicConfig(
            filename="req_scrapper.log",
            level=log,
            format="%(asctime)s:%(levelname)s:%(message)s"
        )

    def setup_browser_controller(self):
        #CHROME_DRIVER_LOCATION = "C:\<path>\chromedriver.exe"
        self.CHROME_DRIVER_LOCATION = os.environ["CHROME_DRIVER_LOCATION"]
        self.URL = os.environ["BASE_URL"]
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            self.driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER_LOCATION,options=options)
        except Exception as e:
            logging.debug(f"Unable to open Chrome Browser, {e} ")

    def get_companies(self, search_str):
        data = [
            {"neq" : "1234", "statut":"radié"},
            {"neq" : "5678", "statut":"en vigueur"}
        ]

        return data


    




