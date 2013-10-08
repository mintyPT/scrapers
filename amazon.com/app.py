from toolbelt.web import getPage
from soupselect import select
from toolbelt.decorators import decomem
from toolbelt.io import data2xls

links = ['http://www.amazon.com/gp/bestsellers/electronics/1077068/ref=sv_e_2',
         'http://www.amazon.com/gp/bestsellers/automotive/ref=sv_auto_2',
         'http://www.amazon.com/gp/bestsellers/toys-and-games/ref=sv_t_0',
         'http://www.amazon.com/gp/bestsellers/baby-products/ref=sv_ba_1',
         'http://www.amazon.com/Best-Sellers-Beauty/zgbs/beauty/ref=sv_bt_0',
         'http://www.amazon.com/gp/bestsellers/hpc/ref=sv_hpc_0',
         'http://www.amazon.com/gp/bestsellers/grocery/ref=sv_gro_0',
         'http://www.amazon.com/gp/bestsellers/hi/ref=sv_hi_0',
         'http://www.amazon.com/gp/bestsellers/hi/511228/ref=sv_hi_1',
         'http://www.amazon.com/gp/bestsellers/hi/3754161/ref=sv_hi_1',
         'http://www.amazon.com/gp/bestsellers/hi/495224/ref=sv_hi_1',
         'http://www.amazon.com/gp/bestsellers/hi/328182011/ref=sv_hi_1',
         'http://www.amazon.com/gp/bestsellers/pet-supplies/ref=sv_petsupplies_1',
         'http://www.amazon.com/gp/bestsellers/arts-crafts/ref=sv_ac_0',
         'http://www.amazon.com/gp/bestsellers/lawn-garden/ref=sv_lg_0',
         'http://www.amazon.com/gp/bestsellers/appliances/ref=sv_la_0',
         'http://www.amazon.com/gp/bestsellers/home-garden/1057792/ref=sv_etk_hg_bb__0',
         'http://www.amazon.com/gp/bestsellers/home-garden/1057794/ref=sv_etk_hg_fd__0',
         'http://www.amazon.com/gp/bestsellers/kitchen/ref=sv_k_0',
         'http://www.amazon.com/gp/bestsellers/pc/541966/ref=sv_pc_1',
         'http://www.amazon.com/gp/bestsellers/musical-instruments/ref=sv_MI_0',
         'http://www.amazon.com/gp/bestsellers/appliances/ref=sv_la_0',
         'http://www.amazon.com/gp/bestsellers/electronics/1077068/ref=sv_e_2',
         'http://www.amazon.com/gp/bestsellers/electronics/172630/ref=sv_e_2',
         'http://www.amazon.com/gp/bestsellers/wireless/ref=sv_cps_2',
         'http://www.amazon.com/gp/bestsellers/electronics/502394/ref=sv_p_1',
         'http://www.amazon.com/gp/bestsellers/electronics/667846011/ref=sv_e_2',
         'http://www.amazon.com/gp/bestsellers/electronics/1266092011/ref=sv_e_1']


@decomem
def parseItem(link, item):

    category = cat

    _temp = select(item, 'div.zg_title a')
    title = _temp[0].text if len(_temp) > 0 else ''
    link = _temp[0]['href'] if len(_temp) > 0 else ''

    _temp = select(item, 'span.price')
    price = _temp[0].text if len(_temp) > 0 else ''

    _temp = select(item, 'div.zg_itemImage_normal a img')
    image = _temp[0]['src'] if len(_temp) > 0 else ''

    _temp = select(item, 'span.swSprite')
    stars = _temp[0]['title'].replace('out of 5 stars', '').strip() if len(_temp) > 0 else ''

    _temp = select(item, 'div.zg_reviews a')
    reviews = _temp[-1].text if len(_temp) > 0 else ''

    data = {
        'category': category.strip().encode('utf-8'),
        'title': title.strip().encode('utf-8'),
        'link': link.strip().encode('utf-8'),
        'price': price.strip().encode('utf-8'),
        'image': image.strip().encode('utf-8'),
        'stars': stars.strip().encode('utf-8'),
        'reviews': reviews.strip().encode('utf-8'),
    }

    for k, v in data.iteritems():
        if v == '':
            print link
            print data
            print '='*60
            break

    return data



soups = []
for link in links:

    soup = getPage(link)
    soups.append((link, soup))

    for l in select(soup, 'a'):
        if l.text in ['21-40', '41-60', '61-80', '81-100']:

            _link = l['href'].encode('utf-8')
            soups.append((_link, getPage(_link)))

items = []
for link, soup in soups:
    cat = select(soup, 'span.category')[0].text

    for item in select(soup, 'div.zg_itemRow'):
        items.append(parseItem(link, item))
    print len(items)


print len(items)
headers = ['title', 'price', 'category', 'stars', 'reviews', 'image', 'link']
data2xls(items, sample=True, headers=headers)

