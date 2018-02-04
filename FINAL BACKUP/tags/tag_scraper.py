from lxml import html
import requests


def scrape_tags():
    page = requests.get('http://www.tagblender.net/')
    tree = html.fromstring(page.content)

    # Scraped tags
    alltags = tree.xpath('//div[@class="tagBox"]/text()')
    list0 = list()

    # Add tags to a list
    for x in range(0,len(alltags)):
        list0 = list0 + alltags[x].split();

    # Convert to dictionary
    popular_tags = dict()
    for x in range(0,len(list0)):
        new_tag = list0[x].replace('#', '').lower()
        popular_tags[new_tag] = x
    print(popular_tags)
    return popular_tags
