import urllib.request
import json
from bs4 import BeautifulSoup
from py2neo import *




def graph():
    '''
    Constructs a database in Neo4J and plots all categories and databases.
    Also, it creates relationships between different databases that normally belong to different categories.
    :return: None
    '''
    with open("dump.json") as file:
        categories = json.load(file)

        authenticate("localhost:7474", "neo4j", "old4j")
        graph = Graph()
        graph.cypher.execute("MATCH (n) DETACH DELETE n")


        
        for category in categories.items():

            category_node = Node("Category", name=category[1]["name"])


            for database in category[1]["entries"]:

                database_node = Node("Database", name=database["name"], url=database["url"], content=database["content"])
                database_category_relationship = Relationship(database_node, "BELONGS TO", category_node)

                graph.create(database_category_relationship)



def export():
    '''
    Reads the content of http://nosql-database.org and exports a JSON file.
    Each key in the JSON file will be a category listed on the website. Under each key there is an array of databases.
    :return: None
    '''
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

if __name__ == "__main__":
    #export()
    graph()