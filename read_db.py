import os
import sqlite3
from atproto import Client
from credentialsbsky import *
from pathlib import Path
import pprint


client = Client()
client.login('randommetalgear.bsky.social', app_password)

con = sqlite3.connect("mgs.db")
cur = con.cursor()
insert_cur = con.cursor()


#Gets number of likes and reposts from all uri addresses in db and updates each db row
for row in cur.execute("SELECT uri FROM mgs_posts"):
    #print(row)
    uri=row[0]

    likes = client.get_likes(uri)
    reposts = client.get_reposted_by(uri)

    number_of_likes = len(likes.likes)
    number_of_reposts = len(reposts.reposted_by)
    #print(likes)
    #print(reposts)
    print(uri, number_of_likes, number_of_reposts)

    #sql_update_values = [number_of_likes, number_of_reposts, uri]
    #print("UPDATE mgs_posts SET num_likes = " + str(number_of_likes) + ",num_reposts = " + str(number_of_reposts)+ " WHERE uri = " + str(uri))

    insert_cur.execute('UPDATE mgs_posts SET num_likes = ?, num_reposts = ? WHERE uri = ?', (number_of_likes,number_of_reposts,uri,))
    #print("Commit")
    con.commit()


cur.execute("SELECT * FROM mgs_posts ORDER BY num_likes DESC")
rows = cur.fetchall()
print("How many rows?" + str(len(rows)))
for row in rows:
   print(row)