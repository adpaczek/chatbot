from bs4 import BeautifulSoup as bs
import requests
import os
import re

DOMAIN = ''
URL = ''
KEYWORD = ''
DOWNLOAD_DIR = './datasets/srt/zip'
TEXT_CLASS = ''
TR_CLASSES = []


def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')


for tr_class in TR_CLASSES:
    for tr_tag in get_soup(URL).find_all('tr', class_=tr_class):
        # Find the <a> tag with the specific class and extract the text
        text = tr_tag.find('a', class_=TEXT_CLASS).text.strip()
        name = re.sub(r'[^\w\s]', '', text).replace(' ', '')
        name = name.replace("\n", "")
        file_link = tr_tag.find('a', href=lambda href: href and KEYWORD in href)
        if file_link:
            link = file_link['href']
            file_path = os.path.join(DOWNLOAD_DIR, f"{name}.zip")
            with open(file_path, 'wb') as file:
                response = requests.get(DOMAIN + link)
                file.write(response.content)
                print(f"Downloaded: {name} from {DOMAIN + link}")




