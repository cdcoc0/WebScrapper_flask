import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_pages(url):
  result = requests.get(url)

  #모든 html요소 가져오기
  #print(indeed_result.text)

  #html로부터 정보 추출하기(페이지 정보)
  #beautiful soup lib
  #quick start
  #soup = data extractor
  soup = BeautifulSoup(result.text, "html.parser")

  pagination = soup.find("div", {"class" : "pagination"})

  #pagination에서 찾은 요소의 list
  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  #span태그 안의 문자열만 갖고와
  #pages.append(link.find("span").string)
  #print(page.find("span"))

  #맨 마지막 요소를 제외하고 가져오기
  #pages = pages[:-1]

  #마지막 페이지 가져오기
  max_page = pages[-1]
  
  return max_page


def extract_job(html):
  title = html.find("h2", {"class": "title"}).find("a")["title"]
  company = html.find("span", {"class": "company"})
  
  if company is not None:
    company_anchor = company.find("a")
  else:
    company_anchor = "blank"

  if company_anchor is not None:
    company = str(company_anchor)
  else:
    company = "blank"
  #python strip
  #양쪽 끝에 있는 space를 없앰..?

  #위의 작업을 했음에도... company가 nonetype인 경우가 존재해 불가피하게 none인 경우는 그냥 blank 출력하게 함
  if company is not None:
    company = company.strip()
  else:
    company = "blank"
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return {'title':  title, 'company': company, 'location': location, "link": f"https://www.indeed.com/viewjob?jk={job_id}"}

#페이지 수만큼 request 사용
#range: 배열 만들어줌
def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page + 1}")
    result = requests.get(f"{url}&start={page * LIMIT}")
    #html에서 데이터 추출(job)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class" : "jobsearch-SerpJobCard"})
    for r in results:
      job = extract_job(r)
      jobs.append(job)
  return jobs


def get_jobs(word):
  url = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}"
  last_page = get_last_pages(url)
  jobs = extract_jobs(last_page, url)
  return jobs