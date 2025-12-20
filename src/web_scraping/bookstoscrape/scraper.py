from bs4 import BeautifulSoup
import requests
import logging

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
