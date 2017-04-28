from bs4 import BeautifulSoup
import requests
import sqlite3
from os import remove

remove("amazonBestSellers.db")
connection = sqlite3.connect("amazonBestSellers.db")
cursor = connection.cursor()

sql_command = """
CREATE TABLE if not exists items ( 
item_number INTEGER PRIMARY KEY, 
name TEXT, 
reviewscore TEXT, 
price FLOAT, 
link TEXT, 
rank INTEGER, 
unique (name, reviewScore, price, link, rank));"""

cursor.execute(sql_command)

r = requests.get('https://www.amazon.com/gp/bestsellers/wireless/ref=sv_cps_6')
asoup = BeautifulSoup(r.text, 'lxml')

items = asoup.find_all('div', class_="zg_itemImmersion")

for item in items:
    wrapper = item.find('div', class_='zg_itemWrapper')
    links = wrapper.find_all('a')
    namestr = links[0].find_all('div')[1].string.strip()
    reviewscorestr = links[1]['title']
    pricestr = ""
    if wrapper.find(class_="a-size-base a-color-price") is not None:
        pricestr = wrapper.find(class_="a-size-base a-color-price").string
    linkstr = "https://www.amazon.com" + wrapper.find('a')['href']
    rankstr = item.find('span', class_='zg_rankNumber').string.strip().rstrip('.')
    
    sql_command = """INSERT INTO items (item_number, name, reviewscore, price, link, rank)
    VALUES (NULL, ?, ?, ?, ?, ?);"""
    cursor.execute(sql_command, (namestr, reviewscorestr, pricestr, linkstr, rankstr))

connection.commit()

with open('AmazonItems.txt', 'w') as f:
    cursor.execute("SELECT * FROM items")
    result = cursor.fetchall()
    
    for item in result:
        f.write(item[1] + "\n")  # Item name
        f.write(item[2] + "\n")  # Review score
        f.write(item[3] + "\n")  # Price
        f.write(item[4] + "\n")  # Link
        f.write("\n")
