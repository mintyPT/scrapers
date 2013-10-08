import requests
from soupselect import select
from BeautifulSoup import BeautifulSoup
from pprint import pprint
import pickle

def soupify(r):
    return BeautifulSoup(r.text)


def saver(r, filename='output_r.html'):
    soup = soupify(r)
    with open(filename, 'w') as h:
        h.write(soup.prettify())


s = requests.session()


def getLinks(cat, sponsor=True):
    _links = []
    r = s.get(cat)
    soup = soupify(r)
    table = select(soup, 'table.categories')[0] if page != 1 or sponsor==False else select(soup, 'table.categories')[1]

    tr = select(table, 'tr')
    for t in tr:
        link = select(t, 'h3 a')
        if link:
            _links.append(str(dict(link[0].attrs)['href']))

    return _links




links = []
page = 1
pageMax = 249
for page in range(1, pageMax+1):
    cat = r'http://benprise.ning.com/forum/categories/uncategorized-1/listForCategory?categoryId=2218885%3ACategory%3A255045&page=' + str(page)
    results = getLinks(cat, True)
    links += results
    print '%s ==> %s' % (page, len(results))

with open('uncategorized.txt', 'w') as h:
    pickle.dump(links, h)