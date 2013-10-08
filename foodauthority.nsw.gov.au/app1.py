'''
    Script to download the data from the table at
    http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results
'''

# to download data
import requests
# to save data to file
import pickle
# to  print
from pprint import pprint
# to grab data from html markup
from soupselect import select
from BeautifulSoup import BeautifulSoup

# grab the html source of the page
r = requests.get('http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results')

# converts the html to an object useful to exctract data
soup = BeautifulSoup(r.text)

# grab the html source of the table
table = select(soup, 'table#myTable')[0]

# select all the row from the table
rows = select(table, 'tr')

data = []
for row in rows[1:]:
    # select all the columns from the row
    cols = select(row, 'td')
    # grab the data from all the columns
    cols = [c.contents[0] for c in cols]
    # using corresponding names to return the data
    trade_name = cols[0]
    suburb = cols[1]
    council = cols[2]
    penalty_notice_no = cols[3]
    date = cols[4]
    party_served = cols[5]
    notes = cols[6]

    info = {
        'trade_name': str(trade_name),
        'suburb': str(suburb),
        'council': str(council),
        'penalty_notice_no': penalty_notice_no,
        'date': str(date),
        'party_served': str(party_served),
        'notes': str(notes),
        }

    # almost all have this but there isn't any usufull info so why keep it
    if info['notes'] == '<a href="/news/offences/definitions-notes-to-register"></a>':
        info['notes'] = ''

    info['penalty_notice_no'] = str(info['penalty_notice_no'].text)
    info['penalty_notice_link'] = str('http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=detail&itemId=%s' % info['penalty_notice_no'])

    data.append(info)

# data2xls(data, 'result.xls', sample=True)

# keeping the data into a .pickle file
with open('data.pickle', 'w') as h:
    pickle.dump(data, h)