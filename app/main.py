# -*- coding: utf-8 -*-
from flask import Flask, render_template, request      

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/autocomplete', methods = ['POST'])
def get_post_javascript_data():
   if request.method == 'POST':
        datafromjs = request.form['mydata']
        result = "return this"
        resp = make_response('{"response": '+result+'}')
        resp.headers['Content-Type'] = "application/json"
        return resp
        return render_template('login.html', message='')


if __name__ == "__main__":
    app.run(debug=True)