from bs4 import BeautifulSoup
import requests
import logging

from src.databases.sqlite3_connection import get_genre_data

logger = logging.getLogger(__name__)


def scraper():
    url = 'https://books.toscrape.com/'
    resp = requests.get(url,verify=False)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text,'html')
        body = soup.body
        children = [i for i in body.children if i!= '\n']
        li = children[1].div.div.ul.ul
        li_children = [i for i in li.children if i!= '\n']
        catalogue_dict = dict()
        for items in li_children:
            catalogue_dict[items.a.string.strip()] = url + items.a['href']
        return catalogue_dict
    else:
        logger.error(f'Unable to capture data due to reason:-{resp.status_code}:{resp.reason}')


def genre_scraper(genre):
    data = get_genre_data(genre)
    if not data:
        raise ValueError("Genre doesn't exist in our database.")
    url = data[0][1]
    resp = requests.get(url,verify=False)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text,'html')
        body = soup.body
        child = [i for i in body.children if i!= '\n'][1]
        list_of_books = [i for i in child.children if i!= '\n'][0]
        print(list_of_books)
    else:
        logger.error(f'Unable to capture data due to reason:-{resp.status_code}:{resp.reason}')
