import scrapy
from scraper.items import SuperProfItem
from scrapy.selector import Selector
from selenium import webdriver
import time

class SuperProfSpider(scrapy.Spider):
    name = "superprof"

    def __init__(self, search_topic, search_location):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.search_topic = search_topic
        self.search_location = search_location

    def start_requests(self):
        
        search_url = f"https://www.superprof.fr/s/{self.search_topic},{self.search_location}.html"

        yield scrapy.Request(search_url, callback=self.scroll, meta={"search_topic": self.search_topic, "search_location": self.search_location})

    def scroll(self, response):

        self.driver.get(response.url)

        offer_indexes_treated = []
        offer_indexes_wasted = []
        
        counter = 0
        n = 0
        z = 288
        self.driver.execute_script(f"window.scrollTo(0, {z});")
        while True:
            time.sleep(5)

            for i in range(5):
                content = Selector(text=self.driver.page_source.encode('utf-8'))
                offers = content.xpath("//ul[@class='search-results']")
                offers = content.xpath(".//li")
                local_offers = offers[n:(n+3)]
                heights = []
                locations = []

                for offer in local_offers:
                    
                    try :
                        item = SuperProfItem()

                        item["website"] = "superprof"

                        index = offer.attrib["index"]
                        item["index"] = index
                        heights.append(self.driver.find_element_by_xpath(f"//li[@index='{index}']").size["height"])
                        locations.append(self.driver.find_element_by_xpath(f"//li[@index='{index}']").location["y"])

                        href = offer.xpath(".//a[@class='landing-v4-ads-bloc tck-announce-link']").attrib['href']
                        item["url"] = f"https://www.superprof.fr{href}"
                        item["search_topic"] = response.meta["search_topic"]
                        item["search_location"] = response.meta["search_location"]

                        item["teacher"] = offer.xpath(".//p[@class='landing-v4-ads-pic-firstname']/text()").get()
                        zone_location = offer.xpath(".//div[@class='landing-v4-ads-pic-location']")
                        item["location"] = zone_location.xpath(".//span[@class='landing-v4-ads-pic-text']/text()").get()

                        item["rating"] = offer.xpath(".//span[@class='landing-v4-ads-badge-rating-text']/text()").get()
                        item["reviews"] = offer.xpath(".//span[@class='landing-v4-ads-badge-rating-view-count']/text()").get()

                        zone_price = offer.xpath(".//span[@class='landing-v4-ads-badge-chips landing-v4-ads-badge-pricing']")
                        item["price"] = zone_price.css('span::text').get()

                        item["first_free"] = 1 if offer.xpath(".//span[@class='landing-v4-ads-badge-free-lesson']/text()").get() else 0

                        item["ambassador"] = 1 if offer.xpath(".//div[@class='landing-v4-ads-badge-ambassadeur']").get() else 0

                        image = offer.xpath(".//div[@class='img']").attrib["style"]
                        item["picture"] = 1 if image != 'background-image: url("/images/photo-default_300.jpg");' else 0

                        yield item
                        
                    except :
                        pass

                n += 3

                offset = -0.85
                # if heights != []:
                z += heights[0] + offset
                self.driver.execute_script(f"window.scrollTo(0, {z});")
                 
                time.sleep(5)

            try :
                button = self.driver.find_element_by_xpath('//button[@class="see-more-button"]')
                button.click()
            except :
                break