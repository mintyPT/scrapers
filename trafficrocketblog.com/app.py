#!/usr/bin/env python
from toolbelt.web import getPage
from soupselect import select
from pprint import pprint

BASE = 'http://trafficrocketblog.com/page/%s/'
links = [BASE % i for i in range(1, 685)]



import Queue
import threading

class grabber(object):

    class myThread(threading.Thread):
        def __init__(self, fun, queue, out_queue, debug):
            threading.Thread.__init__(self)
            self.fun = fun
            self.queue = queue
            self.debug = debug
            self.out_queue = out_queue

        def run(self):
            while True:
                payload = self.queue.get()
                if self.debug:
                    print payload
                result = self.fun(payload)
                self.out_queue.put(result)
                self.queue.task_done()

    def __init__(self, args, fun=None, no_of_threads=50, debug=False):
        self.no_of_threads = no_of_threads

        self.fun = fun
        self.args = args
        self.debug = debug
        self.queue = Queue.Queue()
        self.out_queue = Queue.Queue()

        # spawn a pool of threads, and pass them queue instance
        for i in range(self.no_of_threads):
            t = self.myThread(fun, self.queue, self.out_queue, self.debug)
            t.setDaemon(True)
            t.start()

        # populate queue with data
        for a in self.args:
            self.queue.put(a)

        # wait on the queue until everything has been processed
        self.queue.join()

        self.result = list(self.out_queue.queue)


g = grabber(links, fun=getPage, debug=False, no_of_threads=5)


endGame = []
for soup in g.result:
    posts = select(soup, 'div.post')
    links = [select(post, 'h2.title a')[0]['href'] for post in posts]
    if len(links) != 2:
        print len(links)
    endGame += links




with open('res.csv', 'w') as h:
    for i in endGame:
        h.write(i+',\n')
