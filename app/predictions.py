# -*- coding: utf-8 -*-
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

#import time
#start_time = time.time()

class Prediction(object):
    
    def __init__(self, bus_stop, field_name):
        self.route_dict = self.get_route_dict()
        self.bus_stop = bus_stop
        self.field_name = field_name
        
    def get_route_dict(self):
        with open('route_dict.json', 'r') as f:
            route_dict = json.load(f)
        return route_dict
    
#    def get_bus_stop(self):
#        url = 'https://www.metro.net/riding/nextrip/bus-arrivals/'
#        driver = webdriver.Firefox()
#        driver.get(url)
#        driver.switch_to.frame(0)
#        route_list = Select(driver.find_element_by_name('routeSelector'))
#        bus_stop = route_list.first_selected_option.get_attribute('value')
#        driver.quit()
#        
#        return bus_stop
    
    def get_choices_list(self):
#        bus_stop = self.get_bus_stop()
        
        if self.field_name == 'route':
            return self.route_dict.keys()
        elif self.field_name == 'direction':
            return self.route_dict[self.bus_stop]['direction']
        elif self.field_name == 'stop':
            return self.route_dict[self.bus_stop]['stop']
    
    def get_predictions(self):
        url = 'https://www.metro.net/riding/nextrip/bus-arrivals/'
        driver = webdriver.Firefox()
        driver.get(url)
        driver.switch_to.frame(0)
        
        driver.switch_to.frame('predictionFrame')
        
        results = driver.find_elements(By.XPATH, '//*[contains(@class, "Prediction")]')
        
        ## end the Selenium browser session
        
        return results

        driver.quit()

    
#start_time = time.time()
#print("--- %s seconds ---" % (time.time() - start_time)) 



if __name__ == "__main__":
    app.run(debug=True)