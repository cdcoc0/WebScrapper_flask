from flask import Flask

app = Flask("Flask_Scrapper")

@app.route("/")
def home():
  return "Welcome to Podo home!"

app.run(host="0.0.0.0")