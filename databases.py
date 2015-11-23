import urllib.request
import json
from bs4 import BeautifulSoup

with urllib.request.urlopen("http://nosql-database.org/") as response:
    html = BeautifulSoup(response.read(), "html.parser")

nosql_databases = {}

#each h2 is a group of NoSQL database
categories = html.find_all("h2")

for category in categories:

    category_id = str(category.text).replace(" ","")
    nosql_databases[category_id] = {"name":category.text, "entries":[]}

    '''
    By first finding h2 tags in html we actually got rid of the extra section at the beginning
    Therefore we have to go up one level with 'parent' and seek article tags
    Another alternative would be finding the sibling of h2 or category but there might be more tags other than
    article so this method is safer
    '''
    databases = category.parent.find_all("article")
    for database in databases:

        #some entries don't have much details than just a mention to a product name
        if database.find("h3"):
            database_name = database.find("h3").text
        else:
            continue

        database_url = database.find("a").get('href')
        #by getting rid of h3 completely the whole article tag is now holding the content for the database
        database.h3.extract()
        database_content = database.text.strip()

        entry = {'name':database_name, 'url':database_url, 'content':database_content}

        nosql_databases[category_id]["entries"].append(entry)


json.dump(nosql_databases, open("dump.json","w"), indent="\t", sort_keys=True)
