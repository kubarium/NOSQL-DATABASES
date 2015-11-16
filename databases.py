import sys
import urllib.request
from bs4 import BeautifulSoup

with urllib.request.urlopen("http://nosql-database.org/") as response:
    html = BeautifulSoup(response.read(), "html.parser")


#each h2 is a group of NoSQL database
categories = html.find_all("h2")

for category in categories:
    print(category)


    databases = category.parent.find_all("h3")
    for database in databases:
        database_tag = database.parent

        if database.find("a"):
            print(database_tag)
        else:
            print(database.text)
