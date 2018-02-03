from lxml import html
import requests
import json

page = requests.get('http://www.tagblender.net/')
tree = html.fromstring(page.content)

# Scraped tags
alltags = tree.xpath('//div[@class="tagBox"]/text()')
list = list();

# Add tags to a list
for x in range(0,len(alltags)):
    list = list + alltags[x].split();

# Convert list to a JSON
listJSON = json.dumps(list)

# Write tags to tags.json
with open('tags.json', 'w') as outfile:
    json.dump(listJSON, outfile)