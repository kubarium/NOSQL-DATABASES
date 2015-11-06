import urllib.request
import urllib.parse
import urllib.response
import re


with urllib.request.urlopen("http://nosql-database.org/") as response:
    html = response.read()

#clean up html from \n and \t
html = html.decode().replace('\n','').replace('\t','')


#each h2 is a group of NoSQL database
categories = re.findall("<h2>(.*?)</h2>", html)

for category in categories:
    print(category)
    #each category is followed by a number of articles and these articles are superceded by a final sectin before the next category
    category_content = re.findall("<h2>"+category+"<\/h2>(<article>.*?<\/article>)<\/section>", html)
    articles = re.findall("(<article>.*?</article>)", category_content)

    print(len(articles))
    for article in articles:
        print(article)
