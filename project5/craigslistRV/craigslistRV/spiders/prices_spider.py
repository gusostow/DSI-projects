import scrapy
import pandas as pd
import numpy as np
import requests
from scrapy.selector import Selector

from craigslistRV.items import RVitem

response = requests.get("https://simple.wikipedia.org/wiki/List_of_United_States_cities_by_population")

HTML = response.text

top_cities = Selector(text=HTML).xpath("//tr/td[2]/a/@title").extract()

top_cities = top_cities[:10]

tag = ["newyork",
       "losangeles",
       "chicago",
       "houston",
       "philadelphia",
       "phoenix",
       "sanantonio",
       "sandiego",
       "dallas",
       "sfbay"
]

makeURL = lambda x: "http://" + x + ".craigslist.org/search/sss?query=rv"

#generate a list of search page urls for top 10 cities
top_10_urls = map(makeURL, tag)

#helper function to extract prices from a craigslist search page

class RVprices(scrapy.Spider):
    name = "prices_spider"
    start_urls = top_10_urls

    def parse(self, response):

        location = response.url.split("/")[2].split(".")[0]

        prices_unprocessed = response.xpath("//span[@class='price']/text()").extract()

        prices = [int(price.replace("$", "")) for price in prices_unprocessed]

        for price in prices:
            item = RVitem()
            item["price"] = price
            item["location"] = location
            yield item

        next_page = response.xpath("//a[@class = 'button next']/@href").extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)



