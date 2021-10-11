# Search the "Registraire des entreprises" web site
# 
import os
import sys
import logging
import math
import pandas as pd
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

class req:
    def __init__(self, loglevel=None) -> None:
        # req attributes
        self.BASE_URL = os.environ["BASE_URL"]  # Main REQ URL to enter search string for REQ website (might change over time)
        self.driver = None                      # Holder for Chrome Browser driver
        self.logger = None                      # Holder for the logging system
        self.data = None                        # Holder for company data
        self.search_term = None                 # Holder for search term
        self.setup_logging(loglevel)

        self.log_info(f"REQ Logging setup completed")
        self.setup_browser_driver()
        if self.driver is None:
            self.write_log_msg(f"REQ browser setup failed, check chromedriver version if compatible with your version of chrome")
        else:
            self.log_info(f"REQ browser setup succesfull")


    # ##################################################
    #  Utility methods for unse internally to class    #
    # ##################################################
    def setup_logging(self, loglevel):
        if loglevel is None:
            return
        else:
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

    def log_info(self, info_str):
        if self.logger is not None:
            self.logger.info(info_str)

    def log_debug(self, info_str):
        if self.logger is not None:
            self.logger.debug(info_str)

    def setup_browser_driver(self):
        #CHROME_DRIVER_LOCATION = "C:\<path>\chromedriver.exe"
        CHROME_DRIVER_LOCATION = os.environ["CHROME_DRIVER_LOCATION"]
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOCATION,options=options)
            self.log_debug(f"Chrome Browser opened and waiting for commands.")
        except Exception as e:
            self.driver = None
            self.log_debug(f"Unable to open Chrome Browser, {e} ")

    def open_base_url(self):
        try:
            self.driver.get(self.BASE_URL)
            self.log_info(f"REQ Base page opened, {self.BASE_URL}")
        except Exception as e:
            self.log_debug(f"Unable to open base URL, {e}")

    def send_search_string(self, company_to_search):
        self.search_term = company_to_search
        # Send a company name into the search box of the page
        search_box_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_K1Fieldset1_ChampRecherche__cs"]'
        search_box = self.driver.find_element_by_xpath(search_box_xpath)
        search_box.send_keys(self.search_term)

        # Click the accept conditions check box
        check_box_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_CondUtil_CaseConditionsUtilisation_0"]'
        check_box = self.driver.find_element_by_xpath(check_box_xpath)
        check_box.click()

        # Click the submit button to send search request
        search_btn_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_KRBTRechSimple_btnRechercher"]'
        search_btn = self.driver.find_element_by_xpath(search_btn_xpath)
        search_btn.click()        
        self.log_info(f'Company search completed, search="{company_to_search}"')
    
    def number_of_companies_found(self):
        total = 0
        try: 
            found_number_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_K1ZoneContenu1_Cadr"]/fieldset[2]'
            found_number_str = self.driver.find_element_by_xpath(found_number_xpath).text
            str_end = found_number_str.find('dossier(s) trouvé(s)')
            if not str_end == 0:
                total = found_number_str[0:str_end].strip()
                total = int(total)
                self.log_info(f"Found company count in page, total={total}")
            else:
                total = 0
                self.log_info(f"No companies found")
        except Exception as e:
            total = 0
            self.log_info(f"Unable to locate 'dossier(s) trouvé(s) in search result page")

        return total


    # ###########################################
    #  Methods to call from external program    #
    # ###########################################
    def get_companies(self, search_str):
        #
        # Open Base URL, send search string, extract data from HTML Tables
        #
        self.open_base_url()
        self.send_search_string(search_str)
        total_found = self.number_of_companies_found()
        
        # Some navigation logic based on how web page navigation tool bar is displayed
        #
        if total_found > 0 and total_found <= 10 :
            data = self.extract_companies_from_html()
            self.log_info(f"One page of DATA extracted from REQ Site, total records: {total_found}")
        elif total_found > 10:
            total_pages = math.ceil(total_found / 10)
            # Automatically extract page 1, then proceed by loop for all other pages (all page links are not displayed in navigation tool bar)
            data = self.extract_companies_from_html()
            for page_num in range(2,total_pages+1):
                self.select_results_page(page_num)
                page_data = self.extract_companies_from_html()
                data.extend(page_data)
            self.log_info(f"{total_pages} pages of DATA extracted from REQ Site, total records: {total_found}")
        else:
            data = []
            self.log_info(f"No DATA extracted from REQ Site, total records: 0")

        self.data = data
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
        # Page_num above 10 must come through a loop (web page navigation bar only displays 10 page links at a time)
        
        # Find link to target page in page navigation bar
        page_navigator_element = self.driver.find_element_by_class_name("navigateur")
        # Send click event on the correct page_link found
        page_link = page_navigator_element.find_element_by_link_text(str(page_num))        
        page_link.click()

    def save_results_to_csv(self, filename):
        if self.data != None:
            #TODO: check if filename argument contains an extension
            file_name = f"{filename}.csv"
            df = pd.DataFrame(self.data)
            df.to_csv("DATA/"+file_name, encoding='utf-8', index=False)
            self.log_info(f"Data saved to file: {file_name}")
        else:
            self.log_info(f"No Data saved to file.")

    def save_results_to_json(self, filename):
        if self.data != None:
            #TODO: check if filename argument contains an extension
            file_name = f"{filename}.json"
            df = pd.DataFrame(self.data)
            df.to_json("DATA/"+file_name, orient='records', force_ascii=False, indent=2)
            self.log_info(f"Data saved to file: {file_name}")
        else:
            self.log_info(f"No Data saved to file.")

    def save_results_to_excel(self, filename):
        if self.data != None:
            #TODO: check if filename argument contains an extension
            file_name = f"{filename}.xlsx"
            df = pd.DataFrame(self.data)
            df.to_excel("DATA/"+file_name, encoding='utf-8')
            self.log_info(f"Data saved to file: {file_name}")
        else:
            self.log_info(f"No Data saved to file.")
         