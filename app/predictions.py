# -*- coding: utf-8 -*-
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

#import time
#start_time = time.time()

class Prediction(object):
    
    def __init__(self, driver):
        self.route_dict = self.get_route_dict()
        self.driver = driver
        self.route_choices = self.route_dict.keys()
        self.route_list = Select(self.driver.find_element_by_name('routeSelector'))
        
        
    def get_route_dict(self):
        with open('route_dict.json', 'r') as f:
            route_dict = json.load(f)
        return route_dict
     
    
#    def get_choices_list(self):
#        content = self.driver.find_element(By.XPATH, '//div[@class="iframe-nextrip"]/iframe')
#        self.driver.switch_to.frame(content)
#        bus_num = self.route_list.first_selected_option.get_attribute('value')
        
#        return self.route_dict.keys(), self.route_dict[bus_num]['direction'], self.route_dict[bus_num]['stop']

    
    def grouped(self, iterable, n):
        return zip(*[iter(iterable)]*n)
    
    
    def get_predictions(self):
        direction = self.driver.find_elements(
                By.XPATH, '//select[@name="directionSelector"]/option')
        self.driver.switch_to.frame('predictionFrame')
        predictions = self.driver.find_elements(
                By.XPATH, '//tr[@class="predictionBox"]/td/table/tbody/tr')
        
        if len(direction) > 1:
            results = []
            for x, y in self.grouped(predictions, 2):
                results.append((x.text.strip(), y.text.strip()))
            return results
         
#            results = self.driver.find_elements(By.XPATH, '//*[contains(@class, "Prediction")]')
        return predictions

    def quit_session(self):
        ## end the Selenium browser session
        self.driver.quit()

    
#start_time = time.time()
#print("--- %s seconds ---" % (time.time() - start_time)) 