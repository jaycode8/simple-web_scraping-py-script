
import requests
from bs4 import BeautifulSoup
import time
import pymongo

print('Input skills you arent familiar with')
unfamiliar_skills = input('>')
print(f"Filtering out {unfamiliar_skills} from listed jobs ...")

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
my_db = myclient['WebScrapping']
collection = my_db['test_jobs']

def find_job():
    html_text = requests.get('http://127.0.0.1:5500/jobs.html').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_ = 'card')
    job_lists = []

    for index,job in enumerate(jobs):
        published_day = job.find('span', class_='actions').span.text
        if 'few' in published_day:
            company_name = job.h3.text
            key_skills = job.find('span', class_ = 'key-skils').p.text
           
            if unfamiliar_skills not in key_skills:
                link = job.find('span', class_ = 'actions').a['href']
                filtered_job = {
                    "Company Name": f"{company_name}",
                    "Required Skills": f"{key_skills}",
                    "More Infor": f"{link}",
                    "index": f"{index}"
                    }
                job_lists.append(filtered_job)
    collection.insert_many(job_lists)
    print('saved jobs')
    
if __name__ == '__main__':
    while True:
        find_job()
        time_wait = 1
        print(f"waiting for {time_wait} minute ............")
        print()
        time.sleep(time_wait*60)
