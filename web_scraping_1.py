import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import re

import csv
import os


def find_jobs():
    print('Put a skill you are not familiar with (if multiple, after comma)')
    unfamiliar_skill = input('>')
    # unfamiliar_skill = ''   # ----> Uncomment this and comment 15th and 16th line to get automatic outcomes without rejecting any skills
    print(f'Searching for offers...')
    unfamiliar_skill = unfamiliar_skill.replace(' ', '')
    unfamiliar_skill = unfamiliar_skill.split(',')

    for i in range(len(unfamiliar_skill)):
        unfamiliar_skill[i] = unfamiliar_skill[i].upper()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    URL = 'https://justjoin.it/all-locations/data'

    driver.get(URL)
    time.sleep(4)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    jobs = soup.find_all(class_='MuiBox-root css-1jbajow')

    for job in jobs:
        job_name = job.find('h3', class_='css-1gehlh0')
        element_company = job.find(class_='MuiBox-root css-1mx97sn')
        company = element_company.find('span')
        job_city = job.find(class_='css-1o4wo1x')
        job_salary = job.find(class_='MuiBox-root css-18ypp16')
        elements = job.find_all(class_='MuiBox-root css-1qruno6')
        offer_link = f'https://justjoin.it' + job.find(class_='offer_list_offer_link css-3qyn8a').get('href')

        if job_salary.text != 'Undisclosed Salary':
            job_salary_clean = job_salary.text.replace(' ', '')
            if '-' in job_salary_clean:
                list_salary = job_salary_clean.split('-')
                cradle1 = int(re.sub(r'\D', '', list_salary[0]))      #int(list_salary[0])
                cradle2 = int(re.sub(r'\D', '', list_salary[1]))
                average = (cradle1 + cradle2) / 2
            else:
                average = int(re.sub(r'\D', '', job_salary_clean))
        else:
            average = 'Not known'

        if elements[1].text != 'Fully remote':
            remote = 'not fully remote'
        else:
            remote = elements[1].text

        skills = ''
        required_skills = []
        flag = 0

        for i in range(2, len(elements)):
            skills = skills + elements[i].text + f', '
            required_skills.append(elements[i].text.upper())

        for i in unfamiliar_skill:
            if i in required_skills:
                flag += 1
        if flag == 0:
            with open(r'C:\Users\wikto\PycharmProjects\pythonProject\data_analyst\web_scraping\beaufil_soup_course\Files(Project2)\jobs.csv', mode='a', encoding='utf-8') as csvfile:
                fieldnames = ['Job', 'Company', 'City', 'Salary', 'Average_salary', 'Remote', 'Skills', 'More_info']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                file_path = r'C:\Users\wikto\PycharmProjects\pythonProject\data_analyst\web_scraping\beaufil_soup_course\Files(Project2)\jobs.csv'


                if os.stat(file_path).st_size == 0:
                    writer.writeheader()
                writer.writerow({'Job': job_name.text, 'Company': company.text, 'City': job_city.text, 'Salary':
                    job_salary.text, 'Average_salary': average, 'Remote': remote, 'Skills':
                                     skills, 'More_info': offer_link})

            print(f'''
                Job: {job_name.text}
                Company: {company.text}
                City: {job_city.text}
                Salary: {job_salary.text}
                Average Salary: {average}
                Remote: {remote}
                Skills: {skills}
                More info: {offer_link}
                ''')
            print('')
            print('')


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
