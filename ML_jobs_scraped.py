# Import libraries
import math
import pandas as pd
import requests
from bs4 import BeautifulSoup

Job_Titles = list()
Job_Links = list()
Job_Types = list()
Job_Skills = list()
Companies_Name = list()
Companies_Location = list()

page_num = 0
while True:
    response = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=machine%20learning&start={page_num}")
    soup = BeautifulSoup(response.content, "lxml")

    titles = soup.find_all("h2", {"class": "css-m604qf"})
    for title in titles:
        Job_Titles.append(title.a.text)
        Job_Links.append(("https://wuzzuf.net" + title.a["href"]).replace(' ', '%20'))

    occupations = soup.find_all("div", {"class": "css-1lh32fc"})
    for occupation in occupations:
        Job_Types.append(occupation.text)

    skills = soup.find_all("div", {"class": "css-y4udm8"})
    for job_skills in skills:
        Job_Skills.append(job_skills.text)

    companies = soup.find_all("div", {"class": "css-d7j1kk"})
    for company in companies:
        Companies_Name.append((company.a.text).replace('-', ' ').rstrip())
        Companies_Location.append(company.span.text.strip())

    page_num += 1
    
    page_limit = int(soup.find("strong").text) / 15
    if page_num > (math.ceil(page_limit)):
        break

Scraped_Data = dict()
Scraped_Data["Job_Titles"] = Job_Titles
Scraped_Data["Job_Links"] = Job_Links
Scraped_Data["Job_Skills"] = Job_Skills
Scraped_Data["Job_Types"] = Job_Types
Scraped_Data["Companies_Name"] = Companies_Name
Scraped_Data["Companies_Location"] = Companies_Location

Scraped_Data = pd.DataFrame(Scraped_Data)
Scraped_Data.to_csv("ML Jobs.csv")

