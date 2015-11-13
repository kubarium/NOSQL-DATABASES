import urllib.request

with urllib.request.urlopen("http://nosql-database.org/") as response:
    html = response.read()

#clean up html from \n and \t and double spaces
html = html.decode().replace('\n','').replace('\t','').replace('  ','')

#each h2 is a group of NoSQL database
categories = re.findall("<h2>(.*?)</h2>", html)

for category in categories:
    print(category)
    #each category is followed by a number of articles and these articles are superceded by a final sectin before the next category
    category_content = re.findall("<h2>"+category+"<\/h2>(<article>.*?<\/article>)<\/section>", html)

    articles = re.findall("(<article>.*?</article>)", str(category_content).strip())


    for article in articles:
        print(article)
