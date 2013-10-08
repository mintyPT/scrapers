#!/usr/bin/env python
import os
import Queue
import tablib
import pickle
import hashlib
import requests
import threading
import multiprocessing
from pprint import pprint
from soupselect import select
from BeautifulSoup import BeautifulSoup


join = os.path.join
s = requests.session()


def soupify(r):
    return BeautifulSoup(r.text)


def saver(r, filename='output_r.html'):
    soup = soupify(r)
    with open(filename, 'w') as h:
        h.write(soup.prettify())


def hash(text):
    salt = 'pindupfinder'
    hashed = hashlib.sha1(text + salt).hexdigest()
    return hashed


def mapfolder(fun, folder, extension=None, multi=True):
    '''
        fun - function
        folder - folder with files to process
        extension - extensions of the files to process
        multi - bool for multiprocessing
    '''
    pool = multiprocessing.Pool()
    _files = os.listdir(folder)
    if extension != None:
        _files = filter(lambda _f: _f.split('.')[-1] == extension, _files)
    _files = [join(folder, _f) for _f in _files]

    if multi:
        return pool.map(fun, _files)
    else:
        return map(fun, _files)


def getHeaders(data):
    headers = []
    for d in data:
        for k in d.keys():
            if k not in headers:
                headers.append(k)
    return headers


def data2xls(data, xlsfile='result.xls', sample=False):
    '''
        data - must be an list of dicts
    '''
    headers = getHeaders(data)

    payload = []
    for d in data:
        # element = [d.get(e, '').encode('utf-8') for e in headers]
        try:
            element = []
            for e in headers:
                element.append(d.get(e, ''))#.encode('utf-8'))
            payload.append(element)
        except Exception, e:
            print d
            print e
            print '='*60

    data = tablib.Dataset(*payload, headers=headers)
    open(xlsfile, 'wb').write(data.xls)

    if sample==True:
        splittedFilename = xlsfile.split('.')
        name = '.'.join(splittedFilename[:-1])+'_sample.'
        ext = splittedFilename[-1]
        xlsfile_sample = name+ext

        sample_len = len(payload)/10
        payload_sample = payload[:sample_len]
        data = tablib.Dataset(*payload_sample, headers=headers)
        open(xlsfile_sample, 'wb').write(data.xls)

