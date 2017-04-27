from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.amazon.com/gp/bestsellers/wireless/ref=sv_cps_6')
asoup = BeautifulSoup(r.text, 'lxml')

with open('AmazonItems.txt', 'w') as f:
    items = asoup.find_all('div', class_="zg_itemWrapper")
    for item in items:
        links = item.find_all('a')
        f.write(links[0].find_all('div')[1].string.strip() + "\n")  # Item name
        f.write(links[1]['title'] + "\n")  # Review score
        if item.find(class_="a-size-base a-color-price") is not None:
            f.write(item.find(class_="a-size-base a-color-price").string + "\n")    # Price
        f.write("https://www.amazon.com" + item.find('a')['href'] + "\n")  # Link
        f.write("\n")