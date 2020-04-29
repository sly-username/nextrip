# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from flask import Flask, render_template, request
from autocomplete import AutoCompleter   
from predictions import Prediction



app = Flask(__name__)

url = 'https://www.metro.net/riding/nextrip/bus-arrivals/'
driver = webdriver.Firefox()
driver.get(url)
driver.execute_script("window.stop();")

content = driver.find_element(By.XPATH, '//div[@class="iframe-nextrip"]/iframe')
driver.switch_to.frame(content)

@app.route('/', methods = ['GET', 'POST'])
def home():
#    url = 'https://www.metro.net/riding/nextrip/bus-arrivals/'
#    driver = webdriver.Firefox()
#    driver.get(url)
#    driver.execute_script("window.stop();")
#    
#    content = driver.find_element(By.XPATH, '//div[@class="iframe-nextrip"]/iframe')
#    driver.switch_to.frame(content)
    driver.switch_to.default_content()
    driver.switch_to.frame(content)
    route_list = Select(driver.find_element_by_name('routeSelector'))
    route_list.select_by_value('704')
    predictions = Prediction(driver).get_predictions()
    return render_template('home.html', predictions=predictions)


@app.route('/autocomplete/<user_input>', methods = ['POST'])
def list_possible_choices():
    if request.method == 'POST':
        field_name = request.form('caller') 
        user_input = request.form[field_name].value
        route_choices = Prediction.route_choices
        choices = AutoCompleter(route_choices, user_input).guess_choices()
        return choices
    return render_template('home.html', choices=choices)
     


@app.route('/predict', methods = ['GET'])
def get_predictions():
    predictions = Prediction(driver).get_predictions()
    return render_template('home.html', predictions=predictions)

# =============================================================================
# @app.route('/autocomplete', methods = ['POST'])
# def get_post_javascript_data():
#    if request.method == 'POST':
#         datafromjs = request.form['mydata']
#         result = "return this"
#         resp = make_response('{"response": '+result+'}')
#         resp.headers['Content-Type'] = "application/json"
#         return resp
#         return render_template('login.html', message='')
# =============================================================================


if __name__ == "__main__":
    app.run(debug=True)