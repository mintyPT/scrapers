#!/usr/bin/env python
import os
import re
import sys
import pickle
import requests
from pprint import pprint
from soupselect import select
from BeautifulSoup import BeautifulSoup
import hashlib


def hash(text):
    salt = 'pindupfinder'
    hashed = hashlib.sha1(text + salt).hexdigest()
    return hashed


def soupify(r):
    return BeautifulSoup(r.text)


def getemails(link):

    r = requests.get(link)

    email_pattern = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')

    emails = [str(match[0]) for match in email_pattern.findall(r.text)]
    print len(emails), link

    soup = soupify(r)
    links = select(soup, 'a')
    next = filter(lambda l: 'Next ' in l.text, links)

    if len(next) == 1:
        emails += getemails(dict(next[0].attrs)['href'])

    return emails


def grabber(link, cat):
    filepath = os.path.join('.', cat, hash(link) + '.txt')

    if not os.path.exists(filepath):
        emails = getemails(link)
        with open(filepath, 'w') as h:
            pickle.dump(emails, h)
    else:
        print 'already done', link







import Queue
import threading




class worker(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            link, cat = self.queue.get()
            grabber(link, cat)
            self.queue.task_done()


queue = Queue.Queue()

if __name__ == '__main__':
    cat = 'uncategorized'
    with open('%s.txt' % cat, 'r') as h:
        data = pickle.load(h)

    # spawn a pool of threads, and pass them queue instance
    for i in range(100):
        t = worker(queue)
        t.setDaemon(True)
        t.start()

#  #populate queue with data
    for link in data:
        if 'benprise.ning.com' in link:
            queue.put([link, cat])

#     #wait on the queue until everything has been processed
    queue.join()