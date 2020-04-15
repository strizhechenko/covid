import bs4
import requests


def url2soup(url):
    return bs4.BeautifulSoup(requests.get(url).content, "html.parser")
