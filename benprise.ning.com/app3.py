import os
import pickle

cat = 'uncategorized'

masterList = []

for filename in os.listdir(os.path.join('.',cat)):
    with open(os.path.join('.',cat, filename), 'r') as h:
        data = pickle.load(h)
    masterList += data


filterList = []


for e in masterList:
    if e not in filterList:
        filterList.append(e)

filterList = sorted(filterList)

with open('%s-emails.txt' % cat, 'w') as h:
    for e in filterList:
        h.write('%s\n' % e)
