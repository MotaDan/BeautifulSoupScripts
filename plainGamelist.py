from bs4 import BeautifulSoup
import sqlite3

connection = sqlite3.connect("gameslist.db")
cursor = connection.cursor()

sql_command = """
CREATE TABLE if not exists games ( 
game_number INTEGER PRIMARY KEY, 
name TEXT, 
desc TEXT, 
rating FLOAT, 
releasedate DATE,
developer TEXT,
publisher TEXT,
genre TEXT,
players INT,
path TEXT,
image TEXT,
id INT,
source TEXT);"""

cursor.execute(sql_command)

soup = BeautifulSoup(open("gamelist.xml"), "xml")

games = soup.find_all('game')

for game in games:
    namestr = game.find('name').string if game.find('name') is not None else ""
    descstr = game.desc.string if game.desc is not None else ""
    ratingstr = game.rating.string if game.rating is not None else ""
    releasedatestr = game.releasedate.string if game.releasedate is not None else ""
    developerstr = game.developer.string if game.developer is not None else ""
    publisherstr = game.publisher.string if game.publisher is not None else ""
    genrestr = game.genre.string if game.genre is not None else ""
    playersstr = game.players.string if game.players is not None else ""
    pathstr = game.path.string if game.path is not None else ""
    imagestr = game.image.string if game.image is not None else ""
    
    sql_command = """INSERT INTO games (game_number, name, desc, rating, releasedate, developer, publisher, genre, players, path, image, id, source)
    VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    
    cursor.execute(sql_command, (namestr, descstr, ratingstr, releasedatestr, developerstr, publisherstr, genrestr, playersstr, pathstr, imagestr, 0, ""))

connection.commit()

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
        
connection.close()