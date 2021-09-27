# Web Scraping on public web sites

![GitHub](https://img.shields.io/github/license/poivronjaune/web_scraping?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/poivronjaune/web_scraping?style=plastic)
![PyPI - Python Version](https://img.shields.io/badge/python-3.4%2B-blue?color=blue&style=plastic)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/poivronjaune/web_scraping?logo=github&style=plastic)  
  
  
Web scraping is a simple Selenium project to scrap data from a local provincial government web site.  

##### Disclaimer:
This repo is free to fork or download, it is a selenium and beautiful soup learning project. Make to sure to follow all usage conditions posted by the owner of the web site. 


### 2021-09-24 Features
- req.py contains python code to extract company information from the corresponding public web site (only returns data from the first page)  
- This script controls a Chrome Browser on your local machine
- Save features to csv, json, excel

#### Upcomimg features
- Extract owners and managers from detailed information
- Return data as a json object 

#### Installation
`git clone https://github.com/poivronjaune/web_scraping.git ` : Clone this repo to your workspace  
` python -m venv env ` : Create a virtual environment  
` env\Scripts\Activate ` : Activate the virtual environment (windows)  
` python -m pip install --upgrade pip ` : Upgrade your pip tool  
` pip install -r requirements.txt ` : Install python packages  
` .env ` : Create an .env file and insert the following line ` CHROME_DRIVER_LOCATION = "C:\<path>\chromedriver.exe". Replace <'path'> with the location of your chromedriver.exe file

The selenium package controls a web browser installed on your local machine. Please follow instructions on the pypi installation page : https://pypi.org/project/selenium/ to setup correctly. In a word, you need a special program called "chromedriver.exe" that will be accessible by your app.  
The [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) program is produced and distributed by google.  


#### Usage
Once installation is complete, run ` python app.py <search_str>`. The script will:  
- open a Chrome Web Browser
- enter the <search_str> in the web site form
- automatically submit the form
- extract all company information found (loops through all pages available)  
- display results on command line
- wait for user to press ENTER then close the controlled browser


# Packages
#### Python packages
` python-dotenv ` : pyhton package to manage environment variables     
` selenium ` : pyhton package to extract data from web sites  
` beautifulsoup4 ` : pyhton package to extract information from html web pages    
` requests ` : pyhton package offering a simple python HTTP libray  
` lxml ` : pyhton package offering XML processing library 
` pandas ` : python library to manipulate structured data
` openpyxl ` : Python library used by pandas to save to excel
 

