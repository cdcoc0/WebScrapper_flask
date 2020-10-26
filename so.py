import requests
from bs4 import BeautifulSoup

def get_last_pages(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class": "s-pagination"})
  if pages:
    pages = pages.find_all("a")
    last_page = pages[-3].get_text(strip=True)
    return int(last_page)
  else:
    return 1


def extract_job(html):
  title = html.find("h2", {"class": "fs-body3"}).find("a")["title"]
  company, location = html.find("h3", {"class": "fs-body1"}).find_all("span", recursive=False)
  #recursive=false: don't go deeper
  #unpack values
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  job_id = html['data-jobid']
  return {'title': title, 'company': company, 'location': location, 'link': f"https://stackoverflow.com/jobs?id={job_id}&q=python"}



def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping so page {page + 1}")
    result = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "-job"})
    for r in results:
      job = extract_job(r)
      jobs.append(job)
      #print(r["data-jobid"])
  return jobs


def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
  last_page = get_last_pages(url)
  jobs = extract_jobs(last_page, url)
  return jobs