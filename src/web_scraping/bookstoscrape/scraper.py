from bs4 import BeautifulSoup
import requests
import logging
import urllib3

from src.databases.sqlite3_connection import get_genre_data, get_all_genres, get_book_url

logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


WORD_TO_NUMBER = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

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

def scrape_books(url):
    resp = requests.get(url, verify=False)
    if resp.status_code == 200:
        # Find all article tags from the body
        soup = BeautifulSoup(resp.text, 'html')
        body = soup.body
        articles = body.find_all('article')
        li = []

        # Scrape books data and return the list
        for i in articles:
            paragraphs = i.find_all('p')
            dic = {
                'name': i.h3.a['title'],
                'rating': WORD_TO_NUMBER[paragraphs[0]['class'][1]],
                'price': paragraphs[1].string[2:],
                'availability': paragraphs[2].get_text().strip(),
                'book_detail_url': 'https://books.toscrape.com/catalogue/' + i.a['href'][9:]
            }
            li.append(dic)
        return li

    else:
        logger.error(f'Unable to capture data due to reason:-{resp.status_code}:{resp.reason}')

def genre_scraper(genre):
    data = get_genre_data(genre)
    if not data:
        raise ValueError("Genre doesn't exist in our database.")
    url = data[0][1]
    return scrape_books(url)


def all_books_scraper():
    genre_list = get_all_genres()
    li =[]
    for genre in genre_list:
        logger.info(f"Proceeding to scrape for genre: {genre[0]}")
        li.extend(scrape_books(genre[1]))
    return li

def book_detail_scraper(name=None):
    if not name:
        result = get_book_url()
    else:
        name = name.replace('_', ' ').replace("'","''")
        result = get_book_url(name)
    li = []
    for url in result:
        logger.info(f'Scraping for url: {url[0]}')
        resp = requests.get(url[0], verify=False)
        if resp.status_code == 200:
            # Find all article tags from the body
            soup = BeautifulSoup(resp.text, 'html')
            body = soup.body
            table = body.find_all('table')[0]
            dic = dict()
            dic['book_name'] = body.h1.string
            dic['currency'] = '£'
            for i in table.children:
                if i == '\n':
                    continue
                if i.th.string in ('Price (excl. tax)', 'Price (incl. tax)', 'Tax'):
                    dic[i.th.string] = float(i.td.string[2:])
                elif i.th.string in ('Availability','Number of reviews'):
                    dic[i.th.string] = int(i.td.string.replace("In stock (", "").replace(" available)", ""))
                else:
                    dic[i.th.string] = i.td.string
            li.append(dic)
        else:
            logger.error(f'Unable to capture data due to reason:-{resp.status_code}:{resp.reason}')
            raise
    return li