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
source TEXT,
unique (name, desc, rating, releasedate, developer, publisher, genre, players, path, image, id, source));"""

cursor.execute(sql_command)

soup = BeautifulSoup(open("gamelist.xml"), "xml")

games = soup.find_all('game')

for game in games:
    namestr = game.find('name').string if game.find('name') is not None and game.find('name').string is not None else ""
    descstr = game.desc.string if game.desc is not None and game.desc.string is not None else ""
    ratingstr = game.rating.string if game.rating is not None and game.rating.string is not None else ""
    releasedatestr = game.releasedate.string if game.releasedate is not None and game.releasedate.string is not None else ""
    developerstr = game.developer.string if game.developer is not None and game.developer.string is not None else ""
    publisherstr = game.publisher.string if game.publisher is not None and game.publisher.string is not None else ""
    genrestr = game.genre.string if game.genre is not None and game.genre.string is not None else ""
    playersstr = game.players.string if game.players is not None and game.players.string is not None else ""
    pathstr = game.path.string if game.path is not None and game.path.string is not None else ""
    imagestr = game.image.string if game.image is not None and game.image.string is not None else ""
    
    sql_command = """INSERT OR IGNORE INTO games (game_number, name, desc, rating, releasedate, developer, publisher, genre, players, path, image, id, source)
    VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    
    cursor.execute(sql_command, (namestr, descstr, ratingstr, releasedatestr, developerstr, publisherstr, genrestr, playersstr, pathstr, imagestr, 0, ""))

connection.commit()

cursor.execute("SELECT name FROM games")
result = cursor.fetchall()
result.sort()

with open("plain_gamelist.txt", 'w') as f:
    cursor.execute("SELECT Count(*) FROM games")
    f.write(str(cursor.fetchone()[0]) + "\n")
    
    for name in result:
        f.write(name[0] + "\n")
        
connection.close()