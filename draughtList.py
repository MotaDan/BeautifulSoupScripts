from bs4 import BeautifulSoup
import requests
import csv

r = requests.get('http://www.publichousefl.com/')
tphsoup = BeautifulSoup(r.text, 'lxml')

draughtList = tphsoup.find(id='pu3025')

# Wrting out the draught list to a csv file as one row.
with open('draughtList.csv', 'w', newline='') as f:
    fileWriter = csv.writer(f)
    
    beers = []
    for beer in draughtList.find_all('p'):
        beers.append(beer.string.strip().lstrip('~-'))
    
    fileWriter.writerow(beers)
    
# Reading in from the csv and converting to the txt version.
with open('draughtList.csv', 'r', newline='') as f:
    fileReader = csv.reader(f)

    with open('draughtList.txt', 'w') as txtf:
        for row in fileReader:
            txtf.write("\n".join(row))