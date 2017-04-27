from bs4 import BeautifulSoup
import requests

r = requests.get('http://www.publichousefl.com/')
tphsoup = BeautifulSoup(r.text, 'lxml')

draftList = tphsoup.find(id='pu3025')

with open('draughtList.txt', 'w') as f:
    for beer in draftList.find_all('p'):
        f.write(beer.string + "\n")