# Search the "Registraire des enytreprises" web site
#
#The next line can prevent use from using a global environmenet path variable set on the PC
# System.setProperty("webdriver.chrome.driver","C:\\Users\\ghs6kor\\Desktop\\Java\\chromedriver.exe");
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

CHROME_DRIVER_LOCATION = "C:\Program Files (x86)\chromedriver.exe"
url = "https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436&Clng=F&WT.co_f=2d06b7e3a15d2e0ab951627138812422"
#string_to_search = "hitesh choudhary"

# Open the web page in chrome through python and shut up the error messages using options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOCATION,options=options)
#driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)
driver.get(url)

# Send a company name into the search box of the page
search_box_xpath = '//*[@id="CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_K1Fieldset1_ChampRecherche__cs"]'
search_box = driver.find_element_by_xpath(search_box_xpath)
company_to_search = "Fujitsu"
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


print(f"\n\n\n\n\n ------- DEBUG ------")
for company in companies:
    cells = company.find_elements_by_tag_name("td")
    print(f"neq: {cells[0].text}, statut:{cells[4].text}, nom:{cells[1].text}, adresse: {cells[3].text}")



# print(driver)
# print(datagrid.text)
# print("-------------------------------------------------------")
# print(len(companies))
# print(companies[0].text)
# print("-------------------------------------------------------")


driver.minimize_window()
#time.sleep(30)
#driver.quit()


#############################################################################
"""
driver.get("http://url.com")    : Get a web page using a url

driver.minimize()               : Minimizes the chrome browser window
driver.quit()                   : quit the chorme driver and closes the web page
driver.back()                   : Equivalent of pressing back button
driver.forward()                : Go to page pressed when we pressed back button


driver.find_element_by_name()   : Search the page using a name attribute
driver.find_element_by_id()     : Search the page using an id attribute
driver.clear()                  : clears the inout field before sending keys
driver.sendkeys("some text")    : Send some text into a web component

driver.title                    : Retrieve the web page title attribute
driver.page_source              : Returns the entire source code of the page


"""

