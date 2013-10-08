# some system funcionts
import os
# to hash test
from martelo import hash
import pickle
from pprint import pprint
import requests
from soupselect import select
from BeautifulSoup import BeautifulSoup
from martelo import data2xls
import multiprocessing

# load the data collected in the first part
with open('data.pickle', 'r') as h:
    data = pickle.load(h)


result = []
def process(d, i=None):
    ''' function to process one entry of the table '''
    # to keep a small idea if this is still working (output)
    if i:
        print '%s' % i
    else:
        print '.'

    # extraction of the link of interest
    link = d['penalty_notice_link']

    # if we havn't downloaded the link yet, we do it and keep in into a html file into the temp folder
    if not os.path.exists('./temp/%s.html' % hash(link)):
        r = requests.get(link)
        with open('./temp/%s.html' % hash(link), 'w') as h:
            h.write(r.text.encode('utf-8'))

    # load the hmtl markup
    with open('./temp/%s.html' % hash(link), 'r') as h:
        source = h.read()

    # if we havnt previously extracted the info, we do it now
    if not os.path.exists('./temp/%s.pickle' % hash(link)):

        # to extract info it's usually the same way:
        #   - use BeautifulSoup to create the soup of the source
        #   - use select and some css classes/ids to extract info
        # => it's exaclty what is down below

        soup = BeautifulSoup(source)
        div = select(soup, 'div.cim_content')[0]
        table = select(div, 'table')[0]
        rows = select(table, 'tr')

        address = str(select(rows[2], 'td')[-1].contents[0])
        offence_code = str(select(rows[5], 'td')[-1].contents[0])
        nature = str(select(rows[6], 'td')[-1].contents[0])
        amount = str(select(rows[7], 'td')[-1].contents[0])
        data_penalty = str(select(rows[9], 'td')[-1].contents[0])
        issued_by = str(select(rows[10], 'td')[-1].contents[0])

        d['address'] = address
        d['offence_code'] = offence_code
        d['nature'] = nature
        d['amount'] = amount
        d['data_penalty'] = data_penalty
        d['issued_by'] = issued_by

        with open('./temp/%s.pickle' % hash(link), 'w') as h:
            pickle.dump(d, h)
    else:
        # we have previously extracted the info, we simply load it avoiding extra work
        with open('./temp/%s.pickle' % hash(link), 'r') as h:
            d = pickle.load(h)

    return d

# to download the data and process it using multiple threads
pool = multiprocessing.Pool()
result = pool.map(process, data)


print 'saving results'
data2xls(result, 'result.xls', sample=True)
