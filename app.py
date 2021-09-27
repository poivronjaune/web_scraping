import logging
import os
import sys
from req import req


def setup_logging():
    # https://docs.python.org/3/library/logging.html#logrecord-objects
    #ROOT_DIR = os.path.abspath(os.curdir)
    ROOT_DIR = os.path.dirname(sys.modules["__main__"].__file__)
    if not os.path.isdir(f"{ROOT_DIR}/LOGS"):
        os.makedirs(f"{ROOT_DIR}/LOGS")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:[%(funcName)s(line:%(lineno)d)]:%(message)s")
    file_handler = logging.FileHandler(f"{ROOT_DIR}/LOGS/app.log")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger




# app_logger = setup_logging()


# Read command line search string or use default value
company_to_search = "CHEZ ASHTON"  # Local fast food restaurant serving great poutine :)
if len(sys.argv) > 1:
    company_to_search = sys.argv[1]


# Instantiate a req scraper and extract company data
scraper = req(loglevel=logging.DEBUG)
results = scraper.get_companies(company_to_search)
scraper.save_results_to_csv(company_to_search)
scraper.save_results_to_json(company_to_search)
scraper.save_results_to_excel(company_to_search)


# Display results on command line
print(f"\n\n ------- COMPANY INFORMATION ------")
print(f"Searched string : {company_to_search} \n")
for company in results:
    print(company)




scraper.driver.minimize_window()
# input("Press ENTER to close the controlled Web Browser...")
scraper.driver.quit()

