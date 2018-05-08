"""
Daily Progress Reporting | May 8th 2018
1. Built MeroJob Scraper
2.
"""


import shelve
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://merojob.com"


def parse_urls(key, link):

    shelve_object = shelve.open(key+'.shelve')

    page_load = requests.get(link)
    soup = BeautifulSoup(page_load.content, 'lxml')
    # Create a list of group-item
    faq_group = soup.find_all(class_='list-group-item')

    for faq_soup in faq_group:

        # Get the relative link from <a ...... href=' . . . . .. ' >
        add_url = faq_soup['href']

        page_content = requests.get(BASE_URL+add_url)
        page_soup = BeautifulSoup(page_content.content, 'lxml').find(id='faq_post_container')

        # Card Header
        card_header = page_soup.find_all(class_='card-header')
        # Card Block
        card_block = page_soup.find_all(class_='card-block')

        # Iterate
        for question, answer in zip(card_header, card_block):
            # Extract Question Text
            que = question.text.strip()
            # Extract Answer text
            ans = answer.contents[-1].strip()
            # file[que] = ans
            shelve_object[que] = ans

    shelve_object.close()


def run():
    to_crawl = {
        'employer': "/faq/employers/",
        'jobseeker': "/faq/jobseeker/"
    }
    for keys, values in to_crawl.items():
        parse_urls(keys, BASE_URL+to_crawl[keys])


def load_shelve():
    # Load the Shelve using
    faq_employer = shelve.open('employer.shelve')
    faq_jobseeker = shelve.open('jobseeker.shelve')


run()

