from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import summarize


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_link(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    urlList = []
    for i, li in enumerate(html.select('div.more_stories_scr article.list div.title a')):
        urlList.append(url+li['href'])
    return urlList

def scrape(listUrl):
    title = []
    content = []
    upvote = []
    summary = []
    for i, url in enumerate(listUrl):
        # print(i)
        raw_html = simple_get(url)
        html = BeautifulSoup(raw_html, 'html.parser')
        title.append(html.select('h1#article-title')[0].text)
        content_per_p = []
        for j in html.select('div.entry_content p'):
            content_per_p.append(j.text)
        content.append(''.join(content_per_p))
        upvote.append(html.select('span.float-right.upvote_stat')[0].text)
        summary.append(summarize.summarize_content(title[i], content[i]))
    return title, content, upvote, summary


url = 'https://www.allkpop.com/'
print("\nGet Link...")
list_of_url = get_link(url)
print("Scrapping...")
titles, contents, upvotes, summary = scrape(list_of_url)

for i in range(len(titles)):
    print(i)
    print("     URL: ",list_of_url[i])
    print("     Title: ",titles[i])
    print("     Content: ",contents[i],"\n")
    print("     Summary: ",summary[i],"\n")
    print("     ",upvotes[i])
    print("============================================================")
