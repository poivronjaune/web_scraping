# Search the "Registraire des entreprises" web site
# 
import os
import sys
import logging
import math
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

class req:
    def __init__(self, loglevel=logging.INFO) -> None:
        # req attributes
        self.BASE_URL = os.environ["BASE_URL"]  # Main REQ URL to enter search string
        self.driver = None                      # Holder for Chrome Browser driver
        self.logger = None                      # Holder for the logging system

        self.setup_logging(loglevel)
        self.setup_browser_driver()

        self.logger.info(f"REQ Logging setup completed")       

    def setup_logging(self, loglevel):
        # https://docs.python.org/3/library/logging.html#logrecord-objects
        ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
        if not os.path.isdir(f"{ROOT_DIR}/LOGS"):
            os.makedirs(f"{ROOT_DIR}/LOGS")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(loglevel)
        formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:[%(funcName)s(line:%(lineno)d)]:%(message)s")
        file_handler = logging.FileHandler(f"{ROOT_DIR}/LOGS/{__name__}.log")
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        

    def setup_browser_driver(self):
        #CHROME_DRIVER_LOCATION = "C:\<path>\chromedriver.exe"
        CHROME_DRIVER_LOCATION = os.environ["CHROME_DRIVER_LOCATION"]
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOCATION,options=options)
        except Exception as e:
            self.driver = None
            self.logger.debug(f"Unable to open Chrome Browser, {e} ")




    def open_base_url(self):
        try:
            self.driver.get(self.BASE_URL)
            self.logger.info(f"REQ Base page opened, {self.BASE_URL}")
        except Exception as e:
            self.logger.debug(f"Unable to open base URL, {e}")

    def send_search_string(self, company_to_search):
        # Send a company name into the search box of the page
        search_box_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_K1Fieldset1_ChampRecherche__cs"]'
        search_box = self.driver.find_element_by_xpath(search_box_xpath)
        search_box.send_keys(company_to_search)

        # Click the accept conditions check box
        check_box_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_CondUtil_CaseConditionsUtilisation_0"]'
        check_box = self.driver.find_element_by_xpath(check_box_xpath)
        check_box.click()

        # Click the submit button to send search request
        search_btn_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_KRBTRechSimple_btnRechercher"]'
        search_btn = self.driver.find_element_by_xpath(search_btn_xpath)
        search_btn.click()        
        self.logger.info(f'Company search completed, search="{company_to_search}"')
    
    def number_of_companies_found(self):
        total = 0
        try: 
            found_number_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_K1ZoneContenu1_Cadr"]/fieldset[2]'
            found_number_str = self.driver.find_element_by_xpath(found_number_xpath).text
            str_end = found_number_str.find('dossier(s) trouvé(s)')
            if not str_end == 0:
                total = found_number_str[0:str_end].strip()
                total = int(total)
                self.logger.info(f"Found company count in page, total={total}")
            else:
                total = 0
                self.logger.info(f"No companies found")
        except Exception as e:
            total = 0
            self.logger.info(f"Unable to locate 'dossier(s) trouvé(s) in search result page")

        return total


    # #############################################
    #
    #  Main method to call from external program
    #
    # #############################################
    def get_companies(self, search_str):
        self.open_base_url()
        self.send_search_string(search_str)
        total_found = self.number_of_companies_found()
        
        if total_found > 0 and total_found <= 10 :
            data = self.extract_companies_from_html()
        elif total_found > 10:
            total_pages = math.ceil(total_found / 10)
            # Automatically extract page 1, then proceed by loop for all other pages
            data = self.extract_companies_from_html()
            for page_num in range(2,total_pages+1):
                # Do not jump directly to a page greater than 10 (or a multiple) you must loop through
                self.select_results_page(page_num)
                page_data = self.extract_companies_from_html()
                data.extend(page_data)
        else:
            data = []

        return data

    def extract_companies_from_html(self):
        datagrid = self.driver.find_element_by_class_name("datagrid")
        companies = datagrid.find_elements_by_tag_name("tr")[1:]
        results = []
        for company in companies:
            data = {}
            cells = company.find_elements_by_tag_name("td")
            data["neq"]        = cells[0].text
            data["statut"]     = cells[5].text
            data["creation"]   = cells[6].text
            data["changement"] = cells[4].text
            data["nom"]        = cells[1].text
            data["adresse"]    = cells[2].text
            results.append(data)
        
        return results

    def select_results_page(self, page_num):
        # Do not use this function to set page_num to 1
        # Page_num above 10 must come through a loop (web page only displays 10 page links at a time)
        
        # Find link to page in page navigation 
        page_navigator_element = self.driver.find_element_by_class_name("navigateur")
        # Click the correct page found by page_num
        page_link = page_navigator_element.find_element_by_link_text(str(page_num))        
        page_link.click()

