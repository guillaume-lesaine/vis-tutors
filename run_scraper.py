import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import scraper.spiders as spd
import pandas as pd
import os
import time

spider = spd.SuperProfSpider

settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'ROBOTSTXT_OBEY':False,
    'CONCURRENT_REQUESTS': 1,
    'DOWNLOAD_DELAY': 3,
    'COOKIES_ENABLED': False,
    'ITEM_PIPELINES': {
        'scraper.pipelines.TreatmentPipeline': 200,
        'scraper.pipelines.JsonLinesExportPipeline': 300,
    }
}

current_date = time.strftime("%Y-%m-%d")
directory = f"./data/scraper/{current_date}"

if not os.path.exists(directory):
    os.makedirs(directory)

df_topics = pd.read_csv("./data/context/search_topics.csv", sep=";", index_col="topic")
df_locations = pd.read_csv("./data/context/search_locations.csv", sep=";", index_col="location")

configure_logging()
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    # ["guitar", "italian", "chinese", "bass", "piano", "violin", "saxophone", "tennis", "chess", "swimming"]
    # ["french", "computer_science", "chemistry", "english", "french", "physics", "german", "spanish"]
    # ["maths"]
    for topic in ["guitar"]:
        search_topic = df_topics.loc[topic, "search_topic"]
        search_location = df_locations.loc["reims", "search_location"]
        yield runner.crawl(spider, search_topic = search_topic, search_location = search_location)
    reactor.stop()

crawl()
reactor.run()