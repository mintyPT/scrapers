from martelo import *


def process(i):
    info = {'id': i}

    link = 'http://fatalities.dmp.wa.gov.au/fatalities/detail.asp?id=%s' % i
    r = requests.get(link)
    soup = soupify(r)

    table = select(soup, 'div#01SuggestionPositioningAnchor table')[0]
    _temp = [[col.text for col in select(row, 'td')] for row in select(table, 'tr')]

    two = filter(lambda l: len(l) == 2, _temp)
    one = filter(lambda l: len(l) == 1, _temp)

    for key, value in two:
        key = key.lower().replace(':', '').encode('utf-8')
        value = value.replace('&nbsp;', '').strip().encode('utf-8')
        if value != '':
            info[key] = value

    for o in one:
        o = o[0]
        o = o.replace('&nbsp;', '').strip().encode('utf-8')
        if o and 'report' in o.lower():
            info['report type'] = o.lower()

    return info

import multiprocessing

pool = multiprocessing.Pool()
data = pool.map(process, (i for i in range(1, 652)))
data2xls(data, sample=True)

# for i in range(1, 652):
#     print process(i)
#     break
