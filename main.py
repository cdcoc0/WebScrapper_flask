from flask import Flask, render_template, request, redirect, send_file
from indeed import get_jobs as get_indeed_jobs
from so import get_jobs as get_so_jobs
from export import save_to_file

app = Flask("Flask_Scrapper")

db = {}

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      indeed_jobs = get_indeed_jobs(word)
      so_jobs = get_so_jobs(word)
      jobs = indeed_jobs + so_jobs
      db[word] = jobs
  #else
    #return redirect("/")
  return render_template("report.html", keyword=word, cntResults=len(jobs), jobs = jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

  

#직접 html코드 사용 가능
# def home():
#   return "<h1>Job Search</h1>\
#   <form><input placeholder='find the jobs' required /><button>Search</button>"

#dynamic url
# @app.route("/<username>")
# def show_name(username):
#   return f"Hello {username}"

app.run(host="0.0.0.0")