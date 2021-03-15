# Web scraping using BeautifulSoup

"""
Step 0: Set up the environment
Install and import all the requirements
pip install requests
pip install bs4
pip install html5lib
"""
import requests
from bs4 import BeautifulSoup


def scrapper(url):
    # url = input("Enter the URL you want to scrap: ")

    # Step 1: Get the HTML
    r = requests.get(url)  # r is response object
    HTMLContent = r.content  # r.content - response in bytes, r.text - response in unicode
    # print(HTMLContent)

    # Step 2: Parse the HTML
    soup = BeautifulSoup(HTMLContent, 'html.parser')
    # print(soup.prettify())  # to print html content in tree style

    # Step 3: HTML tree traversal

    # Get the title of the HTML page
    title = soup.title
    print(title.string)

    # Get the paragraph of the HTML page
    paras = soup.find_all('p')
    result = ""
    for i in paras:
        result += i.text + "\n"
    return result
