# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from autocomplete import AutoCompleter   
from predictions import Prediction

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def home():
    bus_stop = '704 Downtown LA - Santa Monica Via Santa'
    predictions = Prediction(bus_stop, 'route').get_predictions()
    return render_template("home.html", predictions=predictions)


@app.route('/autocomplete', methods = ['POST'])
def get_matches():
    if request.method == 'POST':
        field_name = request.form('caller')
        user_input = request.form[field_name].value
        choices_list = Prediction.get_choices_list(field_name)
        choices = AutoCompleter(choices_list, user_input).guess_choices()
        return choices
    return render_template("home.html", choices=choices)


@app.route('/predict', methods = ['GET', 'POST'])
def get_predictions(bus_stop, field_name):
    predictions = Prediction(bus_stop, field_name).get_predictions()
    return predictions
    return render_template("home.html", predictions=predictions)

    


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