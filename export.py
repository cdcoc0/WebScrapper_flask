import csv

def save_to_file(jobs):
  #open file(파일쓰기만 설정)
  file = open("jobs.csv", mode="w")
  #write file
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs:
    #job에서 값만 추출해서 배열로 만듦
    writer.writerow(list(job.values()))
  return