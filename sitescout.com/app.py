import os
# import sys
import json
# import tablib
import requests
from data import *
from lib import raw_input_json
from lib import save2xls


class sitescout:

    def __init__(self, username, password):

        payload = {'email': username,
                   'password': password,
                   'web': '1'}

        self.s = requests.session()

        r = self.s.get('http://sitescout.com/')
        r = self.s.post('https://rtb.sitescout.com/admin/com/login.jsp', data=payload)

        if '<title>SiteScout RTB</title>' not in r.text:
            raise Exception('Could not log in with %s, %s' % (username, password))

    def get(self, limit=75, search=None, view=False, cc=None, channelId=None, types=None, networkId=None):

        link = 'https://rtb.sitescout.com/admin/com/masterSiteStore.jsp'

        base = {
            'sort': 'auctions',
            'dir': 'ASC',
            'start': '0',
            'limit': limit,
            'xaction': 'read'
        }

        if networkId is not None:
            # exchange filter
            #   networkId:3
            base['networkId'] = networkId

        if types is not None:
            # inventory filter
            #   WEB (web only), MOBILE (mobile only), MOBILE_APP (mobile app only), ANY (all)
            base['type'] = types

        if channelId is not None:
            # category filter
            #   channelId:7
            base['channelId'] = channelId

        if cc is not None:
            # country filter
            #   cc:DE
            base['cc'] = cc

        if search is not None:
            # pesquisa:
            #   filter:dog
            base['filter'] = search

        if view is True:
            # new sites only filter
            #   view:new
            base['view'] = 'new'

        # print base

        r = self.s.post(link, data=base)

        # [u'total', u'data', u'success']
        result = json.loads(r.text)

        # pprint(base)

        if result['total'] != limit:
            return self.get(limit=result['total'], search=search, view=view, cc=cc, channelId=channelId, types=types, networkId=networkId)

        if result['success'] is not True:
            raise Exception('Get failed')

        return result


def main():

    # os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.getcwd(), 'cacert.pem')

    username = raw_input('username? ').strip()
    password = raw_input('password? ').strip()
    print ''

    search_term = raw_input('What would you like to search? ')
    search_term = search_term.strip()

    typex = raw_input_json('Inventory?', types)
    # print typex

    exchangex = raw_input_json('Exchange?', exchange)
    # print exchangex

    categoryx = raw_input_json('Choose a category?', channels)
    # print categoryx

    countryx = raw_input_json('Choose a country?', country)
    # print countryx

    view = raw_input_json('New sites only?', news_sites_only)

    s = sitescout(username, password)

    result = s.get(search=search_term or None, cc=countryx, channelId=categoryx, types=typex, networkId=exchangex, view=view)

    print ''
    print 'Got %s results' % (len(result['data']))

    filename = raw_input('Filename to save data? (without .xls extension) ')
    save2xls(result, filename + '.xls')


if __name__ == '__main__':
    main()
