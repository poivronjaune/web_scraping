# Search the "Registraire des enytreprises" web site
#
#The next line can prevent use from using a global environmenet path variable set on the PC
# System.setProperty("webdriver.chrome.driver","C:\\Users\\ghs6kor\\Desktop\\Java\\chromedriver.exe");
import os
import sys
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Load environment variables
load_dotenv()

#CHROME_DRIVER_LOCATION = "C:\<path>\chromedriver.exe"
CHROME_DRIVER_LOCATION = os.environ['CHROME_DRIVER_LOCATION']
url = "https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436&Clng=F&WT.co_f=2d06b7e3a15d2e0ab951627138812422"

company_to_search = "CHEZ ASHTON"  # Local fast food restaurant serving great poutine :)
if len(sys.argv) > 1:
    company_to_search = sys.argv[1]

# Open the web page in chrome through python and shut up the error messages using options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOCATION,options=options)
driver.get(url)

# Send a company name into the search box of the page
search_box_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_K1Fieldset1_ChampRecherche__cs"]'
search_box = driver.find_element_by_xpath(search_box_xpath)
search_box.send_keys(company_to_search)

# Click the accept conditions check box
check_box_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_CondUtil_CaseConditionsUtilisation_0"]'
check_box = driver.find_element_by_xpath(check_box_xpath)
check_box.click()

# Click the submit button to send search request
search_btn_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_KRBTRechSimple_btnRechercher"]'
search_btn = driver.find_element_by_xpath(search_btn_xpath)
search_btn.click()

# Check if results navigation bar exists (previous, next)
try:
    pagination_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_K1ZoneContenu1_Cadr"]/fieldset[2]/div[2]'
    pagination = driver.find_element_by_xpath(pagination_xpath)
except:
    pagination = None

datagrid = driver.find_element_by_class_name("datagrid")
companies = datagrid.find_elements_by_tag_name("tr")[1:]


print(f"\n\n\n\n\n ------- COMPANY INFORMATION ------")
for company in companies:
    cells = company.find_elements_by_tag_name("td")
    print(f"neq: {cells[0].text}, statut:{cells[4].text}, nom:{cells[1].text}, adresse: {cells[3].text}")





driver.minimize_window()
#time.sleep(30)
input("Press ENTER to close the controlled Web Browser...")
driver.quit()


#############################################################################


