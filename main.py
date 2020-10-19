from flask import Flask, render_template

app = Flask("Flask_Scrapper")


@app.route("/")
def home():
  return render_template("index.html")

#직접 html코드 사용 가능
# def home():
#   return "<h1>Job Search</h1>\
#   <form><input placeholder='find the jobs' required /><button>Search</button>"

#dynamic url
# @app.route("/<username>")
# def show_name(username):
#   return f"Hello {username}"

app.run(host="0.0.0.0")