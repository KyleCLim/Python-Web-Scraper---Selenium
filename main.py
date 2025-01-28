from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup

##############################################################
################ RENDERING THE PAGES ###################
##############################################################

url_to_scrape = f"https://webscraper.io/test-sites/e-commerce/scroll/computers/laptops"

# initiate selenium driver
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url_to_scrape)

################# SCROLLING AS FAR AS YOU CAN ###########################

last_height = 0

while True:
    ################# Scroll 1,1000 pixels to the bottom ###########################

    driver.execute_script('window.scrollBy(0, 1000)')

    ################ Wait X seconds ######################################

    time.sleep(1)
    new_height = driver.execute_script('return document.body.scrollHeight')

    ################ Check if height changed (if not, stop) ######################################

    if (new_height == last_height):
        break
    else:
        last_height = new_height

####################### Fetch page source ###########################

page_source = driver.page_source

####################### Parse with soup ###########################

soup = BeautifulSoup(page_source, "html.parser")

data = []

all_items = soup.find_all('div', class_="col-md-4 col-xl-4 col-lg-4")


for item in all_items:
        row = {}
        row['Title'] = item.find('a', class_="title").text
        row['Price'] = item.find('h4', class_="price float-end pull-right").text.replace("$ ", "")
        data.append(row)


################# WRITING TO EXCEL / CSV ###########################
df = pd.DataFrame(data)
df.to_csv('dataset.csv', index=False)