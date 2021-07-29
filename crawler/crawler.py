from sqlite3.dbapi2 import Cursor
import urllib.request
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup
import sqlite3

global start_url
global end_level


class crawler():
    def __init__(self):
        global conn
        global cur

        conn = sqlite3.connect("webcrawler.db")
        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS crawler(url text, title text, level integer)''')
        conn.commit()

    def crawl(self):
        dict = {}
        queue = [start_url]
        dict[start_url] = 1
        level_in_tran = 1
        while((queue and level_in_tran <= end_level) or (queue and end_level == 0)):
            url = queue[0]
            curr_level = dict[url]
            htmlfile = urllib.request.urlopen(url)
            baseurl = urlparse(url).netloc
            print("level: "+str(curr_level))
            print(queue)
            soup = BeautifulSoup(htmlfile.read(), 'html.parser')
            for link in soup.findAll('a', href=True):
                if "www" not in link['href']:
                    try:
                        new_url = urljoin(url, link['href'])
                    except:
                        print("new url problem")
                    if(new_url not in dict):
                        v = new_url
                        t = link.text
                        l = curr_level
                        print(v, t)
                        queue.append(v)
                        dict[v] = l+1
                        cur.execute(
                            '''INSERT INTO crawler VALUES (?,?,?);''', (v, t, l))
                        conn.commit()
                elif baseurl in link['href']:
                    if(link['href'] not in dict):
                        v = link['href']
                        t = link.text
                        l = curr_level
                        queue.append(v)
                        dict[v] = l+1
                        print(v, t)
                        cur.execute(
                            '''INSERT OR REPLACE INTO crawler (url,text,level) VALUES (?,?,?);''', (v, t, l))
                        conn.commit()
            while url in queue:
                queue.remove(url)
            if(queue):
                level_in_tran = dict[queue[0]]


def search(self, text):
    string = '%'+text+'%'
    cur.execute(
        "SELECT * FROM crawler WHERE title LIKE ('%' || ? || '%'", (string))
    row = cur.fetchall()
    print(row)
    return row
