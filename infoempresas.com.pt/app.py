import requests
from pprint import pprint
from soupselect import select
from toolbelt.web import getPage
from toolbelt.io import data2xls
from BeautifulSoup import BeautifulSoup


def make_soup(link):
    return getPage(link)



def make(url):
    soup = make_soup(link)

    contenido = select(soup, 'div.contenido')

    h2Titulon = select(soup, 'h2.h2Titulon')
    spot = h2Titulon[0].parent.parent

    trs = select(spot, 'tr')
    data = []
    for tr in trs[1:]:
        tds = select(tr, 'td')
        empresa = select(tr, 'td.empresa')
        localidad = select(tr, 'td.localidad')
        provincia = select(tr, 'td.provincia')
        url = select(tr, 'td.url')

        n = select(empresa[0], 'a')[0]
        nome, link_interno = n.text, 'http://www.infoempresas.com.pt' + n['href']
        local = localidad[0].text
        provincia = provincia[0].text

        url = select(url[0], 'a')
        url = url[0]['href'] if url else ''

        info = {
            'nome': nome.lower().encode('utf-8'),
            'link_interno': link_interno.lower().encode('utf-8'),
            'local': local.lower().encode('utf-8'),
            'provincia': provincia.lower().encode('utf-8'),
            'link_externo': url.lower().encode('utf-8'),
        }
        data.append(info)

        letras = 'abcdefghifklmnopqrstuvwxyz'
        tipos = ['acute', 'cedil', 'tilde', 'circ']

        reps = [('&amp;', '&')]

        for key in info.keys():

            value = info[key]

            for l in letras:
                for t in tipos:
                    old = '&%s%s;' % (l, t)
                    new = l
                    value = value.replace(old, new)

            for old, new in reps:
                value = value.replace(old, new)

            info[key] = value
    return data

geral = []

link = 'http://www.infoempresas.com.pt/Concelho_PONTA-DELGADA.html'
geral += make(link)

for i in range(2, 90):
    link = 'http://www.infoempresas.com.pt/Concelho_PONTA-DELGADA/Empresas-%s.html' % i
    _temp = make(link)
    geral += _temp
    print i, len(_temp)

data2xls(geral, headers=['nome', 'link_externo', 'local', 'provincia', 'link_interno'])
