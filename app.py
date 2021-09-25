import logging
import sys
from req_scraper import req


# Read command line search string or use default value
company_to_search = "CHEZ ASHTON"  # Local fast food restaurant serving great poutine :)
if len(sys.argv) > 1:
    company_to_search = sys.argv[1]


# Instantiate a req scraper and extract company data
scraper = req(log=logging.DEBUG)
results = scraper.get_companies(company_to_search)


# Display results on command line
print(f"\n\n\n ------- COMPANY INFORMATION ------")
print(f"Searched string : {company_to_search} \n")
for company in results:
    print(company)