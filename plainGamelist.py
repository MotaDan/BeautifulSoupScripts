from bs4 import BeautifulSoup

soup = BeautifulSoup(open("gamelist.xml"), "xml")

names = soup.find_all('name')
numGames = len(names)

plainNames = []
for name in names:
    plainNames.append(name.string)

plainNames.sort()

with open("plain_gamelist.txt", 'w') as f:
    f.write(str(numGames) + "\n")
    
    for name in plainNames:
        f.write(name + "\n")