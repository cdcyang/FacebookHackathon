from lxml import html
import requests

page = requests.get('http://www.tagblender.net/')
tree = html.fromstring(page.content)

# Scraped tags
tags6 = tree.xpath('//div[@id="tags6"]/text()')
tags7 = tree.xpath('//div[@id="tags7"]/text()')
tags8 = tree.xpath('//div[@id="tags8"]/text()')
tags28 = tree.xpath('//div[@id="tags28"]/text()')
tags29 = tree.xpath('//div[@id="tags29"]/text()')
tags33 = tree.xpath('//div[@id="tags33"]/text()')
tags34 = tree.xpath('//div[@id="tags34"]/text()')

alltags = tree.xpath('//div[@class="tagBox"]/text()')

# Write tags to .txt
with open('tags.txt', 'w') as outfile:
    print(alltags, file=outfile)

