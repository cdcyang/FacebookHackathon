from lxml import html
import requests

page = requests.get('http://www.tagblender.net/')
tree = html.fromstring(page.content)

# Scraped tags
alltags = tree.xpath('//div[@class="tagBox"]/text()')

# Write tags to .txt
with open('tags.txt', 'w') as outfile:
    print(alltags, file=outfile)

