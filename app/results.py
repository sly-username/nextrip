# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup

#import time
#start_time = time.time()

## launch url
url = 'https://www.metro.net/riding/nextrip/bus-arrivals/'

## create a new Firefox session
driver = webdriver.Firefox()
#driver.implicitly_wait(30)
driver.get(url)
driver.switch_to.frame(0)

## select bus stop information
route_list = Select(driver.find_element_by_name('routeSelector'))
direction_list = Select(driver.find_element_by_name('directionSelector'))
stop_list = Select(driver.find_element_by_name('stopSelector'))

## set default values
route_list.select_by_value('704')
direction_list.select_by_value('704_165_0')
stop_list.select_by_value('14424')


def select_option(route, direction, stop):
    route_list.select_by_visible_text(route)
    direction_list.select_by_visible_text(direction)
    stop_list.select_by_visible_text(stop)


#Selenium hands the page source to Beautiful Soup
#soup = BeautifulSoup(driver.page_source)

driver.switch_to.frame('predictionFrame')
results = driver.find_elements(By.XPATH, '//*[contains(@class, "Prediction")]')


def get_predictions(results):
    times = []
    for r in results:
        times.append(r.text)
    return times

print(get_predictions(results))

## end the Selenium browser session
driver.quit()
